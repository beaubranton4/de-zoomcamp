import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):

    dates = ['2020-10','2020-11','2020-12']
    base_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_{}.csv.gz'
    green_taxi_dtypes = {
                        'VendorID': pd.Int64Dtype(),
                        'lpep_pickup_datetime': str,
                        'lpep_dropoff_datetime': str,
                        'store_and_fwd_flag':	str,
                        'RatecodeID':	pd.Int64Dtype(),
                        'PULocationID': pd.Int64Dtype(),
                        'DOLocationID': pd.Int64Dtype(),
                        'passenger_count': pd.Int64Dtype(),
                        'trip_distance': float,
                        'fare_amount': float,
                        'extra':	float,   
                        'mta_tax':	float,
                        'tip_amount':	float,
                        'tolls_amount': float,	
                        'ehail_fee':	float,
                        'improvement_surcharge': float,	
                        'total_amount': float,	
                        'payment_type': pd.Int64Dtype(),	
                        'trip_type': pd.Int64Dtype(),	
                        'congestion_surcharge': float
    }

    # native date parsing 
    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
    dfs = []
    for date in dates:
        url = base_url.format(date)
        print(url)
        df = pd.read_csv(url, sep=',', compression='gzip', dtype=green_taxi_dtypes, parse_dates=parse_dates)
        dfs.append(df)
    output = pd.concat(dfs,ignore_index=True)
    return output


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
