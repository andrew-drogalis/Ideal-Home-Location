import json
from collections import defaultdict
from centroid_and_deviation import centroid_and_deviation_calc

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


### Analyze ALL National Disaster Data to Determine Relative Severity

# Init Results Dictionary
all_disaster_results = {}
# Seperate Data into Individual Lists
total_death_list = [event['Total_Deaths'] for event in all_disaster_data]
total_affected_list = [event['Total_Affected'] for event in all_disaster_data]
total_damages_list = [event['Total_Damages'] for event in all_disaster_data]

# ALL Total Deaths
total_death_results = centroid_and_deviation_calc(dataset=total_death_list, name_of_data='Total_Death')
all_disaster_results.update(total_death_results)

# ALL Total Affected
total_affected_results = centroid_and_deviation_calc(dataset=total_affected_list, name_of_data='Total_Affected')
all_disaster_results.update(total_affected_results)

# All Total Damages
total_damages_results = centroid_and_deviation_calc(dataset=total_damages_list, name_of_data='Total_Damages')
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
        yearly_frequency_results = centroid_and_deviation_calc(dataset=yearly_frequency_list, name_of_data='Yearly_Frequency')
        disaster_by_type_results[disaster_type].update(yearly_frequency_results)

        # Total Death Statistics
        total_death_results = centroid_and_deviation_calc(dataset=total_death_list, name_of_data='Total_Death')
        disaster_by_type_results[disaster_type].update(total_death_results)

        # Total Affected Statistics
        total_affected_results = centroid_and_deviation_calc(dataset=total_affected_list, name_of_data='Total_Affected')
        disaster_by_type_results[disaster_type].update(total_affected_results)

        # Total Damages Statistics
        total_damages_results = centroid_and_deviation_calc(dataset=total_damages_list, name_of_data='Total_Damages')
        disaster_by_type_results[disaster_type].update(total_damages_results)



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






