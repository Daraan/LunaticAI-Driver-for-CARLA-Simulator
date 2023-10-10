import json
import carla

class Driver:
    def __init__(self, path, client : carla.Client):
        self.vehicle = None
        self.tm : carla.TrafficManager = client.get_trafficmanager()
        if path is not None:
            with open(path, 'r') as file:
                data = json.load(file)
                self.config = data
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

    def drive(self, carList, with_autopilot=False):
        # this will be our main logic
        self.vehicle.drive(carList)
        if with_autopilot:
            self.actor.set_autopilot(True)

    @property
    def actor(self) -> carla.Actor:
        return self.vehicle.actor

    def configure_autopilot(self):
        # TODO: Set values from config
        self.tm.auto_lane_change(self.actor, True)
        self.tm.distance_to_leading_vehicle(self.actor, self.min_front_distance)
        self.tm.vehicle_percentage_speed_difference(self.actor, self.speed_limit_scale)
        self.tm.keep_right_rule_percentage(self.actor, 0)
        self.tm.random_right_lanechange_percentage(self.actor, 25)
        self.tm.random_left_lanechange_percentage(self.actor, 50)
        self.tm.ignore_vehicles_percentage(self.actor, 40)

    def goNuts(self):
        pass