"""
Module to add high-level semantic return types for obstacle and traffic light detection results via named tuples.

The code is compatible with Python 2.7, <3.6 and >=3.6. The later uses the typed version of named tuples.
"""


# Carla code with compatibility
'''
import sys
if sys.version_info < (3, 6):
    from collections import namedtuple
    ObstacleDetectionResult = namedtuple('ObstacleDetectionResult', ['obstacle_was_found', 'obstacle', 'distance'])
    TrafficLightDetectionResult = namedtuple('TrafficLightDetectionResult', ['traffic_light_was_found', 'traffic_light'])
else:
    from typing import NamedTuple, Union, TYPE_CHECKING
    from carla import Actor, TrafficLight
    """
    # Python 3.6+, incompatible with Python 2.7 syntax
    class ObstacleDetectionResult(NamedTuple):
        obstacle_was_found : bool
        obstacle : Union[Actor, None]
        distance : float 
        # distance : Union[float, Literal[-1]] # Python 3.8+ only

    class TrafficLightDetectionResult(NamedTuple):
        traffic_light_was_found : bool
        traffic_light : Union[TrafficLight, None]
    """
    if TYPE_CHECKING:
        from typing import Literal
        ObstacleDetectionResult = NamedTuple('ObstacleDetectionResult', [('obstacle_was_found', bool), ('obstacle', Union[Actor, None]), ('distance', Union[float, Literal[-1]])])
    else:
        ObstacleDetectionResult = NamedTuple('ObstacleDetectionResult', [('obstacle_was_found', bool), ('obstacle', Union[Actor, None]), ('distance', float)])
    
    TrafficLightDetectionResult = NamedTuple('TrafficLightDetectionResult', [('traffic_light_was_found', bool), ('traffic_light', Union[TrafficLight, None])])
'''

# Modern Python 3.6+ syntax for better type hinting

from typing import NamedTuple, Optional, Union
from launch_tools import Literal
import carla

class TrafficLightDetectionResult(NamedTuple):
    traffic_light_was_found : bool
    """"""
    traffic_light : Optional[carla.TrafficLight]
    """The found traffic light. If no traffic light was found, the value is None."""
    
    def __bool__(self):
        """
        Returns:
            Value of :py:attr:`traffic_light_was_found`.
        """
        return self.traffic_light_was_found


# Use proper NamedTuples (Python 3.6+) and not the compatibility version from carla
class ObstacleDetectionResult(NamedTuple):
    obstacle_was_found : bool
    """"""
    obstacle : Optional[carla.Actor]
    """The found actor that represents the obstacle."""
    distance : Union[float, Literal[-1]]
    """The distance to the obstacle. If no obstacle was found, the distance is -1."""
    
    def __bool__(self) -> bool:
        """
        Returns:
            Value of :py:attr:`obstacle_was_found`.
        """
        return self.obstacle_was_found


class CameraBlueprint(NamedTuple):
    """
    Represents a camera blueprint to spawn a camera sensor 
    to be used with the :py:class:`CameraManager`.
    """
    # TODO: Should be turned into a TypedDict instead of a NamedTuple to handle the setting of actual_blueprint better

    blueprint_path : str
    """Blueprint name for the actor"""
    color_convert : carla.ColorConverter
    """Color converter for the camera"""
    name : str
    """Semantic name of the blueprint, e.g. RGB, Segmentation"""
    actual_blueprint : Optional[carla.ActorBlueprint] = None
    """The actual blueprint object; filled in later"""

