def fetch_datafiles(data_category: str, output_loc: str, output_format: list = ['parquet'],
                        start_timestamp: (None, int) = None, end_timestamp: (None, int) = None, verbose: bool = True):
    """
    Fetch input files info from TLC website, returning a success/error message of file saving.

    Parameters
    ----------
    data_category : str
        The type of data to be extracted. Should be one of {'yellow_green', 'fhv', 'fhvhv', 'zone-ids'}.
    output_loc : str
        The location where the output data files will be saved.
    output_format : list of str, default ['parquet']
        The type of output data files. Should be one or more of {'parquet', 'avro', 'xlsx', 'csv'}.
    start_timestamp : (None, int), default None
        Start timestamp (UNIX format) for filtering data files.
    end_timestamp : (None, int), default None
        End timestamp (UNIX format) for filtering data files.
    verbose : bool, default True
        If True, print additional information during the execution.

    Returns
    -------
    If output_loc and output_format are provided, returns a message indicating the success of saving the requested file types in the provided output location.
    """

    import requests  # HTTP requests
    import pandas as pd  # Data manipulation
    import os  # Operating system interaction
    import re # To perform regex operations
    import logging  # Added for improved logging
    from bs4 import BeautifulSoup  # Web scraping
    from urllib.parse import urlparse  # URL parsing
    from fastavro import writer, parse_schema # To convert DataFrame to avro file format

    # Function to map DataFrame data types to avro data types
    def pandas_to_avro_type(data_type):
        keywords_mapping = {
            'int': 'int',
            'float': 'float',
            'object': 'string',
            'bool': 'boolean',
        }
        
        for keyword, avro_type in keywords_mapping.items():
            if keyword in str(data_type):
                return avro_type

    # Added logging configuration
    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # Define allowed choices for data_category and output_format
    allowed_data_categories = {'yellow_green', 'fhv', 'fhvhv', 'zone-ids'}
    allowed_output_formats = {'parquet', 'avro', 'xlsx', 'csv'}

    # Define parameter names and their expected types
    parameters = {
        'data_category': str,
        'output_loc': str,
        'output_format': list,
        'start_timestamp': (type(None), int),
        'end_timestamp': (type(None), int),
        'verbose': bool
    }

    # Perform type-checks and value-checks using a loop
    for param_name, allowed_types in parameters.items():
        param_value = locals()[param_name]

        # Type-check
        assert isinstance(param_value, allowed_types), f"{param_name} must be one of the allowed types: {allowed_types}"

        # Additional checks for data_category, output_format
        if param_name == 'data_category':
            assert param_value in allowed_data_categories, f"{param_name} must be one of {allowed_data_categories}"
        elif param_name == 'output_format':
            if param_value:
                assert all(item in allowed_output_formats for item in param_value), f"{param_name} must be one or more of {allowed_output_formats}"

    # Ensure proper constraints based on data_category
    if 'zone-ids' in data_category:
        assert start_timestamp is None, "start_timestamp must be None for data_category 'zone-ids'"
        assert end_timestamp is None, "end_timestamp must be None for data_category 'zone-ids'"
    else:
        assert start_timestamp is not None, "start_timestamp must not be None for data_category other than 'zone-ids'"
        assert end_timestamp is not None, "end_timestamp must not be None for data_category other than 'zone-ids'"

    try:

        logger.info("Initiating retrieval of file information from the website.")

        # Define the base URL of the TLC website where trip record data is available
        base_url = 'https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page'

        # Fetch the content of the base URL and parse it using BeautifulSoup
        base_url_content = requests.get(base_url).content
        base_url_soup = BeautifulSoup(base_url_content, 'html.parser')

        # Delete variable to free up memory
        del base_url_content

        # Initialize an empty DataFrame to store file information
        files_info = pd.DataFrame(columns=['file_name', 'file_extension', 'file_category', 'file_monthyear', 'file_link'])

        # Extract all tables from the HTML content
        all_tables = base_url_soup.find_all('table')

        # Delete variable to free up memory
        del base_url_soup

        # Iterate through each table to find file information
        for table in all_tables:

            # Find all anchor tags within the table
            table_rows = table.find_all('a')

            for row in table_rows:

                # Extract file link from the anchor tag
                file_link = row.get('href')

                # Parse the file link to get file name and extension
                url_path = urlparse(file_link).path
                file_name, file_extension = os.path.splitext(os.path.basename(url_path))

                # Extract month and year information from the file name
                file_monthyear = file_name.split('_')[-1]
                file_category = file_name.split('_')[0]

                # Append the file information to the DataFrame
                files_info.loc[len(files_info)] = [file_name, file_extension, file_category, file_monthyear, file_link]

        # Adding info for Taxi Zones file downloading if required
        files_info.loc[len(files_info)] = ['taxi-zones', '.csv', 'zone-ids', '', 'https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv']
        
        # Assign single file_category name to Yellow and Green taxis data
        condition = files_info.file_category.isin(['yellow', 'green'])
        files_info.loc[condition, 'file_category'] = 'yellow_green'

        # Delete variable to free up memory
        del all_tables

        # Convert the 'monthyear' column to UNIX datetime format
        files_info['file_monthyear'] = pd.to_datetime(files_info['file_monthyear'], format="%Y-%m")
        files_info['file_monthyear'] = files_info['file_monthyear'].astype('int64') // 10**9

        logger.info("File information successfully retrieved from the website.")

        # Filter files based on specified criteria and reset the DataFrame index
        if 'zone-ids' in data_category:
            query = 'file_category in @data_category'
        else:
            query = '@start_timestamp <= file_monthyear <= @end_timestamp and file_category in @data_category'
        
        reqd_files = files_info.query(query).reset_index(drop=True)

        # Delete variable to free up memory
        del files_info

        # Filter files based on the current data category
        filter_condition = reqd_files.file_category == data_category
        reqd_files_details = reqd_files[filter_condition][['file_name', 'file_link', 'file_extension', 'file_monthyear']]
        total_files = len(reqd_files_details)

        # Delete variable to free up memory
        del reqd_files

        logger.info("Initiating data retrieval process from files.")

        # Get a list of all monthyears to loop through each monthyear
        all_file_monthyears = reqd_files_details.file_monthyear.unique()

        if total_files > 0:

            # Initialize a counter for file processing progress
            file_counter = 0

            for monthyear in all_file_monthyears:
                
                # Files info for the monthyear 
                monthyear_df = reqd_files_details[reqd_files_details.file_monthyear == monthyear].reset_index(drop=True)

                # Declare empty dataframe for concatenation for data having multiple files in single monthyear e.g. yellow_green
                cum_df = pd.DataFrame()

                # Iterate through each file link for the current data category
                for file_name, file_link, file_extension, file_monthyear in monthyear_df.values:

                    # Read the parquet file into a DataFrame
                    if 'csv' in file_extension:
                        file_df = pd.read_csv(file_link)
                    elif 'parquet' in file_extension:
                        file_df = pd.read_parquet(file_link)

                    # Add a column taxi_category to identify the data of Green and Yellow taxis and change the initial name to 'yellow_green'
                    if 'yellow_green' in data_category:
                        file_df['taxi_category'] = file_name.split('_')[0]
                        file_name = re.sub(r'green|yellow', 'yellow_green', file_name)

                        # Replace initial strings in column names of Yellow and Green datasets to make them same for concatenation
                        items_to_replace = ['tpep_', 'lpep_']
                        for item in items_to_replace:
                            file_df.columns = file_df.columns.str.replace(item, '')
                        
                    # Drop columns with all na values (This speeds up the concatenation process.)
                    columns_to_drop = file_df.columns[file_df.isna().all()]
                    file_df.drop(columns=columns_to_drop, inplace=True)

                    # Identify columns with datetime data type
                    datetime_columns = file_df.select_dtypes(include=['datetime']).columns

                    # Iterate through each datetime column and convert to UNIX timestamp (in seconds)
                    for col in datetime_columns:

                        # Convert datetime to UNIX timestamp and store in the same column
                        file_df[col] = file_df[col].astype('int64') // 10**6

                    # Concatenate to the cum_df decalred earlier
                    cum_df = pd.concat([cum_df, file_df])

                    del file_df
                    
                    # Increment the counter and print progress information
                    file_counter += 1

                    logger.info(f'{data_category} - {file_counter}/{total_files} done.')

                # Output data to specified formats if requested
                if 'parquet' in output_format:
                    cum_df.to_parquet(os.path.join(output_loc, file_name + '.parquet'), index=False)
                if 'xlsx' in output_format:
                    cum_df.to_excel(os.path.join(output_loc, file_name + '.xlsx'), index=False)
                if 'csv' in output_format:
                    cum_df.to_csv(os.path.join(output_loc, file_name + '.csv'), index=False)
                if 'avro' in output_format:
                    df_dtypes = cum_df.dtypes.astype(str).tolist()
                    avro_fields = [
                            {"name": column, "type": ["null", pandas_to_avro_type(df_dtypes[idx])]}
                            for idx, column in enumerate(cum_df.columns)
                        ]

                    schema = {
                        'name': file_name,
                        'type': 'record',
                        'fields': avro_fields
                    }
                    parsed_schema = parse_schema(schema)

                    df_size = len(cum_df)
                    chunk_size = 1000000

                    avro_file_loc = os.path.join(output_loc, file_name + '.avro')

                    # Write initial 2 records
                    with open(avro_file_loc, "wb") as fp:
                        writer(fp, schema, [])

                    for i in range(0, df_size, chunk_size):
                        records = cum_df.loc[(cum_df.index>=i)&(cum_df.index<i+chunk_size)].to_dict('records')
                        with open(avro_file_loc, "a+b") as fp:
                            writer(fp, schema, records)
                            del records

                # Delete the DataFrame containing the current file's data to free up memory
                del cum_df

            final_message = "Data processing and saving completed."
        else:
            error_message = (
                f"No files found for category '{data_category}' within the desired time frame."
            )
            logging.error(error_message)
            final_message = None
            
        # Indicate that the data processing and saving have been completed successfully
        if final_message:
            logger.info(final_message)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return f"Error: {str(e)}"