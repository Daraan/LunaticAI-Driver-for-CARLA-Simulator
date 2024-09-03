"""
This script is used to import the carla module from the `.egg` file.

Please set the `CARLA_ROOT` environment variable to the root directory of the CARLA installation.
"""

import glob
import os
import sys

CARLA_ROOT = os.environ.get("CARLA_ROOT")
FILE_NAME = 'PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
            sys.version_info.major,
            sys.version_info.minor,
            'win-amd64' if os.name == 'nt' else 'linux-x86_64')

def import_carla():
    """
    Can import the carla module from the `.egg` file if it
    is not installed in the python environment. Set the
    :py:obj:`CARLA_ROOT` environment variable to the root directory
    of the CARLA installation.
    """
    if CARLA_ROOT is None:
        # Best guess
        path = os.path.abspath(os.path.join("..","**", FILE_NAME))
    else:
        path = os.path.abspath(os.path.join(CARLA_ROOT, FILE_NAME))
    try:
        sys.path.append(glob.glob(path)[0])
        print("Appended to sys path:", sys.path[-1])
        import carla  # pylint: disable=import-outside-toplevel, redefined-outer-name
    except IndexError:
        print("ERROR: Cannot find", os.path.abspath(os.path.join("..","**", FILE_NAME)))
        return None
    else:
        return carla

carla = import_carla()
