"""
This package provides classes from the original CARLA PythonAPI/examples, included as is or
with slight modifications.

The sensor classes are wrappers for different :external_py_class:`carla.Sensor` types
which used to provide data for the :py:class:`HUD` on the :external_py_mod:`pygame`
interface.

See Also:
    https://github.com/carla-simulator/carla/tree/dev/PythonAPI/examples
"""
from .sensors import CollisionSensor, GnssSensor, IMUSensor, LaneInvasionSensor, RadarSensor

__all__ = [
    'CollisionSensor',
    'GnssSensor',
    'IMUSensor',
    'LaneInvasionSensor',
    'RadarSensor'
]
