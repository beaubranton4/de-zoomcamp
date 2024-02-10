import io
import pandas as pd
import requests
import pyarrow.parquet as pq
from io import BytesIO

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """


    url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-{}.parquet'
    
    #Drastically reduces memory by defining data types
    #Should fail if the data type changes
    dtypes = {
                'VendorID': 'int64',
                'lpep_pickup_datetime': 'datetime64[ns]',
                'lpep_dropoff_datetime': 'datetime64[ns]',
                'store_and_fwd_flag': 'object',
                'RatecodeID': 'float64',
                'PULocationID': 'int64',
                'DOLocationID': 'int64',
                'passenger_count': 'float64',
                'trip_distance': 'float64',
                'fare_amount': 'float64',
                'extra': 'float64',
                'mta_tax': 'float64',
                'tip_amount': 'float64',
                'tolls_amount': 'float64',
                'ehail_fee': 'object',
                'improvement_surcharge': 'float64',
                'total_amount': 'float64',
                'payment_type': 'float64',
                'trip_type': 'float64',
                'congestion_surcharge': 'float64'
    }

    dfs = []
    for i in range(1, 13):
        date = str(i).zfill(2)
        print(date)
        url_chunk = url.format(date)
        print(url_chunk)

        response = requests.get(url_chunk)
        response.raise_for_status()  # Raise exception if invalid response

        # Load parquet data into a pandas dataframe
        df = pq.read_table(BytesIO(response.content)).to_pandas()
        dfs.append(df)
        output = pd.concat(dfs,ignore_index=True)
        print(output['lpep_pickup_datetime'].tail())

    return output


    #returns dataframe as url with dtype = taxi_dtypes defined above, also knows to parse the above two columns as dates
    # return pd.read_csv(
    #     url, sep=',', compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates
    #     )


# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'