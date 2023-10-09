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
    carlaService = CarlaService("Town04", "127.0.0.1", 2000)

    driver1 = Driver("json/driver1.json")
    car1 = Vehicle(carlaService.getWorld(), "model3")

    carlaService.assignDriver(car1, driver1)
    driver1.spawn(carlaService.getWorld().get_map().get_spawn_points()[123])
    driver1.vehicle.focusCamera()
    car1.setThrottle(3)
    time.sleep(1)
    car1.setBrake(2)


if __name__ == '__main__':
    main()
