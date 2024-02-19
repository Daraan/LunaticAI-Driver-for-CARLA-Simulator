import sys
import os
import glob

CARLA_ROOT = os.environ.get("CARLA_ROOT")

def import_carla():
    if CARLA_ROOT is None:
        path = os.path.abspath(os.path.join("..","**", 'PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
            sys.version_info.major,
            sys.version_info.minor,
            'win-amd64' if os.name == 'nt' else 'linux-x86_64')))
    else:
        path = os.path.abspath(os.path.join(CARLA_ROOT, 'PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
            sys.version_info.major,
            sys.version_info.minor,
            'win-amd64' if os.name == 'nt' else 'linux-x86_64')))
    try:
        sys.path.append(glob.glob(path)[0])
        print("Appended", sys.path[-1])
        import carla
        return carla
    except IndexError as e:
        print("Cannot find", os.path.abspath(os.path.join("..","**", 'PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
            sys.version_info.major,
            sys.version_info.minor,
            'win-amd64' if os.name == 'nt' else 'linux-x86_64'))))
        pass

print(os.getcwd(), sys.path)
carla = import_carla()