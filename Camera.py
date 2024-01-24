import time


def follow_car(ego_vehicle, world):
    vehicle_transform = ego_vehicle.get_transform()
    spectator_transform = vehicle_transform
    spectator_transform.location -= (vehicle_transform.get_forward_vector() * 10)
    spectator_transform.location += (vehicle_transform.get_up_vector() * 5)
    world.get_spectator().set_transform(spectator_transform)


def camera_function(ego_vehicle, world):
    while True:
        follow_car(ego_vehicle, world)