from math import cos, pi
"""
    ## Calculation Utilities
    - Reusable Functions for the Data Analysis Class

    Constants:
    1 Degree of Latitude is 69 Miles
    1 Degree of Longitude is cosine(Degree of Latitude) * 69 Miles
"""
miles_per_degree_lat = 69

def find_centroid(c_1: list, c_2: list, c_3: list = []):
    if c_3:
        centroid_latitude = (c_1[0] + c_2[0] + c_3[0]) / 3
        centroid_longitiude = (c_1[1] + c_2[1] + c_3[1]) / 3
    else:
        centroid_latitude = (c_1[0] + c_2[0]) / 2
        centroid_longitiude = (c_1[1] + c_2[1]) / 2
    
    return [centroid_latitude, 
        centroid_longitiude]

def find_hypotenuse(c_1: list, c_2: list):
    # Calculate Differences For Latitude & Longitude
    coordinate_1_2_lat_difference = abs(c_1[0] - c_2[0]) * miles_per_degree_lat
    average_latitude_radians = (c_1[0] + c_2[0]) * pi / 360
    miles_per_degree_lng = cos(average_latitude_radians) * miles_per_degree_lat
    coordinate_1_2_lng_difference = abs(c_1[1] - c_2[1]) * miles_per_degree_lng

    # Calculate Distance w/ Pythagorean theorem
    distance = (coordinate_1_2_lat_difference ** 2 + coordinate_1_2_lng_difference ** 2) ** (1/2)

    return distance

def check_coordinates_distance_to_center(*args):
 
    if len(args) == 2:
        c_1_2_hypotenuse = find_hypotenuse(c_1=args[0], c_2=args[1])
        # Middle Distance in Miles
        distance_to_center = round(c_1_2_hypotenuse / 2)
    else:
        centroid_coordinates = find_centroid(c_1=args[0], c_2=args[1], c_3=args[2])

        c_1_centroid_distance = find_hypotenuse(c_1=args[0], c_2=centroid_coordinates)
        c_2_centroid_distance = find_hypotenuse(c_1=args[1], c_2=centroid_coordinates)
        c_3_centroid_distance = find_hypotenuse(c_1=args[2], c_2=centroid_coordinates)
        
        distance_to_center = round(max(c_1_centroid_distance, c_1_centroid_distance, c_3_centroid_distance))

    return distance_to_center

def location_radius_search(radius_distance: float, city_search_list: list, *args):
    """ 
        Add 5 % Safety Factor 
        Rational: Only Center Point of Zipcodes are stored as Lat & Lng Coordinates 
    """
    radius_distance *= 1.05

    # Initalize Data Storage
    city_results_list = []
    # Set Centriod Coordinates
    if len(args) == 3:
        centroid_coordinates = find_centroid(c_1=args[0], c_2=args[1], c_3=args[2])
    elif len(args) == 2:
        centroid_coordinates = find_centroid(c_1=args[0], c_2=args[1])
    else:
        centroid_coordinates = args[0]

    # Check Each City
    for city in city_search_list:
        city_coordinates = [*city.values()][0]

        coordinate_total_hypotenuse = find_hypotenuse(c_1=centroid_coordinates, c_2=city_coordinates)

        if coordinate_total_hypotenuse <= radius_distance:
            city_results_list.append(city)

    return city_results_list

