from thefuzz import process
"""
    Calculation Utilities
"""

# 1 Degree of Latitude is 69 Miles @ 0.6 Miles Per Minute = 115 Minutes / Degree Latitude
minutes_per_degree_lat = 115
# 1 Degree of Longitude is 54.6 Miles @ 0.6 Miles Per Minute = 91 Minutes / Degree Longitude
minutes_per_degree_lng = 91

def location_radius_search(max_time: float, city_search_list: list, coordinate_1: list, coordinate_2: list = []):
    city_results_list = []

    if check_coordinates_distance(max_time, coordinate_1, coordinate_2):
        for city in city_search_list:
            coordinates = [*city.values()][0]

            coordinate_1_latitude_difference = abs(coordinates[0] - coordinate_1[0]) * minutes_per_degree_lat
            coordinate_1_longitude_difference = abs(coordinates[1] - coordinate_1[1]) * minutes_per_degree_lng

            coordinate_1_total_hypotenuse = (coordinate_1_latitude_difference ** 2 + coordinate_1_longitude_difference ** 2) ** (1/2)

            coordinate_2_latitude_difference = abs(coordinates[0] - coordinate_2[0]) * minutes_per_degree_lat if coordinate_2 else 0
            coordinate_2_longitude_difference = abs(coordinates[1] - coordinate_2[1]) * minutes_per_degree_lng if coordinate_2 else 0

            coordinate_2_total_hypotenuse = (coordinate_2_latitude_difference ** 2 + coordinate_2_longitude_difference ** 2) ** (1/2)

            if coordinate_1_total_hypotenuse <= max_time and coordinate_2_total_hypotenuse <= max_time:
                city_results_list.append(city)

    return city_results_list


def check_coordinates_distance(max_time: float, coordinate_1: list, coordinate_2: list):
    
    coordinate_1_2_latitude_difference = abs(coordinate_1[0] - coordinate_2[0]) * minutes_per_degree_lat if coordinate_2 else 0
    coordinate_1_2_longitude_difference = abs(coordinate_1[1] - coordinate_2[1]) * minutes_per_degree_lng if coordinate_2 else 0

    coordinate_1_2_total_hypotenuse = (coordinate_1_2_latitude_difference ** 2 + coordinate_1_2_longitude_difference ** 2) ** (1/2)

    # Unlikely to Return Any Results 
    if coordinate_1_2_total_hypotenuse > max_time * 1.9: 
        return False
   
    return True


def city_name_zipcode_matcher(state_coordinate_list: list, city: str = '', zipcode: str = ''):

        state_city_names = [[*city.keys()][0] for city in state_coordinate_list]

        if zipcode:
            for city_name in state_city_names:
                if zipcode in city_name:
                    state_city_name = city_name
                    primary_city_result = city_name.split(', ')[0]
                    break
            else:
                # Empty Dictionary for Error
                return {} 
        elif city:
            city_result = process.extract(city, state_city_names)
            primary_city_list = []
            for city_str in city_result:
                common_city_names = city_str[0].split(', ')
                primary_city_list.append(common_city_names[0])
            primary_city_result = process.extract(city, primary_city_list)
            if city_result[0][1] >= primary_city_result[0][1]:
                state_city_name = city_result[0][0]
                common_city_names = state_city_name.split(', ')
                primary_city_result = process.extract(city, common_city_names)[0][0]
            else:
                primary_city_result = primary_city_result[0][0]
                state_city_name = city_result[primary_city_list.index(primary_city_result)][0]
            zipcode = state_city_name.split(', ')[-1]
        
       
        coordinate = state_coordinate_list[state_city_names.index(state_city_name)]
        coordinate = coordinate[state_city_name]

        return {
            'Coordinates': coordinate,
            'City_Name': primary_city_result,
            'Zipcode': zipcode
        }