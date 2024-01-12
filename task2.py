# Day of the week in 2019 and 2020 which has the lowest number of single rider trips

from tlc_taxi_data.fetch_tlc_taxi_data import fetch_datafiles
from datetime import datetime
import time
import os
import pandas as pd

start, end = datetime(2019,1,1), datetime(2020,12,31) 

start_time = int(time.mktime(start.timetuple()))
end_time = int(time.mktime(end.timetuple()))

file_loc = './data-files/'

fetch_datafiles(data_category='yellow_green', start_timestamp=start_time, end_timestamp=end_time,
                output_loc=file_loc, output_format=['parquet'])

reqd_columns = ['pickup_datetime', 'passenger_count']
all_data_files = os.listdir(file_loc)
concat_df = pd.DataFrame()

for file in all_data_files:
    if 'yellow_green' in file:
        new_df = pd.read_parquet(f'{file_loc}{file}')[reqd_columns]
        new_df.dropna(inplace=True)
        new_df = new_df[new_df.passenger_count==1]
        concat_df = pd.concat([concat_df, new_df], ignore_index=True)
        del new_df

concat_df.rename(columns={'pickup_datetime': 'timestamp'}, inplace=True)
concat_df['timestamp'] = pd.to_datetime(concat_df['timestamp'], unit='s')
concat_df['day_of_week'] = concat_df['timestamp'].dt.day_name()

aggr_df = concat_df.groupby(['day_of_week'])['passenger_count'].count().reset_index()
aggr_df = aggr_df.rename(columns={'passenger_count': 'number_of_rides'})
result = aggr_df.iloc[aggr_df['number_of_rides'].idxmin()]
print(result)
