#!/usr/bin/env python

# Copyright (c) 2018 Intel Labs.
# authors: German Ros (german.ros@intel.com)
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

""" Module with auxiliary functions. """

import math
import numpy as np

from typing import TYPE_CHECKING

import carla

from classes.constants import RoadOptionColor # pylint: disable=unused-import

if TYPE_CHECKING:
    from agents.navigation.local_planner import RoadOption
    from agents.lunatic_agent import LunaticAgent
    from classes.worldmodel import GameFramework
    # also checkout RoadOptionColor

__all__ = [
    'roadoption_color',
    'draw_waypoints',
    'draw_route',
    'get_speed',
    'get_trafficlight_trigger_location',
    'is_within_distance',
    'compute_magnitude_angle',
    'distance_vehicle',
    'vector',
    'compute_distance',
    'positive',
]


def draw_waypoints(world : carla.World, waypoints: "list[carla.Waypoint]", z=0.5, *, road_options: "list[RoadOption]"=None, **kwargs):
    """
    Draw a list of waypoints at a certain height given in z.

        :param world: carla.world object
        :param waypoints: list or iterable container with the waypoints to draw
        :param z: height in meters
    """
    if road_options:
        colors = [roadoption_color(o) for o in road_options]
    elif 'colors' in kwargs:
        colors = kwargs.pop('colors')
    else:
        color = kwargs.pop('color', (255, 0, 0))
        if not isinstance(color, carla.Color):
            color = carla.Color(*color)
        colors = [color] * len(waypoints)
    kwargs.setdefault('life_time', 1.0)
    kwargs.setdefault('arrow_size', 0.3)
    for wpt, color in zip(waypoints, colors):
        wpt_t = wpt.transform
        begin = wpt_t.location + carla.Location(z=z)
        angle = math.radians(wpt_t.rotation.yaw)
        end = begin + carla.Location(x=math.cos(angle), y=math.sin(angle))
        world.debug.draw_arrow(begin, end, color=color, **kwargs)
        
def roadoption_color(option: "RoadOption") -> carla.Color:
    """
    Returns the RoadOptionColor for the given RoadOption.
    
    Approximately executes:
    
    if option == RoadOption.LEFT:  # Yellow
        return carla.Color(128, 128, 0)
    elif option == RoadOption.RIGHT:  # Cyan
        return carla.Color(0, 128, 128)
    elif option == RoadOption.CHANGELANELEFT:  # Orange
        return carla.Color(128, 32, 0)
    elif option == RoadOption.CHANGELANERIGHT:  # Dark Cyan
        return carla.Color(0, 32, 128)
    elif option == RoadOption.STRAIGHT:  # Gray
        return carla.Color(64, 64, 64)
    else:  # LANEFOLLOW
        return carla.Color(0, 128, 0)  # Green
    """
    return RoadOptionColor(option)
    
def _draw_route_trans(world: carla.World, waypoints: "list[tuple[carla.Transform, RoadOption]]", vertical_shift=0.5, size=0.3, downsample=1, life_time=1.0):
    """
    Draw a list of waypoints at a certain height given in vertical_shift.
    
    * NOTE: This is based on the one from the leaderboard project.
    """
    for i, w in enumerate(waypoints):
        if i % downsample != 0:
            continue

        color = roadoption_color(w[1])

        wp = w[0].location + carla.Location(z=vertical_shift)
        world.debug.draw_point(wp, size=size, color=color, life_time=life_time)

    world.debug.draw_point(waypoints[0][0].location + carla.Location(z=vertical_shift), size=2*size,
                                color=carla.Color(0, 0, 128), life_time=life_time)
    world.debug.draw_point(waypoints[-1][0].location + carla.Location(z=vertical_shift), size=2*size,
                                color=carla.Color(128, 128, 128), life_time=life_time)
    
def _draw_route_wp(world: carla.World, waypoints: "list[tuple[carla.Waypoint, RoadOption]]", vertical_shift=0.5, size=0.3, downsample=1, life_time=1.0):
    """
    Draw a list of waypoints at a certain height given in vertical_shift.
    
    * NOTE: This is based on the one from the leaderboard project.
    """
    for i, w in enumerate(waypoints):
        if i % downsample != 0:
            continue

        color = roadoption_color(w[1])

        wp = w[0].transform.location + carla.Location(z=vertical_shift)
        world.debug.draw_point(wp, size=size, color=color, life_time=life_time)

    world.debug.draw_point(waypoints[0][0].transform.location + carla.Location(z=vertical_shift), size=2*size,
                                color=carla.Color(0, 0, 128), life_time=life_time)
    world.debug.draw_point(waypoints[-1][0].transform.location + carla.Location(z=vertical_shift), size=2*size,
                                color=carla.Color(128, 128, 128), life_time=life_time)
    
def draw_route(world: carla.World, waypoints: "list[tuple[carla.Transform | carla.Waypoint, RoadOption]]", vertical_shift=0.5, size=0.3, downsample=1, life_time=1.0):
    """
    Draw a list of waypoints at a certain height given in vertical_shift.
    
    * NOTE: This is based on the one from the leaderboard project.
    """
    if len(waypoints) == 0:
        return
    if isinstance(waypoints[0][0], carla.Transform):
        _draw_route_trans(world, waypoints, vertical_shift, size, downsample, life_time)
    elif isinstance(waypoints[0][0], carla.Waypoint):
        _draw_route_wp(world, waypoints, vertical_shift, size, downsample, life_time)
    else:
        print("Drawing of type:", type(waypoints[0][0]), "not supported.")


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


def debug_drawing(agent:"LunaticAgent", game_framework : "GameFramework", destination:carla.Waypoint):
    # Import here to avoid circular imports
    from launch_tools import CarlaDataProvider
    from agents.tools import lane_explorer
    from agents.navigation.local_planner import RoadOption
    
    world_model = game_framework.world_model
    
    # Debug drawing of the route
    try:
        destination = agent._local_planner._waypoints_queue[-1][0].transform.location # TODO find a nicer way
        destination = destination + carla.Vector3D(0, 0, 1.5) # elevate to be not in road
    except IndexError:
        pass
    game_framework.debug.draw_point(destination, life_time=0.5)
    lane_explorer.draw_waypoint_info(game_framework.debug, agent._current_waypoint, lt=10)
    if agent._current_waypoint.is_junction:
        junction = agent._current_waypoint.get_junction()
        lane_explorer.draw_junction(game_framework.debug, junction, 0.1)
    if not agent._last_traffic_light:
        traffic_light = agent.live_info.next_traffic_light
    else:
        traffic_light = agent._last_traffic_light
    
    if traffic_light:
        wps = traffic_light.get_stop_waypoints()
        for wp in wps:
            game_framework.debug.draw_point(wp.transform.location + carla.Location(z=2), life_time=0.6)
            lane_explorer.draw_waypoint_info( game_framework.debug, wp)
        trigger_loc = get_trafficlight_trigger_location(traffic_light)
        trigger_wp = CarlaDataProvider.get_map().get_waypoint(trigger_loc)
        game_framework.debug.draw_point(trigger_wp.transform.location + carla.Location(z=2), life_time=0.6, size=0.2, color=carla.Color(0,0,255))
        
        affected_wps = traffic_light.get_affected_lane_waypoints()
        
        draw_route(world_model.world, 
                    waypoints=[ (wp, RoadOption.LANEFOLLOW) for wp in trigger_wp.next_until_lane_end(0.4) ], 
                    size=0.1)
        draw_route(world_model.world, 
                    waypoints=[ (wp, RoadOption.STRAIGHT) for wp in trigger_wp.next_until_lane_end(0.4) ], 
                    size=0.1)
        draw_route(world_model.world, 
                    waypoints=[ (wp, RoadOption.LEFT) for wp in affected_wps ], 
                    size=0.1)

