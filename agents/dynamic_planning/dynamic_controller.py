# Copyright (c) # Copyright (c) 2018-2020 CVC.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

""" This module contains PID controllers to perform lateral and longitudinal control. """

from collections import deque
import math
import numpy as np
import carla

from agents.navigation.controller import VehiclePIDController, PIDLongitudinalController, PIDLateralController

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents.tools.config_creation import BasicAgentSettings
    from agents.lunatic_agent import LunaticAgent

STEERING_UPDATE_SPEED = 0.1

class DynamicVehiclePIDController(VehiclePIDController):
    """
    VehiclePIDController is the combination of two PID controllers
    (lateral and longitudinal) to perform the
    low level control a vehicle from client side
    """

    @property
    def config(self):
        return self._agent.ctx.config

    def __init__(self, agent : "LunaticAgent"):
        """
        Constructor method.

        :param vehicle: actor to apply to local planner logic onto
        :param args_lateral: dictionary of arguments to set the lateral PID controller
        using the following semantics:
            K_P -- Proportional term
            K_D -- Differential term
            K_I -- Integral term
        :param args_longitudinal: dictionary of arguments to set the longitudinal
        PID controller using the following semantics:
            K_P -- Proportional term
            K_D -- Differential term
            K_I -- Integral term
        :param offset: If different than zero, the vehicle will drive displaced from the center line.
        Positive values imply a right offset while negative ones mean a left one. Numbers high enough
        to cause the vehicle to drive through other lanes might break the controller.
        """
        self._agent = agent
        self._vehicle = agent._vehicle
        self._world = self._vehicle.get_world()

        self.past_steering = self._vehicle.get_control().steer
        self._lon_controller = DynamicPIDLongitudinalController(agent)
        self._lat_controller = DynamicPIDLateralController(agent)

    def run_step(self, waypoint):
        # type: (carla.Waypoint) -> carla.VehicleControl
        """
        Execute one step of control invoking both lateral and longitudinal
        PID controllers to reach a target waypoint
        at a given target_speed.

            :param target_speed: desired vehicle speed
            :param waypoint: target location encoded as a waypoint
            :return: distance (in meters) to the waypoint
        """
        acceleration = self._lon_controller.run_step()
        current_steering = self._lat_controller.run_step(waypoint)
        control = carla.VehicleControl()
        if acceleration >= 0.0:
            control.throttle = min(acceleration, self.config.controls.max_throttle)
            control.brake = 0.0
        else:
            control.throttle = 0.0
            control.brake = min(abs(acceleration), self.config.controls.max_brake)

        # Steering regulation: changes cannot happen abruptly, can't steer too much.

        # NOTE: here could add some too fast too slow steering update.
        if current_steering > self.past_steering + STEERING_UPDATE_SPEED:
            current_steering = self.past_steering + STEERING_UPDATE_SPEED
        elif current_steering < self.past_steering - STEERING_UPDATE_SPEED:
            current_steering = self.past_steering - STEERING_UPDATE_SPEED

        if current_steering >= 0:
            steering = min(self.config.controls.max_steering, current_steering)
        else:
            steering = max(-self.config.controls.max_steering, current_steering)

        control.steer = steering
        control.hand_brake = False
        control.manual_gear_shift = False
        self.past_steering = steering

        return control

    def change_longitudinal_PID(self, args_longitudinal):
        """Changes the parameters of the PIDLongitudinalController"""
        self._lon_controller.change_parameters(**args_longitudinal)

    def change_lateral_PID(self, args_lateral):
        """Changes the parameters of the PIDLateralController"""
        self._lat_controller.change_parameters(**args_lateral)


class DynamicPIDLongitudinalController(PIDLongitudinalController):
    """
    PIDLongitudinalController implements longitudinal control using a PID.
    """

    @property
    def config(self):
        return self._agent.ctx.config

    def __init__(self, agent: "LunaticAgent"):
        """
        Constructor method.

            :param vehicle: actor to apply to local planner logic onto
            :param K_P: Proportional term
            :param K_D: Differential term
            :param K_I: Integral term
            :param dt: time differential in seconds
        """
        self._agent = agent
        self._vehicle = agent._vehicle
        self._error_buffer = deque(maxlen=10)
        
    def run_step(self, debug=False):
        """
        Execute one step of longitudinal control to reach a given target speed.

            :param target_speed: target speed in Km/h
            :param debug: boolean for debugging
            :return: throttle control
        """
        current_speed = self.config.live_info.current_speed
        if debug:
            print('Current speed = {}'.format(current_speed))

        target_speed = self.config.speed.target_speed
        return self._pid_control(target_speed, current_speed)

    def _pid_control(self, target_speed, current_speed):
        """
        Estimate the throttle/brake of the vehicle based on the PID equations

            :param target_speed:  target speed in Km/h
            :param current_speed: current speed of the vehicle in Km/h
            :return: throttle/brake control
        """

        error = target_speed - current_speed
        self._error_buffer.append(error)

        if len(self._error_buffer) >= 2:
            _de = (self._error_buffer[-1] - self._error_buffer[-2]) / self.config.planner.dt
            _ie = sum(self._error_buffer) * self.config.planner.dt
        else:
            _de = 0.0
            _ie = 0.0

        return np.clip((self.config.planner.longitudinal_control_dict.K_P * error) + (self.config.planner.longitudinal_control_dict.K_D * _de) + (self.config.planner.longitudinal_control_dict.K_I * _ie), -1.0, 1.0)

    def change_parameters(self, K_P, K_I, K_D, dt):
        """Changes the PID parameters"""
        self.config.planner.longitudinal_control_dict.K_P = K_P
        self.config.planner.longitudinal_control_dict.K_I = K_I
        self.config.planner.longitudinal_control_dict.K_D = K_D
        self.config.planner.dt = dt


class DynamicPIDLateralController(PIDLateralController):
    """
    PIDLateralController implements lateral control using a PID.
    """

    @property
    def config(self):
        return self._agent.ctx.config

    def __init__(self, agent : "LunaticAgent"):
        """
        Constructor method.

            :param vehicle: actor to apply to local planner logic onto
            :param offset: distance to the center line. If might cause issues if the value
                is large enough to make the vehicle invade other lanes.
            :param K_P: Proportional term
            :param K_D: Differential term
            :param K_I: Integral term
            :param dt: time differential in seconds
        """
        self._agent = agent
        self._vehicle = agent._vehicle
        self._e_buffer = deque(maxlen=10)

    def _pid_control(self, waypoint : carla.Waypoint, vehicle_transform : carla.Transform):
        """
        Estimate the steering angle of the vehicle based on the PID equations

            :param waypoint: target waypoint
            :param vehicle_transform: current transform of the vehicle
            :return: steering control in the range [-1, 1]
        """
        # Get the ego's location and forward vector
        ego_loc = vehicle_transform.location
        v_vec = vehicle_transform.get_forward_vector()
        v_vec = np.array([v_vec.x, v_vec.y, 0.0])

        # Get the vector vehicle-target_wp
        if self.config.planner.offset != 0:
            # Displace the wp to the side
            w_tran = waypoint.transform
            r_vec = w_tran.get_right_vector()
            w_loc = w_tran.location + carla.Location(x=self.config.planner.offset*r_vec.x,
                                                     y=self.config.planner.offset*r_vec.y)
        else:
            w_loc = waypoint.transform.location

        w_vec = np.array([w_loc.x - ego_loc.x,
                          w_loc.y - ego_loc.y,
                          0.0])

        wv_linalg = np.linalg.norm(w_vec) * np.linalg.norm(v_vec)
        if wv_linalg == 0:
            _dot = 1
        else:
            _dot = math.acos(np.clip(np.dot(w_vec, v_vec) / (wv_linalg), -1.0, 1.0))
        _cross = np.cross(v_vec, w_vec)
        if _cross[2] < 0: # TODO: Why is this mentioned as unbound
            _dot *= -1.0

        self._e_buffer.append(_dot)
        if len(self._e_buffer) >= 2:
            _de = (self._e_buffer[-1] - self._e_buffer[-2]) / self.config.planner.dt
            _ie = sum(self._e_buffer) * self.config.planner.dt
        else:
            _de = 0.0
            _ie = 0.0

        return np.clip((self.config.planner.lateral_control_dict.K_P * _dot) + (self.config.planner.lateral_control_dict.K_D * _de) + (self.config.planner.lateral_control_dict.K_I * _ie), -1.0, 1.0)

    def change_parameters(self, K_P, K_I, K_D, dt):
        """Changes the PID parameters"""
        self.config.planner.lateral_control_dict.K_P = K_P
        self.config.planner.lateral_control_dict.K_I = K_I
        self.config.planner.lateral_control_dict.K_D = K_D
        self.config.planner.dt = dt
