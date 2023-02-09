import json

class IdealHomeDataAnalysis():

    def __init__(self):
        # Import Ranked Natural Disaster Data
        with open('./data_processors/processed_data/State_NaturalDisaster_Data.json', newline='') as f: 
            state_disaster_data = json.load(f)

        # Import Ranked Weather Data
        with open('./data_processors/processed_data/State_NaturalDisaster_Data.json', newline='') as f: 
            state_disaster_data = json.load(f)

        # Import Processed Zipcode Prefix Data
        with open('./data_processors/processed_data/State_NaturalDisaster_Data.json', newline='') as f: 
            state_disaster_data = json.load(f)

    def user_defined_prioritization(self):
        """
        
        """

        pass


    def match_weather_data(self):
        pass

    def match_disaster_data(self):
        pass