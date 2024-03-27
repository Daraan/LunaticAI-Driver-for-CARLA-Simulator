import time

import carla

import launch_tools
from data_gathering.car_detection_matrix.informationUtils import get_all_road_lane_ids, initialize_dataframe, follow_car
from data_gathering.car_detection_matrix.run_matrix import DataMatrix
from classes.carla_service import CarlaService
from classes.driver import Driver
from classes.traffic_manager import TrafficManager
from classes.vehicle import Vehicle

vehicles = []

"""
This does not work, we have some problems with the multithreading, but I do not get why
If someone tries to repair this the problem is in the loop found in the DataMatrix file
"""


def main():
    global client
    carla_service = CarlaService("Town04", "127.0.0.1", 2000)
    client = carla_service.client

    world = carla_service.get_world()
    world_map = world.get_map()
    ego_bp, car_bp = launch_tools.blueprint_helpers.get_contrasting_blueprints(world)

    driver1 = Driver("../config/default_driver.json", traffic_manager=client)

    spawn_points = launch_tools.csv_to_transformations("highway_example_car_positions.csv")

    # Spawn Ego
    ego = Vehicle(world, ego_bp)
    try:
        ego.spawn(spawn_points[0])
    except Exception as e:
        pass

    vehicles.append(ego)
    carla_service.assignDriver(ego, driver1)
    ego_vehicle = ego.actor

    # spawn others
    for sp in spawn_points[1:]:
        v = Vehicle(world, car_bp)
        v.spawn(sp)
        vehicles.append(v)
        ap = TrafficManager(v.actor)
        ap.init_passive_driver()
        ap.start_drive()

    tm = TrafficManager(ego.actor)
    tm.init_lunatic_driver()
    tm.start_drive()

    # Define the radius to search for other vehicles
    radius = 100

    # Initialize speed of ego_vehicle to use as global variable
    world.tick()
    highway_shape = None
    road_lane_ids = get_all_road_lane_ids(world_map=world.get_map())
    df = initialize_dataframe()
    t_end = time.time() + 10

    # Create matrix
    dataMatrix = DataMatrix(ego_vehicle, world)

    while time.time() < t_end:
        try:
            follow_car(ego_vehicle, world)
            matrix = dataMatrix.getMatrix()
            street_type = dataMatrix.getStreetType()
            for i in matrix:
                print(i, matrix[i])
            print(street_type)

            time.sleep(0.5)
            world.tick()

        except Exception as e:
            continue

    input("press any key to end...")


if __name__ == '__main__':
    try:
        main()
    finally:
        try:
            client.apply_batch([carla.command.DestroyActor(x.actor) for x in vehicles])
        except NameError:
            # Should be client not defined
            pass
