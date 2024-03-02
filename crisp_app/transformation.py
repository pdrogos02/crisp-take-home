import io, yaml, os

from contextlib import redirect_stderr
from decimal import Decimal
import pandas as pd
from typing import Dict, List
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

def create_target_cols(config_dict: Dict[str, dict], raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns Pandas Dataframe, raw_df, with new target columns

    Parameters: 
            config_dict (Dict[str, dict]): a dict containing transformation config key:value pairs
            raw_df (pd.DataFrame): a Pandas DataFrame containing raw data from uploaded input data file

    Returns: 
            raw_df (pd.DataFrame): Pandas DataFrame, raw_df 
    """
    for key, value in config_dict['new_cols'].items():
        raw_df = create_new_col(raw_df, key, value)

    return raw_df

def rename_target_cols(config_dict: Dict[str, dict], raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns Pandas Dataframe, raw_df, with renamed target columns

    Parameters: 
            config_dict (Dict[str, dict]): a dict containing transformation config key:value pairs
            raw_df (pd.DataFrame): a Pandas DataFrame containing raw data from uploaded input data file

    Returns: 
            raw_df (pd.DataFrame): Pandas DataFrame, raw_df 
    """
    raw_df = raw_df.rename(columns=config_dict['renamed_cols'])

    return raw_df

def convert_target_cols_dtypes(config_dict: Dict[str, dict], raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns Pandas Dataframe, raw_df, with converted target columns' dtypes

    Parameters: 
            config_dict (Dict[str, dict]): a dict containing transformation config key:value pairs
            raw_df (pd.DataFrame): a Pandas DataFrame containing raw data from uploaded input data file

    Returns: 
            raw_df (pd.DataFrame): Pandas DataFrame, raw_df 
    """
    for key, value in config_dict['dtype_cols'].items():
        if 'int' in key or 'str' in key:
            raw_df[value] = raw_df[value].astype(key)
        
        elif 'datetime' in key:
            raw_df[value] = raw_df[value].apply(pd.to_datetime)

        elif 'decimal' in key:
            raw_df[value] = raw_df[value].astype(str).apply(lambda x: x.str.replace(',', "")).apply(lambda x: x.apply(Decimal))

    return raw_df

def manipulate_str_dtype_target_cols(config_dict: Dict[str, dict], raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns Pandas Dataframe, raw_df, with manipulated str dtype target cols

    Parameters: 
            config_dict (Dict[str, dict]): a dict containing transformation config key:value pairs
            raw_df (pd.DataFrame): a Pandas DataFrame containing raw data from uploaded input data file

    Returns: 
            raw_df (pd.DataFrame): Pandas DataFrame, raw_df 
    """
    for key, value in config_dict['str_dtype_cols_manipulation'].items():
        if 'proper_case' in key:
            raw_df[value] = raw_df[value].apply(lambda x: x.str.title())

    return raw_df

def select_target_cols(config_dict: Dict[str, dict], raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns Pandas Dataframe, transformed_df, with selected target columns from raw_df

    Parameters: 
            config_dict (Dict[str, dict]): a dict containing transformation config key:value pairs
            raw_df (pd.DataFrame): a Pandas DataFrame containing raw data from uploaded input data file

    Returns: 
            transformed_df (pd.DataFrame): Pandas DataFrame, transformed_df 
    """
    transformed_df = raw_df[config_dict['select_cols']]
    
    return transformed_df