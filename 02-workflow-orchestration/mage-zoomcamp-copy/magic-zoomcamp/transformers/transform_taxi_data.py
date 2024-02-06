if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

#simple filter on data where passenger_count > 0
@transformer
def transform(data, *args, **kwargs):
   
   print(f"Preprocessing { data['passenger_count'].isin([0]).sum() } rows with zero passengers")
   return data[data['passenger_count'] > 0]

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are no rides with zero passengers'
