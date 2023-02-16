import json
from runtime.utilities.calculation_utilities import location_radius_search, city_name_zipcode_matcher
from timeit import default_timer

class IdealHomeDataAnalysis():

    """ For Full Methodology: https://github.com/andrew-drogalis/Ideal-Home-Location-Matcher/wiki """

    def __init__(self):
        start = default_timer()
        # Import Ranked Natural Disaster Data
        with open('./data_ranking/ranked_data/State_Natural_Disaster_Ranked_Data.json', newline='') as f: 
            self.state_natural_disaster_data = json.load(f)

        # Import Ranked Weather Data
        with open('./data_ranking/ranked_data/Weather_Ranked_Data.json', newline='') as f: 
            self.zipcode_prefix_weather_data = json.load(f)

        # Import Ranked Zipcode Prefix Data
        with open('./data_ranking/ranked_data/Zipcode_Prefix_Ranked_Data.json', newline='') as f: 
            self.zip_code_prefix_data = json.load(f)

        # Import Ranked City Data
        with open('./data_ranking/ranked_data/City_Ranked_Data.json', newline='') as f: 
            self.city_data = json.load(f)

        # Import City Coordinate Data
        with open('./data_ranking/ranked_data/City_Coordinates_Data.json', newline='') as f: 
            self.city_coordinate_data = json.load(f)

        self.all_city_coordinate_data = [city for state_city_list in [*self.city_coordinate_data.values()] for city in state_city_list]

        self.family_location_frame1(state='MA', city='Brimfield')


    def family_location_frame1(self, state: str, city: str = '', zipcode: str = ''):

        state_coordinate_list = self.city_coordinate_data[state]

        matcher_results = city_name_zipcode_matcher(state_coordinate_list=state_coordinate_list,city=city,zipcode=zipcode)
        print(matcher_results)
        if matcher_results:
            results_citys = location_radius_search(max_time=10, city_search_list=self.all_city_coordinate_data, coordinate_1=matcher_results['Coordinates'])

            self.current_citys_list = results_citys

        married_people_priority = [1, 2, 3, 4, 5]


    def family_detailed_frame1b(self):

        kids_priority = [1 ,2, 3, 4, 5]
        kids_school_enrollment_priority = [1, 2, 3, 4, 5]

    def work_location_frame2(self):
        # Work Location
        # Employment Opportunities
        pass

    def work_detailed_frame2b(self):
        pass

    def income_metrics_frame3(self):
        pass

    def area_classification_frame4(self):
        # Eductation Level
        pass

    def weather_metrics_frame5(self):
        pass

    def natural_disaster_risk_frame6(self):
        pass

