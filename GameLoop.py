import threading
import time

import carla

from DataGathering.informationUtils import get_all_road_lane_ids
from DataGathering.matrix_wrap import get_car_coords
from DataGathering.run_matrix import DataMatrix
from VehicleSpawning.vehicle_spawner import VehicleSpawner
from utils.Camera import camera_function

spawner = None
vehicles = []


def main():
    global spawner, vehicles

    # Initialise the class for vehicle spawning
    spawner = VehicleSpawner('VehicleSpawning/config/vehicle_spawn.yaml')
    spawner.initialize_carla_service()
    world, world_map = spawner.setup_world()
    ego_bp, car_bp, driver1, spawn_points, rule_interpreter = spawner.prepare_vehicles(world)

    # Spawn vehicles and assign drivers
    ego = spawner.spawn_vehicles(world, ego_bp, spawn_points)
    ego_vehicle = spawner.assign_drivers(ego, driver1)

    # Spawn traffic
    vehicles, tm = spawner.spawn_traffic(world, car_bp, spawn_points, driver1, ego.vehicle)

    # Initialize loop variables
    world.tick()
    road_lane_ids = get_all_road_lane_ids(world_map=world.get_map())
    t_end = time.time() + 10000

    # Create a thread for the camera functionality
    camera_thread = threading.Thread(target=camera_function, args=(ego_vehicle, world))
    camera_thread.start()

    # Initialize matrix thread
    data_matrix = DataMatrix(ego_vehicle, world, world_map, road_lane_ids)

    while time.time() < t_end:
        try:
            pass
            # Retrieve the latest matrix from the matrix thread
            matrix = data_matrix.getMatrix()

            if matrix is None:
                continue

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
            if spawner and spawner.client:
                spawner.client.apply_batch([carla.command.DestroyActor(x.actor) for x in vehicles])
        except NameError:
            pass
