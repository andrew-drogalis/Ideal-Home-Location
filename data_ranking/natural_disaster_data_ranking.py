import json
from collections import defaultdict
from statistics import mean
from math_functions.statistics_analysis import statistics_calc
from math_functions.ranking_functions import rank_value, rank_value_skewed

"""
    Rank the Natural Disaster Processed Data & Store Results in JSON

    Note: Rare Events are omitted from Data Analysis
    A 98% Confidence Interval was used to determine of the events occured with a greater than 0 mean frequency
        # Insert at Line 67
        '''python
            events_per_year = defaultdict(list)
            for event in disaster_type_events: 
                events_per_year[event['Year']].append(1)
            frequency_list = [sum(events_per_year[f'{i}']) for i in range(1900,2022)]

            # Frequency Statistics
            frequency_results = statistics_calc(dataset=frequency_list, name_of_data='Frequency')

            confidence_interval = 2.326 * frequency_results['Standard_Deviation_Frequency'] / len(frequency_list) ** 0.5
            upper_bounds = frequency_results['Mean_Frequency'] + confidence_interval
            lower_bounds = frequency_results['Mean_Frequency'] - confidence_interval
            if lower_bounds < 0:
                print('Event omitted from Ranking')
        '''
"""

# Import Processed Natural Disaster Data
with open('./data_processors/processed_data/State_Natural_Disaster_Data.json', newline='') as f: 
    state_disaster_data = json.load(f)

with open('./data_processors/processed_data/All_Natural_Disaster_Data.json', newline='') as f: 
    all_disaster_data = json.load(f)

with open('./data_processors/processed_data/Type_Natural_Disaster_Data.json', newline='') as f: 
    disaster_by_type_data = json.load(f)


### Analyze ALL National Disaster Data

all_disaster_results = {}
# Seperate Data into Individual Lists
total_death_list = [event['Total_Deaths'] for event in all_disaster_data if event['Total_Deaths'] != 0]
total_damages_list = [event['Total_Damages'] for event in all_disaster_data if event['Total_Damages'] != 0]
frequency_disaster_per_state = [len(disasters_per_state) for disasters_per_state in [*state_disaster_data.values()]]

# ALL Nationwide Total Deaths
total_death_results = statistics_calc(dataset=total_death_list, name_of_data='Total_Deaths')
all_disaster_results.update(total_death_results)

# All Nationwide Total Damages
total_damages_results = statistics_calc(dataset=total_damages_list, name_of_data='Total_Damages')
all_disaster_results.update(total_damages_results)

# All Nationwide Frequency of Disaster Per State 
frequency_results = statistics_calc(dataset=frequency_disaster_per_state, name_of_data='Frequency_Per_State')
all_disaster_results.update(frequency_results)


### Analyze the Type of Disaster Data

disaster_by_type_results = defaultdict(dict)
# Analyze Frequency and Severity by Disaster Type
for disaster_type, disaster_type_events in disaster_by_type_data.items():

    if disaster_type not in ['Landslide', 'Volcanic activity', 'Sand/Dust storm']:
    
        total_death_list = [event['Total_Deaths'] for event in disaster_type_events if event['Total_Deaths'] != 0]
        total_damages_list = [event['Total_Damages'] for event in disaster_type_events if event['Total_Damages'] != 0]

        frequency_disaster_type_per_state = []
        for disasters_per_state in [*state_disaster_data.values()]:
            i = sum([1 for disaster in disasters_per_state if disaster['Disaster_Type'] == disaster_type])  
            if i: frequency_disaster_type_per_state.append(i)

        # Total Death Statistics
        total_death_results = statistics_calc(dataset=total_death_list, name_of_data='Total_Deaths') if len(total_death_list) > 1 else {}
        disaster_by_type_results[disaster_type].update(total_death_results)

        # Total Damages Statistics
        total_damages_results = statistics_calc(dataset=total_damages_list, name_of_data='Total_Damages') if len(total_damages_list) > 1 else {}
        disaster_by_type_results[disaster_type].update(total_damages_results)

        # Frequency Statistics
        frequency_results = statistics_calc(dataset=frequency_disaster_type_per_state, name_of_data='Frequency_Per_State')
        disaster_by_type_results[disaster_type].update(frequency_results)


### Analyze State Data to Rank Natural Disaster Severity & Frequency

state_disaster_results = defaultdict(list)
# Analyze Disasters by State
for state, disaster_events in state_disaster_data.items():

    total_deaths = sorted([event['Total_Deaths'] for event in disaster_events])
    total_damages = sorted([event['Total_Damages'] for event in disaster_events])

    # Top Quartile of Disaster Total Deaths and Total Damages
    total_deaths = total_deaths[-(max(1, int(len(total_deaths)/4))):]
    total_damages = total_damages[-(max(1, int(len(total_damages)/4))):]
    total_deaths_mean = mean(total_deaths)
    total_damages_mean = mean(total_damages)
    frequency = len(disaster_events)

    # Average Total Deaths & Total Damages for Approximate Severity
    total_damages_deviation_ratio = (total_damages_mean - all_disaster_results['Mean_Total_Damages']) / all_disaster_results['Standard_Deviation_Total_Damages']
    total_deaths_deviation_ratio = (total_deaths_mean - all_disaster_results['Mean_Total_Deaths']) / all_disaster_results['Standard_Deviation_Total_Deaths']
    average_deviation_ratio = (total_deaths_deviation_ratio + total_damages_deviation_ratio) / 2

    severity_rank = rank_value_skewed(deviation_ratio=average_deviation_ratio, rank_label='naturaldisaster')

    frequency_deviation_ratio = (frequency - all_disaster_results['Median_Frequency_Per_State']) / all_disaster_results['MAD_Frequency_Per_State']
    frequency_rank = rank_value(deviation_ratio=frequency_deviation_ratio)

    # Store Relative Rank for Nationwide Data
    state_disaster_results[state].append(
        {
            'All_Severity_Rank': severity_rank,
            'All_Frequency_Rank': frequency_rank
        }
    )


    ## Sort Total Events by Disaster Type
    state_disaster_by_type = defaultdict(list)
    for event in disaster_events:
        disaster_type = event['Disaster_Type']
        state_disaster_by_type[disaster_type].append(event)


    ## For Each Disaster Type in Each State Rank Severity & Frequency
    for disaster_type, disaster_type_events in state_disaster_by_type.items():
        if disaster_type not in ['Landslide', 'Volcanic activity', 'Sand/Dust storm']:
            
            type_total_deaths = sorted([event['Total_Deaths'] for event in disaster_type_events])
            type_total_damages = sorted([event['Total_Damages'] for event in disaster_type_events])
            frequency = len(disaster_type_events)

            # Top Quartile of Disaster Total Deaths and Total Damages
            type_total_deaths = type_total_deaths[-(max(1, int(len(type_total_deaths)/4))):]
            type_total_damages = type_total_damages[-(max(1, int(len(type_total_damages)/4))):]
            total_deaths_mean = mean(type_total_deaths) if type_total_deaths else 0
            total_damages_mean = mean(type_total_damages) if type_total_damages else 0

            try:
                total_deaths_deviation_ratio = (total_deaths_mean - disaster_by_type_results[disaster_type]['Mean_Total_Deaths']) / disaster_by_type_results[disaster_type]['Standard_Deviation_Total_Deaths']
            except:
                total_deaths_deviation_ratio = None

            try:
                total_damages_deviation_ratio = (total_damages_mean - disaster_by_type_results[disaster_type]['Mean_Total_Damages']) / disaster_by_type_results[disaster_type]['Standard_Deviation_Total_Damages']
            except:
                total_damages_deviation_ratio = None

            # Average Total Deaths & Total Damages for Approximate Severity
            average_deviation_ratio = (total_deaths_deviation_ratio + total_damages_deviation_ratio) / 2 if total_deaths_deviation_ratio and total_damages_deviation_ratio else total_deaths_deviation_ratio if total_deaths_deviation_ratio else total_damages_deviation_ratio if total_deaths_deviation_ratio else -1
            severity_rank = rank_value_skewed(deviation_ratio=average_deviation_ratio, rank_label='natural_disaster')

            frequency_deviation_ratio = (frequency - disaster_by_type_results[disaster_type]['Median_Frequency_Per_State']) / disaster_by_type_results[disaster_type]['MAD_Frequency_Per_State']
            frequency_rank = rank_value(deviation_ratio=frequency_deviation_ratio)

        # Store Relative Rank for Disaster Type Data
        state_disaster_results[state].append(
            {
                f'{disaster_type}_Severity_Rank': severity_rank,
                f'{disaster_type}_Frequency_Rank': frequency_rank
            }
        )
    

# ---------------------------------------------------------------------------   

# Save Results Dictionary as JSON File
with open(f"data_ranking/ranked_data/State_Natural_Disaster_Ranked_Data.json", 'w') as f:
    json.dump(state_disaster_results, f)






