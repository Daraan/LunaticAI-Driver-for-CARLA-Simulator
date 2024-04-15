from launch_tools import CarlaDataProvider

import carla

__all__ = ['CustomSensor']

class CustomSensor(object):

    sensor : carla.Sensor

    def destroy(self):
        """Destroys the sensor"""
        if self.sensor is not None:
            try:
                self.sensor.stop()
            except AttributeError:
                pass
            if CarlaDataProvider.actor_id_exists(self.sensor.id):
                CarlaDataProvider.remove_actor_by_id(self.sensor.id)
            else:
                self.sensor.destroy()
            self.sensor = None
            return

    def __del__(self):
        if self.sensor is not None:
            self.destroy()