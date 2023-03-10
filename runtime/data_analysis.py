import json
from runtime.utilities.calculation_utilities import location_radius_search, check_coordinates_distance_to_center
from runtime.utilities.state_abbreviations import states_abbreviation_list
from thefuzz import process

class IdealHomeDataAnalysis():

    """ For Full Methodology: https://github.com/andrew-drogalis/Ideal-Home-Location-Matcher/wiki """

    def __init__(self):
        
        # Import Natural Disaster Ranked Data
        with open('./data_ranking/ranked_data/State_Natural_Disaster_Ranked_Data.json', newline='') as f: 
            self.state_natural_disaster_data = json.load(f)

        # Import Weather Ranked Data
        with open('./data_ranking/ranked_data/Weather_Ranked_Data.json', newline='') as f: 
            self.zipcode_prefix_weather_data = json.load(f)

        # Import Zipcode Ranked Data
        with open('./data_ranking/ranked_data/Zipcode_Ranked_Data.json', newline='') as f: 
            self.zipcode_data = json.load(f)

        # Import Zipcode Coordinate Data
        with open('./data_ranking/ranked_data/Zipcode_Coordinates_Data.json', newline='') as f: 
            self.zipcode_coordinate_data = json.load(f)

        # Initalize Errors List
        self.errors = []
        # Store Coordinates of Family & Work Locations
        self.saved_coordinates_list = [[], [], []]
        # List of all Zipcode Coordinates - Not State Specific
        self.merged_zipcode_coordinate_data = [zipcode for state_coordinate_list in [*self.zipcode_coordinate_data.values()] for zipcode in state_coordinate_list]

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
        self.regional_employment = kwargs['regional_employment']
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
        transition_temperature = float(kwargs['transition_temperature'] or 0)
        winter_temperature = float(kwargs['winter_temperature'] or 0)
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
                precipitation_score = 2 if precipitation_level == zipcode_precipitation else 1 if precipitation_level[5:11] == zipcode_precipitation[5:11] else 0
            elif precipitation_level == 'Below Average':
                precipitation_score = 2 if zipcode_precipitation == 'Below Average' else 1 if zipcode_precipitation == 'Well Below Average' or zipcode_precipitation == 'Average' else 0
            elif precipitation_level == 'Above Average':
                precipitation_score = 2 if zipcode_precipitation == 'Above Average' else 1 if zipcode_precipitation == 'Well Above Average' or zipcode_precipitation == 'Average' else 0
            else:
                precipitation_score = 2 if zipcode_precipitation == 'Average' else 1 if zipcode_precipitation == 'Below Average' or zipcode_precipitation == 'Above Average' else 0

            # Sunshine
            if sunshine_level[:4] == 'Well':
                sunshine_score = 2 if sunshine_level == zipcode_sunshine else 1 if sunshine_level[5:11] == zipcode_sunshine[5:11] else 0
            elif sunshine_level == 'Below Average':
                sunshine_score = 2 if zipcode_sunshine == 'Below Average' else 1 if zipcode_sunshine == 'Well Below Average' or zipcode_sunshine == 'Average' else 0
            elif sunshine_level == 'Above Average':
                sunshine_score = 2 if zipcode_sunshine == 'Above Average' else 1 if zipcode_sunshine == 'Well Above Average' or zipcode_sunshine == 'Average' else 0
            else:
                sunshine_score = 2 if zipcode_sunshine == 'Average' else 1 if zipcode_sunshine == 'Below Average' or zipcode_sunshine == 'Above Average' else 0

            total_score = season_score + precipitation_score + sunshine_score

            self.zipcode_prefix_weather_score.update({zipcode_prefix:total_score})


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

            total_severity_number = 3 if total_severity == 'High' else 2 if total_severity == 'Moderate' else 1 if total_severity == 'Low' else 0
            total_frequency_number = 4 if total_frequency == 'Well Above Average' else 3 if total_frequency == 'Above Average' else 2 if total_frequency == 'Average' else 1 if total_frequency == 'Below Average' else 0

            total_disaster_score = (total_severity_number + total_frequency_number) * natural_disaster_risk

            try:
                disaster_1_severity = disaster_data[f'{disaster_to_avoid}_Severity_Rank']
                disaster_1_frequency = disaster_data[f'{disaster_to_avoid}_Frequency_Rank']
                disaster_1_severity_number = 3 if disaster_1_severity == 'High' else 2 if disaster_1_severity == 'Moderate' else 1 if disaster_1_severity == 'Low' else 0
                disaster_1_frequency_number = 4 if disaster_1_frequency == 'Well Above Average' else 3 if disaster_1_frequency == 'Above Average' else 2 if disaster_1_frequency == 'Average' else 1 if disaster_1_frequency == 'Below Average' else 0
                disaster_1_score = (disaster_1_severity_number + disaster_1_frequency_number) * natural_disaster_risk
            except:
                disaster_1_score = 0

            try:
                disaster_2_severity = disaster_data[f'{disaster_to_avoid2}_Severity_Rank']
                disaster_2_frequency = disaster_data[f'{disaster_to_avoid2}_Frequency_Rank']
                disaster_2_severity_number = 2 if disaster_2_severity == 'High' else 1 if disaster_2_severity == 'Moderate' else 0
                disaster_2_frequency_number = 3 if disaster_2_frequency == 'Well Above Average' else 2 if disaster_2_frequency == 'Above Average' else 1 if disaster_2_frequency == 'Average' else 0
                disaster_2_score = (disaster_2_severity_number + disaster_2_frequency_number) * natural_disaster_risk
            except:
                disaster_2_score = 0

            try:
                disaster_3_severity = disaster_data[f'{disaster_to_avoid3}_Severity_Rank']
                disaster_3_frequency = disaster_data[f'{disaster_to_avoid3}_Frequency_Rank']
                disaster_3_severity_number = 1 if disaster_3_severity == 'High' else 0
                disaster_3_frequency_number = 2 if disaster_3_frequency == 'Well Above Average' else 1 if disaster_3_frequency == 'Above Average' else 0
                disaster_3_score = (disaster_3_severity_number + disaster_3_frequency_number) * natural_disaster_risk
            except:
                disaster_3_score = 0

            total_state_score = total_disaster_score + disaster_1_score + disaster_2_score + disaster_3_score

            self.state_natural_disaster_score.update({state: total_state_score})

    def results_frame_7(self):
        city_results = []

        # Are you Married
        married_importance = int(self.married_importance)
        if self.married_state == 'No':
            married_scoring_order = [2 * married_importance, 1.5 * married_importance, 1 * married_importance, 0.5 * married_importance, 0]
        else:
            married_scoring_order = [0, 0.5 * married_importance, 1 * married_importance, 1.5 * married_importance, 2 * married_importance]

        # Do you have children
        children_importance = int(self.children_importance )
        if self.children_state == 'No':
            children_scoring_order = [2 * children_importance, 1.5 * children_importance, 1 * children_importance, 0.5 * children_importance, 0]
        else:
            children_scoring_order = [0, 0.5 * children__importance, 1 * children__importance, 1.5 * children__importance, 2 * children__importance]

        living_enviornment_scoring_order1 = [4,2,1,0,0] if self.living_enviornment == 'Hyper Rural' else [2,4,2,1,0] if self.living_enviornment == 'Rural' else [1,2,4,2,1] if self.living_enviornment == 'Suburban' else [0,1,2,4,2] if self.living_enviornment == 'Urban' else [0,0,1,2,4]
        living_enviornment_scoring_order2 = [2,1,0,0,0] if self.living_enviornment2 == 'Hyper Rural' else [1,2,1,0,0] if self.living_enviornment2 == 'Rural' else [0,1,2,1,0] if self.living_enviornment2 == 'Suburban' else [0,0,1,2,1] if self.living_enviornment2 == 'Urban' else [0,0,0,1,2]
                

        for city in self.city_radius_results:
            zipcode = [*city.keys()][0][-5:]
            zipcode_prefix = zipcode[:3]
            zipcode_data = self.zipcode_data[zipcode]
            state = zipcode_data["City"][-2:]

            median_home_value = zipcode_data['Median_Home_Value']
            mad_home_value = zipcode_data['MAD_Home_Value']

            # Most Importance
            if self.user_home_price >= median_home_value - mad_home_value * 1.5:

                # Preferance Toward the Median
                whole_mad_home_value_positive = median_home_value + mad_home_value
                half_mad_home_value_positive = median_home_value + mad_home_value * 0.5
                half_mad_home_value_negative = median_home_value - mad_home_value * 0.5
                whole_mad_home_value_negative = median_home_value - mad_home_value

                home_afforability_score = 10 if half_mad_home_value_negative <= self.user_home_price <= half_mad_home_value_positive else 5 if whole_mad_home_value_negative <= self.user_home_price <= whole_mad_home_value_positive else 0

                median_household_income = zipcode_data['Median_Household_Income']
                mad_household_income = zipcode_data['MAD_Household_Income']

                whole_mad_income_positive = median_household_income + mad_household_income
                half_mad_income_positive = median_household_income + mad_household_income * 0.5
                half_mad_income_negative = median_household_income - mad_household_income * 0.5
                whole_mad_income_negative = median_household_income - mad_household_income

                household_income_score = 10 if half_mad_income_negative <= self.user_home_price <= half_mad_income_positive else 5 if whole_mad_income_negative <= self.user_home_price <= whole_mad_income_positive else 0

                married_percentage = zipcode_data["Married_Percentage"]
                married_score = married_scoring_order[0] if married_percentage == 'Well Bellow Average' else married_scoring_order[1] if married_percentage == 'Bellow Average' else married_scoring_order[2] if married_percentage == 'Average' else married_scoring_order[3] if married_percentage == 'Above Average' else married_scoring_order[4]
                
                families_with_children = zipcode_data["Families_with_Children"]
                families_with_children_score = children_scoring_order[0] if families_with_children == 'Well Bellow Average' else children_scoring_order[1] if families_with_children == 'Bellow Average' else children_scoring_order[2] if families_with_children == 'Average' else children_scoring_order[3] if families_with_children == 'Above Average' else children_scoring_order[4]
                    

                school_enrollment_percentage = zipcode_data["School_Enrollment_Percentage"]

                self.school_enrollment_importance

                if self.employment_status == 'Seeking Employment':
                    employment_percentage = zipcode_data['Employment_Percentage']
                    self.regional_employment = kwargs['regional_employment']
                    if self.transportation_method == '':
                        transportation_method = zipcode_data[f'_Work_Percentage']
                    commute_time = zipcode_data["Travel_Time_To_Work"]
                    self.commute_time = kwargs['commute_time']



                # What's your education level:
                education_importance = int(self.education_level_importance)
                self.education_level
                education_score = zipcode_data["Education_Score"]

                area_classification = zipcode_data["Area_Classification"]
                area_classification_list_key = 0 if area_classification == 'Hyper Rural' else 1 if area_classification == 'Rural' else 2 if area_classification == 'Suburban' else 3 if area_classification == 'Urban' else 4
                area_classification_score = living_enviornment_scoring_order1[area_classification_list_key] + living_enviornment_scoring_order2[area_classification_list_key]
               
                weather_score = self.zipcode_prefix_weather_score[zipcode_prefix]
                natural_disaster_score = self.state_natural_disaster_score[states_abbreviation_list[state]]

                total_zipcode_score = home_afforability_score + household_income_score + married_score + families_with_children_score


        return {}

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
        
        if args_list:
            # Miles of Radius
            radius = [10, 20, 40, 60, 100, 200][radius_index]
            # Send All Zipcode Data
            self.city_radius_results = location_radius_search(radius, self.merged_zipcode_coordinate_data, *args_list)
            # Check for Errors
            if len(self.city_results) < 1:
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