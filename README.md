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
