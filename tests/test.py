import math
from datetime import datetime
from collections import defaultdict
from meteostat import Monthly, units, Stations
from uszipcode import SearchEngine

# Fetch Data from last 30 Years
start_time = datetime(1993, 1, 1)
end_time = datetime(2023, 1, 1)

search = SearchEngine()
zip_number = '035'
result = search.by_prefix(zip_number)
monthly_temperature_results = defaultdict(list)
monthly_precipitation_results = defaultdict(list)
monthly_sunshine_results = defaultdict(list)
monthly_airpressure_results = defaultdict(list)
if result:
    first_city = result[0]
    state = first_city.state
    stations = Stations().nearby(first_city.lat, first_city.lng, 100_000).fetch(5).to_dict()
    station_id = [*stations['name'].keys()][0]
    data = Monthly(station_id, start_time, end_time).convert(units.imperial).fetch().to_dict()
    print(state, first_city.lat, first_city.lng, '\n', data, stations)
    # Select Relevant Data
    temperature_avg = data['tavg']
    precipitation_inch = data['prcp']
    sealevel_airpressure = data['pres'] #hPa
    sunshine_minutes = data['tsun']
    # Monthly Keys for 30 years of data
    datetime_keys = [*temperature_avg.keys()]
    for key in datetime_keys:
        temp = temperature_avg[key]
        rainfall = precipitation_inch[key]
        sunshine = sunshine_minutes[key]
        airpressure = sealevel_airpressure[key]
        if not math.isnan(temp):
            monthly_temperature_results[key.month].append(temp)
        if not math.isnan(rainfall):
            monthly_precipitation_results[key.month].append(rainfall)
        if not math.isnan(sunshine):
            monthly_sunshine_results[key.month].append(sunshine)
        if not math.isnan(airpressure):
            monthly_airpressure_results[key.month].append(airpressure)

# data = {
#     "zipcodes": ["90638", "90639", "10020", "85001", "72201", '11530',"11040"],
# }

# major_city1 = []
# county1 = []
# state1 = []
# population1 = []
# population_density1 = []
# land_area_in_sqmi1 = []
# housing_units1 = []
# median_home_value1 = []
# median_household_income1 = []

# search = SearchEngine()
# for i in np.arange(0, len(data["zipcodes"])):
#     zipcode = search.by_zipcode(data["zipcodes"][i])

#     # Checking for non std postal codes
#     # Demographic info in std postal codes
#     if not zipcode.population:
#         # Checking for non std zipcodes like postal boxes
#         res = search.by_city_and_state(city=zipcode.major_city, state=zipcode.state)
#         if (len(res)) > 0:
#             zipcode = res[0]
#     major_city1.append(zipcode.major_city)
#     county1.append(zipcode.county)
#     state1.append(zipcode.state)
#     population1.append(zipcode.population)
#     population_density1.append(zipcode.population_density)
#     land_area_in_sqmi1.append(zipcode.land_area_in_sqmi)
#     housing_units1.append(zipcode.housing_units)
#     median_home_value1.append(zipcode.median_home_value)
#     median_household_income1.append(zipcode.median_household_income)

# print(major_city1)
# print(county1)
# print(state1)
# print(population1)
# print(population_density1)
# print(housing_units1)
# print(median_home_value1)
# print(median_household_income1)