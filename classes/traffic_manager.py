"""
Uses the built in carla.TrafficManager to use the autopilot written in C.
"""

from typing import ClassVar
import carla

from launch_tools import CarlaDataProvider

class TrafficManager:
    tm : ClassVar[carla.TrafficManager] = None

    def __init__(self, actor: carla.Actor, *,
                 speed_limit_scale,
                 min_front_distance,
                 seed=1):
        client = CarlaDataProvider.get_client()
        if client is None:
            raise ValueError("Carla client is not initialized")
        # TODO use a settings file
        if not isinstance(actor, carla.Actor):
            raise TypeError("`actor` must be a carla.Actor")
        if TrafficManager.tm is None:
            # TrafficManager.tm : carla.TrafficManager =\
            TrafficManager.tm = client.get_trafficmanager(port=CarlaDataProvider.get_traffic_manager_port()) # TODO: Should this be different ports? Maybe it is the same traffic manager underneath even if different python instances.
            # TrafficManager.tm.set_random_device_seed(seed)
            TrafficManager.tm.set_random_device_seed(seed)
        self.min_front_distance = min_front_distance
        self.speed_limit_scale: float = speed_limit_scale
        self.actor = actor

    def init_lunatic_driver(self):
        self.tm.auto_lane_change(self.actor, False)
        self.tm.distance_to_leading_vehicle(self.actor, (self.min_front_distance - 1) % 10 + 0.5)
        self.tm.vehicle_percentage_speed_difference(self.actor, self.speed_limit_scale)
        self.tm.keep_right_rule_percentage(self.actor, 0)
        self.tm.random_right_lanechange_percentage(self.actor, 0)
        self.tm.random_left_lanechange_percentage(self.actor, 0)
        self.tm.ignore_vehicles_percentage(self.actor, 40)

    def init_passive_driver(self):
        self.tm.auto_lane_change(self.actor, False)
        self.tm.random_right_lanechange_percentage(self.actor, 0)
        self.tm.random_left_lanechange_percentage(self.actor, 0)
        self.tm.vehicle_percentage_speed_difference(self.actor, self.speed_limit_scale)
        self.tm.distance_to_leading_vehicle(self.actor, self.min_front_distance)
        self.tm.ignore_lights_percentage(self.actor, 100)
        self.actor.set_autopilot(True)

    def force_overtake(self, speed, overtake_direction):
        self.force_lane_change(right=overtake_direction == 1)
        # self.actor.setThrottle(speed)

    def force_lane_change(self, right=False):
        self.tm.force_lane_change(self.actor, right)

    def start_drive(self):
        self.actor.set_autopilot(True)
