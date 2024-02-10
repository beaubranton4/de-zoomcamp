import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    # print(data.dtypes)
    # data['lpep_pickup_datetime'] = pd.to_datetime(data['lpep_pickup_datetime'], errors='coerce')
    # data['lpep_dropoff_datetime'] = pd.to_datetime(data['lpep_pickup_datetime'], errors='coerce')
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    data['lpep_dropoff_date'] = data['lpep_pickup_datetime'].dt.date
    data = data.drop(columns=['lpep_pickup_datetime', 'lpep_dropoff_datetime'])
    print(data.dtypes)
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
