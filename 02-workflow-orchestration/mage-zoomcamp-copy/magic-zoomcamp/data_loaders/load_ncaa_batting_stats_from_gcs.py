from google.cloud import storage
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from mage_ai.io.config import ConfigFileLoader
from mage_ai.settings.repo import get_repo_path
from os import path
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

def extract_dates(object_keys):
    dates = []
    for key in object_keys:
        key = urllib.parse.unquote(key)
        parts = key.split('/')
        for part in parts:
            if part.startswith('date='):
                date = part[len('date='):].split('%')[0]
                # Convert the string to a datetime object and then to a date object
                date = datetime.strptime(date[:19], '%Y-%m-%d %H:%M:%S').date()
                dates.append(date)
    return dates

###SHOULD WE ALSO CHECK BIG QUERY TO SEE WHICH DATA ALREADY EXISTS?
### AND ONLY TRANSFER IN THE NEW DATA? OR SHOULD WE RUN THE WHOLE THING?

@data_loader
def load_all_partitions_from_gcs(*args, **kwargs):
    
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    bucket_name = 'mage_zoomcamp_beau_branton_bucket'
    prefix = 'd1_baseball_project/batting_box_scores_test/date='

    # Create a client
    client = storage.Client()
    # Get the bucket
    bucket = client.get_bucket(bucket_name)
    # Get the blobs (objects) with the specified prefix
    blobs = bucket.list_blobs(prefix=prefix)
    # Get the object keys
    object_keys = [blob.name for blob in blobs if blob.name.endswith('.parquet')]
    
    date_strings = extract_dates(object_keys)
    dates = [date_string for date_string in date_strings]
    
    #Test for checking date type of dates
    # for i, element in enumerate(dates):
    #     print(f"Element {i} is of type: {type(element)}")
    # print(dates)

    ####START # Find the dates that are not in your dates list

    start_date_str = '02/16/2024' #Replace with automatic variable for first day of season
    end_date = datetime.now().date()

    start_date = datetime.strptime(start_date_str, "%m/%d/%Y").date()
    all_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    
    for i, element in enumerate(all_dates):
        print(f"2nd: Element {i} is of type: {type(element)}")
    
    missing_dates = [date for date in all_dates if date not in dates]
    print(missing_dates)

    ####END # Find the dates that are not in your dates list

    df = pd.DataFrame()
    
    # Load each object
    for object_key, date in zip(object_keys, dates):
        data = GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
            bucket_name,
            object_key,
            format='parquet'
        )

        # ADD DATE BACK AS A COLUMN

        df = pd.concat([df,data])
        print(f"Finished appending data from {date}")


    # Return the DataFrame
    return df
