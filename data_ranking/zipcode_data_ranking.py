import json
from collections import defaultdict
from math_functions.statistics_analysis import statistics_calc
from math_functions.ranking_functions import rank_value, rank_value_skewed

"""
    Rank the Zipcode Data & Store Results in JSON

    Only The Zipcode Metrics Provided in this File will be Ranked on a National Level
    All others will be quantitatively user selected.
    Rational: Users typically know income, household values, and education data as a number, but other metrics in terms of qualitative amounts. example: "A high percentage of married people" NOT "17.4% of married persons"
"""

# Import Processed Zipcode Data
with open('./data_processors/processed_data/All_Zipcode_Metrics_Data.json', newline='') as f: 
    all_zipcode_metrics_data = json.load(f)

with open('./data_processors/processed_data/Zipcode_Metrics_Data.json', newline='') as f: 
    city_metrics_data = json.load(f)


### Analyze ALL Zipcode Metrics Data

all_zipcode_results = {}

# ALL Percent Married
married_percent_results = statistics_calc(dataset=all_zipcode_metrics_data['Married_Percentage'], name_of_data="Married_Percentage")
all_zipcode_results.update(married_percent_results)

# ALL Families with Children
families_with_children_results = statistics_calc(dataset=all_zipcode_metrics_data['Families_with_Children'], name_of_data="Families_with_Children")
all_zipcode_results.update(families_with_children_results)

# ALL Home Occupancy
home_occupancy_results = statistics_calc(dataset=all_zipcode_metrics_data['Home_Occupancy'], name_of_data="Home_Occupancy")
all_zipcode_results.update(home_occupancy_results)

# ALL Employment Percentage
employment_results = statistics_calc(dataset=all_zipcode_metrics_data['Employment_Percentage'], name_of_data="Employment_Percentage")
all_zipcode_results.update(employment_results)

# ALL School Enrollment
school_enrollment_results = statistics_calc(dataset=all_zipcode_metrics_data['School_Enrollment_Percentage'], name_of_data="School_Enrollment_Percentage")
all_zipcode_results.update(school_enrollment_results)

# ALL Motor Vehicle to Work
motor_vehicle_results = statistics_calc(dataset=all_zipcode_metrics_data['Motor_Vehicle_Work_Percentage'], name_of_data="Motor_Vehicle_Work_Percentage")
all_zipcode_results.update(motor_vehicle_results)

# ALL Public Transportation to Work
public_transportation_results = statistics_calc(dataset=all_zipcode_metrics_data['Public_Transportation_Work_Percentage'], name_of_data="Public_Transportation_Work_Percentage")
all_zipcode_results.update(public_transportation_results)

# ALL Walking & Biking to Work
walking_biking_results = statistics_calc(dataset=all_zipcode_metrics_data['Walking_Biking_Work_Percentage'], name_of_data="Walking_Biking_Work_Percentage")
all_zipcode_results.update(walking_biking_results)


### Analyze Zipcode Metrics Data to Rank Values

zipcode_metrics_results = {}
# Check All Zipcodes for Deviation from Median & Rank Data
for city, city_metrics in city_metrics_data.items():
    
    married_percent = city_metrics['Married_Percentage']
    families_with_children = city_metrics['Families_with_Children']
    home_occupancy = city_metrics['Home_Occupancy']
    employment_percent = city_metrics['Employment_Percentage']
    school_enrollment = city_metrics['School_Enrollment_Percentage']
    motor_vehicle = city_metrics['Motor_Vehicle_Work_Percentage']
    public_transportation = city_metrics['Public_Transportation_Work_Percentage']
    walking_biking = city_metrics['Walking_Biking_Work_Percentage']

    # Deviation from Median or Mean (See Ranking Functions) and Determine Rank
    married_percent_deviation_ratio = (married_percent - all_zipcode_results['Median_Married_Percentage']) / all_zipcode_results['MAD_Married_Percentage'] if married_percent else None
    married_percent_rank = rank_value(deviation_ratio=married_percent_deviation_ratio) if married_percent else None

    families_with_children_deviation_ratio = (families_with_children - all_zipcode_results['Median_Families_with_Children']) / all_zipcode_results['MAD_Families_with_Children'] if families_with_children else None
    families_with_children_rank = rank_value(deviation_ratio=families_with_children_deviation_ratio) if families_with_children else None

    home_occupancy_deviation_ratio = (home_occupancy - all_zipcode_results['Median_Home_Occupancy']) / all_zipcode_results['MAD_Home_Occupancy'] if home_occupancy else None
    home_occupancy_rank = rank_value(deviation_ratio=home_occupancy_deviation_ratio) if home_occupancy else None

    employment_percent_deviation_ratio = (employment_percent - all_zipcode_results['Median_Employment_Percentage']) / all_zipcode_results['MAD_School_Enrollment_Percentage'] if employment_percent else None
    employment_percent_rank = rank_value(deviation_ratio=employment_percent_deviation_ratio) if employment_percent else None

    school_enrollment_deviation_ratio = (school_enrollment - all_zipcode_results['Median_School_Enrollment_Percentage']) / all_zipcode_results['MAD_School_Enrollment_Percentage'] if school_enrollment else None
    school_enrollment_rank = rank_value(deviation_ratio=school_enrollment_deviation_ratio) if school_enrollment else None

    motor_vehicle_deviation_ratio = (motor_vehicle - all_zipcode_results['Median_Motor_Vehicle_Work_Percentage']) / all_zipcode_results['MAD_Motor_Vehicle_Work_Percentage'] if motor_vehicle else None
    motor_vehicle_rank = rank_value(deviation_ratio=motor_vehicle_deviation_ratio) if motor_vehicle else None

    public_transportation_deviation_ratio = (public_transportation - all_zipcode_results['Mean_Public_Transportation_Work_Percentage']) / all_zipcode_results['Standard_Deviation_Public_Transportation_Work_Percentage'] if public_transportation else None
    public_transportationt_rank = rank_value_skewed(deviation_ratio=public_transportation_deviation_ratio) if public_transportation else None

    walking_biking_deviation_ratio = (walking_biking - all_zipcode_results['Mean_Walking_Biking_Work_Percentage']) / all_zipcode_results['Standard_Deviation_Walking_Biking_Work_Percentage'] if walking_biking else None
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
with open(f"data_ranking/ranked_data/Zipcode_Ranked_Data.json", 'w') as f:
    json.dump(zipcode_metrics_results, f)





