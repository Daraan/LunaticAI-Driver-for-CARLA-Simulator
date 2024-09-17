import __allow_imports_from_root # noqa # type: ignore

import threading
import time
import random

import carla

from classes._data_gathering.car_detection_matrix.informationUtils import get_all_road_lane_ids
from classes._data_gathering.car_detection_matrix.run_matrix import get_car_coords
from classes.detection_matrix import AsyncDetectionMatrix, DetectionMatrix  # noqa: F401
from classes.ui import spectator_follow_actor
from classes.experimental.vehicle_spawner import VehicleSpawner

spawner = None
vehicles = []


def main():
    global spawner, vehicles

    # Initialise the class for vehicle spawning
    spawner = VehicleSpawner('conf/launch_config.yaml', 'conf/experimental_rule_interpreter_examples/traffic_manager/vehicle_spawn.yaml')
    client, world, world_map, = spawner.initialize_carla_service()
    ego_bp, car_bp, driver1, spawn_points, rule_interpreter = spawner.prepare_vehicles(world)

    # Spawn vehicles and assign drivers
    ego = spawner.spawn_vehicles(world, ego_bp, spawn_points)
    ego_vehicle = spawner.assign_drivers(ego, driver1)

    # Spawn traffic
    vehicles, tm = spawner.spawn_traffic(world, car_bp, spawn_points, driver1, ego_vehicle)
    # Initialize loop variables
    world.tick()
    road_lane_ids = get_all_road_lane_ids(world.get_map())
    t_end = time.time() + 10000

    # Create a thread for the camera functionality
    try:
        camera_thread = threading.Thread(target=spectator_follow_actor, args=(ego_vehicle, ))
        camera_thread.start()

        # Initialize matrix thread
        detection_matrix = AsyncDetectionMatrix(ego_vehicle, road_lane_ids=road_lane_ids)
        detection_matrix.start()

        print("Starting game loop")
        while time.time() < t_end:
            # Retrieve the latest matrix from the matrix thread
            matrix = detection_matrix.getMatrix()

            if matrix is None:
                continue

            (i_car, j_car) = get_car_coords(matrix)
            # NEW use RuleInterpreter
            # NOTE: Currently this might not work, need to check back with @Bogdan Oprisiu
            """
            results = rule_interpreter.execute_all_functions(driver1, matrix, i_car, j_car, tm)

            if any(results.values()):
                continue
            """

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
        spectator_follow_actor.stop()  # type: ignore[attr-defined]
        detection_matrix.stop()
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
