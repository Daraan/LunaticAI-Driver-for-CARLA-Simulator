# pylint: disable=unused-import
"""
This package contains helper classes and constants used in this project.

The classes from :py:mod:`carla_originals` are mostly identical to the
ones provided in the examples from the CARLA PythonAPI.

.. include:: /docs/Classes.rst

----------------

"""

__all__ = [
    "CustomSensorInterface",
    "carla_originals",
]

from . import carla_originals

from ._sensor_interface import CustomSensorInterface
