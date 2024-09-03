from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal

import carla

__all__ = ['CustomSensorInterface']

class CustomSensorInterface:
    """
    This is a mixin for classes like the :py:class:`.camera_manager.CameraManager` or the :py:class:`classes.rss_sensor.RssSensor`
    that either wrap around a :external_py_class:`carla.Sensor` or should have a similar interface.
    
    Attention:
        Not to be confused with :py:class:`srunner.autoagents.sensor_interface.SensorInterface`.
    """

    sensor : carla.Sensor

    def destroy(self) -> 'bool | None | Literal["Actor was probably destroyed by the CarlaDataProvider"]':
        """Stops and destroys the actor of the sensor"""
        from launch_tools import CarlaDataProvider  # pylint: disable=import-outside-toplevel # noqa: PLC0415, avoid circular import
        if self.sensor is not None:
            self.stop()
            if CarlaDataProvider.actor_id_exists(self.sensor.id):
                # Note after https://github.com/carla-simulator/scenario_runner/pull/1091
                # x = CarlaDataProvider.remove_actor_by_id(self.sensor.id)
                CarlaDataProvider.remove_actor_by_id(self.sensor.id)
                destroyed = "Actor was probably destroyed by the CarlaDataProvider"
            else:
                destroyed = self.sensor.destroy()
            self.sensor = None  # type: ignore
            return destroyed
        return None
        
    def stop(self) -> None:
        """
        Stop the :py:attr:`sensor` if its in listening mode.
        If it is a :external_py_class:`carla.Sensor`, calls the simulator.
        """
        if self.sensor is None:  # type: ignore
            return
        if isinstance(self.sensor, carla.Sensor):
            if self.sensor.is_listening():
                self.sensor.stop()  # NOTE: calls simulation
        else:
            self.sensor.stop()  # type: ignore

    def __del__(self):
        """
        Calls :py:meth:`stop` and :py:meth:`destroy` when the object is deleted.
        
        :meta public:
        """
        try:
            if self.sensor is not None:
                self.stop()
                self.destroy()
        except Exception:
            pass
