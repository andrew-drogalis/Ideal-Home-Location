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
search = SearchEngine(simple_or_comprehensive=SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive)
city_metric_data = defaultdict(list)
zipcode_prefix_metric_data = {}
city_lat_lng_data = defaultdict(list)

# Store Data for Each Zipcode Prefix
for zip_prefix in zipcode_prefix_data:
    zip_number = zip_prefix[0]
    zip_prefix_search = search.by_prefix(zip_number)
    # Check if Zipcode Prefix is Valid
    if zip_prefix_search:
        # Local Data Storage
        coordinates_dict = {
            'east_bounds': [],
            'west_bounds': [],
            'north_bounds': [],
            'south_bounds': [],
            'latitude': [],
            'longitude': []
        }
        zip_prefix_search = iter(zip_prefix_search)
        # Analyze Each City in the Zipcode Prefix
        for city in zip_prefix_search:
            ## City Information
            city_name = city.major_city
            common_city_list = city.common_city_list
            state = city.state
            latitude = float(city.lat or 0)
            longitude = float(city.lng or 0)
            if latitude == 0 or longitude == 0:
                next(zip_prefix_search, None)
                continue

            ## Max Coordinates of City Limits
            bounds_west = float(city.bounds_west or longitude)
            bounds_east = float(city.bounds_east or longitude)
            bounds_north = float(city.bounds_north or latitude)
            bounds_south = float(city.bounds_south or latitude)

            ## Common City List 
            if common_city_list and city_name not in common_city_list:
                common_city_list += [city_name]
            elif not common_city_list:
                common_city_list = [city_name]

            ## Demographic Metrics
            """
                Not Relevant to the intended use case.
            """
            # population_by_year = city.population_by_year
            # population_by_age = city.population_by_age
            # population_by_gender = city.population_by_gender
            # population_by_race = city.population_by_race
            # head_of_household_by_age = city.head_of_household_by_age

            ## Family Demographics
            # Household Married vs Unmarried
            families_vs_singles = city.families_vs_singles
            if families_vs_singles:
                families_vs_singles = families_vs_singles[0]['values']
                # Husband Wife Family Households
                families = int(families_vs_singles[0]['y'])
                # Single Guardian + Single + Single With Roommate
                singles = int(families_vs_singles[1]['y']) + int(families_vs_singles[2]['y']) + int(families_vs_singles[3]['y'])

                percent_married = round(families / (families + singles), 4) * 100
            else:
                percent_married = None
            # Households with Children Percentage
            households_with_kids = city.households_with_kids
            if households_with_kids:
                households_with_kids = households_with_kids[0]['values']
                without_kids = int(households_with_kids[0]['y'])
                with_kids = int(households_with_kids[1]['y'])
                
                percent_of_with_kids = round(with_kids / (with_kids + without_kids), 4) * 100
            else:
                percent_of_with_kids = None

            ## Housing Metrics
            """
                Home Value Data has a max value of $750,000+. 
            """
            owner_occupied_home_values = city.owner_occupied_home_values
            median_home_value = city.median_home_value
            if owner_occupied_home_values and median_home_value:
                owner_occupied_home_values = owner_occupied_home_values[0]['values']
                median_home_value = int(median_home_value)
                # $1 - $24,999 Home Value (Assumption-Average: $12,500)
                val_1_24k = int(owner_occupied_home_values[0]['y'])
                # $25,000 - $49,999 Home Value (Assumption-Average: $37,500)
                val_25k_49k = int(owner_occupied_home_values[1]['y'])
                # $50,000 - $99,999 Home Value (Assumption-Average: $75,000)
                val_50k_99k = int(owner_occupied_home_values[2]['y'])
                # $100,000 - $149,999 Home Value (Assumption-Average: $125,000)
                val_100k_149k = int(owner_occupied_home_values[3]['y'])
                # $150,000 - $199,999 Home Value (Assumption-Average: $175,000)
                val_150k_199k = int(owner_occupied_home_values[4]['y'])
                # $200,000 - $399,999 Home Value (Assumption-Average: $300,000)
                val_200k_399k = int(owner_occupied_home_values[5]['y'])
                # $400,000 - $749,999 Home Value (Assumption-Average: $575,000)
                val_400k_749k = int(owner_occupied_home_values[6]['y'])
                # $750,000+ Home Value (Assumption-Average: $800,000)
                val_750k_plus = int(owner_occupied_home_values[7]['y'])
                # Accounting for Extremely Weathly Neighborhoods
                val_750k_plus_average = max(800_000, median_home_value + 50_000)
                #
                num_persons_list = [val_1_24k, val_25k_49k, val_50k_99k, val_100k_149k, val_150k_199k, val_200k_399k, val_400k_749k, val_750k_plus]
                home_value_list = [12_500, 37_500, 75_000, 125_000, 175_000, 300_000, 575_000, val_750k_plus_average]
                #
                home_value_distribution_list = []
                for x, home_value in enumerate(home_value_list):
                    home_value_distribution_list += [home_value] * num_persons_list[x]
                # Median Absolute Deviation
                mad_home_value = mad_calc(dataset=home_value_distribution_list, median_of_data=median_home_value)
            else:
                median_home_value = None
                mad_home_value = None
            #
            housing_unit = city.housing_units
            occupied_housing_units = city.occupied_housing_units
            if housing_unit and occupied_housing_units:
                housing_unit = int(housing_unit)
                occupied_housing_units = int(occupied_housing_units)
                percent_housing_occupancy = round(occupied_housing_units / housing_unit, 4) * 100
            else:
                percent_housing_occupancy = None
            
            ## Rental Metrics
            """
                Rental Unit Data has a max value of $1,000+ / Month. With no median rental unit data provided, at this time it's not possible to accurately break down the true rental costs.
            """
            # rental_properties_by_number_of_rooms = city.rental_properties_by_number_of_rooms
            # monthly_rent_including_utilities_studio_apt = city.monthly_rent_including_utilities_studio_apt
            # monthly_rent_including_utilities_1_b = city.monthly_rent_including_utilities_1_b
            # monthly_rent_including_utilities_2_b = city.monthly_rent_including_utilities_2_b
            # monthly_rent_including_utilities_3plus_b = city.monthly_rent_including_utilities_3plus_b

            ## Household Income Metrics
            """
                Household Income Data has a max value of $200,000+. 
            """
            household_income = city.household_income
            median_household_income = city.median_household_income
            if household_income and median_household_income:
                household_income = household_income[0]['values']
                median_household_income = int(median_household_income)
                # $1 - $24,999 Income (Assumption-Average: $12,500)
                income_less_25k = int(household_income[0]['y'])
                # $25,000 - $44,999 Income (Assumption-Average: $35,000)
                income_25k_45k = int(household_income[1]['y'])
                # $45,000 - $59,999 Income (Assumption-Average: $52,500)
                income_45k_60k = int(household_income[2]['y'])
                # $60,000 - $99,999 Income (Assumption-Average: $80,000)
                income_60k_100k = int(household_income[3]['y'])
                # $100,000 - $149,999 Income (Assumption-Average: $125,000)
                income_100k_149k = int(household_income[4]['y'])
                # $150,000 - $199,999 Income (Assumption-Average: $175,000)
                income_150k_199k = int(household_income[5]['y'])
                # $200,000+ Income (Assumption-Average: $250,000)
                income_200k_plus = int(household_income[6]['y'])
                # Accounting for Extremely Weathly Neighborhoods
                income_200k_plus_average = max(250_000, median_household_income + 50_000)
  
                income_persons_list = [income_less_25k, income_25k_45k, income_45k_60k, income_60k_100k, income_100k_149k, income_150k_199k, income_200k_plus]
                income_list = [12_500, 35_000, 52_500, 80_000, 125_000, 175_000, income_200k_plus_average]
               
                income_distribution_list = []
                for x, income in enumerate(income_list):
                    income_distribution_list += [income] * income_persons_list[x]
                # Median Absolute Deviation
                mad_household_income = mad_calc(dataset=income_distribution_list, median_of_data=median_household_income)
            else:
                median_household_income = None
                mad_household_income = None

            ## Household Sources of Income
            """
                Could be of used for a more detailed break down of income stream, but overkill for the design intent.
            """
            # sources_of_household_income____percent_of_households_receiving_income = city.sources_of_household_income____percent_of_households_receiving_income
            # sources_of_household_income____average_income_per_household_by_income_source = city.sources_of_household_income____average_income_per_household_by_income_source
            # household_investment_income____percent_of_households_receiving_investment_income = city.household_investment_income____percent_of_households_receiving_investment_income
            # household_investment_income____average_income_per_household_by_income_source = city.household_investment_income____average_income_per_household_by_income_source
            # household_retirement_income____percent_of_households_receiving_retirement_income = city.household_retirement_income____percent_of_households_receiving_retirement_incom
            # household_retirement_income____average_income_per_household_by_income_source = city.household_retirement_income____average_income_per_household_by_income_source

            ## Job Opportunity Metrics
            employment_status = city.employment_status
            if employment_status:
                employment_status = employment_status[0]['values']
                # Employed Full-time + Employed Part-time
                employed = int(employment_status[0]['y']) + int(employment_status[1]['y'])
                #
                unemployed = int(employment_status[2]['y'])
                #
                percent_employed = round(employed / (employed + unemployed), 4) * 100
            else:
                percent_employed = None
            #
            means_of_transportation_to_work_for_workers_16_and_over = city.means_of_transportation_to_work_for_workers_16_and_over
            if means_of_transportation_to_work_for_workers_16_and_over and employment_status and employed > 0:
                means_of_transportation_to_work_for_workers_16_and_over = means_of_transportation_to_work_for_workers_16_and_over[0]['values']
                # Car, Truck, Van, Motorcycle, or Taxi - Long Distance Motor Vehicle Required
                percent_using_car_truck_van = int(means_of_transportation_to_work_for_workers_16_and_over[0]['y']) + int(means_of_transportation_to_work_for_workers_16_and_over[2]['y']) + int(means_of_transportation_to_work_for_workers_16_and_over[3]['y'])
                percent_using_car_truck_van = round(percent_using_car_truck_van / employed, 4) * 100
                #
                percent_using_public_trasportation = round(int(means_of_transportation_to_work_for_workers_16_and_over[1]['y']) / employed, 4) * 100
                #
                percent_walking_biking_other = round(int(means_of_transportation_to_work_for_workers_16_and_over[4]['y']) / employed, 4) * 100
            else:
                percent_using_car_truck_van = None
                percent_using_public_trasportation = None
                percent_walking_biking_other = None
            #
            travel_time_to_work_in_minutes = city.travel_time_to_work_in_minutes
            if travel_time_to_work_in_minutes:
                travel_time_to_work_in_minutes = travel_time_to_work_in_minutes[0]['values']
                # Less than 10 minutes (Assumption-Average: 5 mins)
                num_less_10 = int(travel_time_to_work_in_minutes[0]['y'])
                # 10 - 19 minutes (Assumption-Average: 14.5 mins)
                num_10_19 = int(travel_time_to_work_in_minutes[1]['y'])
                # 20 - 29 minutes (Assumption-Average:: 24.5 mins)
                num_20_29 = int(travel_time_to_work_in_minutes[2]['y'])
                # 30 - 39 minutes (Assumption-Average: 34.5 mins)
                num_30_39 = int(travel_time_to_work_in_minutes[3]['y'])
                # 40 - 44 minutes (Assumption-Average: 42 mins)
                num_40_44 = int(travel_time_to_work_in_minutes[4]['y'])
                # 45 - 59 minutes (Assumption-Average: 52 mins)
                num_45_59 = int(travel_time_to_work_in_minutes[5]['y'])
                # 60 - 89 minutes (Assumption-Average: 74.5 mins)
                num_60_89 = int(travel_time_to_work_in_minutes[6]['y'])
                # More than 90 minutes (Assumption-Average: 100 mins)
                num_plus_90 = int(travel_time_to_work_in_minutes[7]['y'])

                total_commuters = num_less_10 + num_10_19 + num_20_29 + num_30_39 + num_40_44 + num_45_59 + num_60_89 + num_plus_90
                average_travel_time_to_work = ((num_less_10 * 5) + (num_10_19 * 14.5) + (num_20_29 * 24.5)+ (num_30_39 * 34.5) + (num_40_44 * 42) + (num_45_59 * 52) + (num_plus_90 * 100)) / total_commuters
                average_travel_time_to_work = round(average_travel_time_to_work, 2)
            else:
                average_travel_time_to_work = None

            ## Educational Metrics
            # 
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
                less_than_high_school = int(educational_attainment_for_population_25_and_over[0]['y'])
                high_school = int(educational_attainment_for_population_25_and_over[1]['y'])
                associate = int(educational_attainment_for_population_25_and_over[2]['y'])
                bachelor = int(educational_attainment_for_population_25_and_over[3]['y'])
                masters = int(educational_attainment_for_population_25_and_over[4]['y'])
                professional_school = int(educational_attainment_for_population_25_and_over[5]['y'])
                doctorate = int(educational_attainment_for_population_25_and_over[6]['y'])
                #
                total_peoples = less_than_high_school + high_school + associate + bachelor + masters + professional_school + doctorate
                overall_education_score = ((less_than_high_school * 0) + (high_school * 1) + (associate * 2) + (bachelor * 3) + (professional_school * 3) + (masters * 4) + (doctorate * 5)) / total_peoples
                overall_education_score = round(overall_education_score, 2)
            else:
                overall_education_score = None
            #
            school_enrollment_age_3_to_17 = city.school_enrollment_age_3_to_17
            if school_enrollment_age_3_to_17:
                school_enrollment_age_3_to_17 = school_enrollment_age_3_to_17[0]['values']
                # Public School Enrollment + Private School Enrollment
                enrolled_in_school = int(school_enrollment_age_3_to_17[0]['y']) + int(school_enrollment_age_3_to_17[1]['y'])
                # Not enrolled in School
                not_enrolled_in_school = int(school_enrollment_age_3_to_17[2]['y'])

                percent_enrolled_in_school = round(enrolled_in_school / (enrolled_in_school + not_enrolled_in_school), 4) * 100
            else:
                percent_enrolled_in_school = None

            ## Population Density
            # Urban or Rural Classification Based on US Census Bureau
            """
                Reference: https://www2.census.gov/geo/pdfs/reference/GARM/Ch12GARM.pdf
                Methodology: 5 Classifications of Areas
                    Hyper Urban: 5,000+ Persons / Square Mile
                    Urban: 4,999 - 1,000 Persons / Square Mile
                    Suburban: 999 - 500 Persons / Square Mile
                    Rural: 499 - 100 Persons / Square Mile
                    Hyper Rural: 99 - 0 Persons / Square Mile
            """
            population_density = city.population_density
            if population_density:
                population_density = int(population_density) # Persons / Square Mile
                area_classification = 'Hyper Urban' if population_density >= 5000 else 'Urban' if 5000 > population_density >= 1000 else 'Suburban' if 1000 > population_density >= 500 else 'Rural' if 500 > population_density >= 100 else 'Hyper Rural'
            else:
                area_classification = None
            #
            population = city.population
            land_area = city.land_area_in_sqmi
            if population and land_area:
                population = int(population)
                land_area = float(land_area)
            else: 
                population = None
                land_area = None

            # Store
            city_metric_data[zip_number].append(
                {
                    'city_name': f'{city_name}, {state}',
                    'percent_married': percent_married,
                    'percent_with_kids': percent_of_with_kids,
                    'median_home_value': median_home_value,
                    'mad_home_value': mad_home_value,
                    'percent_housing_occupancy': percent_housing_occupancy,
                    'median_houshold_income': median_household_income,
                    'mad_household_income': mad_household_income,
                    'percent_employment': percent_employed,
                    'percent_using_motor_vehicle': percent_using_car_truck_van,
                    'percent_using_public_transportation': percent_using_public_trasportation,
                    'percent_walking_biking': percent_walking_biking_other,
                    'travel_time_to_work': average_travel_time_to_work,
                    'education_score': overall_education_score,
                    'school_enrollment': percent_enrolled_in_school,
                    'area_classification': area_classification,
                    'population': population,
                    'land_area': land_area
                })

            # Each City, Common Cities, & Zipcode combined for Fuzzy Regex Search
            city_str = ''
            for common_city in common_city_list:
                city_str += f'{common_city}, '
            city_str += f'{city.zipcode}'
            city_lat_lng_data[state].append({city_str:[latitude, longitude]})

            # Save to Bounds List
            coordinates_dict['west_bounds'].append(bounds_west)
            coordinates_dict['east_bounds'].append(bounds_east)
            coordinates_dict['north_bounds'].append(bounds_north)
            coordinates_dict['south_bounds'].append(bounds_south)
            coordinates_dict['latitude'].append(latitude)
            coordinates_dict['longitude'].append(longitude)

        ## Find Averages for Zipcode Prefix Locations


        # Northern & Western Hemisphere for All Locations in the USA 50 States
        northmost_boundary = max(coordinates_dict['north_bounds'])
        southmost_boundary = min(coordinates_dict['south_bounds'])
        westmost_boundary = max(coordinates_dict['west_bounds'])
        eastmost_boundary = min(coordinates_dict['east_bounds'])
        # Exact Center of Area not Required - Only used for Relative Proximity
        average_latitude = mean(coordinates_dict['latitude'])
        average_longitude = mean(coordinates_dict['longitude'])

        # Update Results Dictionary
        zipcode_prefix_metric_data.update({zip_number: 
            {
                'Average_Temperature': 1
            }
        })

    else:
        print(f'No USA Cities at {zip_number} Prefix')


# Save Results Dictionary as JSON File
with open(f"data_processors/processed_data/Zipcode_Prefix_Metrics_Data.json", 'w') as f:
    json.dump(zipcode_prefix_metric_data, f)

with open(f"data_processors/processed_data/City_Metrics_Data.json", 'w') as f:
    json.dump(city_metric_data, f)

with open(f"data_processors/processed_data/City_Position_Data.json", 'w') as f:
    json.dump(city_lat_lng_data, f)