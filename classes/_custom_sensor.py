from functools import wraps
from launch_tools import CarlaDataProvider

import carla

__all__ = ['CustomSensor']

class CustomSensor(object):

    sensor : carla.Sensor

    def destroy(self):
        """Destroys the sensor"""
        if self.sensor is not None:
            self.stop()
            if CarlaDataProvider.actor_id_exists(self.sensor.id):
                CarlaDataProvider.remove_actor_by_id(self.sensor.id)
                x = "Likely true"
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
