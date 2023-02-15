import json
from collections import defaultdict
from math_functions.statistics_analysis import statistics_calc
from math_functions.ranking_functions import rank_value

"""
    Rank the Weather Data & Store Results in JSON
    
    Only Rainfall and Sunshine are Ranked on a Nationwide Level
    The Temperature will be user selected.
    Rational: Users typically know comfortable temperature data as a number, but rainfall and sunshine in terms of qualitative amounts. example: "A lot of rainfall" NOT " 1.4 inches of rainfall"
"""

# Import Processed Weather Data
with open('./data_processors/processed_data/Zipcode_Prefix_Weather_Data.json', newline='') as f: 
    zipcode_weather_data = json.load(f)

with open('./data_processors/processed_data/All_Weather_Data.json', newline='') as f: 
    all_weather_data = json.load(f)


### Analyze ALL Weather Data to Determine Centroid and Deviation

all_weather_results = {}
# Separate Data into Individual Lists
rainfall_list = all_weather_data['Precipitation_Inches']
sunshine_list = all_weather_data['Sunshine_Minutes']

# ALL Nationwide Precipitation
rainfall_results = statistics_calc(dataset=rainfall_list, name_of_data="Yearly_Rainfall")
all_weather_results.update(rainfall_results)

# ALL Nationwide Sunshine
sunshine_results = statistics_calc(dataset=sunshine_list, name_of_data="Yearly_Sunshine")
all_weather_results.update(sunshine_results)


### Analyze Zipcode Weather Data to Determine Rainfall and Sunshine Ranking on a National Level

zip_code_weather_results = {}
# 
for zipcode_prefix, weather_data in zipcode_weather_data.items():
    #
    rainfall_inches = weather_data['Yearly_Rainfall']
    sunshine_minutes = weather_data['Yearly_Sunshine']

    # 
    rainfall_median = all_weather_results['Median_Yearly_Rainfall']
    rainfall_mad = all_weather_results['MAD_Yearly_Rainfall']
    sunshine_median = all_weather_results['Median_Yearly_Sunshine']
    sunshine_mad = all_weather_results['MAD_Yearly_Sunshine']
    
    # Calculate Precipitation Rank
    rainfall_deviation_ratio = (rainfall_inches - rainfall_median) / rainfall_mad
    rainfall_rank = rank_value(deviation_ratio=rainfall_deviation_ratio)

    # Calculate Sunshine Rank
    sunshine_deviation_ratio = (sunshine_minutes - sunshine_median) / sunshine_mad
    sunshine_rank = rank_value(deviation_ratio=sunshine_deviation_ratio)

    # Update Weather Data
    weather_data.update({
        'Yearly_Rainfall': rainfall_rank,
        'Yearly_Sunshine': sunshine_rank
    })
    
    zip_code_weather_results.update({zipcode_prefix:weather_data})


# Save Results Dictionary as JSON File
with open(f"data_ranking/ranked_data/Weather_Ranked_Data.json", 'w') as f:
    json.dump(zip_code_weather_results, f)






