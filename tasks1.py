# The average distance driven by yellow and green taxis per hour
# The data used for this task is spanned over last 3 years (2023, 2022, 2021)

from tlc_taxi_data.fetch_tlc_taxi_data import fetch_datafiles
from datetime import datetime
import time
import os
import pandas as pd

start, end = datetime(2021,1,1), datetime(2023,12,31) 

start_time = int(time.mktime(start.timetuple()))
end_time = int(time.mktime(end.timetuple()))

file_loc = './data-files/'

fetch_datafiles(data_category='yellow_green', start_timestamp=start_time, end_timestamp=end_time,
                output_loc=file_loc, output_format=['parquet'])

reqd_columns = ['pickup_datetime', 'trip_distance', 'taxi_category']
all_data_files = os.listdir(file_loc)
concat_df = pd.DataFrame()

for file in all_data_files:
    if 'yellow_green' in file:
        new_df = pd.read_parquet(f'./data-files/{file}')[reqd_columns]
        new_df.dropna(inplace=True)
        concat_df = pd.concat([concat_df, new_df])
        del new_df

concat_df.rename(columns={'pickup_datetime': 'timestamp'}, inplace=True)
concat_df['timestamp'] = pd.to_datetime(concat_df['timestamp'], unit='s')
concat_df['hour'] = concat_df['timestamp'].dt.hour
result = concat_df.groupby(['taxi_category', 'hour'])['trip_distance'].mean().reset_index()
print(result)