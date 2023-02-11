import json
from collections import defaultdict
from math_functions.centroid_and_deviation import centroid_and_deviation_calc

"""
    Rank the NatDis_USA Data & Store Results in JSON
"""

# Import Processed Natural Disaster Data
with open('./data_processors/processed_data/Zipcode_Weather_Data.json', newline='') as f: 
    zipcode_weather_data = json.load(f)

with open('./data_processors/processed_data/All_Weather_Data.json', newline='') as f: 
    all_weather_data = json.load(f)


### Analyze ALL National Disaster Data to Determine Relative Severity

# Init Results Dictionary
all_weather_results = {}
# Seperate Data into Individual Lists
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


### Analyze ALL National Disaster Data to Determine Relative Severity





# Save Results Dictionary as JSON File
with open(f"data_ranking/ranked_data/Weather_Ranked_Data.json", 'w') as f:
    json.dump(all_weather_results, f)






