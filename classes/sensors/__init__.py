"""
This package implements different sensors classes to be used with the :py:class:`.HUD`
for the :py:mod:`pygame` user interface, as well as the :py:class:`.rss_sensor.RssSensor`.
"""

__all__ = [
    "CustomSensorInterface",
    "carla_originals",
]

from . import carla_originals
from ._sensor_interface import CustomSensorInterface
