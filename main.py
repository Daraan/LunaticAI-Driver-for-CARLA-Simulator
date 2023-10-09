from CarlaService import CarlaService
from Driver import Driver

import numpy
import glob
import os
import sys
import carla
import random
import time

from Vehicle import Vehicle

def main():
    carlaService = CarlaService("Town04", "10.1.0.25", 2000)

    driver1 = Driver("json/driver1.json")
    car1 = carlaService.createCar("model3")

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

if __name__ == '__main__':
    main()
