# pyright: basic
#!/usr/bin/env python

# Copyright (c) 2018 Intel Labs.
# authors: German Ros (german.ros@intel.com)
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

""" Module with auxiliary functions. """

import math
import numpy as np

import carla

from agents.tools import debug_drawing
from agents.tools.debug_drawing import draw_waypoints


__all__ = [
    'draw_waypoints',
    'get_speed',
    'get_trafficlight_trigger_location',
    'is_within_distance',
    'compute_magnitude_angle',
    'distance_vehicle',
    'vector',
    'compute_distance',
    'positive'
]

def get_speed(vehicle, kmh=True, vel=None):
    """
    Compute speed of a vehicle in Km/h.

        :param vehicle: the vehicle for which speed is calculated
        :param kmh: boolean to convert speed to km/h
        :param vel: (optional) velocity of the vehicle.
            Note: 
                Should be from vehicle.get_velocity() 
                or CarlaDataProvider.get_velocity(vehicle)
        :return: speed as a float in Km/h
    """
    # Importing CarlaDataProvider is circular import as it uses this module
    #vel = CarlaDataProvider.get_velocity(vehicle)
    if not vel:
        vel = vehicle.get_velocity()
        vel = math.sqrt(vel.x ** 2 + vel.y ** 2 + vel.z ** 2)
    if kmh:
        return 3.6 * vel
    return vel


def get_trafficlight_trigger_location(traffic_light: carla.TrafficLight):
    """
    Calculates the yaw of the waypoint that represents the trigger volume of the traffic light
    """

    def rotate_point(point, radians):
        """
        rotate a given point by a given angle
        """
        rotated_x = math.cos(radians) * point.x - math.sin(radians) * point.y
        rotated_y = math.sin(radians) * point.x - math.cos(radians) * point.y

        return carla.Vector3D(rotated_x, rotated_y, point.z)

    base_transform = traffic_light.get_transform()
    base_rot = base_transform.rotation.yaw
    area_loc = base_transform.transform(traffic_light.trigger_volume.location)
    area_ext = traffic_light.trigger_volume.extent

    point = rotate_point(carla.Vector3D(0, 0, area_ext.z), math.radians(base_rot))
    point_location = area_loc + carla.Location(x=point.x, y=point.y)

    return carla.Location(point_location.x, point_location.y, point_location.z)


def is_within_distance(target_transform, reference_transform, max_distance, angle_interval=None):
    """
    Check if a location is both within a certain distance from a reference object.
    By using 'angle_interval', the angle between the location and reference transform
    will also be taken into account, being 0 a location in front and 180, one behind.

    :param target_transform: location of the target object
    :param reference_transform: location of the reference object
    :param max_distance: maximum allowed distance
    :param angle_interval: only locations between [min, max] angles will be considered. This isn't checked by default.
    :return: boolean
    """
    target_vector = np.array([
        target_transform.location.x - reference_transform.location.x,
        target_transform.location.y - reference_transform.location.y
    ])
    norm_target = np.linalg.norm(target_vector)

    # If the vector is too short, we can simply stop here
    if norm_target < 0.001:
        return True

    # Further than the max distance
    if norm_target > max_distance:
        return False

    # We don't care about the angle, nothing else to check
    if not angle_interval:
        return True

    min_angle = angle_interval[0]
    max_angle = angle_interval[1]

    fwd = reference_transform.get_forward_vector()
    forward_vector = np.array([fwd.x, fwd.y])
    angle = math.degrees(math.acos(np.clip(np.dot(forward_vector, target_vector) / norm_target, -1., 1.)))

    return min_angle < angle < max_angle


def compute_magnitude_angle(target_location, current_location, orientation):
    """
    Compute relative angle and distance between a target_location and a current_location

        :param target_location: location of the target object
        :param current_location: location of the reference object
        :param orientation: orientation of the reference object
        :return: a tuple composed by the distance to the object and the angle between both objects
    """
    target_vector = np.array([target_location.x - current_location.x, target_location.y - current_location.y])
    norm_target = np.linalg.norm(target_vector)

    forward_vector = np.array([math.cos(math.radians(orientation)), math.sin(math.radians(orientation))])
    d_angle = math.degrees(math.acos(np.clip(np.dot(forward_vector, target_vector) / norm_target, -1., 1.)))

    return (norm_target, d_angle)


def distance_vehicle(waypoint, vehicle_transform):
    """
    Returns the 2D distance from a waypoint to a vehicle

        :param waypoint: actual waypoint
        :param vehicle_transform: transform of the target vehicle
    """
    loc = vehicle_transform.location
    x = waypoint.transform.location.x - loc.x
    y = waypoint.transform.location.y - loc.y

    return math.sqrt(x * x + y * y)


def vector(location_1, location_2):
    """
    Returns the unit vector from location_1 to location_2

        :param location_1, location_2: carla.Location objects
    """
    x = location_2.x - location_1.x
    y = location_2.y - location_1.y
    z = location_2.z - location_1.z
    norm = np.linalg.norm([x, y, z]) + np.finfo(float).eps

    return [x / norm, y / norm, z / norm]


def compute_distance(location_1, location_2):
    """
    Euclidean distance between 3D points

        :param location_1, location_2: 3D points
    """
    x = location_2.x - location_1.x
    y = location_2.y - location_1.y
    z = location_2.z - location_1.z
    norm = np.linalg.norm([x, y, z]) + np.finfo(float).eps
    return norm


def positive(num):
    """
    Return the given number if positive, else 0

        :param num: value to check
    """
    return num if num > 0.0 else 0.0

def lanes_have_same_direction(wp1: carla.Waypoint, wp2: carla.Waypoint) -> bool:
    """
    Check if two lanes have the same direction, i.e. their lane ids
    have the same sign.

        :param wp1: first waypoint
        :param wp2: second waypoint
        
    Returns:
        True if the lanes have the same direction, False otherwise
    """
    return wp1.lane_id * wp2.lane_id > 0


def get_closest_tl_trigger_wp(reference_location: carla.Location, traffic_light: carla.TrafficLight):
    """
    Finds the closest triggering waypoint of the traffic light group to the reference location.

    Args:
        reference_location (carla.Location): The reference location to measure the distance from.
        traffic_light (carla.TrafficLight): The traffic light object.

    Returns:
        carla.Waypoint: The closest traffic light trigger waypoint to the reference location.
        float: The distance between the reference location and the closest waypoint.
    """
    affected_wps = traffic_light.get_affected_lane_waypoints()
    distance = float("inf")
    for wp in affected_wps:
        test_distance = reference_location.distance(wp.transform.location)
        if test_distance < distance:
            closest_wp = wp
            distance = test_distance
    return closest_wp, distance


# patch, to avoid import in function
debug_drawing.get_trafficlight_trigger_location = get_trafficlight_trigger_location # type: ignore
