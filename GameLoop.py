import random
import threading
import time
from asyncio import Queue

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

    driver1 = Driver("config/insane_driver.json", traffic_manager=client)
    driver2 = Driver("config/aggressive_driver.json", traffic_manager=client)
    driver3 = Driver("config/default_driver.json", traffic_manager=client)
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

            # random brake check
            brake_check_choice = random.randint(1, 100)
            if (brake_check_choice <= driver1.brake_check_chance
                    and (matrix[i_car][j_car - 1] == 2)
            ):
                driver1.vehicle.actor.set_autopilot(False)
                driver1.vehicle.setThrottle(0)
                driver1.vehicle.setBrake(10)
                time.sleep(1.0)
                print("Brake check")
                driver1.vehicle.setBrake(0)
                driver1.vehicle.actor.set_autopilot(True)

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
            client.apply_batch([carla.command.DestroyActor(x.actor) for x in vehicles])
        except NameError:
            # Should be client not defined
            pass
