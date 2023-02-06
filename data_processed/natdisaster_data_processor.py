import csv, json
from collections import defaultdict
from statistics import mean, median, stdev
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

# Group Natural Disaster Data by Region & Disaster Type
state_names = [*states_dict.keys()]
disaster_type_dict = defaultdict(list)

# Group Natural Disaster Data by Region & Disaster Type
for event in natural_disaster_data:
    year = event[1]
    disaster_type = event[5]
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

    # Add Specificty to Storm Type | Derecho is a prolonged Storm
    if disaster_type == 'Storm' and disaster_subsubtype and disaster_subsubtype != 'Derecho':
        disaster_type = disaster_subsubtype

    # Filter Out Global Events
    if disaster_type != 'Epidemic':
        relevant_disaster_data = {'Year': year, 'Disaster_Type':disaster_type, 'Total_Deaths':total_death, 'Total_Affected':total_affected, 'Total_Damages':total_damages}
        # Update Disaster Type Dictionary
        disaster_type_dict[disaster_type].append(relevant_disaster_data)
        # Update Region Dictionary
        for state in state_names:
            if state in locations:
                states_dict[state].append(relevant_disaster_data)


"""
    Pearson's Calcuation for Skewness - Could use Fisher's but not necessary in this case
    Skew = 3 * (Mean – Median) / Standard Deviation
    Extreme Skewness < -0.20 or Extreme Skewness > 0.20
    If the Dataset has Extreme Skewness, replace the Standard Deviation with the MAD (Median Absolute Deviation)
"""

# Analyze Relative Severity & Frequency of Disaster Type
disaster_data_analysis_dict = {}
for disaster_type, event_values in disaster_type_dict.items():
    # Low Data Disasters will Receive Warning - Not Enough Data for Full Analysis
    if disaster_type not in ['Landslide', 'Volcanic activity', 'Sand/Dust storm']:
        total_death_list = []
        total_affected_list = []
        total_damages_list = []
        year_list = defaultdict(list)
        for values in event_values:
            total_death_list.append(values['Total_Deaths'])
            total_affected_list.append(values['Total_Affected'])
            total_damages_list.append(values['Total_Damages'])
            year_list[values['Year']].append(1)
        
        # Dates of Data From Source File
        year_disaster_count_list = [sum(year_list[f'{i}']) for i in range(1900,2022)]

        # Total Death Statistics
        mean_total_death = mean(total_death_list)
        median_total_death = median(total_death_list)
        stdv_total_death = stdev(total_death_list)
        skewness_total_death = 3 * (mean_total_death - median_total_death) / stdv_total_death if stdv_total_death else 0
        if skewness_total_death > 0.2 or skewness_total_death < -0.2:
            mad_total_death = [abs(x - median_total_death) for x in total_death_list]
            mad_total_death = median(mad_total_death)
        else:
            mad_total_death = None

        # Total Affected Statistics
        mean_total_affected = mean(total_affected_list)    
        median_total_affected = median(total_affected_list)
        stdv_total_affected = stdev(total_affected_list)
        skewness_total_affected = 3 * (mean_total_affected - median_total_affected) / stdv_total_affected if stdv_total_affected else 0
        if skewness_total_death > 0.2 or skewness_total_death < -0.2:
            mad_total_death = [abs(x - median_total_death) for x in total_death_list]
            mad_total_death = median(mad_total_death)
        else:
            mad_total_death = None

        # Total Damages Statistics
        mean_total_damages = mean(total_damages_list)
        median_total_damages = median(total_damages_list)
        stdv_total_damages = stdev(total_damages_list)
        skewness_total_damages = 3 * (mean_total_damages - median_total_damages) / stdv_total_damages if stdv_total_damages else 0
        if skewness_total_death > 0.2 or skewness_total_death < -0.2:
            mad_total_death = [abs(x - median_total_death) for x in total_death_list]
            mad_total_death = median(mad_total_death)
        else:
            mad_total_death = None

        # Frequency Statistics
        mean_frequency = mean(year_disaster_count_list)
        median_frequency = median(year_disaster_count_list)
        stdv_frequency = stdev(year_disaster_count_list)
        skewness_frequency = 3 * (mean_frequency - median_frequency) / stdv_frequency if stdv_frequency else 0
        if skewness_frequency > 0.2 or skewness_frequency < -0.2:
            mad_frequency = [abs(x - median_frequency) for x in year_disaster_count_list]
            mad_frequency = median(mad_frequency)
        else:
            mad_frequency = None

        disaster_data_analysis_dict.update({disaster_type:
            {
                'Mean_Total_Death': mean_total_death, 'Median_Total_Death': median_total_death, 'STDV_Total_Death':stdv_total_death, 'MAD_Total_Death':mad_total_death,
                'Mean_Total_Affected': mean_total_affected, 'Median_Total_Affected': median_total_affected, 'STDV_Total_Affected':stdv_total_affected, 
                'Mean_Total_Damages': mean_total_damages, 'Median_Total_Damages': median_total_damages, 'STDV_Total_Damages':stdv_total_damages,
                'Mean_Frequency': mean_frequency, 'Median_Frequency': median_freqency, 'STDV_Frequency':stdv_frequency
            }
        })

"""
    Frequency / Severity Key Values:
        - Low: Outside -1 Standard Deviation or Median Absolute Deviation
        - Moderate: Between -1.0 and 1.0 Standard Deviation or Median Absolute Deviation
        - High: Outside 1.0 Standard Deviation or Median Absolute Deviation
"""

# State By State Risk Analysis
for state, event_values in states_disaster_dict.items(): pass

    # Frequency Analysis


    # Severity Analysis


           
# Save File
# with open(f"{file_name}_Days_Count.json", 'w') as json_file: 
#     json.dump({name: self.data_dict[name], 'Data_Length': data_length}, json_file)






