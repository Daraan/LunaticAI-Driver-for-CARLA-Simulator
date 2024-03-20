import carla
import numpy as np

import agents.navigation.behavior_types as _behavior_types
from agents.navigation.behavior_agent import BehaviorAgent

behavior_types = vars(_behavior_types)


class BadEmergencyHandlingAgent(BehaviorAgent):
    def emergency_stop(self):
        """
        Overwrites the throttle a brake values of a control to perform an emergency stop.
        The steering is kept the same to avoid going out of the lane when stopping during turns

            :param speed (carl.VehicleControl): control to be modified
        """
        control = carla.VehicleControl()
        control.throttle = 0.0
        control.brake = self._max_brake
        control.hand_brake = False
        control.steer = np.random.random() - 1
        return control

    def add_emergency_stop(self, control):
        """
        Overwrites the throttle a brake values of a control to perform an emergency stop.
        The steering is kept the same to avoid going out of the lane when stopping during turns

            :param speed (carl.VehicleControl): control to be modified
        """
        control.throttle = 0.0
        control.brake = self._max_brake
        control.hand_brake = False
        control.steer = np.random.random() - 1
        return control
