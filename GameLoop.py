import threading
import time

import carla

from CarlaFunctions import *
from DataGathering.informationUtils import get_all_road_lane_ids
from DataGathering.matrix_wrap import get_car_coords
from DataGathering.run_matrix import DataMatrix
from utils.Camera import camera_function

vehicles = []


def main():
    global client, i_car, j_car, vehicles
    # Usage of functions from CarlaFunctions.py
    # Initialize the Carla service
    carla_service = initialize_carla_service()

    # Set up the world
    world, world_map = setup_world(carla_service)

    # Prepare vehicles
    ego_bp, car_bp, driver1, spawn_points, rule_interpreter = prepare_vehicles(world)

    # Spawn vehicles
    ego = spawn_vehicles(world, ego_bp, car_bp)

    # Assign drivers
    ego_vehicle = assign_drivers(carla_service, ego, driver1)

    # Spawn traffic
    vehicles, tm = spawn_traffic(world, car_bp, spawn_points, driver1, ego_vehicle)

    # Initialize loop variables
    world.tick()
    road_lane_ids = get_all_road_lane_ids(world_map=world.get_map())
    t_end = time.time() + 10000
    i_car, j_car = 0, 0

    # Create a thread for the camera functionality
    camera_thread = threading.Thread(target=camera_function, args=(ego_vehicle, world))
    camera_thread.start()

    # Initialize matrix thread
    data_matrix = DataMatrix(ego_vehicle, world, world_map, road_lane_ids)

    while time.time() < t_end:
        try:
            # matrix = wrap_matrix_functionalities(ego_vehicle, world, world_map, road_lane_ids)

            # Retrieve the latest matrix from the matrix thread
            matrix = data_matrix.getMatrix()

            if matrix is None:
                # time.sleep(0.1)
                continue

            # print(matrix)
            ego_location = ego_vehicle.get_location()
            ego_waypoint = world_map.get_waypoint(ego_location)

            (i_car, j_car) = get_car_coords(matrix)

            results = rule_interpreter.execute_all_functions(driver1, matrix, i_car, j_car, tm)

            if any(results.values()):
                continue

        except Exception as e:
            print(e.__str__())

    input("press any key to end...")
    data_matrix.stop()
    camera_thread.join()


if __name__ == '__main__':
    try:
        main()
    finally:
        try:
            client.apply_batch([carla.command.DestroyActor(x.actor) for x in vehicles])
        except NameError:
            # Should be client not defined
            pass
