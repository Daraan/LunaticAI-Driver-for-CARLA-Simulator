import sys
import os
import glob

def import_carla():
    try:
        sys.path.append(glob.glob(os.path.abspath(os.path.join("..","**", 'PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
            sys.version_info.major,
            sys.version_info.minor,
            'win-amd64' if os.name == 'nt' else 'linux-x86_64'))))[0])
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