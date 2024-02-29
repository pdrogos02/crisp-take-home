import io, yaml, os, shutil

import pandas as pd
from contextlib import redirect_stderr
from decimal import Decimal

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

from utils import get_logger, create_new_col, allowed_file

# from crisp_transformation import execute_transformation

# app = Flask(__name__, template_folder='templates')

app = Flask(__name__, static_url_path='/static', template_folder='templates')  

app.config.from_object('flask_config')

#TODO add in exception handling for two API endpoints


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# TODO: add exception handling
@app.route('/transform', methods=['GET', 'POST'])
def transform():
    # error = None
    if request.method == 'POST':
        # # check if post request uploaded input files
        # if 'input_data_file' not in request.files or 'config_yaml_file' not in request.files:
        #     flash('File upload did not send both input files', 'error')
        #     # return redirect(request.url)
        #     return redirect(url_for('transform'))
        #     # error = 'File upload did not send both input files'
        #     # return redirect(url_for('transform.html'))
        #     # return render_template('transform.html')

        input_data_file = request.files["input_data_file"]

        crisp_config_yaml_file = request.files['crisp_config_yaml_file']
        
        if input_data_file.filename == '' or crisp_config_yaml_file.filename == '':
            flash('Two files needed for upload', 'error')
            
            return redirect(url_for('transform'))
                
        if not allowed_file(input_data_file.filename, ['csv']):
            flash('Incorrect file extension uploaded. Select new file with extension .csv.', 'error')

            return redirect(url_for('transform'))
        
        if not allowed_file(crisp_config_yaml_file.filename, ['yaml', 'yml']):
            flash("Incorrect file extension uploaded. Select new file with extension .yml or .yaml.", 'error')

            return redirect(url_for('transform'))
        
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            # delete UPLOAD FOLDER and its contents from prior request
            shutil.rmtree(app.config['UPLOAD_FOLDER'])

        # create UPLOAD_FOLDER to store request contents
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])


        crisp_config_yaml_filename = secure_filename(crisp_config_yaml_file.filename)

        crisp_config_yaml_file.save(os.path.join(app.config['UPLOAD_FOLDER'], crisp_config_yaml_filename))

       

        input_data_filename = secure_filename(input_data_file.filename)

        with open(os.path.join(app.config['UPLOAD_FOLDER'], input_data_filename), 'ab') as fp:
            chunk_size = 4096

            while True:
                chunk = input_data_file.read(chunk_size)

                if not chunk:
                    break

                fp.write(chunk)

        #TODO need to modularize below code 
        # beginning of transformation code
        try:
            logger = get_logger()

        except Exception as e:
            raise e
    
        try:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], crisp_config_yaml_filename), "r") as file:
                config_dict = yaml.safe_load(file)

        except Exception as e:
            logger.error(f'Unable to read in config file: {e}')

            raise e
        
        f = io.StringIO()

        # can use file-like object in memory to avoid saving file
        with redirect_stderr(f):
            # raw_df = pd.read_csv(request.files.get('input_data_file'), on_bad_lines='warn', encoding='utf8')
            raw_df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], input_data_filename), on_bad_lines='warn')

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
        
        # return render_template('success.html', crisp_config_yaml_file_name=crisp_config_yaml_filename, input_data_file_name=input_data_filename)
        # return render_template('output.html',  name='Transformed Data', input_data_file_name= input_data_filename, crisp_config_yaml_file_name=crisp_config_yaml_filename, input_data_file_shape=raw_df.shape, data=transformed_df.to_html())
    
        return render_template('success.html')
    
        # return redirect(url_for('success'))
    
    else:
        return render_template('transform.html')
    

# @app.route('/transform2', methods=['GET', 'POST'])
# def transform():
#     if request.method == 'POST':
#         pass

#     else:
#         return render_template('transform.html')

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

