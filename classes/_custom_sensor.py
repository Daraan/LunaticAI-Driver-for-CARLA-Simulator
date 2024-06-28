from functools import wraps
from launch_tools import CarlaDataProvider

import carla

__all__ = ['CustomSensor']

class CustomSensor(object):
    """
    This is a mixin for classes like the `CameraManager` or the `RssSensor`
    that either wrap around carla.Sensors or should have a similar interface.
    """

    sensor : carla.Sensor

    def destroy(self):
        """Destroys the sensor"""
        if self.sensor is not None:
            self.stop()
            if CarlaDataProvider.actor_id_exists(self.sensor.id):
                # Note after https://github.com/carla-simulator/scenario_runner/pull/1091
                # x = CarlaDataProvider.remove_actor_by_id(self.sensor.id)
                CarlaDataProvider.remove_actor_by_id(self.sensor.id)
                x = "Actor was probably destroyed by"
            else:
                x = self.sensor.destroy()
            self.sensor = None
            return x
        
    def stop(self):
        if self.sensor is None:
            return
        if isinstance(self.sensor, carla.Sensor):
            if self.sensor.is_listening():
                self.sensor.stop()
        else:
            self.sensor.stop()

    def __del__(self):
        if self.sensor is not None:
            self.stop()
            self.destroy()
