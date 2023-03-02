import math
from datetime import datetime
from collections import defaultdict
from meteostat import Monthly, units, Stations
from uszipcode import SearchEngine

# Fetch Data from last 30 Years
start_time = datetime(1993, 1, 1)
end_time = datetime(2023, 1, 1)

# Check Total # of Stations in the USA
stations_nearby = Stations().nearby(35, 95).fetch(20000).to_dict()

stations_nearby = stations_nearby['country']

values = [*stations_nearby.values()]

total_usa_stations  = []

for value in values:
    if isinstance(value, str) and value == 'US':
        total_usa_stations.append(value)

print(len(total_usa_stations))
