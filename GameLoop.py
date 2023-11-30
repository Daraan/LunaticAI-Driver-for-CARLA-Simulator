import random
import time

import carla
import utils

import utils
from DataGathering.informationUtils import get_all_road_lane_ids, initialize_dataframe, follow_car, \
    check_ego_on_highway, create_city_matrix, detect_surronding_cars
from classes.carla_service import CarlaService
from classes.driver import Driver
from classes.traffic_manager_daniel import TrafficManagerD
from classes.vehicle import Vehicle
from matrix_wrap import wrap_matrix_functionalities, get_car_coords

vehicles = []

def main():
    global client
    carlaService = CarlaService("Town04", "127.0.0.1", 2000)
    client = carlaService.client

    world = carlaService.getWorld()
    world_map = world.get_map()
    ego_bp, car_bp = utils.prepare_blueprints(world)

    driver1 = Driver("config/default_driver.json", traffic_manager=client)
    driver2 = Driver("config/aggressive_driver.json", traffic_manager=client)

    spawn_points = utils.csv_to_transformations("examples/highway_example_car_positions.csv")

    # Spawn Ego
    ego = Vehicle(world, ego_bp)
    try:
        ego.spawn(spawn_points[0])
    except:
        pass

    vehicles.append(ego)
    carlaService.assignDriver(ego, driver1)

    ego_vehicle = ego.actor
    vehicle_type = ego_vehicle.type_id

    # spawn others
    for sp in spawn_points[1:]:
        v = Vehicle(world, car_bp)
        v.spawn(sp)
        vehicles.append(v)
        ap = TrafficManagerD(client, v.actor, speed_limit_scale=-25,
                             min_front_distance=3)
        ap.init_passive_driver()
        ap.start_drive()

    tm = TrafficManagerD(client, ego_vehicle, speed_limit_scale=driver1.speed_range[1],
                         min_front_distance=driver1.distance_range[0])
    tm.init_lunatic_driver()
    tm.start_drive()

    # Define the radius to search for other vehicles
    radius = 100

    # Initialize speed of ego_vehicle to use as global variable
    world.tick()
    road_lane_ids = get_all_road_lane_ids(world_map=world.get_map())
    df = initialize_dataframe()
    t_end = time.time() + 10
    while time.time() < t_end:
        try:
            follow_car(ego_vehicle, world)
            matrix = wrap_matrix_functionalities(ego_vehicle, world, world_map, road_lane_ids)
            # print(matrix)
            ego_location = ego_vehicle.get_location()
            ego_waypoint = world_map.get_waypoint(ego_location)

            (i_car, j_car) = get_car_coords(matrix)
            overtake_direction = 0
            if matrix[i_car + 1][j_car + 1] == 0:
                print("can overtake on right")
                overtake_direction = 1

            if matrix[i_car - 1][j_car + 1] == 0:
                print("can overtake on left")
                overtake_direction = -1

            if matrix[i_car][j_car + 1] == 2:
                choice = random.randint(1, 100)
                if choice > driver1.overtake_mistake_chance:
                    tm.force_overtake(20, overtake_direction)
                    print("overtake!")
                else:
                    print("overtake averted by chance")


        except Exception as e:
            print(e.__str__())

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
