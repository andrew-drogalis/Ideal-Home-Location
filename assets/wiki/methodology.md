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
* [Scoring Criteria](#Scoring-Criteria)
* [Final Analysis](#Final-Analysis)

## Data Source

The data source folder contains the csv files for the natural disaster events and the USA zipcode prefix codes. The source citation has the information on where to download. This folder contains no processing. 

For replicating the results of this repository, copy the natural disaster '.csv' in the project folder. Modifications have been made to how the blizard / snow storm data has been recorded. The orginal file shows severe snow storms affecting the southern states and less affect on the northern states. I believe this is based on 'impact' with the northern states being more prepared for winter weather. The implication of avoiding blizards, based on my understanding, is to avoid the colder climates. That is why these modifications have been made.

## Data Collection

The three main datasets used in the analysis are natural disaster data, weather data, and zipcode census data. The datasets have been scrapped for relevant information and saved in the /data_collection/proccessed_data/{file_name}.json files. 

### Natural Disaster

The natural disaster data from the data sources folder is processed for later data ranking. The data was seperated into events by each state affected, year, disaster type, death total, and total damages. All 50 states and the District of Columbia recorded some level of natural disatster in the 120 years of data available.

### Weather Data

The weather data was fetched from the meteostat api. The weather data was averaged over the three digit zipcode prefix. THis seperated the united states into approimiates 950 weather zones. The monthly average temperature, precipitaion  levels, and sunshine levels were collected and then averaged over a period of 30 years. 

### Zipcode Data

The zipcode data was gathered by using the uszipcode repository. The data was gathered from US Census website and is mostly from 2016. This adds some margin of error to the results. Hopefully, in future updates the 2020 census data can be gathered. This results are representative of over 41,000 US zipcodes. Any data missing for selected zipcode is stored as a null value. The missing results are disrgarded in the final calcuation.

## Data Ranking

The data is ranked for ease of use and reduction of CPU overhead in the final application. The processed data sets are updated with the ranking and stored in the /data_ranking/ranked_data/{file_name}.json files. 

### Finding Skewness

The rank compares each region of the united states agasint each other and provideds a method for sorting based on the dataset distribution. Highly skewed datasets tend to over exaggerate the mean relative to the median. 

### Median Ranking

The data is all 

Median data is used when the data is mostly normally distributed. It's counter inutative because the median absolute deviation is used when the data is NOT normally distributed. None of the data is perfectly normal skewness or kurtosis that is why the median absolute is used.

The deviation ratio in this case is the measure of how many median absolute deviations a data point is away from the median.

```python
deviation_ratio = (value[x] - Yearly_Median) / Yearly_Median_Absolute_Deviation
```

Rank is

```python
rank = 'Well Above Average' if deviation_ratio > 2 else 'Above Average' if 2 >= deviation_ratio > 1 else 'Average' if 1 >= deviation_ratio >= -1 else 'Below Average' if -1 > deviation_ratio >= -2 else 'Well Below Average' 
```

### Mean Ranking
mean
standard deviation

The deviation ratio in this case is the measure of how many standard deviations a data point is away from the mean.

```python
deviation_ratio = (value[x] - Yearly_Mean) / Yearly_Standard_Deviation
```

Rank is

```python
 rank = 'Very Good' if deviation_ratio > 2 else 'Good' if 2 >= deviation_ratio > 1 else 'Exceptable' if 1 >= deviation_ratio > 0 else 'Not Exceptable'
```

## Scoring Criteria

#### 1. Location Search Results

- Based on Most Important Factors 

#### 2. Home Price & Household Income

- T

#### 3. Weather Selections

- T

#### 4. Dynamic Importance Selections

- T

#### 5. Fixed Score Metrics

- T

## Final Analysis

The 


P2