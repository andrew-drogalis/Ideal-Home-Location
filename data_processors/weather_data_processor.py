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
min_exceptable_end_year = 2020
start_time = datetime(1993, 1, 1)
end_time = datetime(2023, 1, 1)

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
    zip_prefix_search = search.by_prefix(prefix=zip_number, returns=100)

    # Data Storage
    monthly_temperature_results = defaultdict(list)
    monthly_precipitation_results = defaultdict(list)
    monthly_sunshine_results = defaultdict(list)
    monthly_airpressure_results = defaultdict(list)

    if zip_prefix_search:
        # Analyze Each Zipcode in the Zipcode Prefix
        zip_prefix_search = iter(zip_prefix_search)
        for city in zip_prefix_search:
            # City State & Position
            state = city.state
            latitude = city.lat
            longitude = city.lng
            if latitude == 0 or longitude == 0:
                next(zip_prefix_search, None)
                continue

            # Fetch List of Nearby Stations
            radius_in_m = 20_000 # meters
            while True:
                stations_nearby = Stations().nearby(latitude, longitude, radius_in_m).fetch(10).to_dict()
                station_ids = [*stations_nearby['name'].keys()]
                # Select Station with Maximum Amount of Data
                station_data_dict = {}
                for station in station_ids:
                    station_start_year = stations_nearby['monthly_start'][station].year
                    station_end_year = stations_nearby['monthly_end'][station].year
                    # Total Data Length
                    station_data_length = station_end_year - station_start_year
                    # Verify Data is Recent
                    if station_end_year >= min_exceptable_end_year:
                        station_data_dict.update({station:station_data_length})
        
                if station_data_dict:
                    station_id = max(station_data_dict, key = station_data_dict.get)
                    break
                # Expand Search Radius
                else: 
                    radius_in_m += 20_000
                
                if radius_in_m > 200_000: # Max Radius is 120 Miles
                    raise Exception('Confirm Data Source is online and inputs are valid')

            # Fetch Data from Nearby Station
            data = Monthly(station_id, start_time, end_time).convert(units.imperial).fetch().to_dict()

            # Select Data to be Analyzed
            temperature_monthly_avg = data['tavg']
            precipitation_inches = data['prcp']
            sealevel_airpressure = data['pres'] # Normalized (hPa)
            sunshine_minutes = data['tsun']

            # Monthly Keys for 30 years of data
            datetime_keys = [*temperature_monthly_avg.keys()]
            for key in datetime_keys:

                temperature = temperature_monthly_avg[key]
                precipitation = precipitation_inches[key]
                sunshine = sunshine_minutes[key]
                airpressure = sealevel_airpressure[key]

                if not math.isnan(temperature):
                    monthly_temperature_results[key.month].append(temperature)
                if not math.isnan(precipitation):
                    monthly_precipitation_results[key.month].append(precipitation)
                if not math.isnan(sunshine) and sunshine != 0:
                    monthly_sunshine_results[key.month].append(sunshine)
                if not math.isnan(airpressure) and airpressure != 0:
                    monthly_airpressure_results[key.month].append(airpressure)

        # Temperature Monthly Averages
        temperature_normals = {}
        for month, temp_data in monthly_temperature_results.items():
            average_temp = mean(temp_data)
            temperature_normals.update({month:average_temp})

        # Precipitation Monthly Averages
        precipitation_normals = {}
        for month, precipitation_data in monthly_precipitation_results.items():
            average_precipitation = mean(precipitation_data)
            precipitation_normals.update({month:average_precipitation})

        # Sunshine Monthly Averages 
        sunshine_normals = {}
        for month, sunshine_data in monthly_sunshine_results.items():
            average_sunshine = mean(sunshine_data)
            sunshine_normals.update({month:average_sunshine})

        # Air Pressure Monthly Averages
        airpressure_normals = {}
        for month, airpressure_data in monthly_airpressure_results.items():
            average_airpressure = mean(airpressure_data)
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
        total_precipitation = round(sum(precipitation_values), 2)

        if total_precipitation <= 0:
            raise Exception('Precipitation Data Error; Total Precipitation Inches Less Than or Equal to Zero')

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
            high_pressure = 1022
            low_pressure = 1009

            sunshine_normals = {}
            for month, airpressure in airpressure_normals.items():
                month = f'{month}'
                # Linear Interpolation 
                percent_of_time_sky_clear = (airpressure - low_pressure) / (high_pressure - low_pressure)
                # Bound Edge Cases
                percent_of_time_sky_clear = max(0.2, percent_of_time_sky_clear)
                percent_of_time_sky_clear = min(0.8, percent_of_time_sky_clear)
                
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

        if total_sunshine <= 0:
            raise Exception('Sunshine Data Error; Total Sunshine Minutes Less Than or Equal to Zero')

        # Update Results Dictionary
        zip_code_weather_data.update({zip_number: 
            {
                'Average_Temperature': temperature_yearly_avg,
                'Min_Temperature': temperature_min,
                'Max_Temperature': temperature_max,
                'Seasons': seasons,
                'Yearly_Precipitation': total_precipitation,
                'Yearly_Sunshine': total_sunshine
            }
        })
      
        all_weather_data['Precipitation_Inches'].append(total_precipitation)
        all_weather_data['Sunshine_Minutes'].append(total_sunshine)

    else:
        print(f'No USA Cities at {zip_number} Prefix')


# ------------------------------------------------------

# Save Results Dictionary as JSON File
with open(f"data_processors/processed_data/Zipcode_Prefix_Weather_Data.json", 'w') as f:
    json.dump(zip_code_weather_data, f)

with open(f"data_processors/processed_data/All_Weather_Data.json", 'w') as f:
    json.dump(all_weather_data, f)