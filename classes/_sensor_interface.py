from functools import wraps
from launch_tools import CarlaDataProvider

import carla

__all__ = ['CustomSensorInterface']

class CustomSensorInterface(object):
    """
    This is a mixin for classes like the :py:class:`.camere_manager.CameraManager` or the :py:class:`classes.rss_sensor.RssSensor`
    that either wrap around a :py:class:`carla.Sensor` or should have a similar interface.
    
    Not to be confused with :py:class:`srunner.autoagents.sensor_interface.SensorInterface`.
    """

    sensor : carla.Sensor

    def destroy(self):
        """Stops and destroys the actor of the sensor"""
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
        """
        Stop the :py:attr:`sensor` if its in listening mode.
        """
        if self.sensor is None:
            return
        if isinstance(self.sensor, carla.Sensor):
            if self.sensor.is_listening():
                self.sensor.stop()
        else:
            self.sensor.stop()

    def __del__(self):
        """
        Calls :py:meth:`stop` and :py:meth:`destroy` when the object is deleted.
        
        :meta public:
        """
        if self.sensor is not None:
            self.stop()
            self.destroy()
