from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    now = kwargs.get('execution_date')
    # print(now)
    # print(now.strftime("%Y-%m-%d"))
    now_fpath = now.strftime("%Y-%m-%d")

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'mage_zoomcamp_beau_branton_bucket'
    object_key = f'Daily_Trips/{now_fpath}_nyc_taxi_daily_trips.parquet'
    print(object_key)

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )
