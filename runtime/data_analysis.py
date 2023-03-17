import json, csv
from collections import defaultdict
from runtime.utilities.calculation_utilities import location_radius_search, check_coordinates_distance_to_center
from runtime.utilities.state_abbreviations import states_abbreviation_list
from thefuzz import process

class IdealHomeDataAnalysis():

    """ For Full Methodology: https://github.com/andrew-drogalis/Ideal-Home-Location-Matcher/wiki """

    def __init__(self):
        
        # Import Natural Disaster Ranked Data
        with open('./data/data_ranking/ranked_data/State_Natural_Disaster_Ranked_Data.json', newline='') as f: 
            self.state_natural_disaster_data = json.load(f)

        # Import Weather Ranked Data
        with open('./data/data_ranking/ranked_data/Weather_Ranked_Data.json', newline='') as f: 
            self.zipcode_prefix_weather_data = json.load(f)

        # Import Zipcode Ranked Data
        with open('./data/data_ranking/ranked_data/Zipcode_Ranked_Data.json', newline='') as f: 
            self.zipcode_data = json.load(f)

        # Import Zipcode Coordinate Data
        with open('./data/data_ranking/ranked_data/Zipcode_Coordinates_Data.json', newline='') as f: 
            self.zipcode_coordinate_data = json.load(f)

        # Import Zipcode Prefix Boundary Data
        with open('./data/data_ranking/ranked_data/Zipcode_Prefix_Boundary_Data.json', newline='') as f: 
            self.zipcode_prefix_boundary_data = json.load(f)

        # Import Zipcode Prefix Region Name
        with open('./data/data_sources/USA_Zipcode_3_Digits.csv', newline='') as f: 
            self.zipcode_prefix_region_names = list(csv.reader(f))

        # Initalize Errors List
        self.errors = []
        # Store Coordinates of Family & Work Locations
        self.saved_coordinates_list = [[], [], []]
        # Convert to Hash Map
        self.zipcode_prefix_region_names = {row[0]:row[1] for row in self.zipcode_prefix_region_names}

    # -------------- Navigation Functions -------------------
    def family_location_frame_1(self, **kwargs):
        self.run_location_radius_search(radius_index=kwargs['radius_index'])

    def family_details_frame_1b(self, **kwargs):
        # Save User Selections to Class Variables
        self.married_state = kwargs['married']
        self.married_importance = kwargs['married_importance']
        self.children_state = kwargs['children']
        self.children_importance = kwargs['children_importance']
        self.school_enrollment_importance = kwargs['school_enrollment_importance']

    def work_frame_2(self, **kwargs):
        # Save User Selections to Class Variables
        self.employment_status = kwargs['employed_status']
        self.regional_employment_importance = kwargs['regional_employment_importance']
        self.transportation_method = kwargs['work_transportation']
        self.commute_time = kwargs['commute_time']
        
        #
        self.run_location_radius_search(radius_index=kwargs['radius_index'])

    def income_frame_3(self, **kwargs):
        # Save User Selections to Class Variables
        self.user_income = kwargs['income']
        self.user_home_price = kwargs['affordable_home_price']

    def area_classification_frame_4(self, **kwargs):
        # Save User Selections to Class Variables
        self.education_level = kwargs['education_level']
        self.education_level_importance = kwargs['education_level_importance']
        self.living_enviornment = kwargs['living_enviornment']
        self.living_enviornment2 = kwargs['living_enviornment2']

    def weather_frame_5(self, **kwargs):
        # Save User Selections to Local Variables
        seasons = kwargs['seasons']
        summer_temperature = float(kwargs['summer_temperature'])
        winter_temperature = float(kwargs['winter_temperature'] or 0)
        transition_temperature = (summer_temperature + winter_temperature) / 2
        precipitation_level = kwargs['precipitation_level']
        sunshine_level = kwargs['sunshine_level']

        # Convert Values From User Friendly to Search Friendly
        precipitation_level = 'Well Below Average' if precipitation_level == 'Very Low' else 'Below Average' if precipitation_level == 'Low' else 'Above Average' if precipitation_level == 'High' else 'Well Above Average' if precipitation_level == 'Very High' else precipitation_level
        sunshine_level = 'Well Below Average' if sunshine_level == 'Very Low' else 'Below Average' if sunshine_level == 'Low' else 'Above Average' if sunshine_level == 'High' else 'Well Above Average' if sunshine_level == 'Very High' else sunshine_level
        
        # See Link Above for Full Methodology
        # Seasons Ranked Double Importance
        self.zipcode_prefix_weather_score = {}

        for zipcode_prefix, weather_data in self.zipcode_prefix_weather_data.items():
            zipcode_seasons = weather_data['Seasons']
            zipcode_avg_temp = weather_data['Average_Temperature']
            zipcode_min_temp = weather_data['Min_Temperature']
            zipcode_max_temp = weather_data['Max_Temperature']
            zipcode_precipitation = weather_data['Yearly_Precipitation']
            zipcode_sunshine = weather_data['Yearly_Sunshine']

            if seasons == '4 Seasons':
                season_score = 4 if zipcode_seasons == 4 else 2 if zipcode_seasons == 2 else 0
                summer_difference = abs(zipcode_max_temp - summer_temperature)
                transition_difference = abs(zipcode_avg_temp - transition_temperature)
                winter_difference = abs(zipcode_min_temp - winter_temperature)
                summer_score = 3 if summer_difference <= 5 else 2 if 5 < summer_difference <= 10 else 1 if 10 < summer_difference <= 15 else 0
                transition_score = 3 if transition_difference <= 5 else 2 if 5 < transition_difference <= 10 else 1 if 10 < transition_difference <= 15 else 0
                winter_score = 3 if winter_difference <= 5 else 2 if 5 < winter_difference <= 10 else 1 if 10 < winter_difference <= 15 else 0

                season_score = season_score + summer_score + transition_score + winter_score
            elif seasons == '2 Seasons':
                season_score = 4 if zipcode_seasons == 2 else 2
                summer_difference = abs(zipcode_max_temp - summer_temperature)
                winter_difference = abs(zipcode_min_temp - winter_temperature)
                summer_score = 3 if summer_difference <= 5 else 2 if 5 < summer_difference <= 10 else 1 if 10 < summer_difference <= 15 else 0
                winter_score = 3 if winter_difference <= 5 else 2 if 5 < winter_difference <= 10 else 1 if 10 < winter_difference <= 15 else 0

                season_score = season_score + summer_score + winter_score
            else:

                season_score = 4 if zipcode_seasons == 1 else 2 if zipcode_seasons == 2 else 0
                outside_difference = abs(zipcode_avg_temp - summer_temperature)
                temperature_score = 3 if outside_difference <= 5 else 2 if 5 < outside_difference <= 10 else 1 if 10 < outside_difference <= 15 else 0

                season_score = season_score + temperature_score

            # Precipitation
            if precipitation_level[:4] == 'Well':
                precipitation_score = 4 if precipitation_level == zipcode_precipitation else 2 if precipitation_level[5:11] == zipcode_precipitation[5:11] else 0
            elif precipitation_level == 'Below Average':
                precipitation_score = 4 if zipcode_precipitation == 'Below Average' else 2 if zipcode_precipitation == 'Well Below Average' or zipcode_precipitation == 'Average' else 0
            elif precipitation_level == 'Above Average':
                precipitation_score = 4 if zipcode_precipitation == 'Above Average' else 2 if zipcode_precipitation == 'Well Above Average' or zipcode_precipitation == 'Average' else 0
            else:
                precipitation_score = 4 if zipcode_precipitation == 'Average' else 2 if zipcode_precipitation == 'Below Average' or zipcode_precipitation == 'Above Average' else 0

            # Sunshine
            if sunshine_level[:4] == 'Well':
                sunshine_score = 4 if sunshine_level == zipcode_sunshine else 2 if sunshine_level[5:11] == zipcode_sunshine[5:11] else 0
            elif sunshine_level == 'Below Average':
                sunshine_score = 4 if zipcode_sunshine == 'Below Average' else 2 if zipcode_sunshine == 'Well Below Average' or zipcode_sunshine == 'Average' else 0
            elif sunshine_level == 'Above Average':
                sunshine_score = 4 if zipcode_sunshine == 'Above Average' else 2 if zipcode_sunshine == 'Well Above Average' or zipcode_sunshine == 'Average' else 0
            else:
                sunshine_score = 4 if zipcode_sunshine == 'Average' else 2 if zipcode_sunshine == 'Below Average' or zipcode_sunshine == 'Above Average' else 0

            total_score = season_score + precipitation_score + sunshine_score

            self.zipcode_prefix_weather_score.update({zipcode_prefix:total_score})

        max_season_score = 13 if seasons == '4 Seasons' else 10 if seasons == '2 Seasons' else 7
        max_precipitation_score = 4
        max_sunshine_score = 4
        self.max_possible_weather_score = max_season_score + max_precipitation_score + max_sunshine_score


    def natural_disaster_risk_frame_6(self, **kwargs):
        # Save User Selections to Local Variables
        natural_disaster_risk = int(kwargs['natural_disaster_risk'])
        disaster_to_avoid = kwargs['disaster_to_avoid'].replace('Thunderstorm','Lightning/Thunderstorms').replace('Hurricane', 'Tropical cyclone')
        disaster_to_avoid2 = kwargs['disaster_to_avoid2'].replace('Thunderstorm','Lightning/Thunderstorms').replace('Hurricane', 'Tropical cyclone')
        disaster_to_avoid3 = kwargs['disaster_to_avoid3'].replace('Thunderstorm','Lightning/Thunderstorms').replace('Hurricane', 'Tropical cyclone')
        
        self.state_natural_disaster_score = {}

        for state, disaster_data in self.state_natural_disaster_data.items():
            disaster_data = disaster_data[0]
            total_severity = disaster_data['All_Severity_Rank']
            total_frequency = disaster_data['All_Frequency_Rank']

            total_severity_number = 0 if total_severity == 'High' else 0.33 if total_severity == 'Moderate' else 0.66 if total_severity == 'Low' else 1
            total_frequency_number = 0 if total_frequency == 'Well Above Average' else 0.25 if total_frequency == 'Above Average' else 0.5 if total_frequency == 'Average' else 0.75 if total_frequency == 'Below Average' else 1

            total_disaster_score = (total_severity_number + total_frequency_number) * natural_disaster_risk

            try:
                disaster_1_severity = disaster_data[f'{disaster_to_avoid}_Severity_Rank']
                disaster_1_frequency = disaster_data[f'{disaster_to_avoid}_Frequency_Rank']
                disaster_1_severity_number = 0 if disaster_1_severity == 'High' else 0.33 if disaster_1_severity == 'Moderate' else 0.66 if disaster_1_severity == 'Low' else 1
                disaster_1_frequency_number = 0 if disaster_1_frequency == 'Well Above Average' else 0.25 if disaster_1_frequency == 'Above Average' else 0.5 if disaster_1_frequency == 'Average' else 0.75 if disaster_1_frequency == 'Below Average' else 1
                disaster_1_score = (disaster_1_severity_number + disaster_1_frequency_number) * natural_disaster_risk
            except:
                disaster_1_score = 2 * natural_disaster_risk

            try:
                disaster_2_severity = disaster_data[f'{disaster_to_avoid2}_Severity_Rank']
                disaster_2_frequency = disaster_data[f'{disaster_to_avoid2}_Frequency_Rank']
                disaster_2_severity_number = 0 if disaster_2_severity == 'High' else 0.33 if disaster_2_severity == 'Moderate' else 0.66
                disaster_2_frequency_number = 0 if disaster_2_frequency == 'Well Above Average' else 0.25 if disaster_2_frequency == 'Above Average' else 0.5 if disaster_2_frequency == 'Average' else 0.75
                disaster_2_score = (disaster_2_severity_number + disaster_2_frequency_number) * natural_disaster_risk
            except:
                disaster_2_score = 1.41 * natural_disaster_risk

            try:
                disaster_3_severity = disaster_data[f'{disaster_to_avoid3}_Severity_Rank']
                disaster_3_frequency = disaster_data[f'{disaster_to_avoid3}_Frequency_Rank']
                disaster_3_severity_number = 0 if disaster_3_severity == 'High' else 0.33
                disaster_3_frequency_number = 0 if disaster_3_frequency == 'Well Above Average' else 0.25 if disaster_3_frequency == 'Above Average' else 0.5
                disaster_3_score = (disaster_3_severity_number + disaster_3_frequency_number) * natural_disaster_risk
            except:
                disaster_3_score = 0.83 * natural_disaster_risk

            total_state_score = total_disaster_score + disaster_1_score + disaster_2_score + disaster_3_score

            self.state_natural_disaster_score.update({state: total_state_score})

        max_total_disaster_score = 2 * natural_disaster_risk
        max_disaster_1_score = 2 * natural_disaster_risk
        max_disaster_2_score = 1.41 * natural_disaster_risk
        max_disaster_3_score = 0.83 * natural_disaster_risk
        self.max_possible_state_disaster_score = max_total_disaster_score + max_disaster_1_score + max_disaster_2_score + max_disaster_3_score

    def results_frame_7(self):

        # Are you Married
        married_importance = int(self.married_importance)
        if self.married_state == 'No':
            married_scoring_order = [1 * married_importance, 0.75 * married_importance, 0.5 * married_importance, 0.25 * married_importance, 0]
        else:
            married_scoring_order = [0, 0.25 * married_importance, 0.5 * married_importance, 0.75 * married_importance, 1 * married_importance]

        # Do you have children
        children_importance = int(self.children_importance )
        if self.children_state == 'No':
            children_scoring_order = [1 * children_importance, 0.75 * children_importance, 0.5 * children_importance, 0.25 * children_importance, 0]
        else:
            children_scoring_order = [0, 0.25 * children_importance, 0.5 * children_importance, 0.75 * children_importance, 1 * children_importance]

        school_enrollment_scoring_order = [0, 0.25, 0.5, 0.75, 1] if self.school_enrollment_importance == '1' else [0, 0.5, 1, 1.5, 2] if self.school_enrollment_importance == '2' else [0, 0.75, 1.5, 2.25, 3] if self.school_enrollment_importance == '3' else [0, 1, 2, 3, 4] if self.school_enrollment_importance == '4' else [0, 1.25, 2.5, 3.75, 5]

        user_commute_time = int(self.commute_time[6:8])
        # What's your education level:
        education_importance = int(self.education_level_importance)
        user_education_number = 0 if self.education_level == 'Less than High School' else 1 if self.education_level == 'High School' else 2 if self.education_level == "Associate's" else 3 if self.education_level == "Bachelor's" else 4 if self.education_level == "Master's" else 5

        living_enviornment_scoring_order1 = [4,2,1,0,0] if self.living_enviornment == 'Hyper Rural' else [2,4,2,1,0] if self.living_enviornment == 'Rural' else [1,2,4,2,1] if self.living_enviornment == 'Suburban' else [0,1,2,4,2] if self.living_enviornment == 'Urban' else [0,0,1,2,4]
        living_enviornment_scoring_order2 = [2,1,0,0,0] if self.living_enviornment2 == 'Hyper Rural' else [1,2,1,0,0] if self.living_enviornment2 == 'Rural' else [0,1,2,1,0] if self.living_enviornment2 == 'Suburban' else [0,0,1,2,1] if self.living_enviornment2 == 'Urban' else [0,0,0,1,2]
                
        unlikely_to_afford_warning = []
        final_city_score = []
        final_zipcode_prefix_score = defaultdict(dict)
        city_coordinates_dictionary = {}
        for city in self.city_radius_results:
            city_name = [*city.keys()][0]
            zipcode = city_name[-5:]
            zipcode_prefix = zipcode[:3]
            zipcode_data = self.zipcode_data[zipcode]
            state = zipcode_data["City"][-2:]
            city_coordinates_dictionary.update(city)

            median_home_value = zipcode_data['Median_Home_Value']
            mad_home_value = zipcode_data['MAD_Home_Value']

            if median_home_value and mad_home_value:
                # Most Importance
                if self.user_home_price < median_home_value - mad_home_value:
                    unlikely_to_afford_warning.append(city_name)

                # Preferance Toward the Median
                whole_mad_home_value_positive = median_home_value + mad_home_value
                half_mad_home_value_positive = median_home_value + mad_home_value * 0.5
                half_mad_home_value_negative = median_home_value - mad_home_value * 0.5
                whole_mad_home_value_negative = median_home_value - mad_home_value

                home_afforability_score = 10 if half_mad_home_value_negative <= self.user_home_price <= half_mad_home_value_positive else 5 if whole_mad_home_value_negative <= self.user_home_price <= whole_mad_home_value_positive else 0
            else:
                home_afforability_score = 0

            median_household_income = zipcode_data['Median_Household_Income']
            mad_household_income = zipcode_data['MAD_Household_Income']

            if median_household_income and mad_household_income:
                whole_mad_income_positive = median_household_income + mad_household_income
                half_mad_income_positive = median_household_income + mad_household_income * 0.5
                half_mad_income_negative = median_household_income - mad_household_income * 0.5
                whole_mad_income_negative = median_household_income - mad_household_income

                household_income_score = 10 if half_mad_income_negative <= self.user_home_price <= half_mad_income_positive else 5 if whole_mad_income_negative <= self.user_home_price <= whole_mad_income_positive else 0
            else:
                household_income_score = 0

            married_percentage = zipcode_data["Married_Percentage"]
            married_score = married_scoring_order[0] if married_percentage == 'Well Below Average' else married_scoring_order[1] if married_percentage == 'Below Average' else married_scoring_order[2] if married_percentage == 'Average' else married_scoring_order[3] if married_percentage == 'Above Average' else married_scoring_order[4]
            
            families_with_children = zipcode_data["Families_with_Children"]
            families_with_children_score = children_scoring_order[0] if families_with_children == 'Well Below Average' else children_scoring_order[1] if families_with_children == 'Below Average' else children_scoring_order[2] if families_with_children == 'Average' else children_scoring_order[3] if families_with_children == 'Above Average' else children_scoring_order[4]
                
            school_enrollment_percentage = zipcode_data["School_Enrollment_Percentage"]
            school_enrollment_score = school_enrollment_scoring_order[0] if school_enrollment_percentage == 'Well Below Average' else school_enrollment_scoring_order[1] if school_enrollment_percentage == 'Below Average' else school_enrollment_scoring_order[2] if school_enrollment_percentage == 'Average' else school_enrollment_scoring_order[3] if school_enrollment_percentage == 'Above Average' else school_enrollment_scoring_order[4]

            if self.employment_status == 'No':
                regional_employment_importance = int(self.regional_employment_importance)
                employment_percentage = zipcode_data['Employment_Percentage']
                employment_score = 1 * regional_employment_importance if employment_percentage == 'Well Above Average' else 0.75 * regional_employment_importance if employment_percentage == 'Above Average' else 0.5 * regional_employment_importance if employment_percentage == 'Average' else 0.25 * regional_employment_importance if employment_percentage == 'Below Average' else 0

                if self.transportation_method == "Personal Vehicle":
                    transportation_method = zipcode_data['Motor_Vehicle_Work_Percentage']
                    transportation_score = 5 if transportation_method == 'Well Above Average' else 4 if transportation_method == 'Above Average' else 3 if transportation_method == 'Average' else 2 if transportation_method == 'Below Average' else 1 
                    max_transportation_score = 5
                elif self.transportation_method in ["Public Transportation", "Walking or Biking"]:
                    name = self.transportation_method.replace('or ', '').replace(' ', '_')
                    transportation_method = zipcode_data[f'{name}_Work_Percentage']
                    transportation_score = 5 if transportation_method == 'Very Good' else 4 if transportation_method == 'Good' else 3 if transportation_method == 'Exceptable' else 0
                    max_transportation_score = 5
                else:
                    transportation_score = 0
                    max_transportation_score = 0

                city_commute_time = zipcode_data["Travel_Time_To_Work"]
                if city_commute_time and self.transportation_method != 'Work From Home':
                    commute_time_difference = user_commute_time - city_commute_time
                    commute_score = 4 if commute_time_difference <= 0 else 3 if commute_time_difference <= 10 else 2 if commute_time_difference <= 15 else 1 if commute_time_difference <= 20 else 0
                    max_commute_score = 4
                else:
                    commute_score = 0
                    max_commute_score = 0 if self.transportation_method != 'Work From Home' else 5

                work_score = employment_score + transportation_score + commute_score
                max_employment_score = regional_employment_importance
                max_work_score = max_employment_score + max_transportation_score + max_commute_score
            else:
                work_score = 0
                max_work_score = 0
            
            city_education_level = zipcode_data["Education_Score"]
            if city_education_level:
                education_level_difference = abs(city_education_level - user_education_number)
                education_score = 1 * education_importance if education_level_difference < 0.5 else 0.75 * education_importance if education_level_difference < 1 else 0.5 * education_importance if education_level_difference < 1.5 else 0.25 * education_importance if education_level_difference < 2 else 0
            else:
                education_score = 0

            area_classification = zipcode_data["Area_Classification"]
            area_classification_list_key = 0 if area_classification == 'Hyper Rural' else 1 if area_classification == 'Rural' else 2 if area_classification == 'Suburban' else 3 if area_classification == 'Urban' else 4
            area_classification_score = living_enviornment_scoring_order1[area_classification_list_key] + living_enviornment_scoring_order2[area_classification_list_key]
            
            weather_score = self.zipcode_prefix_weather_score[zipcode_prefix]
            natural_disaster_score = self.state_natural_disaster_score[states_abbreviation_list[state]]

            total_city_score = home_afforability_score + household_income_score + married_score + families_with_children_score + school_enrollment_score + work_score + education_score + area_classification_score + weather_score + natural_disaster_score
            final_city_score.append((city_name,total_city_score,zipcode_prefix))

            if final_zipcode_prefix_score[zipcode_prefix]:
                final_zipcode_prefix_score[zipcode_prefix]['Score'] += total_city_score
                final_zipcode_prefix_score[zipcode_prefix]['Qty'] += 1
            else:
                final_zipcode_prefix_score[zipcode_prefix].update({'Score': total_city_score, 'Qty': 1})

        max_home_afforabilty = 10
        max_household_income = 10
        max_education_score = education_importance
        max_area_classification_score = max(living_enviornment_scoring_order1) + max(living_enviornment_scoring_order2)
        max_possible_score = max_home_afforabilty + max_household_income + max(married_scoring_order) + max(children_scoring_order) + max(school_enrollment_scoring_order) + max_work_score + max_education_score + max_area_classification_score + self.max_possible_weather_score + self.max_possible_state_disaster_score

        final_zipcode_prefix_score = {zipcode_prefix: score_data['Score'] / score_data['Qty'] for zipcode_prefix, score_data in final_zipcode_prefix_score.items()}
 
        # Add [3] Tuple with Combined City Score and Zipcode Prefix Score
        final_city_score = [(city_data[0], round(city_data[1] * 100 / max_possible_score), city_data[2], city_data[1] + final_zipcode_prefix_score[city_data[2]]) for city_data in final_city_score]
           
        # Utilize in Later Versions*
        top10 = sorted(final_city_score, key=lambda x: x[3], reverse=True)[:10]

        # Top Match
        final_city_results = top10[0]
        
        raise_affordability_warning = True if final_city_results[0] in unlikely_to_afford_warning else False

        zipcode_prefix_boundary = self.zipcode_prefix_boundary_data[final_city_results[2]]

        region_name = self.zipcode_prefix_region_names[final_city_results[2]]

        state = region_name[-2:]

        region_name = f'{region_name.title()[:-3]}, {states_abbreviation_list[state]}'
        
        return {'Result_City': f"{final_city_results[0].split(',')[0]}, {state}",'Result_City_Coordinates': city_coordinates_dictionary[final_city_results[0]],'Match_Percentage':final_city_results[1],'Region_Name':region_name, 'Zipcode_Prefix_Boundary': zipcode_prefix_boundary, 'Afforability_Warning': raise_affordability_warning}

    def find_distance_to_center(self):
        # Order Does Not Matter
        args_list = [coordinate for coordinate in self.saved_coordinates_list if coordinate]
        
        # Return for 2 or 3 Coordinates
        if len(args_list) >= 2:
            return check_coordinates_distance_to_center(*args_list)

        # No Distance if 1 or Zero Coordinates
        return 0

    def run_location_radius_search(self, radius_index: int):
        args_list = [coordinate for coordinate in self.saved_coordinates_list if coordinate]

        # List of all Zipcode Coordinates - Not State Specific
        self.merged_zipcode_coordinate_data = [zipcode for state_coordinate_list in [*self.zipcode_coordinate_data.values()] for zipcode in state_coordinate_list]
        
        if args_list:
            # Miles of Radius
            radius = [10, 20, 40, 60, 100, 200][radius_index]
            # Send All Zipcode Data
            self.city_radius_results = location_radius_search(radius, self.merged_zipcode_coordinate_data, *args_list)
            # Check for Errors
            if len(self.city_radius_results) < 1:
                self.errors.append('Please alter distance or city selections. Zero cities in area selected.')
        else:
            self.city_radius_results = self.merged_zipcode_coordinate_data

    def calculate_affordable_home_price(self, income: float, percent_income_allocated: str, interest_rate: float, morgage_term: str, adjustments: str):
        
        monthly_income = income / 12
        monthly_interest_rate = interest_rate / (12 * 100)
        percent_income_allocated = int(percent_income_allocated[:2]) / 100
        total_months = int(morgage_term[:2]) * 12

        # Approximately 80% of Monthly Payment Goes to Morgage & 20% Goes to Tax & Insurance
        monthly_allowable_morgage_payment = monthly_income * percent_income_allocated * 0.8

        """
            M = P [ i(1 + i)^n ] / [ (1 + i)^n – 1]

            M = Total monthly payment
            P = The total amount of your loan
            I = Your interest rate, as a monthly percentage
            N = The total amount of months in your timeline for paying off your mortgage

            Re-written solving for P
            P = M [ (1 + i)^n – 1] / [ i(1 + i)^n ]
        """
        loan_amount = monthly_allowable_morgage_payment * ((1 + monthly_interest_rate) ** total_months - 1) / (monthly_interest_rate * (1 + monthly_interest_rate) ** total_months)

        # Assuming the Standard 20% Down Payment
        total_morgage = loan_amount / 0.8

        adjustment_percent = int(adjustments[:3].replace('%','').replace('+','')) / 100 if adjustments != 'No Change' else 0

        total_morgage = int(round(total_morgage * (1 + adjustment_percent), -3))

        return total_morgage

    def city_name_zipcode_matcher(self, state: str = '', city: str = '', zipcode: str = '', index: int = 0):
        # Catch Errors
        if not state:
            return 'Provide State'

        if not city and not zipcode:
            return 'Provide City or Zipcode'

        # Check Full State Name Provided
        if state in [*states_abbreviation_list.values()]:
            state_coordinate_list = self.zipcode_coordinate_data[state]

        # Check Abbreviated State Name Provided
        elif state.upper() in [*states_abbreviation_list.keys()]:
            state = states_abbreviation_list[state.upper()]
            state_coordinate_list = self.zipcode_coordinate_data[state]
        else:
            result = process.extractOne(state, [*states_abbreviation_list.values()])
            if int(result[1]) > 90:
                state = result[0]
                state_coordinate_list = self.zipcode_coordinate_data[state]
            else:
                return 'Please Provide Valid US State'

        # List of All Cities in State
        state_city_names = [[*city.keys()][0] for city in state_coordinate_list]

        if zipcode:
            if len(zipcode) != 5:
                return 'Please Provide Valid Zipcode'
            for city_name in state_city_names:
                if zipcode in city_name:
                    state_city_name = city_name
                    primary_city_result = city_name.split(', ')[0]
                    break
            else:
                return 'Please Provide Valid Zipcode'

        elif city:
            # Fuzzy Match City 
            city_result = process.extract(city, state_city_names)
            primary_city_list = []
            for city_str in city_result:
                common_city_names = city_str[0].split(', ')
                primary_city_list.append(common_city_names[0])
            primary_city_result = process.extract(city, primary_city_list)
            # Compare Primary City with Common City Names
            if city_result[0][1] >= primary_city_result[0][1]:
                state_city_name = city_result[0][0]
                common_city_names = state_city_name.split(', ')
                primary_city_result = process.extract(city, common_city_names)[0][0]
            else:
                primary_city_result = primary_city_result[0][0]
                state_city_name = city_result[primary_city_list.index(primary_city_result)][0]
            zipcode = state_city_name.split(', ')[-1]
        
        self.saved_coordinates_list[index] = state_coordinate_list[state_city_names.index(state_city_name)][state_city_name]

        return f'{primary_city_result}, {state} {zipcode}'