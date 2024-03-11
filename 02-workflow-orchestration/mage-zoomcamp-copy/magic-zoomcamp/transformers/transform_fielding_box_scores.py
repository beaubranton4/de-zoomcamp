from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action
from pandas import DataFrame
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
http://localhost:6789/pipelines/ncaa_baseball_daily_box_score_test/edit?sideview=tree#
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def execute_transformer_action(df: DataFrame, *args, **kwargs) -> DataFrame:
    final_fielding_df = df[2]
    #TRANSFORM DATA (CASTING TO CORRECT DTYPES etc.)
    fielding_int_cols = ['G','PO','A','TC','E','CI','PB','SBA','CSB','IDP','TP','game_id','attendance']

    for col in fielding_int_cols:
        final_fielding_df[col] = np.floor(pd.to_numeric(final_fielding_df[col], errors='coerce')).astype('Int64')

    final_fielding_df['ingestion_date'] = datetime.now()
    final_fielding_df = final_fielding_df.astype({
        'Player': str,
        'Pos': str,
        'team': str,
        'location': str,
        'date': 'datetime64[ns]',
        'ingestion_date': 'datetime64[ns]'
    })
    # final_pitching_df['IP'] = np.floor(pd.to_numeric(final_pitching_df['IP'], errors='coerce')).astype('float64')

    return final_fielding_df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'