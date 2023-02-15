"""
    Ranking Functions
    
"""

"""
    Key Values:
        - Well Above Average: Outside 2.0 Deviations from the Median
        - Above Average: Between 2.0 and 1.0 Deviations from the Median
        - Average: Between 1.0 and -1.0 Deviations from the Median
        - Below Average: Between -1.0 and -2.0 Deviations from the Median
        - Well Below Average: Outside -2.0 Deviations from the Median
"""

def rank_value(deviation_ratio: float):
    #
    rank = 'Well Above Average' if deviation_ratio > 2 else 'Above Average' if 2 >= deviation_ratio > 1 else 'Average' if 1 >= deviation_ratio >= -1 else 'Below Average' if -1 > deviation_ratio >= -2 else 'Well Below Average' 
    return rank


"""
    Frequency / Severity Key Values:
        - High: Outside 1.0 Deviations from the Centroid
        - Moderate: Between 1.0 and -1.0 Deviations from the Centroid
        - Low: Outside 1.0 Deviations from the Centroid
"""


def rank_extreme_value(deviation_ratio: float):
    #
    rank = 'Very Good' if deviation_ratio > 2 else 'Good' if 2 >= deviation_ratio > 1 else 'Exceptable' if 1 >= deviation_ratio > 0 else 'Not Exceptable'

    return rank
