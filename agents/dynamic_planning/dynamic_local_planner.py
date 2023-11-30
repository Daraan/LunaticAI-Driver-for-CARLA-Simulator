# Copyright (c) # Copyright (c) 2018-2020 CVC.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

""" This module contains a local planner to perform low-level waypoint following based on PID controllers. """

from agents.navigation import local_planner 
from agents.navigation.local_planner import LocalPlanner, RoadOption

from collections import deque
import random

import carla
from agents.dynamic_planning.dynamic_controller import DynamicVehiclePIDController
from agents.tools.misc import draw_waypoints, get_speed

from omegaconf import DictConfig

'''
# left here for reference
class RoadOption(IntEnum):
    """
    RoadOption represents the possible topological configurations when moving from a segment of lane to other.

    """
    VOID = -1
    LEFT = 1
    RIGHT = 2
    STRAIGHT = 3
    LANEFOLLOW = 4
    CHANGELANELEFT = 5
    CHANGELANERIGHT = 6
'''


class DynamicLocalPlanner(LocalPlanner):
    """
    LocalPlanner implements the basic behavior of following a
    trajectory of waypoints that is generated on-the-fly.

    The low-level motion of the vehicle is computed by using two PID controllers,
    one is used for the lateral control and the other for the longitudinal control (cruise speed).

    When multiple paths are available (intersections) this local planner makes a random choice,
    unless a given global plan has already been specified.
    """

    def __init__(self, vehicle, opt_dict : DictConfig, map_inst=None, world=None):
        """
        :param vehicle: actor to apply to local planner logic onto
        :param opt_dict: dictionary of arguments with different parameters:
            dt: time between simulation steps
            target_speed: desired cruise speed in Km/h
            sampling_radius: distance between the waypoints part of the plan
            lateral_control_dict: values of the lateral PID controller
            longitudinal_control_dict: values of the longitudinal PID controller
            max_throttle: maximum throttle applied to the vehicle
            max_brake: maximum brake applied to the vehicle
            max_steering: maximum steering applied to the vehicle
            offset: distance between the route waypoints and the center of the lane
        :param map_inst: carla.Map instance to avoid the expensive call of getting it.
        """
        self._vehicle = vehicle
        self.config = opt_dict
        self._world = world or self._vehicle.get_world()
        try: 
            if map_inst:
                if isinstance(map_inst, carla.Map):
                    self._map : carla.Map= map_inst
                else:
                    print("Warning: Ignoring the given map as it is not a 'carla.Map'")
                    self._map : carla.Map = self._world.get_map()
            else:
                self._map : carla.Map = self._world.get_map()
        except AttributeError as e:
            print(e)

        self._vehicle_controller = None
        self.target_waypoint = None
        self.target_road_option = None

        self._waypoints_queue = deque(maxlen=10000)
        self._min_waypoint_queue_length = 100
        self._stop_waypoint_creation = False

        # initializing controller
        self._init_controller()


    def _init_controller(self):
        """Controller initialization"""
        self._vehicle_controller = DynamicVehiclePIDController(self._vehicle, self.config)

        # Compute the current vehicle waypoint
        current_waypoint = self._map.get_waypoint(self._vehicle.get_location())
        self.target_waypoint, self.target_road_option = (current_waypoint, RoadOption.LANEFOLLOW)
        self._waypoints_queue.append((self.target_waypoint, self.target_road_option))

    def set_speed(self, speed):
        """
        Changes the target speed

        :param speed: new target speed in Km/h
        :return:
        """
        if self.config.speed.follow_speed_limits:
            print("WARNING: The max speed is currently set to follow the speed limits. "
                  "Use 'follow_speed_limits' to deactivate this")
        self.config.speed.target_speed = speed

    def follow_speed_limits(self, value=True):
        """
        Activates a flag that makes the max speed dynamically vary according to the speed limits

        :param value: bool
        :return:
        """
        self.config.speed.follow_speed_limits = value

    @property # allows to use _compute_next_waypoints of parent
    def _sampling_radius(self):
        return self.config.planer.sampling_radius 

    # set_global_plan -> parent

    def run_step(self, debug=False):
        """
        Execute one step of local planning which involves running the longitudinal and lateral PID controllers to
        follow the waypoints trajectory.

        :param debug: boolean flag to activate waypoints debugging
        :return: control to be applied
        """
        if self.config.speed.follow_speed_limits:
            # TODO: check this config
            self.config.speed.target_speed = self._vehicle.get_speed_limit()

        # Add more waypoints too few in the horizon
        if not self._stop_waypoint_creation and len(self._waypoints_queue) < self._min_waypoint_queue_length:
            self._compute_next_waypoints(k=self._min_waypoint_queue_length)

        # Purge the queue of obsolete waypoints
        veh_location = self._vehicle.get_location()
        vehicle_speed = get_speed(self._vehicle) / 3.6
        self._min_distance = self.config.distance.base_min_distance + self.config.distance.distance_ratio * vehicle_speed

        num_waypoint_removed = 0
        for waypoint, _ in self._waypoints_queue:

            if len(self._waypoints_queue) - num_waypoint_removed == 1:
                min_distance = 1  # Don't remove the last waypoint until very close by
            else:
                min_distance = self._min_distance

            if veh_location.distance(waypoint.transform.location) < min_distance:
                num_waypoint_removed += 1
            else:
                break

        if num_waypoint_removed > 0:
            for _ in range(num_waypoint_removed):
                self._waypoints_queue.popleft()

        # Get the target waypoint and move using the PID controllers. Stop if no target waypoint
        if len(self._waypoints_queue) == 0:
            control = carla.VehicleControl()
            control.steer = 0.0
            control.throttle = 0.0
            control.brake = 1.0
            control.hand_brake = False
            control.manual_gear_shift = False
        else:
            self.target_waypoint, self.target_road_option = self._waypoints_queue[0]
            control = self._vehicle_controller.run_step(self.config.speed.target_speed, self.target_waypoint)

        if debug:
            draw_waypoints(self._vehicle.get_world(), [self.target_waypoint], 1.0)

        return control

# def get_incoming_waypoint_and_direction(self, steps=3):
  
