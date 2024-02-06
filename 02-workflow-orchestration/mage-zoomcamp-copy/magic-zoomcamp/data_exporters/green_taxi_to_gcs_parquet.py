from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path
import os
import pyarrow as pa
import pyarrow.parquet as pq


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./peppy-citron-411704-888e6b9e01ee.json"

bucket_name = 'mage_zoomcamp_beau_branton_bucket'
project_id = 'peppy-citron-411704'

table_name = "green_taxi_data"
root_path = f'{bucket_name}/{table_name}'



@data_exporter
def export_data(data, *args, **kwargs):

    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()
    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs
   )