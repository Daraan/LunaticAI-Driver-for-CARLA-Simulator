import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import carla
    from agents.lunatic_agent import LunaticAgent

def emergency_manager(self : "LunaticAgent", control : "carla.VehicleControl", reason : str):
    """
    Modifies the control values to perform an emergency stop.
    The steering remains unchanged to avoid going out of the lane during turns.

    :param control: (carla.VehicleControl) control to be modified
    :param enable_random_steer: (bool, optional) Flag to enable random steering
    """
    print("Emergency stop", reason)
    if control is None:
        control = self._local_planner.run_step()

    # TODO, future: Use rules here.
    if self.config.emergency.ignore_percentage > 0.0 and self.config.emergency.ignore_percentage / 100 > random.random():
        return control
    
    control.throttle = 0.0
    # negate the chosen default setting
    if self.config.emergency.hand_brake_modify_chance > 0.0 and self.config.emergency.hand_brake_modify_chance / 100 > random.random():
        control.hand_brake = not self.config.emergency.use_hand_brake
    else:
        control.hand_brake = self.config.emergency.use_hand_brake

    # Enable random steering if flagged
    if self.config.emergency.do_random_steering:
        control.steer = random.uniform(*self.config.emergency.random_steering_range)  # Randomly adjust steering

    control.brake = self.config.controls.max_brake

    # TODO: more soffisticated emergency behavior

    return control