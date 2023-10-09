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
    carlaService = CarlaService("Town04", "10.1.0.24", 2000)

    driver1 = Driver("json/driver1.json")
    car1 = Vehicle(carlaService.getWorld(), "model3")

    carlaService.assignDriver(car1, driver1)
    driver1.spawn(carlaService.getWorld().get_map().get_spawn_points()[334])
    driver1.vehicle.focusCamera()
    driver1.drive()


if __name__ == '__main__':
    main()
