# run with python -i 
import glob
import os
import sys
try:
    os.chdir("../useful_scripts")
except FileNotFoundError:
    os.chdir("useful_scripts")

print(os.getcwd())
sys.path.append(os.getcwd())

CARLA_ROOT = os.environ.get("CARLA_ROOT", "./")

try:
    sys.path.append(glob.glob(os.path.join(CARLA_ROOT, "PythonAPI", "carla", "dist",'carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64')))[0])
    print("Using .egg file")
except IndexError:
    print("Trying to use carla installation")
    pass

import carla
import utils, highway_example


client = carla.Client('localhost', 2000)

# Once we have a client we can retrieve the world that is currently
# running.
# client.load_world(town)
world = client.get_world()

town = world.get_map()
spawn_points = town.get_spawn_points()

blueprint_library = world.get_blueprint_library()
car_blueprint = blueprint_library.filter('vehicle')[0]

highway_example.spawn_cars()

