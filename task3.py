# The top 3 of the busiest hours

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
concat_df['hour'] = concat_df['timestamp'].dt.hour

result_df = concat_df.groupby(['hour'])['timestamp'].count().reset_index()
result_df = result_df.sort_values(by='timestamp', ascending=False)
top_3_busiest_hours = result_df.head(3)
print(top_3_busiest_hours)
