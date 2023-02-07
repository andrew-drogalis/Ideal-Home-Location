import json
from collections import defaultdict
from statistics import mean, median, stdev

"""
    Rank the NatDis_USA Data & Store Results in JSON
"""

# Import Processed Natural Disaster Data
with open('./data_processors/processed_data/Zipcode_Weather_Data.json', newline='') as f: 
    zipcode_weather_data = json.load(f)

with open('./data_processors/processed_data/All_Weather_Data.json', newline='') as f: 
    all_weather_data = json.load(f)


"""
    Pearson's Calcuation for Skewness (Fisher's is not necessary in this case)
    Skew = 3 * (Mean – Median) / Standard Deviation
    Extreme Skewness < -0.20 or Extreme Skewness > 0.20
    If the Dataset has Extreme Skewness, replace the Standard Deviation with the MAD (Median Absolute Deviation)
"""

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
mean_total_death = mean(total_death_list)
median_total_death = median(total_death_list)
stdv_total_death = stdev(total_death_list)
skewness_total_death = 3 * (mean_total_death - median_total_death) / stdv_total_death
if skewness_total_death > 0.2 or skewness_total_death < -0.2:
    mad_total_death = [abs(x - median_total_death) for x in total_death_list]
    mad_total_death = median(mad_total_death)
    total_death_results = {
        'Centriod_Total_Death': median_total_death,
        'Deviation_Total_Death': mad_total_death
    }
else:
    total_death_results = {
        'Centriod_Total_Death': mean_total_death,
        'Deviation_Total_Death': stdv_total_death
    }
all_disaster_results.update(total_death_results)

# ALL Sunshine
mean_total_affected = mean(total_affected_list)
median_total_affected = median(total_affected_list)
stdv_total_affected = stdev(total_affected_list)
skewness_total_affected = 3 * (mean_total_affected - median_total_affected) / stdv_total_affected
if skewness_total_affected > 0.2 or skewness_total_affected < -0.2:
    mad_total_affected = [abs(x - median_total_affected) for x in total_affected_list]
    mad_total_affected = median(mad_total_affectedh)
    total_affected_results = {
        'Centriod_Total_Affected': median_total_affected,
        'Deviation_Total_Affected': mad_total_affected
    }
else:
    total_affected_results = {
        'Centriod_Total_Affected': mean_total_affected,
        'Deviation_Total_Affected': stdv_total_affected
    }
all_disaster_results.update(total_affected_results)


### Analyze ALL National Disaster Data to Determine Relative Severity





# Save Results Dictionary as JSON File
with open(f"data_ranking/ranked_data/Weather_Ranked_Data.json", 'w') as f:
    json.dump(all_weather_results, f)






