import carla

from Vehicle import Vehicle


class CarlaService:
    def __init__(self, worldName, ip, port):
        self.client = carla.Client(ip, port)
        self.client.set_timeout(2.0)
        self.vehicleList = []
        # self.client.load_world(worldName)
        self.world = self.client.get_world()

    def createCar(self):
        self.vehicleList.append(Vehicle(self.world, "model3"))

    def assignDriver(self, vehicle, driver):
        driver.vehicle = vehicle

    def getWorld(self):
        return self.world