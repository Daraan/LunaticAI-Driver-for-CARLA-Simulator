import numpy as np
import carla

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent
from agents.tools.misc import get_speed
__epsilon = np.nextafter(0., 1.) # to not divide by 0

def car_following_manager(self:"LunaticAgent", vehicle : carla.Vehicle, distance:float, debug:bool=False) -> carla.VehicleControl:
        """
        Module in charge of car-following behaviors when there's
        someone in front of us.

            :param vehicle: car to follow
            :param distance: distance from vehicle
            :param debug: boolean for debugging
            :return control: carla.VehicleControl
        """

        vehicle_speed = get_speed(vehicle)
        delta_v = max(1, (self.config.live_info.current_speed - vehicle_speed) / 3.6)
        ttc = (distance / delta_v if delta_v != 0  # TimeTillCollision
               else distance / __epsilon  # do not divide by 0,
               )

        # Under safety time distance, slow down.
        if self.config.speed.safety_time > ttc > 0.0:
            target_speed = min([
                max(0.0, vehicle_speed - self.config.speed.speed_decrease),
                self.config.speed.max_speed,
                self.config.live_info.current_speed_limit - self.config.speed.speed_lim_dist])
            self._local_planner.set_speed(target_speed)
            control = self._local_planner.run_step(debug=debug)

        # Actual safety distance area, try to follow the speed of the vehicle in front.
        elif 2 * self.config.speed.safety_time > ttc >= self.config.speed.safety_time:
            target_speed = min([
                max(self.config.speed.min_speed, vehicle_speed),
                self.config.speed.max_speed,
                self.config.live_info.current_speed_limit - self.config.speed.speed_lim_dist])
            self._local_planner.set_speed(target_speed)
            control = self._local_planner.run_step(debug=debug)

        # Normal behavior.
        else:
            target_speed = min([
                self.config.speed.max_speed,
                self.config.live_info.current_speed_limit - self.config.speed.speed_lim_dist])
            self._local_planner.set_speed(target_speed)
            control = self._local_planner.run_step(debug=debug)

        return control