import os, shutil, logging, sys

from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

from utils import allowed_file
from transformation import perform_transformation


app = Flask(__name__, template_folder='templates')  

app.logger.setLevel(logging.INFO)
log_formatter = logging.Formatter("%(asctime)s|%(name)s|%(levelname)s|%(message)s")
# 10 MiB = 10.485M bytes (10*1024*1024)
rotating_file_handler = RotatingFileHandler('crisp_app.log', maxBytes=10*1024*1024, backupCount=5)
rotating_file_handler.setFormatter(log_formatter)
app.logger.addHandler(rotating_file_handler)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_formatter)
app.logger.addHandler(console_handler)

app.config.from_object('flask_config')

#TODO add in exception handling for two API endpoints

@app.route('/')
def index():
    return render_template('index.html')

# TODO: add exception handling
@app.route('/transform', methods=['GET', 'POST'])
def transform():
    """
    Display transformed results (by uploading an 
    input data .csv and a config .yml).
    ---
    responses:
        200 (GET): Successfully display page for uploading input data files.
        description: 
        200 (POST):
        description: Successfully return transformation results.
        400:
        description: Bad request.
        500:
        description: Internal Server Error: Error in Flask Application code. 
    """
    # error = None
    if request.method == 'POST':
        # # check if post request uploaded input files
        if 'input_data_file' not in request.files or 'crisp_config_yaml_file' not in request.files:
            flash('File upload did not send both input files', 'error')

            return redirect(url_for('transform'))

        input_data_file = request.files["input_data_file"]

        crisp_config_yaml_file = request.files['crisp_config_yaml_file']
        
        # check if both files were uploaded
        if input_data_file.filename == '' or crisp_config_yaml_file.filename == '':
            flash('Two files needed for upload', 'error')
            
            return redirect(url_for('transform'))
        
        # check if input data file extension is .csv
        if not allowed_file(input_data_file.filename, ['csv']):
            flash('Incorrect file extension uploaded. Select new file with extension .csv.', 'error')

            return redirect(url_for('transform'))
        
        # check if input config file extension is .yaml or .yml
        if not allowed_file(crisp_config_yaml_file.filename, ['yaml', 'yml']):
            flash("Incorrect file extension uploaded. Select new file with extension .yml or .yaml.", 'error')

            return redirect(url_for('transform'))
        
        # delete UPLOAD FOLDER and its contents from prior request
        if os.path.exists(app.config['UPLOAD_FOLDER']):
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
             
        raw_df_shape, transformed_df = perform_transformation()

        return render_template('output.html', input_data_file_name=input_data_filename, crisp_config_yaml_file_name=crisp_config_yaml_filename, input_data_file_shape=raw_df_shape, data=transformed_df.head(20).to_html(), transformed_data_shape=transformed_df.shape)
    
    else:
        return render_template('transform.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

