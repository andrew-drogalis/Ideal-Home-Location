import json
from collections import defaultdict
from statistics import mean
from math_functions.statistics_analysis import statistics_calc
from math_functions.ranking_functions import rank_extreme_value

"""
    Rank the Natural Disaster Processed Data & Store Results in JSON
"""

# Import Processed Natural Disaster Data
with open('./data_processors/processed_data/State_Natural_Disaster_Data.json', newline='') as f: 
    state_disaster_data = json.load(f)

with open('./data_processors/processed_data/All_Natural_Disaster_Data.json', newline='') as f: 
    all_disaster_data = json.load(f)

with open('./data_processors/processed_data/Type_Natural_Disaster_Data.json', newline='') as f: 
    disaster_by_type_data = json.load(f)


### Analyze ALL National Disaster Data to Determine Relative Severity
"""
    Frequency Ommited from Nationwide Analysis. No meaningful results concluded. All regions have similar frequency independent of disaster type.
"""

all_disaster_results = {}
# Seperate Data into Individual Lists
total_death_list = [event['Total_Deaths'] for event in all_disaster_data]
total_damages_list = [event['Total_Damages'] for event in all_disaster_data]


# ALL Nationwide Total Deaths
total_death_results = statistics_calc(dataset=total_death_list, name_of_data='Total_Deaths')
all_disaster_results.update(total_death_results)

# All Nationwide Total Damages
total_damages_results = statistics_calc(dataset=total_damages_list, name_of_data='Total_Damages')
all_disaster_results.update(total_damages_results)


### Analyze the Type of Disaster Data to Determine Relative Severity & Frequency 

""" 
    Note: Rare Events are omitted from Severity Analysis, these events recieve a Low Frequency Rank
    A 95% Confidence Interval was used to determine of the events occured with a greater than 0 mean frequency
        '''python
            confidence_interval = 1.960 * frequency_results['Standard_Deviation_Frequency'] / len(frequency_list) ** 0.5
            upper_bounds = frequency_results['Mean_Frequency'] + confidence_interval
            lower_bounds = frequency_results['Mean_Frequency'] - confidence_interval
            if lower_bounds < 0:
                print('Event omitted from Severity Rank')
        '''
"""
disaster_by_type_results = defaultdict(dict)
# 
for disaster_type, disaster_type_events in disaster_by_type_data.items():

    if disaster_type not in ['Landslide', 'Volcanic activity', 'Sand/Dust storm']:
    
        total_death_list = [event['Total_Deaths'] for event in disaster_type_events]
        total_damages_list = [event['Total_Damages'] for event in disaster_type_events]

        events_per_year = defaultdict(list)
        for event in disaster_type_events: 
            events_per_year[event['Year']].append(1)
        frequency_list = [sum(events_per_year[f'{i}']) for i in range(1900,2022)]

        # Total Death Statistics
        total_death_results = statistics_calc(dataset=total_death_list, name_of_data='Total_Deaths')
        disaster_by_type_results[disaster_type].update(total_death_results)

        # Total Damages Statistics
        total_damages_results = statistics_calc(dataset=total_damages_list, name_of_data='Total_Damages')
        disaster_by_type_results[disaster_type].update(total_damages_results)

        # Frequency Statistics
        frequency_results = statistics_calc(dataset=frequency_list, name_of_data='Frequency')
        disaster_by_type_results[disaster_type].update(frequency_results)


### Analyze State Data to Rank Natural Disaster Severity & Frequency

state_disaster_results = {}
# 
for state, disaster_events in state_disaster_data.items():

    total_deaths = [event['Total_Deaths'] for event in disaster_events]
    total_damages = [event['Total_Damages'] for event in disaster_events]

    #
    total_deaths_mean = mean(total_deaths)
    total_damages_mean = mean(total_damages)

    #
    all_total_deaths_mean = all_disaster_results['Mean_Total_Deaths']
    all_total_deaths_stdv = all_disaster_results['Standard_Deviation_Total_Deaths']

    all_total_damages_mean = all_disaster_results['Mean_Total_Damages']
    all_total_damages_stdv = all_disaster_results['Standard_Deviation_Total_Damages']

    total_damages_deviation_ratio = (total_damages_mean - all_total_damages_mean) / all_total_damages_stdv
    total_deaths_deviation_ratio = (total_deaths_mean - all_total_deaths_mean) / all_total_deaths_stdv
    average_deviation_ratio = (total_deaths_deviation_ratio + total_damages_deviation_ratio) / 2

    severity_rank = rank_extreme_value(deviation_ratio=average_deviation_ratio)

    #print(state, average_deviation_ratio, severity_rank)

    state_disaster_results.update({state:{
        'All_Severity_Rank': severity_rank,
        }
    })

    # Sort Total Events by Disaster Type
    state_disaster_by_type = defaultdict(list)
    for event in disaster_events:
        disaster_type = event['Disaster_Type']
        state_disaster_by_type[disaster_type].append(event)

    # For Each Disaster Type Rank Severity & Frequency
    for disaster_type, disaster_type_events in state_disaster_by_type.items():
        if disaster_type not in ['Landslide', 'Volcanic activity', 'Sand/Dust storm']:
            type_total_deaths = [event['Total_Deaths'] for event in disaster_type_events]
            type_total_damages = [event['Total_Damages'] for event in disaster_type_events]

            events_per_year = defaultdict(list)
            for event in disaster_type_events: 
                events_per_year[event['Year']].append(1)
            type_frequency_list = [sum(events_per_year[f'{i}']) for i in range(1900,2022)]

            total_deaths_mean = mean(type_total_deaths)
            total_damages_mean = mean(type_total_damages)
            frequency_mean = mean(type_frequency_list)

            type_total_death_mean = disaster_by_type_results[disaster_type]['Mean_Total_Deaths']
            type_total_death_stdv = disaster_by_type_results[disaster_type]['Standard_Deviation_Total_Deaths']

            type_total_damages_mean = disaster_by_type_results[disaster_type]['Mean_Total_Damages']
            type_total_damages_stdv = disaster_by_type_results[disaster_type]['Standard_Deviation_Total_Damages']

            total_deaths_deviation_ratio = (total_deaths_mean - all_total_deaths_mean) / all_total_deaths_stdv
            total_damages_deviation_ratio = (total_damages_mean - all_total_damages_mean) / all_total_damages_stdv
            average_deviation_ratio = (total_deaths_deviation_ratio + total_damages_deviation_ratio) / 2

            severity_rank = rank_extreme_value(deviation_ratio=average_deviation_ratio)

            type_frequency_mean = disaster_by_type_results[disaster_type]['Mean_Frequency']
            type_frequency_stdv = disaster_by_type_results[disaster_type]['Standard_Deviation_Frequency']

            frequency_deviation_ratio = (frequency_mean - all_frequency_mean) / all_frequency_stdv
            frequency_rank = rank_extreme_value(deviation_ratio=frequency_deviation_ratio)

        else:
            severity_rank = None
            frequency_rank = 'Low'

        state_disaster_results.update({state:{
            f'{disaster_type}_Severity_Rank': severity_rank,
            f'{disaster_type}_Frequency_Rank': frequency_rank
            }
        })
    

# ---------------------------------------------------------------------------   

# Save Results Dictionary as JSON File
with open(f"data_ranking/ranked_data/State_Natural_Disaster_Ranked_Data.json", 'w') as f:
    json.dump(state_disaster_results, f)






