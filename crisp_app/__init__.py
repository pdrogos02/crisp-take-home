import os
from flask import Flask, render_template 


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('flask_config.py', silent=True)

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