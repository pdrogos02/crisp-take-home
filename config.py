from flask.helpers import get_root_path

class Config(object):
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = 'uploads/'
    
class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SECRET_KEY = '9\xde)\xcb\xc9\x1f{1lg/c\xb8\xe8\xd3\xe71\xda\xee||\xf0=\xba'

class TestingConfig(Config):
    TESTING = True
    ROOT_PATH = get_root_path('crisp-take-home')