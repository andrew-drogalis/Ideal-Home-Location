import json
from collections import defaultdict
from statistics import mean, median, stdev

"""
    Rank the NatDis_USA Data & Store Results in JSON
"""

# Import Processed Natural Disaster Data
with open('./data_processors/processed_data/State_NaturalDisaster_Data.json', newline='') as f: 
    state_disaster_data = json.load(f)

with open('./data_processors/processed_data/All_NaturalDisaster_Data.json', newline='') as f: 
    all_disaster_data = json.load(f)

with open('./data_processors/processed_data/Type_NaturalDisaster_Data.json', newline='') as f: 
    disaster_by_type_data = json.load(f)


"""
    Pearson's Calcuation for Skewness (Fisher's is not necessary in this case)
    Skew = 3 * (Mean – Median) / Standard Deviation
    Extreme Skewness < -0.20 or Extreme Skewness > 0.20
    If the Dataset has Extreme Skewness, replace the Standard Deviation with the MAD (Median Absolute Deviation)
"""

### Analyze ALL National Disaster Data to Determine Relative Severity

# Init Results Dictionary
all_disaster_results = {}
# Seperate Data into Individual Lists
total_death_list = [event['Total_Deaths'] for event in all_disaster_data]
total_affected_list = [event['Total_Affected'] for event in all_disaster_data]
total_damages_list = [event['Total_Damages'] for event in all_disaster_data]

# ALL Total Deaths
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

# ALL Total Affected
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

# All Total Damages
mean_total_damages = mean(total_damages_list)
median_total_damages = median(total_damages_list)
stdv_total_damages = stdev(total_damages_list)
skewness_total_damages = 3 * (mean_total_damages - median_total_damages) / stdv_total_damages
if skewness_total_damages > 0.2 or skewness_total_damages < -0.2:
    mad_total_damages = [abs(x - median_total_damages) for x in total_damages_list]
    mad_total_damages = median(mad_total_damages)
    total_damages_results = {
        'Centriod_Total_Damages': median_total_damages,
        'Deviation_Total_Damages': mad_total_damages
    }
else:
    total_damages_results = {
        'Centriod_Total_Damages': mean_total_damages,
        'Deviation_Total_Damages': stdv_total_damages
    }
all_disaster_results.update(total_damages_results)


### Analyze the Type of Disaster Data to Determine Relative Severity & Frequency 

# Init Results Dictionary
disaster_by_type_results = {}

# 
for disaster_type, disaster_type_events in disaster_by_type_data.items():
    """ 
        Rare Events are omitted from Severity Analysis, these events recieve a Low Frequency Rank
        A 95% Confidence Interval was used to determine of the events occured with a greater than 0 mean frequency
            '''python
                confidence_interval = 1.960 * stdv_yearly_frequency / len(yearly_frequency_list) ** 0.5
                upper_bounds = mean_yearly_frequency + confidence_interval
                lower_bounds = mean_yearly_frequency - confidence_interval
                if lower_bounds < 0:
                    print('Event omitted from Severity Rank')
            '''
        All Disaster Type Data has an N value > 15. The Sample Standard Deviation will be used instead of population.
    """
    if disaster_type not in ['Landslide', 'Volcanic activity', 'Sand/Dust storm']:
    
        disaster_by_type_results.update({disaster_type:{}})
        year_of_event_list = defaultdict(list)
        total_death_list = [event['Total_Deaths'] for event in disaster_type_events]
        total_affected_list = [event['Total_Affected'] for event in disaster_type_events]
        total_damages_list = [event['Total_Damages'] for event in disaster_type_events]
        
        # Dates of Data From Source File
        for event in disaster_type_events:
            year_of_event_list[event['Year']].append(1)
        yearly_frequency_list = [sum(year_of_event_list[f'{i}']) for i in range(1900,2022)]

        # Frequency Statistics
        mean_yearly_frequency = mean(yearly_frequency_list)
        median_yearly_frequency = median(yearly_frequency_list)
        stdv_yearly_frequency = stdev(yearly_frequency_list)
        skewness_yearly_frequency = 3 * (mean_yearly_frequency - median_yearly_frequency) / stdv_yearly_frequency if stdv_yearly_frequency else 0
        if skewness_yearly_frequency > 0.2 or skewness_yearly_frequency < -0.2:
            mad_yearly_frequency = [abs(x - median_yearly_frequency) for x in yearly_frequency_list]
            mad_yearly_frequency = median(mad_yearly_frequency)
            disaster_by_type_results[disaster_type].update({
                'Centriod_Yearly_Frequency': median_yearly_frequency,
                'Deviation_Yearly_Frequency': mad_yearly_frequency
            })
        else:
            disaster_by_type_results[disaster_type].update({
                'Centriod_Yearly_Frequency': mean_yearly_frequency,
                'Deviation_Yearly_Frequency': stdv_yearly_frequency
            })

        # Total Death Statistics
        mean_total_death = mean(total_death_list)
        median_total_death = median(total_death_list)
        stdv_total_death = stdev(total_death_list)
        skewness_total_death = 3 * (mean_total_death - median_total_death) / stdv_total_death if stdv_total_death else 0
        if skewness_total_death > 0.2 or skewness_total_death < -0.2:
            mad_total_death = [abs(x - median_total_death) for x in total_death_list]
            mad_total_death = median(mad_total_death)
            disaster_by_type_results[disaster_type].update({
                'Centriod_Total_Death': median_total_death,
                'Deviation_Total_Death': mad_total_death
            })
        else:
            disaster_by_type_results[disaster_type].update({
                'Centriod_Total_Death': mean_total_death,
                'Deviation_Total_Death': stdv_total_death
            })

        # Total Affected Statistics
        mean_total_affected = mean(total_affected_list)    
        median_total_affected = median(total_affected_list)
        stdv_total_affected = stdev(total_affected_list)
        skewness_total_affected = 3 * (mean_total_affected - median_total_affected) / stdv_total_affected if stdv_total_affected else 0
        if skewness_total_affected > 0.2 or skewness_total_affected < -0.2:
            mad_total_affected = [abs(x - median_total_affected) for x in total_affected_list]
            mad_total_affected = median(mad_total_affected)
            disaster_by_type_results[disaster_type].update({
                'Centriod_Total_Affected': median_total_affected,
                'Deviation_Total_Affected': mad_total_affected
            })
        else:
            disaster_by_type_results[disaster_type].update({
                'Centriod_Total_Affected': mean_total_affected,
                'Deviation_Total_Affected': stdv_total_affected
            })

        # Total Damages Statistics
        mean_total_damages = mean(total_damages_list)
        median_total_damages = median(total_damages_list)
        stdv_total_damages = stdev(total_damages_list)
        skewness_total_damages = 3 * (mean_total_damages - median_total_damages) / stdv_total_damages if stdv_total_damages else 0
        if skewness_total_damages > 0.2 or skewness_total_damages < -0.2:
            mad_total_damages = [abs(x - median_total_damages) for x in total_damages_list]
            mad_total_damages = median(mad_total_damages)
            disaster_by_type_results[disaster_type].update({
                'Centriod_Total_Damages': median_total_damages,
                'Deviation_Total_Damages': mad_total_damages
            })
        else:
            disaster_by_type_results[disaster_type].update({
                'Centriod_Total_Damages': mean_total_damages,
                'Deviation_Total_Damages': stdv_total_damages
            })


### Rank 

state_disaster_results = {}

# 
for state, disaster_events in state_disaster_data.items():

    """
        Frequency / Severity Key Values:
            - Low: Outside -1 Standard Deviation or Median Absolute Deviation
            - Moderate: Between -1.0 and 1.0 Standard Deviation or Median Absolute Deviation
            - High: Outside 1.0 Standard Deviation or Median Absolute Deviation
    """

    for event in disaster_events:
        event_total_deaths = event['Total_Deaths']
        event_total_deaths = event['Total_Deaths']
        event_total_deaths = event['Total_Deaths']

    # Frequency Analysis


    # Severity Analysis


           
# Save Results Dictionary as JSON File
# with open(f"data_ranking/ranked_data/State_NaturalDisaster_Ranked_Data.json", 'w') as f:
#     json.dump(zip_code_weather_data, f)






