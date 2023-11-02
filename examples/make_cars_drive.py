# see https://carla.readthedocs.io/en/latest/core_map/#changing-the-map
import argparse
import glob
import os
import sys

from numpy.random import random

CARLA_ROOT = os.environ.get("CARLA_ROOT", "./")

if len(sys.argv) > 1:
    town = sys.argv[1]
else:
    town = 'Town04'  # maybe 'Town04_Opt'

# try:
#     sys.path.append(glob.glob(os.path.join(CARLA_ROOT, "PythonAPI", "carla", "dist", 'carla-*%d.%d-%s.egg' % (
#         sys.version_info.major,
#         sys.version_info.minor,
#         'win-amd64' if os.name == 'nt' else 'linux-x86_64')))[0])
#     print("Using .egg file")
# except IndexError:
#     print("Trying to use carla installation")
#     pass


import carla

from carla.libcarla import Transform, Vector3D


def destroy():
    client.apply_batch([carla.command.DestroyActor(x) for x in vehicles])


def get_actor_blueprints(world, filter, generation):
    bps = world.get_blueprint_library().filter(filter)

    if generation.lower() == "all":
        return bps

    # If the filter returns only one bp, we assume that this one needed
    # and therefore, we ignore the generation
    if len(bps) == 1:
        return bps

    try:
        int_generation = int(generation)
        # Check if generation is in available generations
        if int_generation in [1, 2]:
            bps = [x for x in bps if int(x.get_attribute('generation')) == int_generation]
            return bps
        else:
            print("   Warning! Actor Generation is not valid. No actor will be spawned.")
            return []
    except:
        print("   Warning! Actor Generation is not valid. No actor will be spawned.")
        return []


client = carla.Client('localhost', 2000)

# Once we have a client we can retrieve the world that is currently
# running.
world = client.load_world(town)
town = world.get_map()
spawn_points = town.get_spawn_points()

blueprint_library = world.get_blueprint_library()
car_blueprint = blueprint_library.filter('vehicle')[0]

if car_blueprint.has_attribute('color'):
    color = car_blueprint.get_attribute('color').recommended_values[-1]
    car_blueprint.set_attribute('color', color)

ego_bp = world.get_blueprint_library().find('vehicle.lincoln.mkz_2020')
if ego_bp.has_attribute('color'):
    color = ego_bp.get_attribute('color').recommended_values[0]
    ego_bp.set_attribute('color', "191,62,255")

ego_bp.set_attribute('role_name', 'hero')

SpawnActor = carla.command.SpawnActor
SetAutopilot = carla.command.SetAutopilot
FutureActor = carla.command.FutureActor

# Traffic Manager
tm = client.get_trafficmanager(8000)

# --------------
# Spawn vehicles
# --------------
vehicles = []

# --------------
# Spawn the ego vehicle
# --------------
ego_spawn = spawn_points[242]
ego = world.spawn_actor(ego_bp, ego_spawn)
vehicles.append(ego)
ego.set_autopilot(True, 8000)

# Define a route or waypoints for the ego vehicle to follow
ego_location = ego_spawn.location

# other npcs
for idx in [115, 243, 116]:
    v = world.spawn_actor(car_blueprint, spawn_points[idx])
    vehicles.append(v)

for dist in [20, -40]:
    v = world.spawn_actor(car_blueprint,
                          Transform(ego_spawn.location + Vector3D(dist), ego_spawn.rotation))
    vehicles.append(v)

input("press any key to end...")
destroy()