import time

import carla

import utils
from DataGathering.informationUtils import get_all_road_lane_ids, follow_car
from classes.carla_service import CarlaService
from classes.driver import Driver
from classes.traffic_manager_daniel import TrafficManagerD
from classes.vehicle import Vehicle
from utils.logging import log
from DataGathering.matrix_wrap import wrap_matrix_functionalities

vehicles = []


def main():
    global client
    carlaService = CarlaService("Town04", "127.0.0.1", 2000)
    client = carlaService.client

    world = carlaService.getWorld()
    world_map = world.get_map()
    ego_bp, car_bp = utils.prepare_blueprints(world)

    driver1 = Driver("config/default_driver.json", traffic_manager=client)

    spawn_points = utils.csv_to_transformations("doc/highway_example_car_positions.csv")

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
        ap = TrafficManagerD(client, v.actor)
        ap.init_passive_driver()
        ap.start_drive()

    tm = TrafficManagerD(client, ego_vehicle)
    tm.init_lunatic_driver()
    tm.start_drive()

    # Initialize speed of ego_vehicle to use as global variable
    world.tick()
    road_lane_ids = get_all_road_lane_ids(world_map=world.get_map())
    t_end = time.time() + 10000
    while time.time() < t_end:
        try:
            follow_car(ego_vehicle, world)
            matrix = wrap_matrix_functionalities(ego_vehicle, world, world_map, road_lane_ids)

            (i_car, j_car) = (0, 0)

            for lane in matrix:
                for i in range(len(matrix[lane])):
                    if matrix[lane][i] == 1:
                        (i_car, j_car) = (lane, i)

            if matrix[i_car][j_car + 1] == 2:
                log("overtake!")
                tm.force_overtake(20)

            world.tick()

        except Exception as e:
            log(e.__str__())

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
