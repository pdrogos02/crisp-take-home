from typing import List

import pandas as pd

def allowed_file(filename: str, allowed_extensions_list: List[str]) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions_list

def create_new_col(raw_df: pd.DataFrame, key: str, value: List[str]) -> pd.DataFrame:
    if not any(col in value for col in raw_df.columns):
        raw_df[key] = ''.join(map(str, value))
    
    else:
        raw_df[key] = raw_df[value].astype(str).apply('-'.join, axis=1)

    return raw_df





