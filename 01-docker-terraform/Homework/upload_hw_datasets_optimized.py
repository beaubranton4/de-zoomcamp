import time
import pandas as pd
from sqlalchemy import create_engine

# Connect to Postgres DB
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

# Define the chunk size
chunksize = 100000  # Adjust this value depending on your available memory

# Define the URLs
green_taxi_data_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz'
zones_url = 'https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv'

# Read and upload the zones data
zones = pd.read_csv(zones_url)
zones.head(n=0).to_sql(name='zones', con=engine, if_exists='replace')
zones.to_sql(name='zones', con=engine, if_exists='append')

# Read and upload the green_taxi_data in chunks
for i, chunk in enumerate(pd.read_csv(green_taxi_data_url, compression='gzip', chunksize=chunksize, low_memory=False)):
    start_time = time.time()  # Start time

    # Convert datetime columns to datetime data type
    chunk.lpep_pickup_datetime = pd.to_datetime(chunk.lpep_pickup_datetime)
    chunk.lpep_dropoff_datetime = pd.to_datetime(chunk.lpep_dropoff_datetime)

    # Upload the chunk to Postgres
    chunk.to_sql(name='green_taxi_data', con=engine, if_exists='append')

    end_time = time.time()  # End time
    print(f"Chunk {i+1} processed in {end_time - start_time} seconds. Number of rows ingested: {len(chunk)}")