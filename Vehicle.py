from cmath import sqrt

import carla
from carla import Vector3D

def calculateDistance(location1, location2):
    return sqrt(
        (location1.x ** 2 - location2.x ** 2) +
        (location1.y ** 2 - location2.y ** 2) +
        (location1.z ** 2 - location2.z ** 2)
    ).real

from carla import Vector3D

class Vehicle:
    # TODO would be nice if we could derive this from carla.Vehicle
    # should be able to use some functions directly without using functions for all

    instances : list = [] # for easier destruction later

    def __init__(self, world : carla.World, make=""):
        self.actor : carla.Actor = None
        self.world = world
        self.control : carla.VehicleControl = carla.VehicleControl()
        blueprint_library = world.get_blueprint_library()
        if isinstance(make, carla.ActorBlueprint):
            self.actorBlueprint : carla.ActorBlueprint = make
        else:
            self.actorBlueprint : carla.ActorBlueprint = blueprint_library.filter(make)[0]
        Vehicle.instances.append(self) # access all instances over the class

    def __eq__(self, other):
        return not (
                self.getLocation().x != other.getLocation().x
                or self.getLocation().y != other.getLocation().y
                or self.getLocation().z != other.getLocation().z
        )


    def spawn(self, transform):
        self.actor : carla.Actor = self.world.spawn_actor(self.actorBlueprint, transform)
        self.actor.apply_control(self.control)

    def focusCamera(self):
        self.world.get_spectator().set_transform(self.actor.get_transform())

    def setThrottle(self, value):
        self.control.brake = 0
        self.control.throttle = value
        self.actor.apply_control(self.control)

    def setVelocity(self, speed : Vector3D =3):
        if not isinstance(speed, Vector3D):
            self.actor.enable_constant_velocity(Vector3D(x=speed))
        else:
            self.actor.enable_constant_velocity(speed)

    def setBrake(self, value):
        self.control.throttle = 0
        self.control.brake = value
        self.actor.apply_control(self.control)

    def setSteering(self, value):
        self.control.steer = value
        self.actor.apply_control(self.control)

    def setHandbrake(self, value):
        self.control.hand_brake = value
        self.actor.apply_control(self.control)

    def getLocation(self):
        return self.actor.get_transform().location

    def findCarBehind(self, vehicles: []):
        closestCar = None
        for car in vehicles:
            if (
                    car != self
                    and self.getLocation().y < car.getLocation().y
                    and (closestCar is None or car.getLocation().y < closestCar.getLocation().y)
            ):
                closestCar = car

        return closestCar

    def findCarAhead(self, vehicles: []):
        closestCar = None
        for car in vehicles:
            if (
                    car != self
                    and car.getLocation().y > self.getLocation().y
                    and (closestCar is None or car.getLocation().y < closestCar.getLocation().y)
            ):
                closestCar = car

        return closestCar

    def distanceToCarAhead(self, vehicles: []):
        vehicleAhead = self.findCarAhead(vehicles)
        if vehicleAhead is None:
            return None
        locationAhead = vehicleAhead.actor.get_transform().location

        return calculateDistance(self.getLocation(), locationAhead)

    def distanceToCarBehind(self, vehicles: []):
        vehicleBehind = self.findCarBehind(vehicles)
        if vehicleBehind is None:
            return None
        locationBehind = vehicleBehind.actor.get_transform().location

        return calculateDistance(self.getLocation(), locationBehind)
