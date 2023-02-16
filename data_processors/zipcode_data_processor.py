import csv, json, sys, pathlib
from statistics import mean
from collections import defaultdict
from uszipcode import SearchEngine
sys.path.insert(1, str(pathlib.Path(__file__).parent.parent))
from data_ranking.math_functions.statistics_analysis import mad_calc

"""
    Process the Zipcode Data & Store Results in JSON
"""

# Import Raw Zipcode Prefix Data
with open('./data_src/USA_Zipcode_3_Digits.csv', newline='') as f: 
    zipcode_prefix_data = list(csv.reader(f))

# Initalize Search Engine & Results Dictionary
search = SearchEngine(
    simple_or_comprehensive=SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive)

city_metric_data = defaultdict(list)
city_coordinate_data = defaultdict(list)
zipcode_prefix_metric_data = {}
all_zipcode_data = {
    'Married_Percentage': [],
    'Families_with_Children': [],
    'Home_Occupancy': [],
    'Employment_Percentage': [],
    'School_Enrollment_Percentage': [], 
    'Motor_Vehicle_Work_Percentage': [],
    'Public_Transportation_Work_Percentage': [],
    'Walking_Biking_Work_Percentage': [],
}

# Store Data for Each Zipcode Prefix
for zip_prefix in zipcode_prefix_data:
    zip_number = zip_prefix[0]
    zip_prefix_search = search.by_prefix(prefix=zip_number, returns=100)
    # Check if Zipcode Prefix is Valid
    if zip_prefix_search:
        # Local Data Storage
        home_income_dict = {
            'Total_Persons': [],
            'Distribution_Profile': []
        }
        home_value_dict = {
            'Total_Persons': [],
            'Distribution_Profile': []
        }
        coordinates_dict = {
            'East_Bounds': [],
            'West_Bounds': [],
            'North_Bounds': [],
            'South_Bounds': [],
            'Latitude': [],
            'Longitude': []
        }
        zip_prefix_search = iter(zip_prefix_search)
        # Analyze Each City in the Zipcode Prefix
        for city in zip_prefix_search:
            ## City Information
            city_name = city.major_city
            state = city.state
            common_city_list = city.common_city_list
            latitude = float(city.lat or 0)
            longitude = float(city.lng or 0)
            if not latitude or not longitude:
                next(zip_prefix_search, None)
                continue

            ## Max Boundary of City Limits
            bounds_west = float(city.bounds_west or longitude)
            bounds_east = float(city.bounds_east or longitude)
            bounds_north = float(city.bounds_north or latitude)
            bounds_south = float(city.bounds_south or latitude)

            ## Common City List 
            if common_city_list and common_city_list[0] != city_name:
                common_city_list = [city_name] + common_city_list
            elif not common_city_list:
                common_city_list = [city_name]
                

            ## Demographic Metrics
            """ Not included in this analysis. """
            # population_by_year = city.population_by_year
            # population_by_age = city.population_by_age
            # population_by_gender = city.population_by_gender
            # population_by_race = city.population_by_race
            # head_of_household_by_age = city.head_of_household_by_age

            ## Family Demographics
            families_vs_singles = city.families_vs_singles
            if families_vs_singles:
                families_vs_singles = families_vs_singles[0]['values']
                # Husband Wife Family Households
                families = int(
                    families_vs_singles[0]['y'])
                # Single Guardian + Single + Single With Roommate
                singles = int(
                    families_vs_singles[1]['y']) + int(families_vs_singles[2]['y']) + int(families_vs_singles[3]['y'])
                # Percent Married of Total Persons
                percent_married = round(families * 100 / (families + singles), 2)
            else:
                percent_married = None

            ## Households with Children Percentage
            households_with_kids = city.households_with_kids
            if households_with_kids:
                households_with_kids = households_with_kids[0]['values']
                without_kids = int(
                    households_with_kids[0]['y'])
                with_kids = int(
                    households_with_kids[1]['y'])
                # Percent of Households with Kids of Total Households
                percent_of_with_kids = round(with_kids * 100 / (with_kids + without_kids), 2)
            else:
                percent_of_with_kids = None

            ## Housing Metrics
            """ Home Value Data has a max value of $750,000+. This will introduce Error into the Mean Absolute Deviation Calculation. """
            owner_occupied_home_values = city.owner_occupied_home_values
            median_home_value = city.median_home_value
            if owner_occupied_home_values and median_home_value:
                owner_occupied_home_values = owner_occupied_home_values[0]['values']
                median_home_value = int(median_home_value)
                # Assumption-Average: $12,500
                val_1_24k = int(
                    owner_occupied_home_values[0]['y'])
                # Assumption-Average: $37,500
                val_25k_49k = int(
                    owner_occupied_home_values[1]['y'])
                # Assumption-Average: $75,000
                val_50k_99k = int(
                    owner_occupied_home_values[2]['y'])
                # Assumption-Average: $125,000
                val_100k_149k = int(
                    owner_occupied_home_values[3]['y'])
                # Assumption-Average: $175,000
                val_150k_199k = int(
                    owner_occupied_home_values[4]['y'])
                # Assumption-Average: $300,000
                val_200k_399k = int(
                    owner_occupied_home_values[5]['y'])
                # Assumption-Average: $575,000
                val_400k_749k = int(
                    owner_occupied_home_values[6]['y'])
                # Assumption-Average: $800,000
                val_750k_plus = int(
                    owner_occupied_home_values[7]['y'])

                # Accounting for Extremely Weathly Neighborhoods
                val_750k_plus_average = max(800_000, median_home_value + 50_000)
                # List of # of People in Each Home Value Range
                persons_list = [val_1_24k, val_25k_49k, val_50k_99k, val_100k_149k, val_150k_199k, val_200k_399k, val_400k_749k, val_750k_plus]
                # Average Home Value in the Range is Assummed
                home_value_list = [12_500, 37_500, 75_000, 125_000, 175_000, 300_000, 575_000, val_750k_plus_average]
                # Create List of Each Home Value from Assumed Value List & Persons List
                home_value_distribution_list = []
                for x, home_value in enumerate(home_value_list):
                    home_value_distribution_list += [home_value] * persons_list[x]

                # Median Absolute Deviation
                mad_home_value = round(mad_calc(dataset=home_value_distribution_list, median_of_data=median_home_value))
                # Use for Zipcode Prefix Average
                home_value_dict['Total_Persons'].append(sum(persons_list))
                home_value_dict['Distribution_Profile'].append(home_value_distribution_list)
            else:
                median_home_value = None
                mad_home_value = None

            ## Home Occupancy
            housing_unit = city.housing_units
            occupied_housing_units = city.occupied_housing_units
            if housing_unit and occupied_housing_units:
                housing_unit = int(housing_unit)
                occupied_housing_units = int(occupied_housing_units)
                # Percent of Occupied Homes of Total Homes
                percent_housing_occupancy = round(occupied_housing_units * 100 / housing_unit, 2)
            else:
                percent_housing_occupancy = None
            
            ## Rental Metrics
            """ Rental Unit Data has a max value of $1,000+ per Month. With no median rental unit data provided, it's not possible to accurately break down the true rental costs at this time. """
            # rental_properties_by_number_of_rooms = city.rental_properties_by_number_of_rooms
            # monthly_rent_including_utilities_studio_apt = city.monthly_rent_including_utilities_studio_apt
            # monthly_rent_including_utilities_1_b = city.monthly_rent_including_utilities_1_b
            # monthly_rent_including_utilities_2_b = city.monthly_rent_including_utilities_2_b
            # monthly_rent_including_utilities_3plus_b = city.monthly_rent_including_utilities_3plus_b

            ## Household Income Metrics
            """ Household Income Data has a max value of $200,000+. This will introduce Error into the Mean Absolute Deviation Calculation. """
            household_income = city.household_income
            median_household_income = city.median_household_income
            if household_income and median_household_income:
                household_income = household_income[0]['values']
                median_household_income = int(median_household_income)
                # Assumption-Average: $12,500
                income_less_25k = int(
                    household_income[0]['y'])
                # Assumption-Average: $35,000
                income_25k_45k = int(
                    household_income[1]['y'])
                # Assumption-Average: $52,500
                income_45k_60k = int(
                    household_income[2]['y'])
                # Assumption-Average: $80,000
                income_60k_100k = int(
                    household_income[3]['y'])
                # Assumption-Average: $125,000
                income_100k_149k = int(
                    household_income[4]['y'])
                # Assumption-Average: $175,000
                income_150k_199k = int(
                    household_income[5]['y'])
                # Assumption-Average: $250,000
                income_200k_plus = int(
                    household_income[6]['y'])

                # Accounting for Extremely Weathly Neighborhoods
                income_200k_plus_average = max(250_000, median_household_income + 50_000)
                # List of # of People in Each Income Range
                income_persons_list = [income_less_25k, income_25k_45k, income_45k_60k, income_60k_100k, income_100k_149k, income_150k_199k, income_200k_plus]
                # Average Income in the Range is Assummed
                income_list = [12_500, 35_000, 52_500, 80_000, 125_000, 175_000, income_200k_plus_average]
                # Create List of Each Income from Assumed Income List & Persons List
                income_distribution_list = []
                for x, income in enumerate(income_list):
                    income_distribution_list += [income] * income_persons_list[x]

                # Median Absolute Deviation
                mad_household_income = round(mad_calc(dataset=income_distribution_list, median_of_data=median_household_income))
                # Use for Zipcode Prefix Average
                home_income_dict['Total_Persons'].append(sum(income_persons_list))
                home_income_dict['Distribution_Profile'].append(income_distribution_list)
            else:
                median_household_income = None
                mad_household_income = None

            ## Household Sources of Income
            """ Could be used for a more detailed break down of income streams, but outside the scope for this project. """
            # percent_of_households_receiving_income = city.sources_of_household_income____percent_of_households_receiving_income
            # average_income_per_household_by_income_source = city.sources_of_household_income____average_income_per_household_by_income_source
            # percent_of_households_receiving_investment_income = city.household_investment_income____percent_of_households_receiving_investment_income
            # average_income_per_household_by_income_source = city.household_investment_income____average_income_per_household_by_income_source

            ## Job Opportunity Metrics
            employment_status = city.employment_status
            if employment_status:
                employment_status = employment_status[0]['values']
                # Employed Full-time + Employed Part-time
                employed = int(
                    employment_status[0]['y']) + int(employment_status[1]['y'])
                unemployed = int(
                    employment_status[2]['y'])
                # Percent of Persons Employed of Total Persons
                percent_employed = round(employed * 100 / (employed + unemployed), 2) 
            else:
                percent_employed = None

            ## Work Transportation Metrics
            means_of_transportation_to_work_for_workers_16_and_over = city.means_of_transportation_to_work_for_workers_16_and_over
            if means_of_transportation_to_work_for_workers_16_and_over and employment_status and employed > 0:
                means_of_transportation_to_work_for_workers_16_and_over = means_of_transportation_to_work_for_workers_16_and_over[0]['values']
                # Combined Total of Car, Truck, Van, Motorcycle, and Taxi
                percent_using_motor_vehicle = int(
                    means_of_transportation_to_work_for_workers_16_and_over[0]['y']) + int(means_of_transportation_to_work_for_workers_16_and_over[2]['y']) + int(means_of_transportation_to_work_for_workers_16_and_over[3]['y'])
                percent_using_motor_vehicle = round(percent_using_motor_vehicle * 100 / employed, 2)
                # Percent of Persons Commuting using Public Transportation of Total Employed
                percent_using_public_trasportation = round(int(means_of_transportation_to_work_for_workers_16_and_over[1]['y']) * 100 / employed, 2) 
                # Percent of Persons Commuting using Walking or Biking of Total Employed
                percent_using_walking_biking = round(int(means_of_transportation_to_work_for_workers_16_and_over[4]['y']) * 100 / employed, 2)
            else:
                percent_using_motor_vehicle = None
                percent_using_public_trasportation = None
                percent_using_walking_biking = None
            
            ## Commute Time Metrics
            travel_time_to_work_in_minutes = city.travel_time_to_work_in_minutes
            if travel_time_to_work_in_minutes:
                travel_time_to_work_in_minutes = travel_time_to_work_in_minutes[0]['values']
                # Assumption-Average: 5 mins
                num_less_10 = int(
                    travel_time_to_work_in_minutes[0]['y'])
                # Assumption-Average: 14.5 mins
                num_10_19 = int(
                    travel_time_to_work_in_minutes[1]['y'])
                # Assumption-Average:: 24.5 mins
                num_20_29 = int(
                    travel_time_to_work_in_minutes[2]['y'])
                # Assumption-Average: 34.5 mins
                num_30_39 = int(
                    travel_time_to_work_in_minutes[3]['y'])
                # Assumption-Average: 42 mins
                num_40_44 = int(
                    travel_time_to_work_in_minutes[4]['y'])
                # Assumption-Average: 52 mins
                num_45_59 = int(
                    travel_time_to_work_in_minutes[5]['y'])
                # Assumption-Average: 74.5 mins
                num_60_89 = int(
                    travel_time_to_work_in_minutes[6]['y'])
                # Assumption-Average: 100 mins
                num_plus_90 = int(
                    travel_time_to_work_in_minutes[7]['y'])

                # List of # of People in Each Commuting Time Range
                total_commuters = num_less_10 + num_10_19 + num_20_29 + num_30_39 + num_40_44 + num_45_59 + num_60_89 + num_plus_90
                # Weighted Sum of the # of Commuters * Average Commute Time
                average_travel_time_to_work = ((num_less_10 * 5) + (num_10_19 * 14.5) + (num_20_29 * 24.5)+ (num_30_39 * 34.5) + (num_40_44 * 42) + (num_45_59 * 52) + (num_plus_90 * 100)) / total_commuters
                average_travel_time_to_work = round(average_travel_time_to_work, 2)
            else:
                average_travel_time_to_work = None

            ## Educational Metrics
            """
                Methodology: Each Level of Degree Certification is +1 Point.
                    Less than High School: 0 Points
                    High School Graduate: 1 Point
                    Associate's Degree: 2 Points
                    Bachelor's Degree: 3 Points
                    Professional School Degree: 3 Points (Equivalent to Bachelor's, but for Trade School)
                    Master's Degree: 4 Points
                    Doctorate Degree: 5 Points
            """
            educational_attainment_for_population_25_and_over = city.educational_attainment_for_population_25_and_over
            if educational_attainment_for_population_25_and_over:
                educational_attainment_for_population_25_and_over = educational_attainment_for_population_25_and_over[0]['values']
                less_than_high_school = int(
                    educational_attainment_for_population_25_and_over[0]['y'])
                high_school = int(
                    educational_attainment_for_population_25_and_over[1]['y'])
                associate = int(
                    educational_attainment_for_population_25_and_over[2]['y'])
                bachelor = int(
                    educational_attainment_for_population_25_and_over[3]['y'])
                masters = int(
                    educational_attainment_for_population_25_and_over[4]['y'])
                professional_school = int(
                    educational_attainment_for_population_25_and_over[5]['y'])
                doctorate = int(
                    educational_attainment_for_population_25_and_over[6]['y'])
                # Sum of Total Number of Persons
                total_peoples = less_than_high_school + high_school + associate + bachelor + masters + professional_school + doctorate
                # Weighted Sum of the # of Persons * Education Points
                overall_education_score = ((less_than_high_school * 0) + (high_school * 1) + (associate * 2) + (bachelor * 3) + (professional_school * 3) + (masters * 4) + (doctorate * 5)) / total_peoples
                overall_education_score = round(overall_education_score, 2)
            else:
                overall_education_score = None

            ## School Enrollment Metrics
            school_enrollment_age_3_to_17 = city.school_enrollment_age_3_to_17
            if school_enrollment_age_3_to_17:
                school_enrollment_age_3_to_17 = school_enrollment_age_3_to_17[0]['values']
                # Public School Enrollment + Private School Enrollment
                enrolled_in_school = int(
                    school_enrollment_age_3_to_17[0]['y']) + int(school_enrollment_age_3_to_17[1]['y'])
                # Not Enrolled in School
                not_enrolled_in_school = int(
                    school_enrollment_age_3_to_17[2]['y'])
                # Percent of Students Enrolled in School of Total Students
                percent_enrolled_in_school = round(enrolled_in_school * 100 / (enrolled_in_school + not_enrolled_in_school), 2)
            else:
                percent_enrolled_in_school = None

            ## Population Density
            """
                Reference: https://www2.census.gov/geo/pdfs/reference/GARM/Ch12GARM.pdf
                Urban or Rural Classification Based on US Census Bureau. Additional Intermediate Values added for depth of analysis.
                Classifications of Areas:
                    Hyper Urban: 5,000+ Persons / Square Mile
                    Urban: 4,999 - 1,000 Persons / Square Mile
                    Suburban: 999 - 500 Persons / Square Mile
                    Rural: 499 - 100 Persons / Square Mile
                    Hyper Rural: 99 - 0 Persons / Square Mile
            """
            population_density = int(city.population_density or 0)
            if population_density:
                area_classification = 'Hyper Urban' if population_density >= 5000 else 'Urban' if 5000 > population_density >= 1000 else 'Suburban' if 1000 > population_density >= 500 else 'Rural' if 500 > population_density >= 100 else 'Hyper Rural'
            else:
                area_classification = None

            ## Population & Land Area
            population = int(city.population) if city.population else None
            land_area = float(city.land_area_in_sqmi) if city.land_area_in_sqmi else None

            # Store City Metric Data
            city_metric_data[zip_number].append(
                {
                    'City': f'{city_name}, {state}',
                    'Zipcode': city.zipcode,
                    'Married_Percentage': percent_married,
                    'Families_with_Children': percent_of_with_kids,
                    'Median_Home_Value': median_home_value,
                    'MAD_Home_Value': mad_home_value,
                    'Home_Occupancy': percent_housing_occupancy,
                    'Median_Household_Income': median_household_income,
                    'MAD_Household_Income': mad_household_income,
                    'Employment_Percentage': percent_employed,
                    'Motor_Vehicle_Work_Percentage': percent_using_motor_vehicle,
                    'Public_Transportation_Work_Percentage': percent_using_public_trasportation,
                    'Walking_Biking_Work_Percentage': percent_using_walking_biking,
                    'Travel_Time_To_Work': average_travel_time_to_work,
                    'Education_Score': overall_education_score,
                    'School_Enrollment_Percentage': percent_enrolled_in_school,
                    'Area_Classification': area_classification,
                    'Population': population,
                    'Land_Area_sqmi': land_area
                })

            # All Zipcode Data Storage
            if percent_married:
                all_zipcode_data['Married_Percentage'].append(percent_married)
            if percent_of_with_kids:
                all_zipcode_data['Families_with_Children'].append(percent_of_with_kids)
            if percent_housing_occupancy:
                all_zipcode_data['Home_Occupancy'].append(percent_housing_occupancy)
            if percent_employed:
                all_zipcode_data['Employment_Percentage'].append(percent_employed)
            if percent_enrolled_in_school:
                all_zipcode_data['School_Enrollment_Percentage'].append(percent_enrolled_in_school)
            if percent_using_motor_vehicle:
                all_zipcode_data['Motor_Vehicle_Work_Percentage'].append(percent_using_motor_vehicle)
            if percent_using_public_trasportation:
                all_zipcode_data['Public_Transportation_Work_Percentage'].append(percent_using_public_trasportation)
            if percent_using_walking_biking:
                all_zipcode_data['Walking_Biking_Work_Percentage'].append(percent_using_walking_biking)

            # Each Major City, Common Cities, & Zipcode combined for Fuzzy String Search in Runtime
            city_str = ''
            for common_city in common_city_list:
                if '...' not in common_city:
                    city_str += f'{common_city}, '
            city_str += f'{city.zipcode}'
            city_coordinate_data[state].append({city_str:[latitude, longitude]})


            # Save to Bounds List
            coordinates_dict['West_Bounds'].append(bounds_west)
            coordinates_dict['East_Bounds'].append(bounds_east)
            coordinates_dict['North_Bounds'].append(bounds_north)
            coordinates_dict['South_Bounds'].append(bounds_south)
            coordinates_dict['Latitude'].append(latitude)
            coordinates_dict['Longitude'].append(longitude)

        # ---------------------------------------------------------
        ## Find Averages for Zipcode Prefix Locations
        average_percent_married = [city['Married_Percentage'] for city in city_metric_data[zip_number] if city['Married_Percentage'] is not None]
        average_percent_married = round(mean(average_percent_married), 2) if average_percent_married else None

        average_families_with_children = [city['Families_with_Children'] for city in city_metric_data[zip_number] if city['Families_with_Children'] is not None]
        average_families_with_children = round(mean(average_families_with_children), 2) if average_families_with_children else None

        average_home_occupancy = [city['Home_Occupancy'] for city in city_metric_data[zip_number] if city['Home_Occupancy'] is not None]
        average_home_occupancy = round(mean(average_home_occupancy), 2) if average_home_occupancy else None

        average_employment_percentage = [city['Employment_Percentage'] for city in city_metric_data[zip_number] if city['Employment_Percentage'] is not None]
        average_employment_percentage = round(mean(average_employment_percentage), 2) if average_employment_percentage else None

        average_motor_vehicle_use = [city['Motor_Vehicle_Work_Percentage'] for city in city_metric_data[zip_number] if city['Motor_Vehicle_Work_Percentage'] is not None]
        average_motor_vehicle_use = round(mean(average_motor_vehicle_use), 2) if average_motor_vehicle_use else None

        average_public_transportation_use = [city['Public_Transportation_Work_Percentage'] for city in city_metric_data[zip_number] if city['Public_Transportation_Work_Percentage'] is not None]
        average_public_transportation_use = round(mean(average_public_transportation_use), 2) if average_public_transportation_use else None

        average_walking_biking_use = [city['Walking_Biking_Work_Percentage'] for city in city_metric_data[zip_number] if city['Walking_Biking_Work_Percentage'] is not None]
        average_walking_biking_use = round(mean(average_walking_biking_use), 2) if average_walking_biking_use else None

        average_travel_time_to_work = [city['Travel_Time_To_Work'] for city in city_metric_data[zip_number] if city['Travel_Time_To_Work'] is not None]
        average_travel_time_to_work = round(mean(average_travel_time_to_work), 2) if average_travel_time_to_work else None

        average_education_score = [city['Education_Score'] for city in city_metric_data[zip_number] if city['Education_Score'] is not None]
        average_education_score = round(mean(average_education_score), 2) if average_education_score else None

        average_school_enrollment = [city['School_Enrollment_Percentage'] for city in city_metric_data[zip_number] if city['School_Enrollment_Percentage'] is not None]
        average_school_enrollment = round(mean(average_school_enrollment), 2) if average_school_enrollment else None

        ## Average Home Values for Zipcode Prefix Locations
        median_home_value = [city['Median_Home_Value'] for city in city_metric_data[zip_number] if city['Median_Home_Value'] is not None]
        total_persons_list = home_value_dict['Total_Persons']
        distribution_lists = home_value_dict['Distribution_Profile']

        combined_persons_total = 0
        combined_median_persons = 0
        combined_distribution_list = []
        for x, median_value in enumerate(median_home_value):
            combined_persons_total += total_persons_list[x]
            combined_median_persons += median_value * total_persons_list[x]
            combined_distribution_list += distribution_lists[x]
        median_home_value = combined_median_persons / combined_persons_total if combined_persons_total else None
        mad_home_value = mad_calc(dataset=combined_distribution_list, median_of_data=median_home_value) if median_home_value else None

        ## Average Household Income for Zipcode Prefix Locations
        median_household_income = [city['Median_Household_Income'] for city in city_metric_data[zip_number] if city['Median_Household_Income'] is not None]
        total_persons_list = home_income_dict['Total_Persons']
        distribution_lists = home_income_dict['Distribution_Profile']

        combined_persons_total = 0
        combined_median_persons = 0
        combined_distribution_list = []
        for x, median_value in enumerate(median_household_income):
            combined_persons_total += total_persons_list[x]
            combined_median_persons += median_value * total_persons_list[x]
            combined_distribution_list += distribution_lists[x]
        median_household_income = combined_median_persons / combined_persons_total if combined_persons_total else None
        mad_household_income = mad_calc(dataset=combined_distribution_list, median_of_data=median_household_income) if median_household_income else None

        # Population & Land Area for Zipcode Prefix Locations
        total_population = sum(
            [city['Population'] for city in city_metric_data[zip_number] if city['Population'] is not None])
        total_land_area = sum(
            [city['Land_Area_sqmi'] for city in city_metric_data[zip_number] if city['Land_Area_sqmi'] is not None])

        # Area Classification for Zipcode Prefix Locations
        if total_land_area:
            population_density = total_population / total_land_area
            average_area_classification = 'Hyper Urban' if population_density >= 5000 else 'Urban' if 5000 > population_density >= 1000 else 'Suburban' if 1000 > population_density >= 500 else 'Rural' if 500 > population_density >= 100 else 'Hyper Rural'
        else:
            average_area_classification = None
       
        # Boundaries for All since All in Northern & Western Hemisphere for All Locations in the USA 50 States
        northmost_boundary = max(coordinates_dict['North_Bounds'])
        southmost_boundary = min(coordinates_dict['South_Bounds'])
        westmost_boundary = max(coordinates_dict['West_Bounds'])
        eastmost_boundary = min(coordinates_dict['East_Bounds'])
        # Approximate Center of Area (Exact Not Required)
        average_latitude = round(mean(coordinates_dict['Latitude']), 2)
        average_longitude = round(mean(coordinates_dict['Longitude']), 2)

        # Update Results Dictionary
        zipcode_prefix_metric_data.update({zip_number: 
            {
                'Married_Percentage': average_percent_married,
                'Families_with_Children': average_families_with_children,
                'Median_Home_Value': median_home_value,
                'MAD_Home_Value': mad_home_value,
                'Home_Occupancy': average_home_occupancy,
                'Median_Houshold_Income': median_household_income,
                'MAD_Household_Income': mad_household_income,
                'Employment_Percentage': average_employment_percentage,
                'Motor_Vehicle_Work_Percentage': average_motor_vehicle_use,
                'Public_Transportation_Work_Percentage': average_public_transportation_use,
                'Walking_Biking_Work_Percentage': average_walking_biking_use,
                'Travel_Time_To_Work': average_travel_time_to_work,
                'Education_Score': average_education_score,
                'School_Enrollment_Percentage': average_school_enrollment,
                'Area_Classification': average_area_classification,
                'North_Boundary': northmost_boundary,
                'South_Boundary': southmost_boundary,
                'East_Boundary': eastmost_boundary,
                'West_Boundary': westmost_boundary,
                'Latitude': average_latitude,
                'Longitude': average_longitude
            }
        })

    else:
        print(f'No USA Cities at {zip_number} Prefix')

# 
zipcode_metric_data = {}
for cities_list in [*city_metric_data.values()]:
    for city in cities_list:
        zipcode_metric_data.update({city['Zipcode']:city})

# Save Results Dictionary as JSON File
with open(f"data_processors/processed_data/Zipcode_Prefix_Metrics_Data.json", 'w') as f:
    json.dump(zipcode_prefix_metric_data, f)

with open(f"data_processors/processed_data/All_Zipcode_Metrics_Data.json", 'w') as f:
    json.dump(all_zipcode_data, f)

with open(f"data_processors/processed_data/City_Metrics_Data.json", 'w') as f:
    json.dump(zipcode_metric_data, f)

with open(f"data_ranking/ranked_data/City_Coordinates_Data.json", 'w') as f:
    json.dump(city_coordinate_data, f)