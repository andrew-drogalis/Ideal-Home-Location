import csv, json
from collections import defaultdict
from constants.usa_states import states_dict

"""
    Process the NatDis_USA Data & Store Results in JSON
"""

# Import Raw Natural Disaster Data
with open('./data_src/EMDAT_1900-2021_NatDis_USA.csv', newline='') as f: 
    natural_disaster_data = list(csv.reader(f))

"""
    Relevant Data:
    key:  1 -> field: Year
    key:  5 -> field: Disaster Type
    key:  6 -> field: Disaster SubType
    key:  7 -> field: Disaster Subsubtype
    key: 14 -> field: Location
    key: 34 -> field: Total Deaths
    key: 35 -> field: No. Injured
    key: 36 -> field: No. Affected
    key: 37 -> field: No. Homeless
    key: 38 -> field: Total Affected
    key: 41 -> field: Total Damages ('000 USD)

    Note: Due to limitations in the data provided, redundant key information is used. example: No. Affected vs. Total Affected
"""

# Init
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
    no_injured = int(event[35] or 0)
    no_affected = int(event[36] or 0)
    no_homeless = int(event[37] or 0)
    total_affected = int(event[38] or 0)
    total_damages = float(event[41] or 0)
    
    # Calculate Total Affected if not provided
    if not total_affected: 
        total_affected = no_injured + no_affected + no_homeless

    # Add Specificity to Storm Type | Derecho is a prolonged Storm
    if disaster_type == 'Storm' and disaster_subsubtype and disaster_subsubtype != 'Derecho':
        disaster_type = disaster_subsubtype
    elif disaster_type == 'Storm' and disaster_subtype == 'Tropical cyclone':
        disaster_type = disaster_subtype

    # Filter Out Global Events
    if disaster_type != 'Epidemic':
        relevant_disaster_data = {'Year': year, 'Disaster_Type':disaster_type, 'Total_Deaths':total_death, 'Total_Affected':total_affected, 'Total_Damages':total_damages}
        # Update Region Dictionary
        for state in state_names:
            if state in locations:
                states_dict[state].append(relevant_disaster_data)
        # Update All Disaster List
        all_disaster_data.append(relevant_disaster_data)
        # Update Disaster Type Dictionary
        disaster_by_type_data[disaster_type].append(relevant_disaster_data)


# Save Results Dictionary as JSON File
with open(f"data_processors/processed_data/State_NaturalDisaster_Data.json", 'w') as f:
    json.dump(states_dict, f)

with open(f"data_processors/processed_data/All_NaturalDisaster_Data.json", 'w') as f:
    json.dump(all_disaster_data, f)

with open(f"data_processors/processed_data/Type_NaturalDisaster_Data.json", 'w') as f:
    json.dump(disaster_by_type_data, f)






