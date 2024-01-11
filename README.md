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

from tlc_taxi_data import fetch_datafiles
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

* **Output Format Check:**
Verifies that the 'output_format' parameter contains only allowed values ('parquet', 'avro', 'xlsx', 'csv'). This ensures that the specified output formats are valid.

* **Constraints for 'zone-ids' data_category:**
Enforces constraints specific to the 'zone-ids' data category, ensuring that 'start_timestamp' and 'end_timestamp' must be None for this category.

* **Constraints for Timestamps:**
Requires that 'start_timestamp' and 'end_timestamp' are not None, ensuring that a time range is specified for data categories other than 'zone-ids'.

## Key Decisions in Data Transformation
### 1. Monthly Data Files for Easy Processing
In an effort to streamline data processing and enhance user-friendliness, output data files are saved individually for each month. This approach simplifies analysis and storage, allowing for more efficient handling of data on a monthly basis. Each file follows a clear naming convention, indicating the data category and the specific month and year, promoting a well-organized and easily navigable dataset.
### 2. Timestamp Format Conversion
The original timestamp format in the dataset is transformed to UNIX format (in seconds). This change improves compatibility and consistency across datasets, making it easier to work with time-related information. The conversion aligns with widely adopted practices in data processing.
### 3. Concatenation of Yellow and Green Taxi Data
'yellow' and 'green' taxi datasets are combined into one group called 'yellow_green.' as these both share identical columns. Additional column ('taxi_category') is added into output datafiles to tell them apart. This makes it easier to handle the data, avoids repetition, and simplifies the analysis process.
