import warnings, json, io, yaml

import pandas as pd
from contextlib import redirect_stderr
from decimal import Decimal

from flask import Flask, render_template, request, redirect

from utils import get_logger, create_new_col

# from crisp_transformation import execute_transformation

# UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'csv', 'yml', 'yaml'}

app = Flask(__name__, template_folder='templates')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#TODO add in exception handling for two API endpoints

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_data', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        raw_df = pd.read_csv(request.files.get('input_data_file'))

        return render_template('upload.html', shape=raw_df.shape)
    
    return render_template('upload.html')

# TODO: add exception handling
@app.route('/transform', methods=["POST"])
def transform():
    logger = get_logger()

    try:
        # can use file-like object in memory to avoid saving file
        with open(request.files.get('config_yaml_file'), "r") as file:
            config_dict = yaml.safe_load(file)

    except Exception as e:
        logger.error(f'Unable to read in config file: {e}')

        raise Exception(f'Unable to read in config file: {e}')
    
    f = io.StringIO()

    # can use file-like object in memory to avoid saving file
    with redirect_stderr(f):
        raw_df = pd.read_csv(request.files.get('input_data_file'), on_bad_lines='warn', encoding='utf8')

    if f.getvalue():
        logger.warning(f"Reading input data lines - bad line(s): \n{f.getvalue()}")

    try:
        # transformation, step 1) rename cols
        raw_df = raw_df.rename(columns=config_dict['renamed_cols'])

        # transformation, step 2) create new cols
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

        transformed_df = raw_df[['OrderId', 'OrderDate', 'ProductId', 'ProductName', 'Quantity', 'Unit']]

    except Exception as e:
        logger.error(f"Error in transforming data: {e}")

        raise Exception(f"Error in transforming data: {e}")

    return render_template('transform.html',  tables=[transformed_df.to_html(classes='data')], titles=transformed_df.columns.values)
    
# @app.route('/hello/', methods=['GET', 'POST'])
# def welcome():
#     return "Hello World!"

# @app.route('/crisp_transformation/', methods=['POST'])
# def execute_transformation():
#     execute_transformation()

#     return '', 201, { 'location': f'/crisp_transformation/{employee["id"]}' }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

