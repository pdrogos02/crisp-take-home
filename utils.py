import json, logging, sys

from logging.handlers import RotatingFileHandler


def get_logger():
    logger = logging.getLogger('data_wrangling_logger')
    
    log_formatter = logging.Formatter("%(asctime)s|%(name)s|%(levelname)s|%(message)s")
    
    # TODO: set logging level to INFO
    logger.setLevel(logging.DEBUG)
    
    # 10 MiB = 10.485M bytes (10*1024*1024)
    rotating_file_handler = RotatingFileHandler('data_wrangling.log', maxBytes=10*1024*1024, backupCount=5)
    
    rotating_file_handler.setFormatter(log_formatter)
    
    logger.addHandler(rotating_file_handler)
    
    console_handler = logging.StreamHandler(sys.stdout)
    
    # TODO: set logging level to INFO
    console_handler.setLevel(logging.DEBUG)
    
    console_handler.setFormatter(log_formatter)
    
    logger.addHandler(console_handler)
    
    return logger





