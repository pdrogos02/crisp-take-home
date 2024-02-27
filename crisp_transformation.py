import warnings, json, io
import pandas as pd
from contextlib import redirect_stderr
from decimal import Decimal

from utils import get_logger

def create_new_col(raw_df, key, value):
    if not any(col in value for col in raw_df.columns):
        raw_df[key] = ''.join(map(str, value))
    
    else:
        raw_df[key] = raw_df[value].astype(str).apply('-'.join, axis=1)

    return raw_df

def execute_transformation():
    try:
        logger = get_logger()

    except Exception as e:
        raise Exception(f'Unable to generate logger: {e}')
    
    try:
        with open('transformation_config.json') as f:
            config_dict = json.load(f)
    
    except Exception as e:
        logger.error(f'Unable to read in config file: {e}')

        raise Exception(f'Unable to read in config file: {e}')
    
    f = io.StringIO()

    with redirect_stderr(f):
        raw_df = pd.read_csv(config_dict['input_data_file_path'], on_bad_lines='warn')

    if f.getvalue():
        logger.warning(f"Reading input data lines - bad line(s): \n{f.getvalue()}")

    try:
        # 1) rename cols
        raw_df = raw_df.rename(columns=config_dict['renamed_cols'])

        # 2) create new cols
        for key, value in config_dict['new_cols'].items():
            raw_df = create_new_col(raw_df, key, value)
            
        # 3) dtype conversions
        for key, value in config_dict['dtype_cols'].items():
            if 'int' in key or 'str' in key:
                raw_df[value] = raw_df[value].astype(key)
            
            elif 'datetime' in key:
                raw_df[value] = raw_df[value].apply(pd.to_datetime)

            elif 'decimal' in key:
                raw_df[value] = raw_df[value].apply(lambda x: x.str.replace(',', "")).apply(lambda x: x.apply(Decimal))

        # 4) str dtype conversions
        for key, value in config_dict['str_cols_conversion'].items():
            if 'proper_case' in key:
                raw_df[value] = raw_df[value].apply(lambda x: x.str.title())

        raw_df = raw_df[['OrderId', 'OrderDate', 'ProductId', 'ProductName', 'Quantity', 'Unit']]

    except Exception as e:
        logger.error(f"Error in transforming data: {e}")

        raise Exception(f"Error in transforming data: {e}")

    return

if __name__=="__main__":
    main()