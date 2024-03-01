import io, yaml, os

from contextlib import redirect_stderr
from decimal import Decimal

import pandas as pd

from crisp_app.utils import get_logger, create_new_col

from flask import current_app, request
from werkzeug.utils import secure_filename


def perform_transformation():
    try:
        logger = get_logger()

    except Exception as e:
        raise e

    crisp_config_yaml_file = request.files['crisp_config_yaml_file']
        
    crisp_config_yaml_filename = secure_filename(crisp_config_yaml_file.filename)

    input_data_file = request.files["input_data_file"]

    input_data_filename = secure_filename(input_data_file.filename)

    try:
        with open(os.path.join(current_app.config['UPLOAD_FOLDER'], crisp_config_yaml_filename), "r") as file:
            config_dict = yaml.safe_load(file)

    except Exception as e:
        logger.error(f'Unable to read in config file: {e}')

        raise e
    
    f = io.StringIO()

    with redirect_stderr(f):
        raw_df = pd.read_csv(os.path.join(current_app.config['UPLOAD_FOLDER'], input_data_filename), on_bad_lines='warn')

    if f.getvalue():
        logger.warning(f"Reading input data lines - bad line(s): \n{f.getvalue()}")

    try:
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
        transformed_df = raw_df[['OrderId', 'OrderDate', 'ProductId', 'ProductName', 'Quantity', 'Unit']]

    except Exception as e:
        logger.error(f"Error in transforming data: {e}")

        raise e
    
    return raw_df.shape, transformed_df