"""
    ## Calculation Utilities
    - Reusable Functions for the Data Analysis Class

    Constants:
    1 Degree of Latitude is 69 Miles
    1 Degree of Longitude is 54.6 Miles
"""
miles_per_degree_lat = 69
miles_per_degree_lng = 54.6

def find_centroid(c_1: list, c_2: list, c_3: list = []):
    if c_3:
        centroid_latitude = (c_1[0] + c_2[0] + c_3[0]) / 3
        centroid_longitiude = (c_1[1] + c_2[1] + c_3[1]) / 3
    else:
        centroid_latitude = (c_1[0] + c_2[0]) / 2
        centroid_longitiude = (c_1[1] + c_2[1]) / 2
    
    return [centroid_latitude, centroid_longitiude]

def find_hypotenuse(c_1: list, c_2: list):
    # Calculate Differences For Latitude & Longitude
    coordinate_1_2_lat_difference = abs(c_1[0] - c_2[0]) * miles_per_degree_lat
    coordinate_1_2_lng_difference = abs(c_1[1] - c_2[1]) * miles_per_degree_lng

    # Calculate Distance w/ Pythagorean theorem
    return (coordinate_1_2_lat_difference ** 2 + coordinate_1_2_lng_difference ** 2) ** (1/2)

def check_coordinates_distance(coordinate_1: list, coordinate_2: list, coordinate_3: list = []):
  
    if not coordinate_3:
        coordinate_1_2_hypotenuse = find_hypotenuse(coordinate_1, coordinate_2)

        # Middle Distance in Miles
        return round(coordinate_1_2_hypotenuse / 2)

    else:
        centroid_coordinates = find_centroid(coordinate_1, coordinate_2, coordinate_3)

        coordinate_1_centroid_hypotenuse = find_hypotenuse(coordinate_1, centroid_coordinates)
        coordinate_2_centroid_hypotenuse = find_hypotenuse(coordinate_2, centroid_coordinates)
        coordinate_3_centroid_hypotenuse = find_hypotenuse(coordinate_3, centroid_coordinates)
        
        max_distance = max(coordinate_1_centroid_hypotenuse, coordinate_1_centroid_hypotenuse, coordinate_3_centroid_hypotenuse)

        return round(max_distance)

def location_radius_search(radius_distance: float, city_search_list: list, coordinate_1: list, coordinate_2: list = [], coordinate_3: list = []):
    """ Add 5 % Safety Factor 
        Rational: Only Center Point of Zipcodes are stored as Lat & Lng Coordinates """
    radius_distance *= 1.05
    # Initalize Data Storage
    city_results_list = []

    # Set Centriod Coordinates
    if coordinate_2:
        centroid_coordinates = find_centroid(coordinate_1, coordinate_2, coordinate_3)
    else:
        centroid_coordinates = coordinate_1

    # Check Each City
    for city in city_search_list:
        coordinate_total_hypotenuse = find_hypotenuse(centroid_coordinates, [*city.values()][0])

        if coordinate_total_hypotenuse <= radius_distance:
            city_results_list.append(city)

    return city_results_list

