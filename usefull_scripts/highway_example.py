# see https://carla.readthedocs.io/en/latest/core_map/#changing-the-map


import glob
import os
import sys
import pandas as pd

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
import utils

def destroy():
    client.apply_batch([carla.command.DestroyActor(x) for x in vehicles])

client = carla.Client('localhost', 2000)

if len(sys.argv) > 1:
    town = sys.argv[1]
else:
    town = 'Town04' # maybe 'Town04_Opt'

# Once we have a client we can retrieve the world that is currently
# running.
world = client.load_world(town)
town = world.get_map()

blueprint_library = world.get_blueprint_library()
car_blueprint = blueprint_library.filter('vehicle')[0]

if car_blueprint.has_attribute('color'):
    color = car_blueprint.get_attribute('color').recommended_values[-1]
    car_blueprint.set_attribute('color', color)

ego_bp = world.get_blueprint_library().find('vehicle.lincoln.mkz_2020')
if ego_bp.has_attribute('color'):
    color = ego_bp.get_attribute('color').recommended_values[0]
    ego_bp.set_attribute('color', "255,0,0")

ego_bp.set_attribute('role_name', 'hero')

# Spawn

#spawn_points = town.get_spawn_points()

spawn_points = utils.csv_to_transformations("highway_example_car_positions.csv")

vehicles = []

def destroy():
    client.apply_batch([carla.command.DestroyActor(x) for x in vehicles])

ego_spawn = spawn_points[0]
ego = world.spawn_actor(ego_bp, ego_spawn)
vehicles.append(ego)

# other npcs
#for idx in [115, 243, 116]:
#    v = world.spawn_actor(car_blueprint, spawn_points[idx])
#    vehicles.append(v)

for dist in [20, -40]:
    v = world.spawn_actor(car_blueprint, 
                          Transform(ego_spawn.location + Vector3D(dist), ego_spawn.rotation))
    vehicles.append(v)


def destroy():
    client.apply_batch([carla.command.DestroyActor(x) for x in vehicles])
