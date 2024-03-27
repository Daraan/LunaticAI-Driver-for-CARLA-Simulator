import carla

from classes.vehicle import Vehicle
from agents.tools.logging import log

from launch_tools import CarlaDataProvider

class CarlaService(CarlaDataProvider):
    def __init__(self, worldName=None, ip="localhost", port=2000):
        client = self.get_client()
        if client is None:
            client = carla.Client(ip, port)
            client.set_timeout(10.0)
            self.set_client(client)
        if not self.get_world():
            world = client.get_world()
            self.set_world(world)
        if worldName and self.get_map().name != "Carla/Maps/" + worldName:
            world = client.load_world(worldName)
            self.set_world(world)
        else:
            log("skipped loading world, already loaded")
        self.vehicleList: "list[Vehicle]" = []

    def createCar(self, model):
        car = Vehicle(self.get_world, model)
        self.vehicleList.append(car)
        return car

    @staticmethod
    def assignDriver(vehicle, driver):
        driver.vehicle = vehicle

    def removeAllCars(self):
        for i in range(len(self.vehicleList)):
            car = self.vehicleList.pop()  # remove element from list. Keeps list up-to-data
            if car.actor is not None:  # actor is None if car was not spawned
                car.actor.destroy()
                car.actor = None

    def __del__(self):
        self.removeAllCars()
