"""
Sets up a custom :py:mod:`logging.Logger <logging>` for the project.
:python:`from agents.tools.logging import logger` can be used to access the logger.
"""

import datetime
import logging
import os
from typing import Optional

USE_HYDRA_IF_POSSIBLE = True
"""
If :python:`True` and Hydra_ is available, :py:func:`make_logger` will
return only a simple logger with just the name set.
"""

DEFAULT_NAME = "__main__"

TRACE = 5
"""Logging value below :py:obj:`logging.DEBUG`"""

def log(text: str):
    """
    .. deprecated::
        use :py:obj:`logger` instead
        
    :meta private:
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

def make_logger(name: Optional[str] = None, level: int = logging.DEBUG) -> logging.Logger:
    """
    Create a logger object with the specified name and log level.
    If :py:obj:`USE_HYDRA_IF_POSSIBLE` is :python:`True` and the `hydra <https://hydra.cc/>`_
    package is installed, this function will return a simple :py:class:`logging.Logger` with only
    the **name** set.
    Otherwise it will create a logger that is formatted based on :code:`_setup_logger`
    from this file.
    
    Parameters:
        name: The name of the logger. Defaults to "__main__".
        level: The log level for the logger. Defaults to :py:attr:`logging.DEBUG`.
    
    Returns:
        The logger object.
    """
    if not name:
        name = DEFAULT_NAME
    if USE_HYDRA_IF_POSSIBLE:
        try:
            import hydra          # type: ignore # noqa
            hydra_logging = True
        except ImportError:
            hydra_logging = False
    else:
        hydra_logging = False
        
    if hydra_logging:
        return logging.getLogger(DEFAULT_NAME)
    return _setup_logger(name, level)

logger: logging.Logger = make_logger()
"""
A constant logger object that can be imported and used throughout the project.
"""
