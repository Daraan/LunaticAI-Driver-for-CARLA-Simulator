import random
import threading
import time
from asyncio import Queue

import carla
import utils

from DataGathering.informationUtils import get_all_road_lane_ids
from DataGathering.matrix_wrap import get_car_coords
from DataGathering.run_matrix import DataMatrix
from utils.Camera import camera_function
from VehicleSpawning.vehicle_spawner import VehicleSpawner

spawner = None
vehicles = []

def main():
    global spawner, vehicles
    carlaService = CarlaService("Town04", "127.0.0.1", 2000)

    # Initialise the class for vehicle spawning
    spawner = VehicleSpawner('VehicleSpawning/config/vehicle_spawn.yaml')
    spawner.initialize_carla_service()
    world, world_map = spawner.setup_world()
    ego_bp, car_bp, driver1, spawn_points, rule_interpreter = spawner.prepare_vehicles(world)

    # Spawn vehicles and assign drivers
    ego = spawner.spawn_vehicles(world, ego_bp, spawn_points)
    ego_vehicle = spawner.assign_drivers(ego, driver1)
    driver1 = Driver("config/aggressive_driver.json", traffic_manager=client)

    spawn_points = utils.csv_to_transformations("examples/highway_example_car_positions.csv")
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

            overtake_direction = 0
            # Random lane change
            overtake_choice = random.randint(1, 100)
            if overtake_choice <= driver1.risky_overtake_chance:
                if matrix[i_car + 1][j_car + 1] == 3 and matrix[i_car - 1][j_car + 1] == 3:
                    continue
                elif matrix[i_car + 1][j_car + 1] == 3:
                    tm.force_overtake(100, -1)
                elif matrix[i_car - 1][j_car + 1] == 3:
                    tm.force_overtake(100, 1)
                else:
                    overtake_direction = random.choice([-1, 1])
                    tm.force_overtake(100, overtake_direction)
                print("Random lane change")
                continue

            if matrix[i_car + 1][j_car + 1] == 0:
                # print("can overtake on right")
                overtake_direction = 1
            if matrix[i_car - 1][j_car + 1] == 0:
                # print("can overtake on left")
                overtake_direction = -1

            # Overtake logic
            if matrix[i_car][j_car + 1] == 2 or matrix[i_car][j_car + 2] == 2:
                overtake_choice = random.randint(1, 100)
                if overtake_choice >= driver1.overtake_mistake_chance:
                    tm.force_overtake(100, overtake_direction)
                    print("overtake!")
                    continue
                else:
                    print("overtake averted by chance")

            # brake logic
            if matrix[i_car][j_car + 1] == 2:
                driver1.vehicle.setBrake(4)

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
