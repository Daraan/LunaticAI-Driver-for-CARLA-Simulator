import time

from classes.constants import StreetType
import launch_tools
from data_gathering.car_detection_matrix.informationUtils import *
from classes.carla_service import CarlaService
from classes.driver import Driver
from classes.traffic_manager import TrafficManager
from classes.vehicle import Vehicle

vehicles = []


def main():
    global client
    carlaService = CarlaService("Town04", "127.0.0.1", 2000)
    client = carlaService.client

    world = carlaService.getWorld()
    world_map = world.get_map()
    ego_bp, car_bp = launch_tools.prepare_blueprints(world)

    driver1 = Driver("config/default_driver.json", traffic_manager=client)

    spawn_points = launch_tools.csv_to_transformations("examples/highway_example_car_positions.csv")

    # Spawn Ego
    ego = Vehicle(world, ego_bp)
    try:
        ego.spawn(spawn_points[0])
    except Exception as e:
        pass

    vehicles.append(ego)
    carlaService.assignDriver(ego, driver1)
    ego_vehicle = ego.actor

    # spawn others
    for sp in spawn_points[1:]:
        v = Vehicle(world, car_bp)
        v.spawn(sp)
        vehicles.append(v)
        ap = TrafficManager(client, v.actor)
        ap.init_passive_driver()
        ap.start_drive()

    tm = TrafficManager(client, ego.actor)
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
    while time.time() < t_end:
        try:
            follow_car(ego_vehicle, world)
            ego_location = ego_vehicle.get_location()
            ego_waypoint = world_map.get_waypoint(ego_location)
            ego_on_highway = check_ego_on_highway(ego_location, road_lane_ids, world_map)

            current_lanes = []
            for id in road_lane_ids:
                if str(ego_waypoint.road_id) == id.split("_")[0]:
                    current_lanes.append(int(id.split("_")[1]))

            # Normal Road
            if ego_on_highway:
                street_type = StreetType.ON_HIGHWAY
            else:
                street_type = StreetType.NON_HIGHWAY_STREET
            matrix = create_city_matrix(ego_location, road_lane_ids, world_map)

            if matrix:
                matrix, _ = detect_surrounding_cars(
                    ego_location, ego_vehicle, matrix, road_lane_ids, world, radius, ego_on_highway, highway_shape
                )

            for i in matrix:
                print(i, matrix[i])
            print(street_type)

            df = safe_data(ego_vehicle, matrix, street_type, df)

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
