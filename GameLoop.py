import threading
import time
import random

import carla

from data_gathering.car_detection_matrix.informationUtils import get_all_road_lane_ids
from data_gathering.car_detection_matrix.matrix_wrap import get_car_coords
from data_gathering.car_detection_matrix.run_matrix import AsyncDataMatrix, DataMatrix
from classes.camera_manager import camera_function
from VehicleSpawning.vehicle_spawner import VehicleSpawner

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
    vehicles, tm = spawner.spawn_traffic(world, car_bp, spawn_points, driver1, ego_vehicle)
    # Initialize loop variables
    world.tick()
    road_lane_ids = get_all_road_lane_ids(world_map=world.get_map())
    t_end = time.time() + 10000

    # Create a thread for the camera functionality
    try:
        camera_thread = threading.Thread(target=camera_function, args=(ego_vehicle, world))
        camera_thread.start()

        # Initialize matrix thread
        data_matrix = AsyncDataMatrix(ego_vehicle, world, world_map, road_lane_ids)
        data_matrix.start()

        print("Starting game loop")
        while time.time() < t_end:
            # Retrieve the latest matrix from the matrix thread
            matrix = data_matrix.getMatrix()

            if matrix is None:
                continue

            (i_car, j_car) = get_car_coords(matrix)
            # NEW use RuleInterpreter
            results = rule_interpreter.execute_all_functions(driver1, matrix, i_car, j_car, tm)

            if any(results.values()):
                continue

            # OLD:
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

    finally:
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
