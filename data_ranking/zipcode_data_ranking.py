import json
from collections import defaultdict
from math_functions.statistics_analysis import statistics_calc
from math_functions.ranking_functions import rank_value, rank_value_skewed

"""
    Rank the Zipcode Data & Store Results in JSON

    Only Rainfall and Sunshine are Ranked on a National Level
    The Temperature will be user selected.
    Rational: Users typically know comfortable temperature data as a number, but rainfall and sunshine in terms of qualitative amounts. example: "A lot of rainfall" NOT " 1.4 inches of rainfall"
"""

# Import Processed Zipcode Data
with open('./data_processors/processed_data/All_Zipcode_Metrics_Data.json', newline='') as f: 
    all_zipcode_metrics_data = json.load(f)

with open('./data_processors/processed_data/Zipcode_Prefix_Metrics_Data.json', newline='') as f: 
    zipcode_prefix_metrics_data = json.load(f)

with open('./data_processors/processed_data/Zipcode_Metrics_Data.json', newline='') as f: 
    city_metrics_data = json.load(f)


### Analyze ALL National Disaster Data to Determine Relative Severity

all_zipcode_results = {}
# Separate Data into Individual Lists
percentage_married_list = all_zipcode_metrics_data['Married_Percentage']
families_with_children_list = all_zipcode_metrics_data['Families_with_Children']
home_occupancy_list = all_zipcode_metrics_data['Home_Occupancy']
employment_percentage_list = all_zipcode_metrics_data['Employment_Percentage']
school_enrollment_list = all_zipcode_metrics_data['School_Enrollment_Percentage']
motor_vehicle_list = all_zipcode_metrics_data['Motor_Vehicle_Work_Percentage']
public_transportation_list = all_zipcode_metrics_data['Public_Transportation_Work_Percentage']
walking_biking_list = all_zipcode_metrics_data['Walking_Biking_Work_Percentage']


# ALL Percent Married
married_percent_results = statistics_calc(dataset=percentage_married_list, name_of_data="Married_Percentage")
all_zipcode_results.update(married_percent_results)

# ALL Families with Children
families_with_children_results = statistics_calc(dataset=families_with_children_list, name_of_data="Families_with_Children")
all_zipcode_results.update(families_with_children_results)

# ALL Home Occupancy
home_occupancy_results = statistics_calc(dataset=home_occupancy_list, name_of_data="Home_Occupancy")
all_zipcode_results.update(home_occupancy_results)

# ALL Employment Percentage
employment_results = statistics_calc(dataset=employment_percentage_list, name_of_data="Employment_Percentage")
all_zipcode_results.update(employment_results)

# ALL School Enrollment
school_enrollment_results = statistics_calc(dataset=school_enrollment_list, name_of_data="School_Enrollment_Percentage")
all_zipcode_results.update(school_enrollment_results)

# ALL Motor Vehicle to Work
motor_vehicle_results = statistics_calc(dataset=motor_vehicle_list, name_of_data="Motor_Vehicle_Work_Percentage")
all_zipcode_results.update(motor_vehicle_results)

# ALL Public Transportation to Work
public_transportation_results = statistics_calc(dataset=public_transportation_list, name_of_data="Public_Transportation_Work_Percentage")
all_zipcode_results.update(public_transportation_results)

# ALL Walking & Biking to Work
walking_biking_results = statistics_calc(dataset=walking_biking_list, name_of_data="Walking_Biking_Work_Percentage")
all_zipcode_results.update(walking_biking_results)


### Analyze Zipcode Prefix Metrics Data to Determine Relative Severity

zipcode_prefix_results = {}
zipcode_metrics_results = {}
# Seperate Data into Individual Lists
for zipcode_prefix, metrics_data in zipcode_prefix_metrics_data.items():
    
    married_percent = metrics_data['Married_Percentage']
    families_with_children = metrics_data['Families_with_Children']
    home_occupancy = metrics_data['Home_Occupancy']
    employment_percent = metrics_data['Employment_Percentage']
    school_enrollment = metrics_data['School_Enrollment_Percentage']
    motor_vehicle = metrics_data['Motor_Vehicle_Work_Percentage']
    public_transportation = metrics_data['Public_Transportation_Work_Percentage']
    walking_biking = metrics_data['Walking_Biking_Work_Percentage']

    #
    married_percent_median = all_zipcode_results['Median_Married_Percentage']
    married_percent_mad = all_zipcode_results['MAD_Married_Percentage']

    married_percent_deviation_ratio = (married_percent - married_percent_median) / married_percent_mad if married_percent else None
    married_percent_rank = rank_value(deviation_ratio=married_percent_deviation_ratio) if married_percent else None

    #
    families_with_children_median = all_zipcode_results['Median_Families_with_Children']
    families_with_children_mad = all_zipcode_results['MAD_Families_with_Children']

    families_with_children_deviation_ratio = (families_with_children - families_with_children_median) / families_with_children_mad if families_with_children else None
    families_with_children_rank = rank_value(deviation_ratio=families_with_children_deviation_ratio) if families_with_children else None

    #
    home_occupancy_median = all_zipcode_results['Median_Home_Occupancy']
    home_occupancy_mad = all_zipcode_results['MAD_Home_Occupancy']

    home_occupancy_deviation_ratio = (home_occupancy - home_occupancy_median) / home_occupancy_mad if home_occupancy else None
    home_occupancy_rank = rank_value(deviation_ratio=home_occupancy_deviation_ratio) if home_occupancy else None

    #
    employment_percent_median = all_zipcode_results['Median_Employment_Percentage']
    employment_percent_mad = all_zipcode_results['MAD_Employment_Percentage']

    employment_percent_deviation_ratio = (employment_percent - employment_percent_median) / employment_percent_mad if employment_percent else None
    employment_percent_rank = rank_value(deviation_ratio=employment_percent_deviation_ratio) if employment_percent else None

    #
    school_enrollment_median = all_zipcode_results['Median_School_Enrollment_Percentage']
    school_enrollment_mad = all_zipcode_results['MAD_School_Enrollment_Percentage']

    school_enrollment_deviation_ratio = (school_enrollment - school_enrollment_median) / school_enrollment_mad if school_enrollment else None
    school_enrollment_rank = rank_value(deviation_ratio=school_enrollment_deviation_ratio) if school_enrollment else None

    #
    motor_vehicle_median = all_zipcode_results['Median_Motor_Vehicle_Work_Percentage']
    motor_vehicle_mad = all_zipcode_results['MAD_Motor_Vehicle_Work_Percentage']

    motor_vehicle_deviation_ratio = (motor_vehicle - motor_vehicle_median) / motor_vehicle_mad if motor_vehicle else None
    motor_vehicle_rank = rank_value(deviation_ratio=motor_vehicle_deviation_ratio) if motor_vehicle else None

    #
    public_transportation_mean = all_zipcode_results['Mean_Public_Transportation_Work_Percentage']
    public_transportation_stdv = all_zipcode_results['Standard_Deviation_Public_Transportation_Work_Percentage']

    public_transportation_deviation_ratio = (public_transportation - public_transportation_mean) / public_transportation_stdv if public_transportation else None
    public_transportation_rank = rank_value_skewed(deviation_ratio=public_transportation_deviation_ratio) if public_transportation else None

    #
    walking_biking_mean = all_zipcode_results['Mean_Walking_Biking_Work_Percentage']
    walking_biking_stdv = all_zipcode_results['Standard_Deviation_Walking_Biking_Work_Percentage']

    walking_biking_deviation_ratio = (walking_biking - walking_biking_mean) / walking_biking_stdv if walking_biking else None
    walking_biking_rank = rank_value_skewed(deviation_ratio=walking_biking_deviation_ratio) if walking_biking else None


    # Update Zipcode Prefix Data
    metrics_data.update({
        'Married_Percentage': married_percent_rank,
        'Families_with_Children': families_with_children_rank,
        'Home_Occupancy': home_occupancy_rank,
        'Employment_Percentage': employment_percent_rank,
        'School_Enrollment_Percentage': school_enrollment_rank,
        'Motor_Vehicle_Work_Percentage': motor_vehicle_rank,
        'Public_Transportation_Work_Percentage': public_transportation_rank,
        'Walking_Biking_Work_Percentage': walking_biking_rank
    })
    
    zipcode_prefix_results.update({zipcode_prefix:metrics_data})


### Analyze Zipcode Prefix Metrics Data to Determine Relative Severity

for city, city_metrics in city_metrics_data.items():
    
    married_percent = city_metrics['Married_Percentage']
    families_with_children = city_metrics['Families_with_Children']
    home_occupancy = city_metrics['Home_Occupancy']
    employment_percent = city_metrics['Employment_Percentage']
    school_enrollment = city_metrics['School_Enrollment_Percentage']
    motor_vehicle = city_metrics['Motor_Vehicle_Work_Percentage']
    public_transportation = city_metrics['Public_Transportation_Work_Percentage']
    walking_biking = city_metrics['Walking_Biking_Work_Percentage']

    # 
    married_percent_deviation_ratio = (married_percent - married_percent_median) / married_percent_mad if married_percent else None
    married_percent_rank = rank_value(deviation_ratio=married_percent_deviation_ratio) if married_percent else None

    families_with_children_deviation_ratio = (families_with_children - families_with_children_median) / families_with_children_mad if families_with_children else None
    families_with_children_rank = rank_value(deviation_ratio=families_with_children_deviation_ratio) if families_with_children else None

    home_occupancy_deviation_ratio = (home_occupancy - home_occupancy_median) / home_occupancy_mad if home_occupancy else None
    home_occupancy_rank = rank_value(deviation_ratio=home_occupancy_deviation_ratio) if home_occupancy else None

    employment_percent_deviation_ratio = (employment_percent - employment_percent_median) / employment_percent_mad if employment_percent else None
    employment_percent_rank = rank_value(deviation_ratio=employment_percent_deviation_ratio) if employment_percent else None

    school_enrollment_deviation_ratio = (school_enrollment - school_enrollment_median) / school_enrollment_mad if school_enrollment else None
    school_enrollment_rank = rank_value(deviation_ratio=school_enrollment_deviation_ratio) if school_enrollment else None

    motor_vehicle_deviation_ratio = (motor_vehicle - motor_vehicle_median) / motor_vehicle_mad if motor_vehicle else None
    motor_vehicle_rank = rank_value(deviation_ratio=motor_vehicle_deviation_ratio) if motor_vehicle else None

    public_transportation_deviation_ratio = (public_transportation - public_transportation_mean) / public_transportation_stdv if public_transportation else None
    public_transportationt_rank = rank_value_skewed(deviation_ratio=public_transportation_deviation_ratio) if public_transportation else None

    walking_biking_deviation_ratio = (walking_biking - walking_biking_mean) / walking_biking_stdv if walking_biking else None
    walking_biking_rank = rank_value_skewed(deviation_ratio=walking_biking_deviation_ratio) if walking_biking else None

    # Update Zipcode Data
    city_metrics.update({
        'Married_Percentage': married_percent_rank,
        'Families_with_Children': families_with_children_rank,
        'Home_Occupancy': home_occupancy_rank,
        'Employment_Percentage': employment_percent_rank,
        'School_Enrollment_Percentage': school_enrollment_rank,
        'Motor_Vehicle_Work_Percentage': motor_vehicle_rank,
        'Public_Transportation_Work_Percentage': public_transportation_rank,
        'Walking_Biking_Work_Percentage': walking_biking_rank
    })

    zipcode_metrics_results.update({city:city_metrics})


# ---------------------------------------------------------------------------

# Save Results Dictionary as JSON File
with open(f"data_ranking/ranked_data/Zipcode_Prefix_Ranked_Data.json", 'w') as f:
    json.dump(zipcode_prefix_results, f)

with open(f"data_ranking/ranked_data/Zipcode_Ranked_Data.json", 'w') as f:
    json.dump(zipcode_metrics_results, f)





