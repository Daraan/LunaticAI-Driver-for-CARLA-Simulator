import sys
import os
import glob

CARLA_ROOT = os.environ.get("CARLA_ROOT")
FILE_NAME = 'PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
            sys.version_info.major,
            sys.version_info.minor,
            'win-amd64' if os.name == 'nt' else 'linux-x86_64')

def import_carla():
    if CARLA_ROOT is None:
        # Best guess
        path = os.path.abspath(os.path.join("..","**", ))
    else:
        path = os.path.abspath(os.path.join(CARLA_ROOT, FILE_NAME))
    try:
        sys.path.append(glob.glob(path)[0])
        print("Appended to sys path:", sys.path[-1])
        import carla
        return carla
    except IndexError as e:
        print("Cannot find", os.path.abspath(os.path.join("..","**", FILE_NAME)))
        pass

carla = import_carla()