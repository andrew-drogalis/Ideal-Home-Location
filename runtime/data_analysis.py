import json
from thefuzz import process

class IdealHomeDataAnalysis():

    """ For Full Methodology: https://github.com/andrew-drogalis/Ideal-Home-Location-Matcher/wiki """

    def __init__(self):
        # Import Ranked Natural Disaster Data
        with open('./data_ranking/ranked_data/State_Natural_Disaster_Ranked_Data.json', newline='') as f: 
            state_natural_disaster_data = json.load(f)

        # Import Ranked Weather Data
        with open('./data_ranking/ranked_data/Weather_Ranked_Data.json', newline='') as f: 
            zipcode_prefix_weather_data = json.load(f)

        # Import Ranked Zipcode Prefix Data
        with open('./data_ranking/ranked_data/Zipcode_Prefix_Ranked_Data.json', newline='') as f: 
            zip_code_prefix_data = json.load(f)

        # Import Ranked City Data
        with open('./data_ranking/ranked_data/City_Ranked_Data.json', newline='') as f: 
            city_data = json.load(f)

        # Import City Coordinate Data
        with open('./data_ranking/ranked_data/City_Coordinate_Data.json', newline='') as f: 
            city_coordinate_data = json.load(f)


    def family_location_frame1(self):

        # Relationship
        pass

    def family_detailed_frame1b(self):
        pass

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

   