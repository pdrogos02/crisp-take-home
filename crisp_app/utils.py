import logging, sys

from logging.handlers import RotatingFileHandler

def allowed_file(filename, allowed_extensions_list):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions_list

def create_new_col(raw_df, key, value):
    if not any(col in value for col in raw_df.columns):
        raw_df[key] = ''.join(map(str, value))
    
    else:
        raw_df[key] = raw_df[value].astype(str).apply('-'.join, axis=1)

    return raw_df

def get_logger():
    logger = logging.getLogger('crisp_app_logger')
    
    log_formatter = logging.Formatter("%(asctime)s|%(name)s|%(levelname)s|%(message)s")
    
    # TODO: set logging level to INFO
    logger.setLevel(logging.DEBUG)
    
    # 10 MiB = 10.485M bytes (10*1024*1024)
    rotating_file_handler = RotatingFileHandler('crisp_app.log', maxBytes=10*1024*1024, backupCount=5)
    
    rotating_file_handler.setFormatter(log_formatter)
    
    logger.addHandler(rotating_file_handler)
    
    console_handler = logging.StreamHandler(sys.stdout)
    
    # TODO: set logging level to INFO
    console_handler.setLevel(logging.DEBUG)
    
    console_handler.setFormatter(log_formatter)
    
    logger.addHandler(console_handler)
    
    return logger





