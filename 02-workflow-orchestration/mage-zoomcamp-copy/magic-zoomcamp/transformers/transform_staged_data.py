if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    data.columns = (data.columns
                    .str.replace(' ','_')
                    .str.lower()
    )
    data['tpep_pickup_datetime'] = data['tpep_pickup_datetime'].dt.date
    data['tpep_dropoff_datetime'] = data['tpep_dropoff_datetime'].dt.date
    return data
