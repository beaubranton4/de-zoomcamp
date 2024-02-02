import re

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower().lstrip('_')

@transformer
def transform(data, *args, **kwargs):

    data = data[(data['passenger_count'] != 0) & (data['trip_distance'] != 0)] #Assumes trip distance and passenger count must be >= 0
    # print( len(data[data['passenger_count'] == 0 ]))
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    data.columns = [camel_to_snake(col) for col in data.columns]
    # print(data.columns)
    
    return data


@test
def test_output(output, *args) -> None:

    assert 'vendor_id' in output.columns, 'The column vendor_id does not exist'
    assert (output['passenger_count']>0).all(), 'Some rows have passenger_count >= 0'
    assert (output['trip_distance']>0).all(), 'Some rows have trip_distance >= 0'
