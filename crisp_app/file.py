import os, shutil

from flask import (
    Blueprint, flash, current_app, redirect, render_template, request, url_for
)

from werkzeug.utils import secure_filename

from crisp_app.utils import allowed_file

bp = Blueprint('file', __name__, url_prefix='/file')

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Upload two input files for transformation, i.e. 
    input data .csv and a config .yml.
    ---
    responses:
        200 (GET): Display page for uploading input data files.
        description: 
        200 (POST):
        description: Successful file upload message.
        400:
        description: Bad request.
        500:
        description: Internal Server Error: Error in Flask Application code. 
    """
    if request.method == 'POST':
        # # check if post request uploaded input files
        if 'input_data_file' not in request.files or 'crisp_config_yaml_file' not in request.files:
            flash('File upload did not send both input files', 'error')

            return redirect(url_for('file.upload'))

        input_data_file = request.files["input_data_file"]

        crisp_config_yaml_file = request.files['crisp_config_yaml_file']
        
        # check if both files were uploaded
        if input_data_file.filename == '' or crisp_config_yaml_file.filename == '':
            flash('Two files needed for upload', 'error')
            
            return redirect(url_for('file.upload'))
        
        # check if input data file extension is .csv
        if not allowed_file(input_data_file.filename, ['csv']):
            flash('Incorrect file extension uploaded. Select new file with extension .csv.', 'error')

            return redirect(url_for('file.upload'))
        
        # check if input config file extension is .yaml or .yml
        if not allowed_file(crisp_config_yaml_file.filename, ['yaml', 'yml']):
            flash("Incorrect file extension uploaded. Select new file with extension .yml or .yaml.", 'error')

            return redirect(url_for('file.upload'))
        
        # delete UPLOAD FOLDER and its contents from prior request
        if os.path.exists(current_app.config['UPLOAD_FOLDER']):
            shutil.rmtree(current_app.config['UPLOAD_FOLDER'])

        # create UPLOAD_FOLDER to store request contents
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        crisp_config_yaml_filename = secure_filename(crisp_config_yaml_file.filename)

        crisp_config_yaml_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], crisp_config_yaml_filename))

        input_data_filename = secure_filename(input_data_file.filename)

        with open(os.path.join(current_app.config['UPLOAD_FOLDER'], input_data_filename), 'ab') as fp:
            chunk_size = 4096

            while True:
                chunk = input_data_file.read(chunk_size)

                if not chunk:
                    break

                fp.write(chunk)
        
        return render_template('file/success.html', input_data_file_name=input_data_filename, crisp_config_yaml_file_name=crisp_config_yaml_filename)

    else:
        return render_template('file/upload.html')
    