import json
import os
from typing import Union, Optional

import carla
from launch_tools import CarlaDataProvider

TRAFFIC_MANAGER_CONFIG_SUBDIR = ""


class Driver:
    def __init__(self, path,
                 traffic_manager: Optional[Union[carla.Client, carla.TrafficManager]] = None,
                 config_update: dict = None):
        """
        Args:
            path:
            traffic_manager: either the client or a traffic manger
                    todo: find out if multiple client.get_trafficmanager() are the same thing or not
            config_update: dict : To modify/path the file found in path.
        """
        self.vehicle = None
        self.config = None
        self.overtake_mistake_chance = 0
        self.risky_overtake_chance = 0
        self.ignore_obstacle_chance = 0
        self.brake_check_chance = 0

        if isinstance(traffic_manager, carla.TrafficManager):
            self.tm = traffic_manager  # Traffic manager short alias
        elif isinstance(traffic_manager, carla.Client):
            self.tm: carla.TrafficManager = traffic_manager.get_trafficmanager(CarlaDataProvider.get_traffic_manager_port())  # todo find out if there is a different to useing
        elif traffic_manager is not None:
            raise TypeError("manager wrong type", type(traffic_manager))
        if path is not None:
            with open(path, 'r') as file:
                data = json.load(file)
            self.config: dict = data
            driver_data = data.get("driver", {})
            speed_range = driver_data.get("speed", {})
            self.overtake_mistake_chance = int(driver_data.get("overtake_mistake_chance", {}))
            self.risky_overtake_chance = int(driver_data.get("risky_overtake_chance", {}))
            self.ignore_obstacle_chance = int(driver_data.get("ignore_obstacle_chance", {}))
            self.brake_check_chance = int(driver_data.get("brake_check_chance", {}))
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
        if self.config is None:
            self.config = config_update
        elif config_update is not None:
            self.config.update(config_update)  # TODO add some sanity check for correct format
        if self.config["use_traffic_manager"]:
            dir = os.path.split(path)[0]
            path_tm = os.path.join(dir, TRAFFIC_MANAGER_CONFIG_SUBDIR, self.config["use_traffic_manager"] + ".json", )
            with open(path_tm, 'r') as file:
                self.tm_config = json.load(file)

    def spawn(self, transform):
        self.vehicle.spawn(transform)

    @property
    def actor(self) -> carla.Actor:
        return self.vehicle.actor

    @property
    def traffic_manager(self) -> carla.TrafficManager:
        return self.tm

    def drive(self, carList, with_autopilot=False):
        # this will be our main logic
        self.vehicle.drive(carList)
        if with_autopilot:
            self.actor.set_autopilot(True)

    def set_autopilot(self, yes=True):
        self.actor.set_autopilot(yes)

    def configure_autopilot(self):
        """
        Configures the autopilot of the vehicle, e.g. by calling these but based on the config file
        
        self.tm.auto_lane_change(self.actor, tmc["auto_lane_change"])
        self.tm.distance_to_leading_vehicle(self.actor, tmc["distance_to_leading_vehicle"])
        self.tm.vehicle_percentage_speed_difference(self.actor, tmc["vehicle_percentage_speed_difference"])
        self.tm.keep_right_rule_percentage(self.actor, 0)
        self.tm.random_right_lanechange_percentage(self.actor, 25)
        self.tm.random_left_lanechange_percentage(self.actor, 50)
        self.tm.ignore_vehicles_percentage(self.actor, 40)
        """
        if self.tm is None:
            raise ValueError(
                "To use the Traffic Manager the driver needs to be initialized with the client. Or set Driver.tm manually to a manager")
        # TODO Test lazy notation
        tm_config = self.tm_config["traffic_manager"]
        for k, v in tm_config.items():
            setter = getattr(self.tm, k)
            if setter is None:
                raise ValueError(f"{k} invalid function for carla.TrafficManager")
            setter(self.actor, v)

        # manual way:

