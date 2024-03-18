import datetime
import os

USE_HYDRA_IF_POSSIBLE = True

def log(text: str):
    logging = (os.getenv('SHOW_LOGS') == "true") | False
    if logging:
        print(datetime.datetime.now(), text)

import logging
def _make_own_logger(name="__main__"):
    # todo: use conf/logger dict config.
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # NOTE: un-comment a line to adjust the format
    form  = ("" 
    #+ "/////////////////////////\n"                          # When using multiple lines, e.g. for full path
    + "[%(levelname)s][%(filename)s:%(lineno)d, %(funcName)s]: %(message)s" # note blank space before filename for IDE support
    #+ "\nin %(pathname)s %(lineno)d, %(funcName)s"
    #+ "\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\" # escaping so double the characters
    )

    formatter = logging.Formatter(form)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

def make_logger(name="__main__"):
    if USE_HYDRA_IF_POSSIBLE:
        try:
            import hydra
            hydra_logging = True
        except ImportError:
            hydra_logging = False
    else:
        hydra_logging = False
        
    if hydra_logging:
        return logging.getLogger("__main__")
    return _make_own_logger(name)

logger = make_logger()