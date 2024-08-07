import os
import logging
import datetime

USE_HYDRA_IF_POSSIBLE = True
"""
If :python:`True` and Hydra_ is available, :py:func:`make_logger` will
return only a simple logger with just the name set.
"""

TRACE = 5
"""Logging value below :py:attr:`logging.DEBUG`"""

def log(text: str):
    """
    .. deprecated::
        use :py:obj:`logger` instead
    """
    logging = (os.getenv('SHOW_LOGS') == "true") | False
    if logging:
        print(datetime.datetime.now(), text)

def _setup_logger(name : str ="__main__", level : int = logging.DEBUG):
    """Backup when Hydra_ is not available."""
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
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

def make_logger(name: str = "__main__", level: int = logging.DEBUG) -> logging.Logger:
    """
    Create a logger object with the specified name and log level.
    If :py:obj:`USE_HYDRA_IF_POSSIBLE` is True and the :code:`hydra <https://hydra.cc/>`_
    package is installed, this function will return a simple variant with only
    the **name** set.
    Otherwise it will create a logger that is formatted based on :code:`_setup_logger`
    from this file.
    
    Parameters:
        name : The name of the logger. Defaults to "__main__".
        level : The log level for the logger. Defaults to :py:attr:`logging.DEBUG`.
    
    Returns:
        logging.Logger: The logger object.
    """
    if USE_HYDRA_IF_POSSIBLE:
        try:
            import hydra          # type: ignore
            hydra_logging = True
        except ImportError:
            hydra_logging = False
    else:
        hydra_logging = False
        
    if hydra_logging:
        return logging.getLogger("__main__")
    return _setup_logger(name, level)

logger = make_logger()