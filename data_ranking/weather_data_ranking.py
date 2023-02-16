import json
from collections import defaultdict
from math_functions.statistics_analysis import statistics_calc
from math_functions.ranking_functions import rank_value

"""
    Rank the Weather Data & Store Results in JSON
    
    Only Precipitation and Sunshine are Ranked on a Nationwide Level
    The Temperature will be user selected.
    Rational: Users typically know comfortable temperature data as a number, but precipitation and sunshine in terms of qualitative amounts. example: "A lot of precipitation" NOT " 1.4 inches of precipitation"
"""

# Import Processed Weather Data
with open('./data_processors/processed_data/Zipcode_Prefix_Weather_Data.json', newline='') as f: 
    zipcode_weather_data = json.load(f)

with open('./data_processors/processed_data/All_Weather_Data.json', newline='') as f: 
    all_weather_data = json.load(f)


### Analyze ALL Weather Data to Determine Centroid and Deviation

all_weather_results = {}
# Separate Data into Individual Lists
precipitation_list = all_weather_data['Precipitation_Inches']
sunshine_list = all_weather_data['Sunshine_Minutes']

# ALL Nationwide Precipitation
precipitation_results = statistics_calc(dataset=precipitation_list, name_of_data="Yearly_Precipitation")
all_weather_results.update(precipitation_results)

# ALL Nationwide Sunshine
sunshine_results = statistics_calc(dataset=sunshine_list, name_of_data="Yearly_Sunshine")
all_weather_results.update(sunshine_results)


### Analyze Zipcode Weather Data to Determine Precipitation and Sunshine Ranking on a National Level

zip_code_weather_results = {}
# 
for zipcode_prefix, weather_data in zipcode_weather_data.items():
    #
    precipitation_inches = weather_data['Yearly_Precipitation']
    sunshine_minutes = weather_data['Yearly_Sunshine']

    # 
    precipitation_median = all_weather_results['Median_Yearly_Precipitation']
    precipitation_mad = all_weather_results['MAD_Yearly_Precipitation']
    sunshine_median = all_weather_results['Median_Yearly_Sunshine']
    sunshine_mad = all_weather_results['MAD_Yearly_Sunshine']
    
    # Calculate Precipitation Rank
    precipitation_deviation_ratio = (precipitation_inches - precipitation_median) / precipitation_mad
    precipitation_rank = rank_value(deviation_ratio=precipitation_deviation_ratio)

    # Calculate Sunshine Rank
    sunshine_deviation_ratio = (sunshine_minutes - sunshine_median) / sunshine_mad
    sunshine_rank = rank_value(deviation_ratio=sunshine_deviation_ratio)

    # Update Weather Data
    weather_data.update({
        'Yearly_Precipitation': precipitation_rank,
        'Yearly_Sunshine': sunshine_rank
    })
    
    zip_code_weather_results.update({zipcode_prefix:weather_data})


# Save Results Dictionary as JSON File
with open(f"data_ranking/ranked_data/Weather_Ranked_Data.json", 'w') as f:
    json.dump(zip_code_weather_results, f)






