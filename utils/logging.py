import datetime
import os


def log(text: str):
    logging = (os.getenv('SHOW_LOGS') == "true") | False
    if logging:
        print(datetime.datetime.now(), text)
