# Methodology

## Table of Contents

* [Data Source](#Data-Source)
* [Data Collection](#Data-Collection)
    * [Natural Disaster Data](#Natural-Disaster-Data)
    * [Weather Data](#Weather-Data)
    * [Zipcode Data](#Zipcode-Data)
* [Data Ranking](#Data-Ranking)
    * [Finding Skewness](#Finding-Skewness)
    * [Median Ranking](#Median-Ranking)
    * [Mean Ranking](#Mean-Ranking)
* [Scoring Prioritization](#Scoring-Prioritization)
    * [Location Search Results](#Location-Search-Results)
    * [Home Affordability & Household Income](#Home-Affordability-&-Household-Income)
    * [Weather Selections](#Weather-Selections)
    * [Dynamic Importance Selections](#Dynamic-Importance-Selections)
    * [Fixed Score Metrics](#Fixed-Score-Metrics)
* [Final Results](#Final-Results)

## Data Source

The data source folder contains the csv files for the natural disaster events and the USA zipcode prefix codes. The source citation has the information on where to download the files. This folder contains no data processing. 

For replicating the results of this repository, copy the natural disaster '.csv' in the project folder. Modifications have been made to how the blizzard / snow storm data has been recorded. The original file shows severe snow storms affecting the southern states and less affect on the northern states. I believe this is based on 'impact' with the northern states being more prepared for winter weather. The implication of avoiding blizzards, based on my understanding, is to avoid the colder climates. This is the rational behind these modifications.

## Data Collection

The three main datasets used in the analysis are natural disaster data, weather data, and zipcode census data. The datasets have been scrapped for relevant information and saved in the /data_collection/proccessed_data/{file_name}.json files. This is to reduce runtime CPU overhead and reduce memory footprint.

### Natural Disaster Data

The natural disaster data from the data sources folder is processed for later data ranking. The data is separated into events on a per state and per disaster type basis. All 50 states, and the District of Columbia, have recorded some type of natural disaster in the last 120 years since the dataset began.

### Weather Data

The weather data was fetched from the Meteostat API. The weather data for each city was collected and averaged over the three digit zipcode prefix which the city belonged. This separated the united states into approximately 950 weather zones. The monthly temperature, precipitation, and sunshine levels were collected and then averaged over a period of 30 years. 

### Zipcode Data

The zipcode data was gathered by using the uszipcode repository. The data was gathered from US Census website. Unfortunately, the data is mostly from 2016, and this will add some margin of error to the results. Hopefully, in future updates the 2020 census data can be incorporated. This results are representative of over 41,000 US zipcodes. Any data missing for selected zipcode is stored as a null value and disregarded in the final calculation.

## Data Ranking

The data is ranked for ease of use and to reduce the CPU overhead during runtime. The processed datasets are updated with the ranking and stored in the /data_ranking/ranked_data/{file_name}.json files. 

### Finding Skewness

The rank compares each region of the united states against each other and provideds a method for sorting based on the dataset distribution. Highly skewed datasets tend to over exaggerate the mean relative to the median. 

### Median Ranking

The median ranking was used when it was appropriate to find an approximate normal distribution for moderately skewed datasets. All of the values are include in the final analysis, both the left and right tails. The deviation ratio in this case is the measure of how many median absolute deviations a data point is away from the median.

```python
deviation_ratio = (value[x] - Yearly_Median) / Yearly_Median_Absolute_Deviation

rank = 'Well Above Average' if deviation_ratio > 2 else 'Above Average' if 2 >= deviation_ratio > 1 else 'Average' if 1 >= deviation_ratio >= -1 else 'Below Average' if -1 > deviation_ratio >= -2 else 'Well Below Average' 
```

### Mean Ranking

The mean ranking was used when it was appropriate to isolate the extreme values for highly skewed datasets. Only the right tail values are included in the final analysis, while the left tail values are disregarded. The deviation ratio in this case is the measure of how many standard deviations a data point is away from the mean.

```python
deviation_ratio = (value[x] - Yearly_Mean) / Yearly_Standard_Deviation

rank = 'Very Good' if deviation_ratio > 2 else 'Good' if 2 >= deviation_ratio > 1 else 'Exceptable' if 1 >= deviation_ratio > 0 else 'Not Exceptable'
```

## Scoring Prioritization

The 

### Location Search Results

The location search results takes first priority over all other metrics. The location radius selected will limit the results to only show the cities within the radius of the submitted city. If more than one cities is input the results will be from the center distance of the cities. 

### Home Affordability & Household Income

T

### Weather Selections

T

### Dynamic Importance Selections

T

### Fixed Score Metrics

T

## Final Results

The final result is the city with the highest score and the final region is the three digit zipcode prefix for the associated city. 



The final result is calcuated by using the sum of the city score and the region score. 
