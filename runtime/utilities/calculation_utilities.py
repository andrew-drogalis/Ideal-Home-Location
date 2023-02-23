"""
    ## Calculation Utilities
    - Reusable Functions for the Data Analysis Class

    Constants:
    1 Degree of Latitude is 69 Miles @ 0.6 Miles Per Minute = 115 Minutes / Degree Latitude
    1 Degree of Longitude is 54.6 Miles @ 0.6 Miles Per Minute = 91 Minutes / Degree Longitude
"""
minutes_per_degree_lat = 115
minutes_per_degree_lng = 91

def check_coordinates_middle_distance(coordinate_1: list, coordinate_2: list, coordinate_3: list):

    # Calculate Differences For Latitude & Longitude
    coordinate_1_2_lat_difference = abs(coordinate_1[0] - coordinate_2[0]) * minutes_per_degree_lat if coordinate_2 else 0
    coordinate_1_2_lng_difference = abs(coordinate_1[1] - coordinate_2[1]) * minutes_per_degree_lng if coordinate_2 else 0

    # Calculate Distance w/ Pythagorean theorem
    coordinate_1_2_hypotenuse = (coordinate_1_2_latitude_difference ** 2 + coordinate_1_2_longitude_difference ** 2) ** (1/2)

    # 2x Max Distance is Not Possible to Find Results - Leave Safety Factor 1.9x
    # max_time *= 1.9
    # if max_time < coordinate_1_2_hypotenuse: 
    #     return False
    # return True

#
def location_radius_search(max_time: float, city_search_list: list, coordinate_1: list, coordinate_2: list = []):
    city_results_list = []

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

