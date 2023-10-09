import carla
from carla import Vector3D

class Vehicle:
    # TODO would be nice if we could derive this from carla.Vehicle
    # should be able to use some functions directly without using functions for all

    instances : list = [] # for easier destruction later

    def __init__(self, world, make=""):
        self.actor = None
        self.world = world
        self.control = carla.VehicleControl()
        blueprint_library = world.get_blueprint_library()
        if isinstance(make, carla.ActorBlueprint):
            self.actorBlueprint = make
        else:
            self.actorBlueprint = blueprint_library.filter(make)[0]
        Vehicle.instances.append(self) # access all instances over the class

    def spawn(self, transform):
        self.actor = self.world.spawn_actor(self.actorBlueprint, transform)
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