from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action
from pandas import DataFrame
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def execute_transformer_action(df: DataFrame, *args, **kwargs) -> DataFrame:
    final_batting_df = df

    #TRANSFORM DATA (CASTING TO CORRECT DTYPES etc.)
    batting_int_cols = ['G', 'R', 'AB', 'H', '2B', '3B', 'TB', 'HR', 'RBI', 'BB', 'HBP', 'SF', 'SH', 'K', 'OPP DP', 'CS', 'Picked', 'SB', 'IBB', 'GDP', 'RBI2out','game_id','attendance']
    # pitching_int_cols = ['G', 'App', 'GS', 'CG', 'H', 'R', 'ER', 'BB', 'SO', 'SHO', 'BF', 'P-OAB', '2B-A', '3B-A', 'Bk', 'HR-A', 'WP', 'HB', 'IBB', 'Inh Run', 'Inh Run Score', 'SHA', 'SFA', 'Pitches', 'GO', 'FO', 'W', 'L', 'SV', 'OrdAppeared', 'KL', 'pickoffs','game_id','attendance']
    # fielding_int_cols = ['G','PO','A','TC','E','CI','PB','SBA','CSB','IDP','TP','game_id','attendance']

    for col in batting_int_cols:   
        # final_batting_df[col].replace('', 0)
        # final_batting_df[col].fillna(0)
        final_batting_df[col] = np.floor(pd.to_numeric(final_batting_df[col], errors='coerce')).astype('Int64')

    final_batting_df['ingestion_date'] = datetime.now()
    final_batting_df = final_batting_df.astype({
        'Player': str,
        'Pos': str,
        'team': str,
        'location': str,
        'date': 'datetime64[ns]',
        'ingestion_date': 'datetime64[ns]'
    })

    # final_batting_df['date']=final_batting_df['date'].dt.date
    # final_pitching_df['IP'] = np.floor(pd.to_numeric(final_pitching_df['IP'], errors='coerce')).astype('float64')

    return final_batting_df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'