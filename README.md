# Data Pipeline: *fetch_datafiles*

## Overview
The *fetch_datafiles* data pipeline is a versatile Python script designed to retrieve and process data files from the TLC (Taxi and Limousine Commission) website. It supports a range of data categories, including 'yellow', 'green', 'fhv', 'fhvhv', and 'zone-ids', allowing users to extract specific datasets based on their needs.

## Features
* **Dynamic Output Formats:** The function supports multiple output formats, including 'parquet', 'avro', 'xlsx', and 'csv', providing flexibility for diverse use cases.
* **Intelligent Data Filtering:** Data can be filtered based on data category, time range (start and end timestamps), and other criteria, ensuring precision in file retrieval.
* **Web Scraping:** Utilizes web scraping techniques with BeautifulSoup to extract file information from the TLC website, providing an up-to-date source of data.
* **Data Concatenation and Transformation:** Handles scenarios where multiple files need to be concatenated (e.g., 'yellow_green' category), transforming data for consistency.
* **Robust Logging:** Incorporates logging functionality to capture progress, errors, and completion messages, aiding in troubleshooting and monitoring.

## Installation
This module requires Python3.9 or greater and can be installed directly from GitHub using pip. You will need a secret key which will be provided separately.
```bash
pip install git+https://<github-secret-key>@github.com/imz33shan/fetch-tlc-data.git
```

## Usage
Once you have successfully installed the fetch-tlc-data module, you can use the fetch_datafiles function in your Python scripts or Jupyter Notebooks. The installation process automatically takes care of installing the required dependencies.

### Example
```python
# Extract datafiles for Yellow and Green taxis for Jan-2023 and Feb-2023 in avro file format

from tlc_taxi_data.fetch_tlc_taxi_data import fetch_datafiles
from datetime import datetime
import time

start, end = datetime(2023,1,1), datetime(2023,2,28) 

start_time = int(time.mktime(start.timetuple()))
end_time = int(time.mktime(end.timetuple()))

out_loc = r".\data-files"
fetch_datafiles(data_category='yellow_green', start_timestamp=start_time, end_timestamp=end_time,
                output_loc=out_loc, output_format=['avro'])
```
### Function Usage and Assertions
The fetch_datafiles function incorporates various assertions and data type checks to ensure correct usage and enhance the robustness of the data retrieval process. Below are the key considerations and assertions to be aware of when using the function:
#### Input Parameters
* **data_category (str):**
Must be one of {'yellow_green', 'fhv', 'fhvhv', 'zone-ids'}.
* **output_loc (str):**
Specifies the location where the output data files will be saved.
* **output_format (list of str, default ['parquet']):**
Specifies the type of output data files.
Should be one or more of {'parquet', 'avro', 'xlsx', 'csv'}.
* **start_timestamp ({None, int}, default None):**
Start timestamp (UNIX format) for filtering data files.
* **end_timestamp ({None, int}, default None):**
End timestamp (UNIX format) for filtering data files.
* **verbose (bool, default True):**
If True, additional information is printed during execution.

#### Assertions
* **Type Checks for Parameters:**
The function checks that input parameters have the correct data type, ensuring compatibility and preventing unintended usage.

* **data_category Check:**
Ensures that the 'data_category' parameter is one of the allowed values ('yellow_green', 'fhv', 'fhvhv', 'zone-ids'). This ensures that the function operates on valid data categories.

* **output_format Check:**
Verifies that the 'output_format' parameter contains only allowed values ('parquet', 'avro', 'xlsx', 'csv'). This ensures that the specified output formats are valid.

* **Constraints for 'zone-ids' data_category:**
Enforces constraints specific to the 'zone-ids' data category, ensuring that 'start_timestamp' and 'end_timestamp' must be None for this category.

* **Constraints for Timestamps:**
Requires that 'start_timestamp' and 'end_timestamp' are not None, ensuring that a time range is specified for data categories other than 'zone-ids'.

## Key Decisions in Data Extraction/Transformation
* ### Monthly Data Files for Easy Processing
In an effort to streamline data processing and enhance user-friendliness, output data files are saved individually for each month. This approach simplifies analysis and storage, allowing for more efficient handling of data on a monthly basis. Each file follows a clear naming convention, indicating the data category and the specific month and year, promoting a well-organized and easily navigable dataset.
* ### Timestamp Format Conversion
The original timestamp format in the dataset is transformed to UNIX format (in seconds). This change improves compatibility and consistency across datasets, making it easier to work with time-related information. The conversion aligns with widely adopted practices in data processing.
* ### Concatenation of Yellow and Green Taxi Data
'yellow' and 'green' taxi datasets are combined into one group called 'yellow_green.' as these both share identical columns. Additional column ('taxi_category') is added into output datafiles to tell them apart. This makes it easier to handle the data, avoids repetition, and simplifies the analysis process.

## Structured Output Data Definition

The output data files are structured in various formats, catering to different analytical needs. The following formats are available for data conversion:

- **Parquet**: A columnar storage format that optimizes data compression and is well-suited for analytics.
- **CSV (Comma-Separated Values)**: A widely supported plain-text format, suitable for easy data exchange and compatibility with various tools.
- **Avro**: A binary serialization format that supports schema evolution, making it ideal for storing evolving datasets.
- **Excel (XLSX)**: A spreadsheet format that allows for easy visualization and analysis, suitable for smaller datasets.

> [!NOTE]  
> If any of the output data files exceed the row limit of Excel (approximately 1,048,576 rows), attempting to export to xlsx format may result in an error. In such cases, consider exporting to other formats like CSV to avoid potential issues with file size constraints in Excel.

Choose the format that best fits your analysis requirements and tool compatibility. Detailed schema information for each format is provided in the respective sections below.

### Output File Naming Conventions:
* For 'zone-ids' data: taxi-zones
* For other data categories: data_category_tripdata_YYYY-MM
These naming conventions provide a clear structure, indicating the type of data and the corresponding time frame for each output file.
### Output Datasets Definition
* #### yellow_green Data Files

| Column                 | Data Type |
|------------------------|-----------|
| VendorID               | Integer   |
| pickup_datetime        | Integer   |
| dropoff_datetime       | Integer   |
| passenger_count        | Float     |
| trip_distance          | Float     |
| RatecodeID             | Float     |
| store_and_fwd_flag     | String    |
| PULocationID           | Integer   |
| DOLocationID           | Integer   |
| payment_type           | Float     |
| fare_amount            | Float     |
| extra                  | Float     |
| mta_tax                | Float     |
| tip_amount             | Float     |
| tolls_amount           | Float     |
| improvement_surcharge  | Float     |
| total_amount           | Float     |
| congestion_surcharge   | Float     |
| airport_fee            | Float     |
| taxi_category          | String    |
| trip_type              | Float     |

* #### fhv Data Files

| Column                  | Data Type |
|-------------------------|-----------|
| dispatching_base_num    | String    |
| pickup_datetime         | Integer   |
| dropOff_datetime        | Integer   |
| PUlocationID            | Float     |
| DOlocationID            | Float     |
| Affiliated_base_number  | String    |

* #### fhvhv Data Files

| Column                | Data Type        |
|-----------------------|------------------|
| hvfhs_license_num     | String           |
| dispatching_base_num  | String           |
| originating_base_num  | String           |
| request_datetime      | Integer          |
| on_scene_datetime     | Integer          |
| pickup_datetime       | Integer          |
| dropoff_datetime      | Integer          |
| PULocationID          | Integer          |
| DOLocationID          | Integer          |
| trip_miles            | Float            |
| trip_time             | Integer          |
| base_passenger_fare   | Float            |
| tolls                 | Float            |
| bcf                   | Float            |
| sales_tax             | Float            |
| congestion_surcharge  | Float            |
| airport_fee           | Float            |
| tips                  | Float            |
| driver_pay            | Float            |
| shared_request_flag   | String           |
| shared_match_flag     | String           |
| access_a_ride_flag    | String           |
| wav_request_flag      | String           |
| wav_match_flag        | String           |

* #### zone-ids Data Files

| Column        | Data Type |
|---------------|-----------|
| LocationID    | Integer   |
| Borough       | String    |
| Zone          | String    |
| service_zone  | String    |

