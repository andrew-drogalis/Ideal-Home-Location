from statistics import mean, median, stdev
from scipy.stats import skew, median_abs_deviation

# 'K' is a scale factor to use the MAD as a consistent estimator for the standard deviation. For this application the standard multiplier of 1.4826 for a normal distribution will suffice.
# Source: https://stats.stackexchange.com/questions/355943/how-to-estimate-the-scale-factor-for-mad-for-a-non-normal-distribution 
k_scaler = 1.4826

"""
    Skewness Calcuated using Fisher-Pearson Coefficent w/ Bias
    Values over 1.0 and below -1.0 are considered highly skewed
"""

def statistics_calc(dataset: list, name_of_data: str):
    # Find Mean, Median, Standard Deviation, Skewness, & Median Absolute Deviation
    mean_dataset = mean(dataset)
    median_dataset = median(dataset)
    stdv_dataset = stdev(dataset)
    skew_dataset = skew(dataset)
    mad_dataset = median_abs_deviation(dataset) * k_scaler

    return {
        f'Mean_{name_of_data}': mean_dataset,
        f'Median_{name_of_data}': median_dataset,
        f'MAD_{name_of_data}': mad_dataset,
        f'Standard_Deviation_{name_of_data}': stdv_dataset,
        f'Skewness_{name_of_data}': skew_dataset
    }
    
def mad_calc(dataset: list, median_of_data: float):
    # Determine Median Absolute Deviation
    mad_dataset = [abs(x - median_of_data) for x in dataset]
    mad_dataset = median(mad_dataset) * k_scaler

    return mad_dataset
    