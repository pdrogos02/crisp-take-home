import os, logging, sys

from flask import Flask, render_template 
from logging.handlers import RotatingFileHandler

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # flask logger 
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

    # NOTE: prior to executing app
    # "flask --app crisp_app run"
    # export the following environment variable, CONFIG_CLASS via the terminal using
    # "export FLASK_ENV=<environment>"
    # examples of <environment>: production, development, staging
    app.config.from_envvar('FLASK_CONFIG')

    app.config.from_object(f"config.{os.environ.get('FLASK_ENV').capitalize()}Config")

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config', silent=True)    

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    @app.route('/')
    def index():
        return render_template('index.html')
    
    from . import data
    app.register_blueprint(data.bp)

    from . import file
    app.register_blueprint(file.bp)

    return app