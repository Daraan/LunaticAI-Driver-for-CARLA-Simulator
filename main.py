import carla

from classes.carla_service import CarlaService
# TODO: maybe we can merge these or make them more unified & marge with agent
from classes.driver import Driver
from classes.vehicle import Vehicle

import argparse
import glob
import os
import sys
import random
import time

from classes.traffic_manager_daniel import TrafficManagerD
import utils

vehicles = []

def main(args={}):
    global client
    carlaService = CarlaService("Town04", args.host, args.port)
    client = carlaService.client

    world = carlaService.getWorld()
    level = world.get_map()
    ego_bp, car_bp = utils.blueprint_helpers.get_contrasting_blueprints(world)

    driver1 = Driver("config/driver1.json", traffic_manager=client)

    spawn_points = utils.general.csv_to_transformations("examples/highway_example_car_positions.csv")
    car1 = carlaService.createCar("model3")

    # Spawn Ego
    ego = Vehicle(world, ego_bp)
    ego.spawn(spawn_points[0])
    vehicles.append(ego)
    carlaService.assignDriver(ego, driver1)

    # TODO: let Driver class manage autopilot and not the TrafficMangerD class

    # spawn others
    for sp in spawn_points[1:]:
        v = Vehicle(world, car_bp)
        v.spawn(sp)
        vehicles.append(v)
        # v.setVelocity(1)
        print(v.actor)
        ap = TrafficManagerD(client, v.actor)
        ap.init_passive_driver()
        ap.start_drive()

    tm = TrafficManagerD(client, ego.actor,
                         # config="config/driver1.json" # Not implemented yet
                         )
    tm.init_lunatic_driver()
    # ego.setThrottle(1)
    # time.sleep(1)
    tm.start_drive()

    #driver1.spawn(carlaService.getWorld().get_map().get_spawn_points()[123])
    #driver1.vehicle.focusCamera()
    #ego.setThrottle(8)
    #time.sleep(4)
    #ego.setBrake(2)

    """
    driver2 = Driver("json/driver1.json")
    car2 = carlaService.createCar("coupe")

    driver3 = Driver("json/driver1.json")
    car3 = carlaService.createCar("mustang")

    carlaService.assignDriver(car1, driver1)
    carlaService.assignDriver(car2, driver2)
    carlaService.assignDriver(car3, driver3)

    spawnPoint = carlaService.getWorld().get_map().get_spawn_points()[123]
    driver1.spawn(spawnPoint)
    spawnPoint.location.y += 8
    driver2.spawn(spawnPoint)
    spawnPoint.location.y -= 16
    driver3.spawn(spawnPoint)

    # driver1.vehicle.focusCamera()
    car3.setThrottle(0.2)
    driver1.drive(carlaService.vehicleList)
    # car2.setThrottle(2)


    time.sleep(1)
    # car1.setBrake(2)
    # car1.setSteering(3)
    # car1.setHandbrake(True)
    time.sleep(5)
    """
    if args.interactive: 
        # goes into interactive mode here
        import code
        v = globals().copy()
        v.update(locals())
        code.interact(local=v)
    input("press any key to end...")

def parse():
    parser = argparse.ArgumentParser(description='Carla Highway Example')
    parser.add_argument('-I', '--interactive', action='store_true', help='Interactive mode', default=False)
    parser.add_argument('-p', '--port', help='TCP Port', default="2000", type=int)
    parser.add_argument('-i', '--host', help='Host', default="localhost", type=str)
    return parser.parse_args()  


if __name__ == '__main__':
    args = parse()
    from pprint import pprint
    pprint(args)
    try:
        main(args)
    finally:
        try:
            client.apply_batch([carla.command.DestroyActor(x.actor) for x in vehicles])
        except NameError:
            # client not defined yet to earlier errors
            pass
