import random
from typing import TYPE_CHECKING, Optional

from agents.tools.logging import logger

if TYPE_CHECKING:
    import carla

    from agents.lunatic_agent import LunaticAgent
    from classes.constants import Hazard

def emergency_manager(self : "LunaticAgent", *, reasons:"set[Hazard]", control : Optional["carla.VehicleControl"]=None, force=False) -> "carla.VehicleControl":
    """
    Modifies the control values to perform an emergency stop.
    The steering remains unchanged to avoid going out of the lane during turns.

    Parameters:
        reasons: set of :py:class:`.Hazard` that triggered the emergency stop.
            If empty this function will do nothing. Normally :py:attr:`detected_hazards <.LunaticAgent.detected_hazards>`.
        control: control to be modified in place.
            If :code:`None` the control for the current step will be calculated.
        force: if True, the emergency stop will be performed even if the **reasons**  are empty.
    """
    control = control or self.get_control()
    if control is None:
        control = self._calculate_control(debug=self.debug)
    if not reasons and not force:
        return control
    logger.debug("Emergency Manager: Hazards not cleared or forced stopping. Reason: %s", reasons)

    # TODO, future: Can be turned into a rule. Problem here and with rule it will trigger each step -> new random value
    # rule should return consistent result for a period of time
    if self.config.emergency.ignore_percentage > 0.0 and self.config.emergency.ignore_percentage / 100 > random.random():
        return control
    
    control.throttle = 0.0
    # negate the chosen default setting
    if self.config.emergency.hand_brake_modify_chance > 0.0 and self.config.emergency.hand_brake_modify_chance / 100 > random.random():
        control.hand_brake = not self.config.emergency.hand_brake
    else:
        control.hand_brake = self.config.emergency.hand_brake

    # Enable random steering if flagged
    if self.config.emergency.do_random_steering:
        control.steer = random.uniform(*self.config.emergency.random_steering_range)  # Randomly adjust steering

    control.brake = self.config.controls.max_brake

    # TODO: more sophisticated emergency behavior

    return control
