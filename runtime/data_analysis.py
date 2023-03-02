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

        # Import Zipcode Prefix Ranked Data
        with open('./data_ranking/ranked_data/Zipcode_Prefix_Ranked_Data.json', newline='') as f: 
            self.zipcode_prefix_data = json.load(f)

        # Import Zipcode Ranked Data
        with open('./data_ranking/ranked_data/Zipcode_Ranked_Data.json', newline='') as f: 
            self.zipcode_data = json.load(f)

        # Import Zipcode Coordinate Data
        with open('./data_ranking/ranked_data/Zipcode_Coordinates_Data.json', newline='') as f: 
            self.zipcode_coordinate_data = json.load(f)

        # Store Coordinates of Family & Work Locations
        self.saved_coordinates_list = [[], [], []]
        # Initalize Errors List
        self.errors = []
        # List of all Zipcode Coordinates - Not State Specific
        self.merged_zipcode_coordinate_data = [zipcode for state_coordinate_list in [*self.zipcode_coordinate_data.values()] for zipcode in state_coordinate_list]

    # -------------- Navigation Functions
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
        work_transporation = kwargs['work_transportation']
        self.commute_time = kwargs['commute_time']
        self.transportation_method = work_transporation.replace(' ','_').replace('Personal','Motor').replace('or_','')  if work_transportation != "Work From Home" else ''

        self.run_location_radius_search(radius_index=kwargs['radius_index'])

    def income_frame_3(self, **kwargs):
        # Save User Selections to Class Variables
        self.user_income = kwargs['income']
        self.user_home_price = kwargs['affordable_home_price']

    def area_classification_frame_4(self, **kwargs):
        # Save User Selections to Class Variables
        self.education_level = kwargs['education_level']
        self.married_state = kwargs['education_level_importance']
        self.married_state = kwargs['living_enviornment']
        self.married_state = kwargs['living_enviornment2']

    def weather_frame_5(self, **kwargs):
        # Save User Selections to Class Variables
        self.married_state = kwargs['seasons']
        self.married_state = kwargs['summer_temperature']
        self.married_state = kwargs['transition_temperature']
        self.married_state = kwargs['winter_temperature']
        self.married_state = kwargs['precipitation_level']
        self.married_state = kwargs['sunshine_level']

        for zipcode_prefix, weather_data in self.zipcode_prefix_weather_data.items():
            pass

    def natural_disaster_risk_frame_6(self, **kwargs):
        # Save User Selections to Class Variables
        self.married_state = kwargs['natural_disaster_risk']
        self.married_state = kwargs['disaster_to_avoid']
        self.married_state = kwargs['disaster_to_avoid2']
        self.married_state = kwargs['disaster_to_avoid3']

        for state, disaster_data in self.state_natural_disaster_data.items():
            pass

    def results_frame_7(self):
        city_results = []

        for city in self.city_radius_results:
            zipcode = city[-5:]
            zipcode_prefix = zipcode[:3]
            zipcode_data = self.zipcode_data[zipcode]
            state = zipcode_data["City"][-2:]

            married_percentage = zipcode_data["Married_Percentage"]
            families_with_children = zipcode_data["Families_with_Children"]
            school_enrollment_percentage = zipcode_data["School_Enrollment_Percentage"]
            median_home_value = zipcode_data['Median_Home_Value']
            mad_home_value = zipcode_data['MAD_Home_Value']
            median_household_income = zipcode_data['Median_Household_Income']
            mad_household_income = zipcode_data['MAD_Household_Income']

            if self.employment_status == 'Seeking Employment':
                employment_percentage = zipcode_data['Employment_Percentage']
                transportation_method = zipcode_data[f'{self.transportation_method}_Work_Percentage'] if self.transportation_method else ''
                commute_time = zipcode_data["Travel_Time_To_Work"]

            education_score = zipcode_data["Education_Score"]
            area_classification = zipcode_data["Area_Classification"]
    

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