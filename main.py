import carla
from CarlaService import CarlaService
from Driver import Driver

import numpy
import glob
import os
import sys
import random
import time

from useful_scripts import utils

from Vehicle import Vehicle

vehicles = []
def main():
    global client
    carlaService = CarlaService("Town04", "127.0.0.1", 2000)
    client = carlaService.client
    world = carlaService.getWorld()
    ego_bp, car_bp = utils.prepare_blueprints(world)

    driver1 = Driver("json/driver1.json")

    spawn_points = utils.csv_to_transformations("useful_scripts/highway_example_car_positions.csv")

    # Spawn Ego
    ego = Vehicle(world, ego_bp)
    ego.spawn(spawn_points[0])
    vehicles.append(ego)

    # spawn others
    for sp in spawn_points[1:]:
        v = Vehicle(world, car_bp)
        v.spawn(sp)
        vehicles.append(v)

    carlaService.assignDriver(ego, driver1)
    #driver1.spawn(carlaService.getWorld().get_map().get_spawn_points()[123])
    #driver1.vehicle.focusCamera()
    ego.setThrottle(3)
    time.sleep(1)
    ego.setBrake(2)
    input("press any key to end...")

if __name__ == '__main__':
    try:
        main()
    finally:
        client.apply_batch([carla.command.DestroyActor(x.vehicle) for x in vehicles])

