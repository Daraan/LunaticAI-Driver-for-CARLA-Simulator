import carla

from classes.vehicle import Vehicle


class CarlaService:
    def __init__(self, worldName=None, ip="localhost", port=2000):
        self.client = carla.Client(ip, port)
        self.client.set_timeout(10.0)
        self.vehicleList = []
        if worldName:
            self.client.load_world(worldName)
        self.world = self.client.get_world()

    def createCar(self, model):
        car = Vehicle(self.world, model)
        self.vehicleList.append(car)
        return car

    @staticmethod
    def assignDriver(vehicle, driver):
        driver.vehicle = vehicle

    def getWorld(self):
        return self.world

    def removeAllCars(self):
        for i in range(len(self.vehicleList)):
            car = self.vehicleList.pop()  # remove element from list. Keeps list up-to-data
            if car.actor is not None:  # actor is None if car was not spawned
                car.actor.destroy()

    def __del__(self):
        self.removeAllCars()
