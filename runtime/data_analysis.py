import json
from runtime.utilities.calculation_utilities import location_radius_search, city_name_zipcode_matcher
from timeit import default_timer

class IdealHomeDataAnalysis():

    """ For Full Methodology: https://github.com/andrew-drogalis/Ideal-Home-Location-Matcher/wiki """

    def __init__(self):
        start = default_timer()
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

        # List of all Zipcode Coordinates - Not State Specific
        self.merged_zipcode_coordinate_data = [zipcode for state_coordinate_list in [*self.zipcode_coordinate_data.values()] for zipcode in state_coordinate_list]


    def family_location_frame_1(self, state: str, city: str = '', zipcode: str = ''):

        state_coordinate_list = self.zipcode_coordinate_data[state]

        matcher_results = city_name_zipcode_matcher(state_coordinate_list=state_coordinate_list,city=city,zipcode=zipcode)
        print(matcher_results)
        if matcher_results:
            results_citys = location_radius_search(max_time=10, city_search_list=self.merged_zipcode_coordinate_data, coordinate_1=matcher_results['Coordinates'])

            self.current_citys_list = results_citys

        married_people_priority = [1, 2, 3, 4, 5]


    def family_detailed_frame_1b(self):

        kids_priority = [1 ,2, 3, 4, 5]
        kids_school_enrollment_priority = [1, 2, 3, 4, 5]


    def work_location_frame_2(self):
        # Work Location
        # Employment Opportunities
        pass


    def work_detailed_frame_2b(self):
        pass


    def income_metrics_frame_3(self):
        pass


    def area_classification_frame_4(self):
        # Eductation Level
        pass


    def weather_metrics_frame_5(self):
        pass


    def natural_disaster_risk_frame_6(self):
        pass

