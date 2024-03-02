import os

from flask import (
    Blueprint, current_app, render_template, request
)

from werkzeug.utils import secure_filename

from crisp_app.transformation import perform_transformation, read_input_data, read_input_config

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/transform', methods=['GET', 'POST'])
def transform():
    """
    Submit transformation request using previously-uploaded input files (i.e.
    input data .csv and a config .yml).
    ---
    responses:
        200 (GET):  Display transformation request.
        description: 
        200 (POST):
        description: Display transformation results.
        400:
        description: Bad request.
        500:
        description: Internal Server Error: Error in Flask Application code. 
    """
    if request.method == 'POST':
        crisp_config_yaml_filename = ''.join([file_name for file_name in os.listdir(current_app.config['UPLOAD_FOLDER']) if '.yml' in file_name or '.yaml' in file_name])

        input_data_filename = ''.join([file_name for file_name in os.listdir(current_app.config['UPLOAD_FOLDER']) if '.csv' in file_name])

        config_dict = read_input_config(os.path.join(current_app.config['UPLOAD_FOLDER'], crisp_config_yaml_filename))

        raw_df = read_input_data(os.path.join(current_app.config['UPLOAD_FOLDER'], input_data_filename))
        
        raw_df_shape, transformed_df = perform_transformation(config_dict, raw_df)
        
        return render_template('data/output.html', input_data_file_shape=raw_df_shape, transformed_data_shape=transformed_df.shape, data=transformed_df.head(20).to_html())

    else:
        crisp_config_yaml_filename = ''.join([file_name for file_name in os.listdir(current_app.config['UPLOAD_FOLDER']) if '.yml' in file_name or '.yaml' in file_name])

        input_data_filename = ''.join([file_name for file_name in os.listdir(current_app.config['UPLOAD_FOLDER']) if '.csv' in file_name])

        return render_template('data/transform.html', input_data_file_name=input_data_filename, crisp_config_yaml_file_name=crisp_config_yaml_filename)