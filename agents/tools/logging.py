import datetime
import os


def log(text: str):
    logging = (os.getenv('SHOW_LOGS') == "true") | False
    if logging:
        print(datetime.datetime.now(), text)


import logging
logger = logging.getLogger("LunaticAI")
logger.setLevel(logging.DEBUG)

# NOTE: un-comment a line to adjust the format
form  = ("" 
#+ "/////////////////////////\n"                          # When using multiple lines, e.g. for full path
+ "[%(levelname)s] %(filename)s, line %(lineno)d, %(funcName)s : %(message)s" # note blank space before filename for IDE support
#+ "\nin %(pathname)s %(lineno)d, %(funcName)s"
#+ "\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\" # escaping so double the characters
)

formatter = logging.Formatter(form)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger.addHandler(handler)