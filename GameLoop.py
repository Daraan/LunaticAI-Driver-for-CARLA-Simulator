import carla

from DataGathering.informationUtils import follow_car
from classes.carla_service import CarlaService
# TODO: maybe we can merge these or make them more unfied
from classes.driver import Driver
from classes.vehicle import Vehicle
from DataGathering.run_matrix import DataMatrix

import numpy
import glob
import os
import sys
import random
import time

import utils
from classes.traffic_manager_daniel import TrafficManagerD

vehicles = []


def main():
    global client
    carlaService = CarlaService("Town04", "127.0.0.1", 2000)
    client = carlaService.client

    world = carlaService.getWorld()
    level = world.get_map()
    ego_bp, car_bp = utils.prepare_blueprints(world)

    driver1 = Driver("config/default_driver.json", traffic_manager=client)
    spawn_points = utils.csv_to_transformations("examples/highway_example_car_positions.csv")

    # Spawn Ego
    ego = Vehicle(world, ego_bp)
    ego.spawn(spawn_points[0])
    vehicles.append(ego)
    carlaService.assignDriver(ego, driver1)

    matrix = DataMatrix(ego, world)

    # spawn others
    for sp in spawn_points[1:]:
        v = Vehicle(world, car_bp)
        v.spawn(sp)
        vehicles.append(v)
        print(v.actor)
        ap = TrafficManagerD(client, v.actor)
        ap.init_passive_driver()
        ap.start_drive()

    tm = TrafficManagerD(client, ego.actor,
                         # config="json/driver1.json" # Not implemented yet
                         )
    tm.init_lunatic_driver()
    tm.start_drive()
    t_end = time.time() + 10

    m = matrix.getMatrix()

    for i in m:
        print(i)

    if "-I" in sys.argv:
        # goes into interactive mode here
        import code
        v = globals().copy()
        v.update(locals())
        code.interact(local=v)

    while time.time() < t_end:
        try:
            follow_car(ego_vehicle, world)

            

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
