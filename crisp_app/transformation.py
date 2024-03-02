import io, yaml, os

from contextlib import redirect_stderr
from decimal import Decimal
import pandas as pd
from typing import Dict
from flask import current_app

from crisp_app.utils import create_new_col

def read_input_config(input_config_file_path: str) -> Dict[str, dict]:
    """
    Returns a dict containing key:value pairs from the uploaded input config .yaml file.

    Parameters: 
            input_config_file_path (str): the file path of the uploaded input config .yaml

    Returns: 
            config_dict (Dict[str, dict]): a dict containing config file key:value pairs
    """
    with open(input_config_file_path, "r") as file:
        config_dict = yaml.safe_load(file)
    
    return config_dict


def read_input_data(input_data_file_path: str) -> pd.DataFrame:    
    """
    Returns a Pandas Dataframe containing raw data from the uploaded input data .csv file.

    Parameters: 
            input_data_file_path (str): the file path of the uploaded input data .csv file

    Returns: 
            raw_df (pd.DataFrame): a Pandas DataFrame of the raw data from the uploaded input data .csv file
    """
    f = io.StringIO()

    with redirect_stderr(f):
        raw_df = pd.read_csv(input_data_file_path, on_bad_lines='warn')

    if f.getvalue():
        current_app.logger.warning(f"Reading input data lines - bad line(s): \n{f.getvalue()}")

    return raw_df

def perform_transformation(config_dict: Dict[str, dict], raw_df: pd.DataFrame) -> tuple[tuple[int, int], pd.DataFrame]:
    """
    Returns the shape (rows, columns) of the raw_df Pandas Dataframe
    and the transformed_df Pandas DataFrame.

    Parameters: 
            config_dict (Dict[str, dict]): a dict containing transformation config key:value pairs
            raw_df (pd.DataFrame): a Pandas DataFrame containing raw data from uploaded input data file

    Returns: 
            raw_df.shape, transformed_df (tuple): a tuple containing
            1) the shape of raw_df
            2) Pandas DataFrame, transformed_df 
    """
    # transformation, step 1: create new target cols
    for key, value in config_dict['new_cols'].items():
        raw_df = create_new_col(raw_df, key, value)

    # transformation, step 2: rename target cols
    raw_df = raw_df.rename(columns=config_dict['renamed_cols'])

    # transformation, step 3: convert target cols' dtypes
    for key, value in config_dict['dtype_cols'].items():
        if 'int' in key or 'str' in key:
            raw_df[value] = raw_df[value].astype(key)
        
        elif 'datetime' in key:
            raw_df[value] = raw_df[value].apply(pd.to_datetime)

        elif 'decimal' in key:
            raw_df[value] = raw_df[value].astype(str).apply(lambda x: x.str.replace(',', "")).apply(lambda x: x.apply(Decimal))

    # 4) transformation, step 4: manipulate str dtype target cols
    for key, value in config_dict['str_dtype_cols_manipulation'].items():
        if 'proper_case' in key:
            raw_df[value] = raw_df[value].apply(lambda x: x.str.title())

    # transformation, step 5: select target cols
    transformed_df = raw_df[config_dict['select_cols']]
    
    return raw_df.shape, transformed_df