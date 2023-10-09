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
    #car1 = carlaService.createCar("model3")

    # Spawn Ego
    ego = Vehicle(world, ego_bp)
    ego.spawn(spawn_points[0])
    vehicles.append(ego)

    # spawn others
    for sp in spawn_points[1:]:
        v = Vehicle(world, car_bp)
        v.spawn(sp)
        vehicles.append(v)
        v.setVelocity(1)

    carlaService.assignDriver(ego, driver1)

    from trafic_manager_daniel import TrafficManagerD

    tm = TrafficManagerD(client, ego.actor)
    #ego.setThrottle(1)
    #time.sleep(1)
    ego.actor.set_autopilot(True)

    driver1.spawn(carlaService.getWorld().get_map().get_spawn_points()[123])
    #driver1.vehicle.focusCamera()
    #ego.setThrottle(8)
    #time.sleep(4)
    #ego.setBrake(2)
    input("press any key to end...")

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
    spawnPoint.location.x += 8
    driver2.spawn(spawnPoint)
    spawnPoint.location.x -= 16
    driver3.spawn(spawnPoint)

    driver1.vehicle.focusCamera()
    driver1.drive(carlaService.vehicleList)
    # car2.setThrottle(2)
    # car3.setThrottle(2.1)

    time.sleep(1)
    # car1.setBrake(2)
    # car1.setSteering(3)
    # car1.setHandbrake(True)
    time.sleep(5)
    """

if __name__ == '__main__':
    try:
        main()
    finally:
        client.apply_batch([carla.command.DestroyActor(x.actor) for x in vehicles])

