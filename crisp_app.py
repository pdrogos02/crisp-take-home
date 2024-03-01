import os, shutil

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

from utils import allowed_file
from crisp_transformation import perform_transformation

# app = Flask(__name__, static_url_path='/static', template_folder='templates')  
app = Flask(__name__, template_folder='templates')  

app.config.from_object('flask_config')

#TODO add in exception handling for two API endpoints

@app.route('/')
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
        raw_df_shape, transformed_df = perform_transformation()

        return render_template('output.html', input_data_file_name=input_data_filename, crisp_config_yaml_file_name=crisp_config_yaml_filename, input_data_file_shape=raw_df_shape, data=transformed_df.head(20).to_html(), transformed_data_shape=transformed_df.shape)
    
    else:
        return render_template('transform.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

