"""
This script is used to import the carla module from the `.egg` file.

Please set the `CARLA_ROOT` environment variable to the root directory of the CARLA installation.
"""

import os
from pathlib import Path
import sys

CARLA_ROOT = os.environ.get("CARLA_ROOT")
FILE_NAME = 'PythonAPI/carla/dist/carla-*{major}.{minor}-{syst}.egg'.format(
            major=sys.version_info.major,
            minor=sys.version_info.minor,
            syst='win-amd64' if os.name == 'nt' else 'linux-x86_64')


def import_carla():
    """
    Can import the carla module from the `.egg` file if it
    is not installed in the python environment. Set the
    :py:obj:`CARLA_ROOT` environment variable to the root directory
    of the CARLA installation.
    """
    if CARLA_ROOT is None:
        # Best guess, like in carla examples
        path = Path("..") / "**"
        eggs = list(path.glob(FILE_NAME))
    else:
        path = Path(CARLA_ROOT)
    eggs = list(path.glob(FILE_NAME))
    if len(eggs) == 0:
        print("ERROR: Cannot find", (path / FILE_NAME).resolve())
        return None
    if len(eggs) > 1:
        print("WARNING: Found multiple eggs, choosing last one by string. If you are using CARLA 0.10+ add the .egg file to your PYTHONPATH.")
        egg_path = max(eggs)
    else:
        egg_path = eggs[0]
    try:
        sys.path.append(str(egg_path))
        print("Appended to sys path:", sys.path[-1])
        import carla  # pylint: disable=import-outside-toplevel, redefined-outer-name # noqa: PLC0415
    except IndexError:
        print("ERROR: Cannot find", (Path("..") / "**" / FILE_NAME).resolve())
        return None
    else:
        return carla


carla = import_carla()
