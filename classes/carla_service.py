
import carla

from classes.vehicle import Vehicle


class CarlaService:
    def __init__(self, worldName, ip, port):
        self.client = carla.Client(ip, port)
        self.client.set_timeout(2.0)
        self.vehicleList = []
        # self.client.load_world(worldName)
        self.world = self.client.get_world()

    def createCar(self, model):
        car = Vehicle(self.world, model)
        self.vehicleList.append(car)
        return car

    def assignDriver(self, vehicle, driver):
        driver.vehicle = vehicle

    def getWorld(self):
        return self.world

    def removeAllCars(self):
        for car in self.vehicleList:
            car.actor.destroy()

    def __del__(self):
        self.removeAllCars()
