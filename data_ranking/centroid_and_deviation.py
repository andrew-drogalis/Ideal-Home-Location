from statistics import mean, median, stdev

"""
    Pearson's Calcuation for Skewness (Fisher's is not necessary in this case)
    Skew = 3 * (Mean – Median) / Standard Deviation
    Extreme Skewness < -0.20 or Extreme Skewness > 0.20
    If the Dataset has Extreme Skewness, replace the Standard Deviation with the MAD (Median Absolute Deviation)
"""

def centroid_and_deviation_calc(dataset: list, name_of_data: str):

    mean_dataset = mean(dataset)
    median_dataset = median(dataset)
    stdv_dataset = stdev(dataset)

    skewness_dataset = 3 * (mean_dataset - median_dataset) / stdv_dataset if stdv_dataset else 0
    if skewness_dataset > 0.2 or skewness_dataset < -0.2:

        mad_dataset = [abs(x - median_dataset) for x in dataset]
        mad_dataset = median(mad_dataset)
        return {
            f'Centriod_{name_of_data}': median_dataset,
            f'Deviation_{name_of_data}': mad_dataset
        }

    return {
        f'Centriod_{name_of_data}': mean_dataset,
        f'Deviation_{name_of_data}': stdv_dataset
    }