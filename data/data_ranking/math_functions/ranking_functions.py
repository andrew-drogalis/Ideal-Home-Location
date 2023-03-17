# Ranking Functions

"""
    Key Values:
        - Well Above Average: Outside 2.0 Deviations from the Median
        - Above Average: Between 2.0 and 1.0 Deviations from the Median
        - Average: Between 1.0 and -1.0 Deviations from the Median
        - Below Average: Between -1.0 and -2.0 Deviations from the Median
        - Well Below Average: Outside -2.0 Deviations from the Median
    Usage:
        - For Determining Closeness to the Center for Data where the Skewness is Negligable for our Analysis
"""
def rank_value(deviation_ratio: float):
    # Return Rank for Median & Median Absolute Deviation Type Data
    rank = 'Well Above Average' if deviation_ratio > 2 else 'Above Average' if 2 >= deviation_ratio > 1 else 'Average' if 1 >= deviation_ratio >= -1 else 'Below Average' if -1 > deviation_ratio >= -2 else 'Well Below Average' 
    return rank


"""
    Key Values:
        - High: Outside 2.0 Standard Deviations from the Mean
        - Moderate: Between 2.0 and 1.0 Standard Deviations from the Mean 
        - Low: Between 1.0 and 0.0 Standard Deviations from the Mean
        - No Risk: Less thank 0.0 Standard Deviations from the Mean
    Usage:
        - For Determining Extreme Values for Highly Skewed Data. Used to Isolate High Risk / High Likelihood Rare occurrences.
"""
def rank_value_skewed(deviation_ratio: float, rank_label='zipcode'):
    # Return Rank for Mean & Standard Deviation Type Data
    if rank_label == 'zipcode':
        # Labeling for Zipcode Data
        rank = 'Very Good' if deviation_ratio > 2 else 'Good' if 2 >= deviation_ratio > 1 else 'Exceptable' if 1 >= deviation_ratio > 0 else 'Not Exceptable'
    # Labeling for Natural Disaster Data
    else:
        rank = 'High' if deviation_ratio > 2 else 'Moderate' if 2 >= deviation_ratio > 1 else 'Low' if 1 >= deviation_ratio > 0 else 'No Risk'
    return rank


