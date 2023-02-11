from statistics import mean, median, stdev

# 'K' is a scale factor to use the MAD as a consistent estimator for the standard deviation. For this application the standard multiplier of 1.4826 for a normal distribution will suffice.
# Source: https://stats.stackexchange.com/questions/355943/how-to-estimate-the-scale-factor-for-mad-for-a-non-normal-distribution 
k_scaler = 1.4826

"""
    Pearson's Calcuation for Skewness (Fisher's is not necessary in this case)
    Skew = 3 * (Mean – Median) / Standard Deviation
    Extreme Skewness < -0.20 or Extreme Skewness > 0.20
    If the Dataset has Extreme Skewness, replace the Standard Deviation with the MAD (Median Absolute Deviation)
"""

def centroid_and_deviation_calc(dataset: list, name_of_data: str):
    # Find Mean, Medain, & Standard Deviation
    mean_dataset = mean(dataset)
    median_dataset = median(dataset)
    stdv_dataset = stdev(dataset)
    # Calculate Skewness from Pearson's Method
    skewness_dataset = 3 * (mean_dataset - median_dataset) / stdv_dataset if stdv_dataset else 0
    if skewness_dataset > 0.2 or skewness_dataset < -0.2:
        # Determine Median Absolute Deviation
        mad_dataset = [abs(x - median_dataset) for x in dataset]
        mad_dataset = median(mad_dataset) * k_scaler
        return {
            f'Centriod_{name_of_data}': median_dataset,
            f'Deviation_{name_of_data}': mad_dataset
        }
    
    return {
        f'Centriod_{name_of_data}': mean_dataset,
        f'Deviation_{name_of_data}': stdv_dataset
    }