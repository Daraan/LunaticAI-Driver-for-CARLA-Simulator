import time

import carla
from carla import Vector3D

import utils

TOWN = 'Town04'  # maybe 'Town04_Opt'


def make_client():
    client = carla.Client('localhost', 2000)

    # Once we have a client we can retrieve the world that is currently
    # running.
    world = client.load_world(TOWN)
    return client


# Spawn

# spawn_points = town.get_spawn_points()

vehicles = []


def spawn_cars(client=None):
    global vehicles
    if client is None:
        client = make_client()
    world = client.get_world()
    level = world.get_map()
    ego_bp, car_blueprint = utils.blueprint_helpers.get_contrasting_blueprints(world)
    if ego_bp.has_attribute('color'):
        color = ego_bp.get_attribute('color').recommended_values[0]
        ego_bp.set_attribute('color', "255,0,0")

    ego_bp.set_attribute('role_name', 'hero')

    try:
        spawn_points = utils.csv_to_transformations("highway_example_car_positions.csv")
    except FileNotFoundError:
        spawn_points = utils.csv_to_transformations("examples/highway_example_car_positions.csv")

    ego_spawn = spawn_points[0]
    ego = world.spawn_actor(ego_bp, ego_spawn)
    vehicles.append(ego)

    # other npcs
    for sp in spawn_points[1:]:
        v = world.spawn_actor(car_blueprint, sp)
        vehicles.append(v)
    return vehicles


def apply_constant_velocity(speed=5, to_ego=True):
    cars = vehicles if to_ego else vehicles[1:]
    for v in cars:
        v.enable_constant_velocity(Vector3D(x=speed))
    print("Applied velocity to", len(cars), "cars")


def destroy():
    client.apply_batch([carla.command.DestroyActor(x) for x in vehicles])


if __name__ == "__main__":
    try:
        global client
        client = make_client()
        spawn_cars(client)
        time.sleep(1.5)
        print("adding speed")
        apply_constant_velocity(speed=3, to_ego=True)
        input("Press any key do destroy cars...")
    finally:
        destroy()
