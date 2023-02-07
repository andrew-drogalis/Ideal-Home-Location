import csv, json, math
from collections import defaultdict
from uszipcode import SearchEngine

"""
    Process the Zipcode Data & Store Results in JSON
"""

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
        # 
        for city in zip_prefix_search:
            state = city.state
            # 
           

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

        # Precipitation Results
        precipitation_values = [*precipitation_normals.values()]
        total_rainfall = round(sum(precipitation_values), 2)

     

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
with open(f"data_processors/processed_data/Zipcode_Weather_Data.json", 'w') as f:
    json.dump(zip_code_weather_data, f)