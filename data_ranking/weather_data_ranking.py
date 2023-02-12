import json
from collections import defaultdict
from math_functions.centroid_and_deviation import centroid_and_deviation_calc

"""
    Rank the Weather Data & Store Results in JSON
"""

# Import Processed Weather Data
with open('./data_processors/processed_data/Zipcode_Prefix_Weather_Data.json', newline='') as f: 
    zipcode_weather_data = json.load(f)

with open('./data_processors/processed_data/All_Weather_Data.json', newline='') as f: 
    all_weather_data = json.load(f)


### Analyze ALL Weather Data to Determine Centroid and Deviation

# Init Results Dictionary
all_weather_results = {}
# Separate Data into Individual Lists
rainfall_list = all_weather_data['Precipitation_Inches']
sunshine_list = all_weather_data['Sunshine_Minutes']

"""
    Only Rainfall and Sunshine are Ranked on a National Level
    The Temperature will be user selected.
    Rational: Users typically know comfortable temperature data as a number, but rainfall and sunshine in terms of qualitative amounts. example: "A lot of rainfall" NOT " 1.4 inches of rainfall"
"""

# ALL Rainfall
rainfall_results = centroid_and_deviation_calc(dataset=rainfall_list, name_of_data="Yearly_Rainfall")
all_weather_results.update(rainfall_results)

# ALL Sunshine
sunshine_results = centroid_and_deviation_calc(dataset=sunshine_list, name_of_data="Yearly_Sunshine")
all_weather_results.update(sunshine_results)


### Analyze Zipcode Weather Data to Determine Rainfall and Sunshine Ranking on a National Level

"""
    Key Values:
        - Well Above Average: Outside 1.5 Deviations from the Centroid
        - Above Average: Between 1.5 and 0.5 Deviations from the Centroid
        - Average: Between -0.5 and 0.5 Deviations from the Centroid
        - Below Average: Between -0.5 and -1.5 Deviations from the Centroid
        - Well Below Average: Outside -1.5 Deviations from the Centroid
"""
# Init Results Dictionary
zip_code_weather_results = {}

# 
for zipcode_prefix, weather_data in zipcode_weather_data.items():
    #
    rainfall_inches = weather_data['Yearly_Rainfall']
    sunshine_minutes = weather_data['Yearly_Sunshine']

    #
    rainfall_centroid = all_weather_results['Centroid_Yearly_Rainfall']
    rainfall_deviation = all_weather_results['Deviation_Yearly_Rainfall']
    sunshine_centroid = all_weather_results['Centroid_Yearly_Rainfall']
    sunshine_deviation = all_weather_results['Deviation_Yearly_Rainfall']

    #
    rainfall_deviation_ratio = (rainfall_inches - rainfall_centroid) / rainfall_deviation
    rainfall_rank = 'Well Below Average' if rainfall_deviation_ratio < -1.5 else 'Below Average' if -1.5 <= rainfall_deviation_ratio < -0.5 else 'Average' if -0.5 <= rainfall_deviation_ratio <= 0.5 else 'Above Average' if 0.5 < rainfall_deviation <= 1.5 else 'Well Above Average'

    zip_code_weather_results.update({zipcode_prefix:weather_data})

# Save Results Dictionary as JSON File
with open(f"data_ranking/ranked_data/Weather_Ranked_Data.json", 'w') as f:
    json.dump(zip_code_weather_results, f)






