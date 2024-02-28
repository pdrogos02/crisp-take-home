import warnings, json, io, yaml

import pandas as pd
from contextlib import redirect_stderr
from decimal import Decimal

from flask import Flask, render_template, request, flash

from utils import get_logger, create_new_col

# from crisp_transformation import execute_transformation

# UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'csv', 'yml', 'yaml'}

app = Flask(__name__, template_folder='templates')

#TODO add in exception handling for two API endpoints

@app.route('/')
def index():
    return render_template('index.html')

# TODO: add exception handling
@app.route('/transform_crisp_data', methods=['GET', 'POST'])
def transform():
    if request.method == 'POST':
        # # check if post request uploaded input files
        # if 'input_data_file' not in request.files or 'config_yaml_file' not in request.files:
        #     flash("Input file upload did not send both files")

        # input_data_file = request.files["input_data_file"]

        # config_yaml_file = request.files["config_yaml_file"]

        # if input_data_file.filename == '' or config_yaml_file.filename == '':
        #     flash("Need to upload both files")

        try:   
            logger = get_logger()

        except Exception as e:
            raise e

        try:
            # can use file-like object in memory to avoid saving file
            config_dict = yaml.safe_load(request.files.get('config_yaml_file'))

        except Exception as e:
            logger.error(f'Unable to read in config file: {e}')

            raise e
        
        f = io.StringIO()

        # can use file-like object in memory to avoid saving file
        with redirect_stderr(f):
            raw_df = pd.read_csv(request.files.get('input_data_file'), on_bad_lines='warn', encoding='utf8')

        if f.getvalue():
            logger.warning(f"Reading input data lines - bad line(s): \n{f.getvalue()}")

        try:
            # transformation, step 1: rename cols
            raw_df = raw_df.rename(columns=config_dict['renamed_cols'])

            # transformation, step 2: create new cols
            for key, value in config_dict['new_cols'].items():
                raw_df = create_new_col(raw_df, key, value)

            # transformation, step 3: convert col dtypes
            for key, value in config_dict['dtype_cols'].items():
                if 'int' in key or 'str' in key:
                    raw_df[value] = raw_df[value].astype(key)
                
                elif 'datetime' in key:
                    raw_df[value] = raw_df[value].apply(pd.to_datetime)

                elif 'decimal' in key:
                    raw_df[value] = raw_df[value].apply(lambda x: x.str.replace(',', "")).apply(lambda x: x.apply(Decimal))

            # 4) transformation, step 4: manipulate str col dtypes
            for key, value in config_dict['str_dtype_cols_manipulation'].items():
                if 'proper_case' in key:
                    raw_df[value] = raw_df[value].apply(lambda x: x.str.title())

            # final df displayed as html
            transformed_df = raw_df[['OrderId', 'OrderDate', 'ProductId', 'ProductName', 'Quantity', 'Unit']]

        except Exception as e:
            logger.error(f"Error in transforming data: {e}")

            raise e

        return render_template('transform.html',  name='Transformed Data', data=transformed_df.to_html())
    
    else:
        return render_template('upload.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

