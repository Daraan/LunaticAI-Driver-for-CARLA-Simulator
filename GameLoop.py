import random
import threading
import time
from asyncio import Queue

import carla

import utils
from utils.Camera import camera_function
from DataGathering.informationUtils import get_all_road_lane_ids
from DataGathering.run_matrix import matrix_function
from classes.carla_service import CarlaService
from classes.driver import Driver
from classes.traffic_manager import TrafficManager
from classes.vehicle import Vehicle
from DataGathering.matrix_wrap import get_car_coords, wrap_matrix_functionalities

vehicles = []


def main():
    global client, i_car, j_car
    carlaService = CarlaService("Town04", "127.0.0.1", 2000)
    # carlaService = CarlaService()
    client = carlaService.client

    world = carlaService.getWorld()
    world_map = world.get_map()
    ego_bp, car_bp = utils.prepare_blueprints(world)

    driver1 = Driver("config/insane_driver.json", traffic_manager=client)
    driver2 = Driver("config/aggressive_driver.json", traffic_manager=client)
    driver3 = Driver("config/default_driver.json", traffic_manager=client)

    spawn_points = utils.csv_to_transformations("doc/highway_example_car_positions.csv")

    # Spawn Ego
    ego = Vehicle(world, ego_bp)
    try:
        ego.spawn(spawn_points[0])
    except Exception as e:
        print(e.__str__())

    vehicles.append(ego)
    carlaService.assignDriver(ego, driver1)

    ego_vehicle = ego.actor

    # spawn others
    for sp in spawn_points[1:5]:
        v = Vehicle(world, car_bp)
        v.spawn(sp)
        vehicles.append(v)
        ap = TrafficManager(client, v.actor, speed_limit_scale=-driver1.speed_range[1],
                            min_front_distance=driver1.distance_range[0])
        ap.init_lunatic_driver()
        ap.start_drive()

    for sp in spawn_points[5:]:
        v = Vehicle(world, car_bp)
        v.spawn(sp)
        vehicles.append(v)
        ap = TrafficManager(client, v.actor, speed_limit_scale=60, min_front_distance=8)
        ap.init_passive_driver()
        ap.start_drive()

    tm = TrafficManager(client, ego_vehicle,
                        speed_limit_scale=-driver1.speed_range[1],
                        min_front_distance=driver1.distance_range[0])
    tm.init_lunatic_driver()
    # tm.init_passive_driver()
    tm.start_drive()

    # Define the radius to search for other vehicles
    radius = 100

    # Initialize speed of ego_vehicle to use as global variable
    world.tick()
    road_lane_ids = get_all_road_lane_ids(world_map=world.get_map())
    t_end = time.time() + 10000
    crazy = False
    lane_change = False

    # Create a thread for the camera functionality
    camera_thread = threading.Thread(target=camera_function, args=(ego_vehicle, world))
    camera_thread.start()

    while time.time() < t_end:
        try:
            disable_collision = random.randint(1, 1000)
            if disable_collision <= driver1.ignore_obstacle_chance:
                driver1.vehicle.actor.set_autopilot(False)
                driver1.vehicle.setThrottle(20)
                print("Crazy")
                time.sleep(1)
                driver1.vehicle.actor.set_autopilot(True)
                driver1.vehicle.setThrottle(0)
                print("Crazy over")

            matrix = wrap_matrix_functionalities(ego_vehicle, world, world_map, road_lane_ids)

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
