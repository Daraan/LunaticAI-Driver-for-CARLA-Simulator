import glob
import os
import sys
import time
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
from carla import Vector3D
import utils

client = carla.Client('localhost', 2000)

TOWN = 'Town04' # maybe 'Town04_Opt'

# Once we have a client we can retrieve the world that is currently
# running.
world = client.load_world(TOWN)
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

vehicles = []
def spawn_cars():

    spawn_points = utils.csv_to_transformations("highway_example_car_positions.csv")
    ego_spawn = spawn_points[0]
    ego = world.spawn_actor(ego_bp, ego_spawn)
    vehicles.append(ego)

    # other npcs
    for sp in spawn_points[1:]:
        v = world.spawn_actor(car_blueprint, sp)
        vehicles.append(v)

def apply_constant_velocity(speed=5, to_ego=True):
    cars = vehicles if to_ego else vehicles[1:]
    for v in cars:
        v.enable_constant_velocity(Vector3D(x=speed))
    print("Applied velocity to", len(cars), "cars")


def destroy():
    client.apply_batch([carla.command.DestroyActor(x) for x in vehicles])

if __name__ == "__main__":
    try:
        spawn_cars()
        time.sleep(1.5)
        print("adding speed")
        apply_constant_velocity(speed=5, to_ego=True)
        input("Press any key do destroy cars...")
    finally:
        destroy()