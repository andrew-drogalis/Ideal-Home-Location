import csv, json, math
from collections import defaultdict
from datetime import datetime
from statistics import mean
from meteostat import Monthly, Stations, units
from uszipcode import SearchEngine
from constants.sunlight_hours import days_in_month, daily_sunlight_hours_contential, daily_sunlight_hours_hawaii, daily_sunlight_hours_alaska

"""
    Process the Weather Data & Store Results in JSON
"""

# Fetch Data from last 30 Years
start_time = datetime(1993, 1, 1)
end_time = datetime(2023, 1, 1)
min_exceptable_start_year = 2000
min_exceptable_end_year = 2020

# Import Raw Zipcode Prefix Data
with open('./data_src/USA_Zipcode_3_Digits.csv', newline='') as f: 
    zipcode_prefix_data = list(csv.reader(f))

# Initalize Search Engine & Results Dictionary
search = SearchEngine()
zip_code_weather_data = {}
all_weather_data = {
    'Precipitation_Inches': [],
    'Sunshine_Minutes': []
}

# Store Weather Data for Each Zipcode Prefix
for zip_prefix in zipcode_prefix_data:
    zip_number = zip_prefix[0]
    zip_prefix_search = search.by_prefix(zip_number)
    monthly_temperature_results = defaultdict(list)
    monthly_precipitation_results = defaultdict(list)
    monthly_sunshine_results = defaultdict(list)
    monthly_airpressure_results = defaultdict(list)
    if zip_prefix_search:
        # Analyze Each City in the Zipcode Prefix
        for city in zip_prefix_search:
            state = city.state
            # 
            stations_nearby = Stations().nearby(city.lat, city.lng, 100_000).fetch(5).to_dict()
            station_ids = [*stations_nearby['name'].keys()]
            #
            for station in station_ids:
                station_start_year = stations_nearby['monthly_start'][station].year
                station_end_year = stations_nearby['monthly_end'][station].year
                if station_start_year < min_exceptable_start_year and station_end_year > min_exceptable_end_year:
                    station_id = station
                    break
            #
            data = Monthly(station_id, start_time, end_time).convert(units.imperial).fetch().to_dict()
            # Select Relevant Data
            temperature_avg = data['tavg']
            precipitation_inch = data['prcp']
            sealevel_airpressure = data['pres'] # Normalized (hPa)
            sunshine_minutes = data['tsun']
            # Monthly Keys for 30 years of data
            datetime_keys = [*temperature_avg.keys()]
            for key in datetime_keys:
                temp = temperature_avg[key]
                rainfall = precipitation_inch[key]
                sunshine = sunshine_minutes[key]
                airpressure = sealevel_airpressure[key]
                if not math.isnan(temp):
                    monthly_temperature_results[key.month].append(temp)
                if not math.isnan(rainfall):
                    monthly_precipitation_results[key.month].append(rainfall)
                if not math.isnan(sunshine) and sunshine != 0:
                    monthly_sunshine_results[key.month].append(sunshine)
                if not math.isnan(airpressure) and airpressure != 0:
                    monthly_airpressure_results[key.month].append(airpressure)
        # Monthly Averages
        temperature_normals = {}
        for month, temp_data in monthly_temperature_results.items():
            average_temp = sum(temp_data) / len(temp_data)
            temperature_normals.update({month:average_temp})
        precipitation_normals = {}
        for month, rainfall_data in monthly_precipitation_results.items():
            average_precipitation = sum(rainfall_data) / len(rainfall_data)
            precipitation_normals.update({month:average_precipitation})
        sunshine_normals = {}
        for month, sunshine_data in monthly_sunshine_results.items():
            average_sunshine = sum(sunshine_data) / len(sunshine_data)
            sunshine_normals.update({month:average_sunshine})
        airpressure_normals = {}
        for month, airpressure_data in monthly_airpressure_results.items():
            average_airpressure = sum(airpressure_data) / len(airpressure_data)
            airpressure_normals.update({month:average_airpressure})

        # Temperature Results
        temperature_values = [*temperature_normals.values()]
        temperature_min = round(min(temperature_values), 2)
        temperature_max = round(max(temperature_values), 2)
        temperature_yearly_avg = round(sum(temperature_values) / len(temperature_values), 2)

        # Seasons Results
        """ 
            Value of 35 degree delta choosen for (4) seasons
            Value of 20 degree delta choosen for (2) seasons
            Note: Arbitrary values choosen to satisfy edge case. example: Georgia
        """
        seasons = 4 if temperature_max - temperature_min > 35 else 2 if temperature_max - temperature_min > 20 else 1

        # Precipitation Results
        precipitation_values = [*precipitation_normals.values()]
        total_rainfall = round(sum(precipitation_values), 2)

        # Sunshine Results            
        sunshine_values = [*sunshine_normals.values()]
        if sunshine_values and len(sunshine_values) == 12:
            total_sunshine = round(sum(sunshine_values))
        else:
            """
                Air Pressure is used when Sunshine data is not avialable
                High Air Pressure > 1022 hPa for Clear Sky
                1022 hPa > Normal Air Pressure > 1009 hPa
                Low Air Pressure < 1009 hPa for Cloudy Sky
                Assumption: High Air Pressure and Low Air Pressure is not 100% Clear Sky and 0% Clear Sky respectively. 
                            Exceptable Values are 80% Clear Sky for High Air Pressure and 20% Clear Sky for Low Air Pressure
            """
            sunshine_normals = {}
            high_pressure = 1022
            low_pressure = 1009
            for month, airpressure in airpressure_normals.items():
                month = f'{month}'
                # Linear Interpolation 
                percent_of_time_sky_clear = (airpressure - low_pressure) / (high_pressure - low_pressure)
                # Bound Edge Cases
                if percent_of_time_sky_clear < 0.2:
                    percent_of_time_sky_clear = 0.2
                if percent_of_time_sky_clear > 0.8:
                    percent_of_time_sky_clear = 0.8
                
                # Minutes of Sunshine
                if state == 'AK':
                    minutes_of_sunshine = daily_sunlight_hours_alaska[month] * days_in_month[month] * 60 * percent_of_time_sky_clear
                elif state == 'HI':
                    minutes_of_sunshine = daily_sunlight_hours_hawaii[month] * days_in_month[month] * 60 * percent_of_time_sky_clear
                else:
                    minutes_of_sunshine = daily_sunlight_hours_contential[month] * days_in_month[month] * 60 * percent_of_time_sky_clear
                sunshine_normals.update({month:minutes_of_sunshine})
            
            # Linear Interpolated Sunshine Results
            sunshine_values = [*sunshine_normals.values()]
            total_sunshine = round(sum(sunshine_values))

        # Update Results Dictionary
        zip_number_weather_data = {zip_number: 
            {
                'Average_Temperature': temperature_yearly_avg,
                'Min_Temperature': temperature_min,
                'Max_Temperature': temperature_max,
                'Seasons': seasons,
                'Yearly_Rainfall': total_rainfall,
                'Yearly_Sunshine': total_sunshine
            }
        }
        zip_code_weather_data.update(zip_number_weather_data)
        all_weather_data['Precipitation_Inches'].append(total_rainfall)
        all_weather_data['Sunshine_Minutes'].append(total_sunshine)

    else:
        print(f'No USA Cities at {zip_number} Prefix')


# Save Results Dictionary as JSON File
with open(f"data_processors/processed_data/Zipcode_Prefix_Weather_Data.json", 'w') as f:
    json.dump(zip_code_weather_data, f)

with open(f"data_processors/processed_data/All_Weather_Data.json", 'w') as f:
    json.dump(all_weather_data, f)