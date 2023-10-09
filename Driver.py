import json


class Driver:
    def __init__(self, path):
        self.vehicle = None
        if path is not None:
            with open(path, 'r') as file:
                data = json.load(file)
                driver_data = data.get("driver", {})
                speed_range = driver_data.get("speed", {})
                distance_range = driver_data.get("distance", {})

                # Store the specified speed and distance ranges
                self.speed_range = (speed_range.get("from", 0), speed_range.get("to", 1))
                self.distance_range = (distance_range.get("from", 0), distance_range.get("to", 1))

                # Initialize with default values
                self.speed = 0
                self.distance_x = 0
        else:
            self.speed_range = (0, 1)  # Default speed range
            self.distance_range = (0, 1)  # Default distance range
            self.speed = 0  # Default speed
            self.distance_x = 0  # Default distance

    def spawn(self, transform):
        self.vehicle.spawn(transform)

    def drive(self):
        self.vehicle.control.throttle = 1
        self.vehicle.actor.apply_control(self.vehicle.control)


    def goNuts(self):
        pass