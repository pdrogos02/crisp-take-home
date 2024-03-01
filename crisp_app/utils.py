from typing import List

import pandas as pd

def allowed_file(filename: str, allowed_extensions_list: List[str]) -> bool:
    """
    Returns a Boolean value. 

    Parameters:
            filename (str): file name; e.g. "input_data.csv", "crisp_config.yml"
            allowed_extensions_list (list): a list of allowed file extensions; e.g. csv, yml, yaml

    Returns: 
            (bool): Boolean value (True, False)
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions_list

def create_new_col(raw_df: pd.DataFrame, key: str, value: List[str]) -> pd.DataFrame:
    """
    Returns a Pandas DataFrame containing new, created column. 

    Parameters:
            raw_df (pd.DataFrame): Pandas DataFrame of raw data being transformed.
                                   key (str): key from key:value pair that 
                                   contains new column name
            value (List[str]): value from key:value pair that contains a list of strings 
                               or the value of the new column

    Returns: 
            raw_df (pd.DataFrame): Pandas DataFrame, raw_df, containing the new column and column value
    """
    if not any(col in value for col in raw_df.columns):
        raw_df[key] = ''.join(map(str, value))
    
    else:
        raw_df[key] = raw_df[value].astype(str).apply('-'.join, axis=1)

    return raw_df





