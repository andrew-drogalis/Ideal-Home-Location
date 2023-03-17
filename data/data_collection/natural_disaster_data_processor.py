import csv, json
from collections import defaultdict
from constants.usa_states import states_dict

"""
    Process the EMDAT_NatDis_USA Data & Store Results in JSON
"""

# Import Raw Natural Disaster Data
with open('./data/data_sources/EMDAT_1900-2021_NatDis_USA.csv', newline='') as f: 
    natural_disaster_data = list(csv.reader(f))

"""
    Update v0.9.0: After careful review of the data, Total Affected person has been removed from the analysis due to significant lack of data and unclear definition in the data collection methodology

    Relevant Data:
    key:  1 -> field: Year
    key:  5 -> field: Disaster Type
    key:  6 -> field: Disaster SubType
    key:  7 -> field: Disaster Subsubtype
    key: 14 -> field: Location
    key: 34 -> field: Total Deaths
    key: 41 -> field: Total Damages ('000 USD)
"""

state_names = [*states_dict.keys()]
all_disaster_data = []
disaster_by_type_data = defaultdict(list)

# Group Natural Disaster Data by Region & Disaster Type
for event in natural_disaster_data:
    year = event[1]
    disaster_type = event[5]
    disaster_subtype = event[6]
    disaster_subsubtype = event[7]
    locations = event[14]
    total_death = int(event[34] or 0)
    total_damages = float(event[41] or 0)

    # Add Specificity to Storm Type | Derecho is a prolonged Storm
    if disaster_type == 'Storm' and disaster_subsubtype and disaster_subsubtype != 'Derecho':
        disaster_type = disaster_subsubtype
    elif disaster_type == 'Storm' and disaster_subtype == 'Tropical cyclone':
        disaster_type = disaster_subtype

    # Filter Out Global Events
    if disaster_type != 'Epidemic':
        relevant_disaster_data = {'Year': year, 'Disaster_Type':disaster_type, 'Total_Deaths':total_death, 'Total_Damages':total_damages}
        # Update Region Dictionary
        for state in state_names:
            if state in locations:
                states_dict[state].append(relevant_disaster_data)
        # Update All Disaster List
        all_disaster_data.append(relevant_disaster_data)
        # Update Disaster Type Dictionary
        disaster_by_type_data[disaster_type].append(relevant_disaster_data)

# Add District of Columbia 
states_dict.update({'District of Columbia':states_dict['Maryland']})

# Save Results Dictionary as JSON File
with open(f"data/data_collection/processed_data/State_Natural_Disaster_Data.json", 'w') as f:
    json.dump(states_dict, f)

with open(f"data/data_collection/processed_data/All_Natural_Disaster_Data.json", 'w') as f:
    json.dump(all_disaster_data, f)

with open(f"data/data_collection/processed_data/Type_Natural_Disaster_Data.json", 'w') as f:
    json.dump(disaster_by_type_data, f)






