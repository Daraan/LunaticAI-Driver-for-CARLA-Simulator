import carla


class Vehicle:
    def __init__(self, world, make):
        self.actor = None
        self.world = world
        self.control = carla.VehicleControl()
        blueprint_library = world.get_blueprint_library()
        self.actorBlueprint = blueprint_library.filter(make)[0]

    def spawn(self, transform):
        self.actor = self.world.spawn_actor(self.actorBlueprint, transform)
        self.actor.apply_control(self.control)

    def focusCamera(self):
        self.world.get_spectator().set_transform(self.actor.get_transform())
