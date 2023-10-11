import carla
from carla import Vector3D
from vehicle import VehicleBase


# DONE: we likely can derive this from our base class and just add t
# NOTE: This file is not used
class Vehicle:
    # Wrap our own VehicleBase class and the CARLA vehicle class

    instances: list = []  # for easier destruction later

    def __init__(self, world: carla.World, make=""):
        self.vehicle = VehicleBase(world, make)

    def __getattr__(self, attr):
        # Delegate attribute access to the CARLA Vehicle class
        if hasattr(self.vehicle.actor, attr):
            return getattr(self.vehicle.actor, attr)
        raise AttributeError(f"'Invalid attribute {attr}'{attr}'")

    def getCarlaVehicle(self):
        return self.carlaVehicle

    def __eq__(self, other):
        return self.vehicle == other.vehicle

    def spawn(self, transform):
        self.vehicle.spawn(transform)

    def focusCamera(self):
        self.vehicle.focusCamera()

    def setThrottle(self, value):
        self.vehicle.setThrottle(value)

    def setVelocity(self, speed: Vector3D = 3):
        self.vehicle.setVelocity(speed)

    def setBrake(self, value):
        self.vehicle.setBrake(value)

    def setSteering(self, value):
        self.vehicle.setSteering(value)

    def setHandbrake(self, value):
        self.vehicle.setHandbrake(value)

    def getLocation(self):
        return self.vehicle.getLocation()

    def findCarBehind(self, vehicles: []):
        return self.vehicle.findCarBehind(vehicles)

    def findCarAhead(self, vehicles: []):
        return self.vehicle.findCarAhead(vehicles)

    def distanceToCarAhead(self, vehicles: []):
        return self.vehicle.distanceToCarAhead(vehicles)

    def distanceToCarBehind(self, vehicles: []):
        return self.vehicle.distanceToCarBehind(vehicles)
