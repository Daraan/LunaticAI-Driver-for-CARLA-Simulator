from __future__ import annotations

import collections
import math
from operator import attrgetter
from typing import List, NamedTuple, Optional, Set

import carla
import numpy as np
from cachetools import LRUCache, cached

from agents.tools.logging import logger
from launch_tools import CarlaDataProvider


class RoadLaneId(NamedTuple):
    road_id: int
    lane_id: int
    
    def __str__(self) -> str:
        return f"{self.road_id}_{self.lane_id}"

def check_ego_on_highway(ego_vehicle_location, road_lane_ids, world_map):
    """
    Check if the ego vehicle is on a highway based on its location. The function considers the ego vehicle to be on a highway if:
        - it's on a road that has at least six lanes
        - or if it's on a road with a set of lanes with consecutive lane identifiers (e.g., 1, 2, 3) and contains at least three lanes
          because a city road with more than three lanes is missing lane_id=0 (e.g., -2, -1, 1, 2)

    Args:
        ego_vehicle_location (carla.Location): The current location of the ego vehicle.
        road_lane_ids (list): A list of all road-lane identifiers of the map, where each identifier is a string
            in the format "roadId_laneId". For example, ["1_2", "2_1", "3_2"].
        world_map (carla.Map): A carla object representing the map of the world.

    Returns:
        bool: True if the ego vehicle is on a highway, False otherwise.
    """
    # get waypoints of ego and its left and right lanes
    waypoints: List[carla.Waypoint] = []
    ego_waypoint = world_map.get_waypoint(ego_vehicle_location)
    waypoints.append(ego_waypoint)
    if ego_waypoint.get_left_lane() is not None:
        waypoints.append(ego_waypoint.get_left_lane())
    if ego_waypoint.get_right_lane() is not None:
        waypoints.append(ego_waypoint.get_right_lane())
    
    # check for all waypoints if they are on a highway, in case they have different road_id's
    for wp in waypoints:
        ego_vehicle_road_id = wp.road_id
        # get all lanes of the respective road
        lanes = [rl_id[1] for rl_id in road_lane_ids if ego_vehicle_road_id == rl_id[0]]
        # cast lane_id's to int and check for highway condition
        lanes = [int(lane) for lane in lanes]
        if len(lanes) >= 6 or (
            sorted(lanes) == list(range(min(lanes), max(lanes) + 1)) and len(lanes) >= 3
        ):
            return True

    return False

_all_lane_ids: 'list[Set[RoadLaneId]]' = []
"""List of length 1 of RoadLaneId sets to check if the lane ids are consistent"""

# @functools.lru_cache(maxsize=1) # Faster but not safe when changing the map without changing the map object/ or clearing the cache
@cached(cache=LRUCache(maxsize=1), key=attrgetter("name"))
def get_all_road_lane_ids(world_map : carla.Map):
    """
    Retrieve a set of unique road and lane identifiers in the format "roadId_laneId" from the given world map.

    Args:
        world_map (carla.Map): The map of the world from which road and lane identifiers are obtained.

    Returns:
        set: A set containing unique road and lane identifiers in the format "roadId_laneId".
    """
    road_lane_ids : Set[RoadLaneId] = set()

    # iterate through all waypoints in the world map
    for waypoint in world_map.generate_waypoints(1.0):
        # extract lane and road id's
        lane_id = waypoint.lane_id
        road_id = waypoint.road_id
        # add road and lane identifiers to set
        road_lane_ids.add(RoadLaneId(road_id, lane_id))

    _all_lane_ids.append(road_lane_ids)
    if len(_all_lane_ids) > 1:
        match = _all_lane_ids[0] == _all_lane_ids[1]
        if match:
            _all_lane_ids.pop(0)
        else:
            raise ValueError("Lane ids do not match")

    return road_lane_ids

def distance(p1, p2):
    """Define a function to calculate the distance between two points (carla Location objects).

    Args:
        p1 (carla.Location): First location object.
        p2 (carla.Location): Second location object.

    Returns:
        float: Distance between point 1 and 2.
    """
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)

def create_city_matrix(ego_vehicle_location: carla.Location,
                       road_lane_ids: "set[RoadLaneId]",
                       world_map: carla.Map,
                       ghost: bool=False,
                       ego_on_bad_highway_street:bool=False) -> Optional["dict[str | tuple[int, int], list[int]]"]:
    """
    Create a matrix representing the lanes around the ego vehicle.

    Parameters:
        ego_vehicle_location (carla.Location): The location object of ego vehicle for which to create the city matrix.
        road_lane_ids (list): A list of all road-lane identifiers of the map, where each identifier is a string in the format "roadId_laneId".
            Format: ["1_2", "2_1", "3_2"].
        world_map (carla.Map): The map representing the environment.
        ghost (bool): Ghost mode when ego is exiting/entering a highway - fix a location of an imaginary vehicle on highway to correctly build matrix from this ghost perspective.
        ego_on_bad_highway_street (bool): Indicates that ego is on the right lane of a highway that is an exit/entry and accounts as another road_id

    Returns:
        collections.OrderedDict: An ordered dictionary representing the city matrix. The keys for existing lanes are the lane IDs in the format "road_id_lane_id".
            For non-existing lanes different placeholder exist, e.g.  left_outer_lane, left_inner_lane, No_4th_lane, No_opposing_direction
            The values indicate whether a vehicle is present: 0 - No vehicle, 1 - Ego vehicle, 3 - No road.
            Format example: {
                "left_outer_lane": [3, 3, 3, 3, 3, 3, 3, 3],
                "left_inner_lane": [3, 3, 3, 3, 3, 3, 3, 3],
                "1_2": [0, 0, 0, 0, 0, 0, 0, 0],
                "1_1": [0, 0, 0, 0, 0, 0, 0, 0],
                "1_-1": [0, 0, 0, 0, 0, 0, 0, 0],
                "1_-2": [0, 0, 0, 0, 0, 0, 0, 0],
                "right_inner_lane": [3, 3, 3, 3, 3, 3, 3, 3],
                "right_outer_lane": [3, 3, 3, 3, 3, 3, 3, 3],
            }
    """
    # Get lane & road id for ego_vehicle
    ego_vehicle_waypoint = world_map.get_waypoint(ego_vehicle_location)
    ego_vehicle_lane_id = ego_vehicle_waypoint.lane_id
    #logger.info("ego_vehicle_lane_id: ", ego_vehilce_lane_id)
    ego_vehicle_road_id = ego_vehicle_waypoint.road_id

    # get all lanes of ego's road
    lanes = sorted(rl_id[1] for rl_id in road_lane_ids if ego_vehicle_road_id == rl_id[0])
    lanes = [int(l_id) for l_id in lanes] # TODO: should be redundant
    
    # split lanes into directions & sort, e.g. [-2,-1,1,2] -> [[-2,-1],[2,1]]
    lanes_splitted: list[list[int]] = []
    z = 0
    for i in range(1, len(lanes)):
        if lanes[i] == lanes[i - 1] - 1 or lanes[i] == lanes[i - 1] + 1:
            continue
        else:
            lanes_splitted.append(lanes[z:i])
            z = i
    lanes_splitted.append(lanes[z:])
    lanes_splitted = [
        sorted(direction, key=abs, reverse=True) for direction in lanes_splitted
    ]

    # Initialize matrix and key_value_pairs
    matrix = None
    key_value_pairs: Optional[list[tuple["str | tuple[int, int]", list[int]]]] = None
    other_direction = []
    ego_direction = []
    # Identify list of lanes of ego's direction and opposite direction
    for direction in lanes_splitted:
        if ego_vehicle_lane_id in direction:
            ego_direction = direction
        else:
            other_direction = direction
    
    if len(ego_direction) >= 4:
        # ego is on a highway with 4 or more lanes
        key_value_pairs = [
            ("left_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("left_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            (
                (ego_vehicle_road_id, ego_direction[3]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                (ego_vehicle_road_id, ego_direction[2]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                (ego_vehicle_road_id, ego_direction[1]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                (ego_vehicle_road_id, ego_direction[0]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            ("right_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("right_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
        ]
    
    elif len(ego_direction) == 3:
        # ego is on highway with 3 lanes, i.e. the 4th lane is most likely an exit/entry
        key_value_pairs = [
            ("left_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("left_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            (
                (ego_vehicle_road_id, ego_direction[2]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                (ego_vehicle_road_id, ego_direction[1]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                (ego_vehicle_road_id, ego_direction[0]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            ("No_4th_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("right_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("right_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
        ]

    elif len(ego_direction) == 2 and len(other_direction) == 2:
        # ego is on normal city road with 2 lanes in each direction
        key_value_pairs = [
            ("left_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("left_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            (
                (ego_vehicle_road_id, other_direction[0]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                (ego_vehicle_road_id, other_direction[1]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                (ego_vehicle_road_id, ego_direction[1]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                (ego_vehicle_road_id, ego_direction[0]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            ("right_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("right_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
        ]
        
    elif len(ego_direction) == 2 and len(other_direction) == 0:
        # ego is on road with 2 lanes in one direction and no lanes in the other direction
        key_value_pairs = [
            ("left_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("left_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("No_opposing_direction", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("No_opposing_direction", [3, 3, 3, 3, 3, 3, 3, 3]),
            (
                (ego_vehicle_road_id, ego_direction[1]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                (ego_vehicle_road_id, ego_direction[0]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            ("right_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("right_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
        ]
        
    elif len(ego_direction) == 1 and len(other_direction) == 1:
        # ego is on normal road with 1 lane in each direction
        key_value_pairs = [
            ("left_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("left_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("No_opposing_direction", [3, 3, 3, 3, 3, 3, 3, 3]),
            (
                (ego_vehicle_road_id, other_direction[0]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                (ego_vehicle_road_id, ego_direction[0]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            ("No_own_right_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("right_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("right_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
        ]
        
    elif len(ego_direction) == 1 and len(other_direction) == 0:
        # ego is on road with 1 lane in one direction and no lanes in the other direction
        key_value_pairs = [
            ("left_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("left_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("No_other_right_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("No_opposing_direction", [3, 3, 3, 3, 3, 3, 3, 3]),
            (
                (ego_vehicle_road_id, ego_direction[0]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            ("No_own_right_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("right_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("right_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
        ]
    else:
        # Unsupported case
        # Keep at info level to allow suppression
        logger.info("Could not infer road type to create city matrix")

    # Update matrix
    if key_value_pairs:
        matrix = collections.OrderedDict(key_value_pairs)
    
    # Insert ego in matrix, in case ego is not entering/exiting a highway
    if matrix and not ghost:
        try:
            if ego_on_bad_highway_street:
                if int(ego_vehicle_lane_id) > 0:
                    matrix[ego_vehicle_road_id, ego_vehicle_lane_id + 1][3] = 1
                else:
                    matrix[ego_vehicle_road_id, ego_vehicle_lane_id - 1][3] = 1
            else:
                matrix[ego_vehicle_road_id, ego_vehicle_lane_id][3] = 1
        except KeyError:
            matrix[ego_vehicle_road_id, ego_vehicle_lane_id][3] = 1
    return matrix

# NOTE: sub function of detect_surrounding_cars
def check_road_change(ego_vehicle_location, road_lane_ids, front, world_map):
    """
    Determine if the ego vehicle is about to change to a different road (in next/previous 60m).

    Parameters:
        ego_vehicle_location (carla.Location): The location of the ego vehicle for which we want to check the road change.
        road_lane_ids (list): A list of all road-lane identifiers of the map, where each identifier is a string in the format "roadId_laneId".
            Format: ["1_2", "2_1", "3_2"].
        front (bool): If True, check the road change in the front direction of the ego vehicle,
                      otherwise check in the rear direction.
        world_map (carla.Map): The map representing the environment.

    Returns:
        tuple: A tuple containing two elements:
            - next_road_id (str): The ID of the next/previous road if the ego vehicle is about to change
                                 to a different road, otherwise None.
            - next_lanes (list of str): A list of lane IDs of the next/previous road if the ego vehicle is
                                        about to change to a different road, otherwise None.
    """
    ego_vehicle_waypoint = world_map.get_waypoint(ego_vehicle_location)
    
    # get first waypoint infront of / behind ego vehicle that is not on the same road id
    if front: # look in front of ego vehicle
        for i in range(1, 60, 5):
            next_waypoint = ego_vehicle_waypoint.next(i)[0]
            if next_waypoint.road_id != ego_vehicle_waypoint.road_id:
                break
    else: # look behind ego vehicle
        for i in range(1, 60, 5):
            next_waypoint = ego_vehicle_waypoint.previous(i)[0]
            if next_waypoint.road_id != ego_vehicle_waypoint.road_id:
                break

    # get road_id and lanes of road in front of / behind ego vehicle
    next_lanes = None
    next_road_id = None
    if next_waypoint.road_id != ego_vehicle_waypoint.road_id:
        next_road_id = next_waypoint.road_id
        next_lanes = [
            rl_id[1]
            for rl_id in road_lane_ids
            if next_road_id == rl_id[0]
        ]
        
    # get lanes of ego vehicle's road
    our_lanes = [
        rl_id[1]
        for rl_id in road_lane_ids
        if ego_vehicle_waypoint.road_id == rl_id[0]
    ]
    
    # return next_road_id and next_lanes if they exist, otherwise return None
    if next_lanes:
        next_lanes.sort()
        our_lanes.sort()
    if next_lanes == our_lanes:
        return (next_road_id, next_lanes) # TODO: add semantics
    else:
        return (None, None)

def detect_surrounding_cars(
    ego_location : carla.Location,
    ego_vehicle :  carla.Actor,
    matrix : dict[str | tuple[int, int], list[int]],
    road_lane_ids : set[RoadLaneId],
    world,
    radius,
    on_highway,
    highway_shape,
    ghost=False,
):
    """
    Detect surrounding cars and update the base matrix accordingly.

    Parameters:
        ego_location (carla.Location): The location object of the ego vehicle.
        ego_vehicle (carla.Vehicle): The ego vehicle for which to detect surrounding cars.
        matrix (collections.OrderedDict): An ordered dictionary representing the city matrix. The keys for existing lanes are the lane IDs in the format "road_id_lane_id".
            For non-existing lanes different placeholder exist, e.g.  left_outer_lane, left_inner_lane, No_4th_lane, No_opposing_direction.
            The values indicate whether a vehicle is present: 0 - No vehicle, 1 - Ego vehicle, 3 - No road.
            Format example: {
                "left_outer_lane": [3, 3, 3, 3, 3, 3, 3, 3],
                "left_inner_lane": [3, 3, 3, 3, 3, 3, 3, 3],
                "1_2": [0, 0, 0, 0, 0, 0, 0, 0],
                "1_1": [0, 0, 0, 0, 0, 0, 0, 0],
                "1_-1": [0, 0, 0, 1, 0, 0, 0, 0],
                "1_-2": [0, 0, 0, 0, 0, 0, 0, 0],
                "right_inner_lane": [3, 3, 3, 3, 3, 3, 3, 3],
                "right_outer_lane": [3, 3, 3, 3, 3, 3, 3, 3]}
        road_lane_ids (list): A list of all road-lane identifiers of the map, where each identifier is a string in the format "roadId_laneId".
            Format: ["1_2", "2_1", "3_2"].
        world (carla.World): The game world where the simulation is running.
        radius (int): The radius within which to detect surrounding cars.
        on_highway (bool): True if the ego vehicle is on a highway, False otherwise.
        highway_shape (tuple): Tuple containing highway_type, number of straight highway lanes, entry waypoint tuple and/ exit waypoint tuple.
            Format: (highway_type: string, straight_lanes: int, entry_wps: ([wp,..], [wp,..]), exit_wps: ([wp,..], [wp,..]))
        ghost (bool): Ghost mode when ego is exiting/entering a highway - fix a location of an imaginary vehicle on highway to correctly build matrix from this ghost perspective.

    Returns:
        collections.OrderedDict: The updated city matrix with detected surrounding cars.
            Format example: {
                "left_outer_lane": [3, 3, 3, 3, 3, 3, 3, 3],
                "left_inner_lane": [3, 3, 3, 3, 3, 3, 3, 3],
                "1_2": [0, 0, 2, 0, 0, 0, 0, 0],
                "1_1": [0, 0, 0, 0, 0, 0, 0, 0],
                "1_-1": [0, 2, 0, 1, 0, 2, 0, 0],
                "1_-2": [0, 0, 0, 0, 0, 0, 0, 0],
                "right_inner_lane": [3, 3, 3, 3, 3, 3, 3, 3],
                "right_outer_lane": [3, 3, 3, 3, 3, 3, 3, 3],

    """
    world_map = CarlaDataProvider.get_map()
    ego_vehicle_waypoint = world_map.get_waypoint(ego_location)
    ego_vehicle_road_id = ego_vehicle_waypoint.road_id

    # Get all surrounding cars in specified radius
    surrounding_cars = []
    surrounding_cars_on_highway_entryExit = []
    for actor in world.get_actors():
        if "vehicle" in actor.type_id and (actor.id != ego_vehicle.id or ghost):
            distance_to_actor = distance(actor.get_location(), ego_location)
            if distance_to_actor <= radius:
                surrounding_cars.append(actor)

    # check if road id changes before/behind ego vehicle, if yes get list of lane_id's of next/previous road
    _, next_lanes = check_road_change(ego_location, road_lane_ids, True, world_map)
    _, prev_lanes = check_road_change(ego_location, road_lane_ids, False, world_map)
    lanes_exist_further = False
    lanes = [rl_id[1] for rl_id in road_lane_ids if ego_vehicle_road_id == rl_id[0]]
    try:
        if next_lanes and matrix:
            # lanes = [road_lane.split("_")[1] for road_lane in matrix.keys()]
            lanes_exist_further = all(lane in next_lanes for lane in lanes) or all(
                lane in lanes for lane in next_lanes
            )
    except IndexError:
        pass

    lanes_existed_before = False
    try:
        if prev_lanes and matrix:
            # lanes = [road_lane.split("_")[1] for road_lane in matrix.keys()]
            lanes_existed_before = all(lane in prev_lanes for lane in lanes) or all(
                lane in lanes for lane in prev_lanes
            )
    except IndexError:
        pass

    # in the following, ignore cars that are on highway exit/entry lanes
    if highway_shape is not None:
        entry_wps = highway_shape[2] # Tuple with start and end waypoint of the entry: ([start_wp, start_wp..], [end_wp, end_wp..])
        exit_wps = highway_shape[3]  # Tuple with start and end waypoint of the exit: ([start_wp, start_wp..], [end_wp, end_wp..])

        # get all road id's of entry and exit and previous/next road
        entry_road_ids = []
        exit_road_ids = []
        entry_city_road = [] # road before an entry in city
        exit_city_road = [] # road after an exit in city
        entry_highway_road: list[int] # road after an entry on highway
        exit_highway_road : list[int] # road before an exit on highway
        if entry_wps:
            for entry_wp in entry_wps[0]: # entry_wps[0] contains all start waypoints of entry
                entry_city_road.append(entry_wp.previous(3)[0].road_id)
                entry_road_ids.append(entry_wp.road_id)
            # TODO: Check if all cars on highway entry are captured: especially on road after entry on highway
            if (entry_wp.next(3)[0] and entry_wp.next(3)[0].get_left_lane()
                    and entry_wp.next(3)[0].road_id == entry_wp.next(3)[0].get_left_lane().road_id):
                entry_highway_road = []
            else:
                entry_highway_road = [entry_wp.next(3)[0].road_id for entry_wp in entry_wps[1]]
        else:
            entry_highway_road = []
        if exit_wps:
            for exit_wp in exit_wps[1]: # exit_wps[1] contains all end waypoints of exit
                exit_city_road.append(exit_wp.next(3)[0].road_id)
                exit_road_ids.append(exit_wp.road_id)
            # TODO: Check if all cars on highway exit are captured: especially on road before exit on highway
            if (exit_wp.next(3)[0] and exit_wp.next(3)[0].get_left_lane()
                    and exit_wp.next(3)[0].road_id == exit_wp.next(3)[0].get_left_lane().road_id):
                exit_highway_road = []
            else:
                exit_highway_road = [exit_wp.previous(3)[0].road_id for exit_wp in exit_wps[0]]
        else:
            entry_highway_road = []
            
        road_ids: list[int] = entry_road_ids + entry_city_road + exit_road_ids + exit_city_road + exit_highway_road + entry_highway_road

    # Update matrix based on the lane and position/distance to ego vehicle of other car
    if (
        on_highway
        and highway_shape is not None  # below are bound if this is True
        and ego_vehicle_road_id in road_ids
    ):
        surrounding_cars_on_highway_entryExit.append(ego_vehicle)
    
    ego_on_highway = check_ego_on_highway(ego_location, road_lane_ids, world_map)
    
    # Update matrix based on the lane and position/distance to ego vehicle of other car
    for car in surrounding_cars:
        # Get road and lane_id of other car
        other_car_waypoint = world_map.get_waypoint(car.get_location())
        other_car_lane_id = other_car_waypoint.lane_id
        other_car_road_id = other_car_waypoint.road_id
        other_car_road_lane_id = RoadLaneId(other_car_road_id, other_car_lane_id)

        # ignore car on highway entry / Exit bc. considered in update_matrix()
        if (
            on_highway
            and highway_shape is not None
            and other_car_road_id in road_ids
        ):
            surrounding_cars_on_highway_entryExit.append(car)
            continue
        
        # get column in matrix of other car
        col = calculate_position_in_matrix(
            ego_location,
            ego_vehicle,
            car,
            matrix,
            world_map,
            #ego_vehicle.get_velocity(),
            ego_on_highway=ego_on_highway,
            ghost=ghost,
        )
        
        if col is None:
            continue
        
        # insert car in matrix
        if matrix:
            # if road id & lane id of other exist already in matrix (normal case, w/o other car on different road_id in front/behind)
            if other_car_road_lane_id in matrix.keys():
                if car.id == ego_vehicle.id:
                    matrix[other_car_road_lane_id][col] = 1
                else:
                    matrix[other_car_road_lane_id][col] = 2
                continue
            
            # elif road id changes in front / behind then place other car based on lane id
            elif (lanes_exist_further or lanes_existed_before) and (
                other_car_lane_id
             in [road_lane[1] for road_lane in matrix.keys()]):
                if car.id == ego_vehicle.id:
                    matrix[(ego_vehicle_road_id, other_car_lane_id)][
                        col
                    ] = 1
                else:
                    try:
                        matrix[(ego_vehicle_road_id, other_car_lane_id)][
                            col
                        ] = 2
                    except Exception:
                        pass

    return matrix, surrounding_cars_on_highway_entryExit

def check_car_in_front_or_behind(ego_location: carla.Location,
                                 other_location: carla.Location,
                                 rotation: carla.Rotation) -> float:
    """
    Check if other car is in front or behind ego vehicle.

    Args:
        ego_location (carla.Location): The location object of the ego vehicle.
        other_location (carla.Location): The location object of the other car.
        rotation (carla.Rotation): The rotation object of the ego vehicle.

    Returns:
        float: The dot_product between forward vectors (similarity between the vectors): dot_product > 0 ==> in front, dot_product < 0 ==> behind
    """
    # Get ego to other vector location
    ego_to_other_vector = other_location - ego_location
    # Calculate forward vector of ego
    ego_forward_vector = rotation.get_forward_vector()
    
    # Calculate dot_product (similarity between the vectors):
    # dot_product > 0 ==> in front, dot_product < 0 ==> behind
    # ignore z component
    return ego_to_other_vector.dot_2d(ego_forward_vector)

def get_forward_vector_distance(ego_vehicle_location: carla.Location,
                                other_car: carla.Actor,
                                world_map: carla.Map) -> float:
    """
    Calculate the distance between point B (other vehicle) and point C (parallel point right/left of ego on lane of other vehicle) in a right-angled triangle.

    Parameters:
        ego_vehicle_location (carla.Location): The location of the ego vehicle in 3D space.
        other_car_location (carla.Location): The location of the other car in 3D space.
        world_map (carla.WorldMap): The map representing the environment.

    Returns:
        float: The distance between perpendicular_wp (waypoint left/right in parallel to ego) and other car in triangle calculation.
    """

    # Get the location of the other car
    other_car_location = other_car.get_location()

    # Calculate straight line distance between ego and other car
    distance_ego_other = ego_vehicle_location.distance(other_car_location)

    # Get waypoints
    ego_waypoint = world_map.get_waypoint(ego_vehicle_location)
    other_waypoint = world_map.get_waypoint(other_car_location)

    other_lane_id = other_waypoint.lane_id

    # get perpendicular waypoint (either ego_waypoint or waypoint on left/right lane of ego_waypoint), which is on same lane as other car
    left_lane_wp, right_lane_wp = ego_waypoint, ego_waypoint
    old_left_lane_wps, old_right_lane_wps = [], []
    while True:
        # termination condition: perpendicular waypoint not found, return straight distance
        if (not left_lane_wp or left_lane_wp.id in old_left_lane_wps) and (
            not right_lane_wp or right_lane_wp.id in old_right_lane_wps
        ):
            return distance_ego_other
        
        # if ego is on same lane as other then we can use straight distance calculation
        if ego_waypoint.lane_id == other_lane_id:
            return distance_ego_other
        
        # check if one waypoint to the left is on same lane as other car
        if left_lane_wp:
            old_left_lane_wps.append(left_lane_wp.id)
            left_lane_wp = left_lane_wp.get_left_lane()
            if left_lane_wp:
                if left_lane_wp.lane_id == other_lane_id:
                    perpendicular_wp = left_lane_wp
                    break
        
        # check if one waypoint to the right is on same lane as other car
        if right_lane_wp:
            old_right_lane_wps.append(right_lane_wp.id)
            right_lane_wp = right_lane_wp.get_right_lane()
            if right_lane_wp:
                if right_lane_wp.lane_id == other_lane_id:
                    perpendicular_wp = right_lane_wp
                    break


    # calculate distance between ego and perpendicular waypoint (i.e. distance we go left/right in parallel to street)
    distance_opposite = ego_vehicle_location.distance(
        perpendicular_wp.transform.location
    )

    # return distance between perpendicular_wp and other car in right-angled triangle
    return math.sqrt(abs(distance_ego_other**2 - distance_opposite**2))

def calculate_position_in_matrix(
        ego_location: carla.Location,
        ego_vehicle: carla.Actor,
        other_car: carla.Actor,
        matrix,
        world_map,
        #velocity,
        *,
        ego_on_highway: bool,
        ghost: bool=False,
):
    """
    Calculate the position of the other car in the city matrix based on its relative location and distance from the ego vehicle.
    Only determines the column, not the row since that is based on the lane_id of the other car.

    Parameters:
        ego_location (carla.Location): The location object of the ego vehicle.
        ego_vehicle (carla.Vehicle): The ego vehicle for reference.
        other_car (carla.Vehicle): The other car whose position is to be determined.
        matrix (collections.OrderedDict): An ordered dictionary representing the city matrix.
            The keys for existing lanes are the lane IDs in the format "road_id_lane_id".
            For non-existing lanes different placeholder exist,
            e.g.  left_outer_lane, left_inner_lane, No_4th_lane, No_opposing_direction.
            The values indicate whether a vehicle is present: 0 - No vehicle, 1 - Ego vehicle, 3 - No road.
            Format example: {
                "left_outer_lane": [3, 3, 3, 3, 3, 3, 3, 3],
                "left_inner_lane": [3, 3, 3, 3, 3, 3, 3, 3],
                "1_2": [0, 0, 0, 0, 0, 0, 0, 0],
                "1_1": [0, 0, 0, 0, 0, 0, 0, 0],
                "1_-1": [0, 0, 0, 1, 0, 0, 0, 0],
                "1_-2": [0, 0, 0, 0, 0, 0, 0, 0],
                "right_inner_lane": [3, 3, 3, 3, 3, 3, 3, 3],
                "right_outer_lane": [3, 3, 3, 3, 3, 3, 3, 3],
        world_map (carla.WorldMap): The map representing the environment.
        ego_on_highway (bool): Wether the ego is on a highway, if so will consider greater distances.
        ghost (bool): Ghost mode when ego is exiting/entering a highway - fix a location of an
            imaginary vehicle on highway to correctly build matrix from this ghost perspective.

    Returns:
        int or None: The column index in the city matrix representing the column in the city matrix of the other car,
                    or None if the other car is not within the specified distance range.

    Note:
        The city matrix should be pre-generated using the 'create_basic_matrix' function.
        Other cars are detected using the detect_surrounding_cars func.
    """

    # Get ego vehicle rotation and location
    if ghost:
        rotation = other_car.get_transform().rotation # for simplicity use other actors rotation when in ghost mode
    else:
        rotation = ego_vehicle.get_transform().rotation

    # Get other car vehicle location
    other_location = other_car.get_transform().location

    # Calculate new distance: ego to other car
    new_distance = get_forward_vector_distance(ego_location, other_car, world_map)

    # Get distance between ego_vehicle and other car
    # NOTE: Unused, but could be useful for future extensions
    #distance_to_actor = other_location.distance(ego_location)

    # check if car is behind or in front of ego vehicle: dot_product > 0 ==> in front, dot_product < 0 ==> behind
    dot_product = check_car_in_front_or_behind(ego_location, other_location, rotation)

    # Get road_lane_id of other vehicle
    other_car_waypoint = world_map.get_waypoint(other_location)
    other_car_lane_id = other_car_waypoint.lane_id
    other_car_road_id = other_car_waypoint.road_id
    other_car_road_lane_id = (other_car_road_id, other_car_lane_id)

    # Get road_lane_id of ego vehicle
    # NOTE: Unused, but could be useful for future extensions
    #ego_car_waypoint = world_map.get_waypoint(ego_location)
    #ego_car_lane_id = ego_car_waypoint.lane_id
    #ego_car_road_id = ego_car_waypoint.road_id
    #ego_car_road_lane_id = (ego_car_road_id, ego_car_lane_id)

    # velocity = ego_vehicle.get_velocity()
    #ego_speed = (
    #        3.6 * (velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2) ** 0.5
    #)  # Convert m/s to km/h
    
    # if ego is on highway use different speed factor --> we look further ahead/behind on highway
    if ego_on_highway:
        speed_factor = 2.0
    else:
        speed_factor = 1

    col = None

    # Other car is in front of ego_vehicle
    if (
        abs(dot_product) < 4
        and other_car_road_lane_id in list(matrix.keys())
        and matrix[other_car_road_lane_id][3] != 1
    ):
        col = 3
    # Other car is in front of ego_vehicle
    elif dot_product > 0:
        if new_distance < 10 * speed_factor:
            col = 4
        elif new_distance < 20 * speed_factor:
            col = 5
        elif new_distance < 30 * speed_factor:
            col = 6
        elif new_distance < 40 * speed_factor:
            col = 7

    # Other car is behind ego_vehicle
    else:
        if new_distance < 10 * speed_factor:
            col = 2
        elif new_distance < 20 * speed_factor:
            col = 1
        elif new_distance < 30 * speed_factor:
            col = 0
    return col

#########################################
# help functions for junctions:
#########################################

##### General #####

def is_highway_junction(ego_vehicle, ego_wp, junction, road_lane_ids, direction_angle):
    """This function checks if the junction is a highway junction.
    
    Args:
        ego_vehicle (carla.Vehicle): The vehicle object of the ego vehicle.
        ego_wp (carla.Waypoint): Waypoint object of ego vehicle.
        junction (carla.Junction): Junction object to be tested if it is on highway.
        road_lane_ids (list): A list of all road-lane identifiers of the map, where each identifier is a string in the format "roadId_laneId".
            Format: ["1_2", "2_1", "3_2"].
        direction_angle (float): The angle used to determine directions from the ego vehicle.
        world_map (carla.Map): The map representing the environment.
    
    Returns:
        bool: Boolean indicating if the considered junction is a highway junction.
    """
    lanes_all, junction_roads = get_all_lanes(
        ego_vehicle, ego_wp, junction.get_waypoints(carla.LaneType().Driving), road_lane_ids, direction_angle
    )

    highway_junction = False
    for lanes in lanes_all.values():
        if len(lanes) >= 8:
            highway_junction = True
            break
    return highway_junction

def get_distance_junction_start(wp):
    """Get distance from waypoint until the first junction wp behind.

    Args:
        wp (carla.Waypoint): Initial waypoint to look back.

    Returns:
        int: Distance in meters from waypoint until the first junction wp behind.
    """
    x = 1
    while wp.previous(x)[0].is_junction:
        x = x + 1
    return x

def get_distance_junction_end(wp):
    """Get distance from waypoint until the first junction wp in front.

    Args:
        wp (carla.Waypoint): Initial waypoint to look in front.

    Returns:
        int: Distance in meters from waypoint until the first junction wp in front.
    """
    x = 1
    while wp.next(x)[0].is_junction:
        x = x + 1
    return x

def is_junction_ahead(ego_waypoint, distance):
    """
    Check if a junction is ahead of the ego vehicle within a specified distance.

    Parameters:
        ego_waypoint (carla.Waypoint): The current waypoint of the ego vehicle.
        distance (int): The maximum distance (in meters) to search for a junction ahead.

    Returns:
        bool: True if a junction is found ahead within the specified distance, False otherwise.
    """
    # return True if junction is ahead of ego in <= distance meter, start checking at 1m ahead and increment by 1 every loop
    for x in list(range(1, distance + 1)):
        if ego_waypoint.next(x)[0].is_junction:
            return True
    if ego_waypoint.is_junction:
        return True
    return False


def is_junction_behind(ego_waypoint, distance):
    """
    Check if a junction is ahead of the ego vehicle within a specified distance.

    Parameters:
        ego_waypoint (carla.Waypoint): The current waypoint of the ego vehicle.
        distance (int): The maximum distance (in meters) to search for a junction ahead.

    Returns:
        bool: True if a junction is found ahead within the specified distance, False otherwise.
    """
    # return True if junction is ahead of ego in <= distance meter, start checking at 1m ahead and increment by 1 every loop
    for x in list(range(1, distance + 1)):
        if ego_waypoint.previous(x)[0].is_junction:
            return True
    if ego_waypoint.is_junction:
        return True
    return False


def get_junction_ahead(ego_waypoint, distance):
    """
    Get the junction ahead of the ego vehicle within a specified distance.

    Parameters:
        ego_waypoint (carla.Waypoint): The current waypoint of the ego vehicle.
        distance (int): The maximum distance (in meters) to search for a junction ahead.

    Returns:
        carla.Junction or None: The carla.Junction object representing the junction ahead if found within
                                 the specified distance. Returns None if no junction is found.
    """

    for x in list(range(1, distance + 1)):
        if ego_waypoint.next(x)[0].is_junction:
            return ego_waypoint.next(x)[0].get_junction()
    if ego_waypoint.is_junction:
        return ego_waypoint.get_junction()
    return None


def get_junction_behind(ego_waypoint, distance):
    """
    Get the junction ahead of the ego vehicle within a specified distance.

    Parameters:
        ego_waypoint (carla.Waypoint): The current waypoint of the ego vehicle.
        distance (int): The maximum distance (in meters) to search for a junction ahead.

    Returns:
        carla.Junction or None: The carla.Junction object representing the junction ahead if found within
                                 the specified distance. Returns None if no junction is found.
    """
    for x in list(range(1, distance + 1)):
        if ego_waypoint.previous(x)[0].is_junction:
            return ego_waypoint.previous(x)[0].get_junction()
    if ego_waypoint.is_junction:
        return ego_waypoint.get_junction()
    return None


def get_waypoint_direction(
    ego_vehicle, closest_start_wp, junction_waypoint, direction_angle
):
    """
    Get the direction of a waypoint from ego vehicle's perspective relative to a junction.
    If ego approaches a junction, then junction wps can be classified as "straight", "left", or "right" roads entering the junction (from ego perspective).

    Parameters:
        ego_vehicle (carla.Vehicle): The ego vehicle for which to determine the direction.
        closest_start_wp (carla.Waypoint): The closest waypoint to the junction where the ego vehicle enters.
        junction_waypoint (carla.Waypoint): The waypoint representing the junction.
        direction_angle (float): The angle threshold in degrees to classify the direction.

    Returns:
        str: The direction of the waypoint relative to the ego vehicle and the junction.
             Possible return values: "straight", "left", or "right".
    """

    # Get the location of the ego vehicle when entering junction
    ego_location = closest_start_wp.transform.location

    point1_x = closest_start_wp.transform.location.x
    point1_y = closest_start_wp.transform.location.y
    next_waypoint = closest_start_wp.next(5)[0]
    point2_x = next_waypoint.transform.location.x
    point2_y = next_waypoint.transform.location.y

    # Calculate the vector components
    vector_x = point2_x - point1_x
    vector_y = point2_y - point1_y

    # Calculate the yaw angle
    yaw = math.atan2(vector_y, vector_x)
    yaw_degrees = math.degrees(yaw)
    ego_rotation = yaw_degrees
    # Get the orientation of the ego vehicle
    # NOTE: This was changed
    #ego_rotation_1 = ego_vehicle.get_transform().rotation.yaw
    #ego_rotation = ego_rotation_1
    
    # Get the location of the junction waypoint
    junction_location = junction_waypoint.transform.location

    # Calculate the angle between the ego vehicle and the junction waypoint
    angle = math.atan2(
        junction_location.y - ego_location.y, junction_location.x - ego_location.x
    )
    angle = math.degrees(angle)

    if abs(ego_rotation) > 100:
        if angle < 0:
            angle = 360 - abs(angle)
        if ego_rotation < 0:
            ego_rotation = 360 - abs(ego_rotation)

    # Calculate the difference between the angles
    angle_diff = angle - ego_rotation

    # Determine the direction of the junction waypoint
    if abs(angle_diff) < direction_angle:
        return "straight"
    elif angle_diff <= -direction_angle:
        return "left"
    else:
        return "right"


def detect_ego_before_junction(
        key_value_pairs, junction_roads, lanes_all, lane_id_ego, ego_wp, distance_to_junc, junction
):
    """
    Update the city matrix to detect the position of the ego vehicle relative to a junction.

    Parameters:
        key_value_pairs (list of tuples): A list of tuples representing the city matrix.
        junction_roads (list of tuples): A list of tuples containing road IDs and lane IDs of the junction.
        lanes_all (dict): A dictionary containing lane IDs of the roads around the junction.
        lane_id_ego (int): The lane ID of the ego vehicle.
        ego_wp (carla.Waypoint): The waypoint of the ego vehicle.
        distance_to_junc (int): The distance in meters from the ego vehicle to the junction.

    Returns:
        list of tuples: The updated city matrix with the position of the ego vehicle detected.
    """
    # detect ego before junction

    # cast lane id's to int
    for road in junction_roads:
        lanes_all[road[1]] = [int(l_id) for l_id in lanes_all[road[1]]]

    logger.info("all lanes %s", lanes_all)

    # check on which lane ego is: i=0 means most out
    if lane_id_ego > 0:
        lanes_all["ego"].sort(reverse=True)
    else:
        lanes_all["ego"].sort()
    for i in range(int(len(lanes_all["ego"]))):
        if lanes_all["ego"][i] == lane_id_ego:
            break  # i=0: lane most out

    # check how many lanes the roads right and left of ego have
    if len(lanes_all["left"]) == 0:
        columns = int((8 - len(lanes_all["right"])) / 2)
    elif len(lanes_all["right"]) == 0:
        columns = int((8 - len(lanes_all["left"])) / 2)
    else:
        columns = int(
            (8 - min([len(lanes_all["left"]), len(lanes_all["right"])])) / 2
        )  # min number of lanes of right/left

    # determine cell of ego in matrix
    if ego_wp.next(int(distance_to_junc / columns))[
        0
    ].is_junction:  # doesn't matter how many columns: write "1" in the cell clostest to junction inner part
        c = columns - 1
    elif columns == 2:  # if 2 columns that it must be the cell farsest away
        c = columns - 2
    elif ego_wp.next(int(distance_to_junc / columns) * 2)[
        0
    ].is_junction:  # if 3 columns check if junction is closer than 10m, then middle cell
        c = columns - 2
    else:  # if 3 columns and further away than 10m, then cell farsest away
        c = columns - 3
    if ego_wp.road_id == 23:
        return key_value_pairs

    for j in range(8):
        if key_value_pairs[-1 - j][1][c] != 3:
            key_value_pairs[-1 - j - i][1][c] = 1
            break

    return key_value_pairs


def detect_surrounding_cars_outside_junction(
        key_value_pairs,
        junction_roads,
        lanes_all,
        ego_vehicle,
        world,
        distance_to_junc,
        junction,
):
    """
    Detects and records surrounding cars outside the junction in the city matrix.

    Parameters:
        key_value_pairs (list): A list of key-value pairs representing the city matrix.
        junction_roads (list): List of junction roads and lane information.
                               Format: [road_id, direction, outgoing_lane_wp, lane_id].
        lanes_all (dict): A dictionary containing lane information for different directions.
                          Format: {"ego": [lane_ids], "left": [lane_ids], "straight": [lane_ids], "right": [lane_ids]}.
        ego_vehicle (Vehicle): The ego vehicle.
        world (CarlaWorld): The world representation.
        distance_to_junc (float): Distance from ego vehicle to the junction in meters.
        junction (Junction): The junction object.

    Returns:
        list: Updated key-value pairs representing the city matrix with information about surrounding cars.
    """
    world_map = CarlaDataProvider.get_map()
    world = CarlaDataProvider.get_world()
    ego_waypoint = world_map.get_waypoint(ego_vehicle.get_location())
    junction_id = junction.id
    # junction_roads =
    #   [road_id of incoming road, direction from ego-perspective, wp of outgoing lane of incoming road, corresponding lane_id ],
    #       ... for all 4 directions ego, left, right, straight
    #   ]    # Special Highway Traffic

    surrounding_cars = {"ego": [], "left": [], "straight": [], "right": []}
    actors = world.get_actors()
    ego_actor = actors.find(ego_vehicle.id)
    actors = [ego_actor] + [actor for actor in actors if actor.id != ego_vehicle.id]
    if isinstance(key_value_pairs, dict):
        ego_already_in_matrix = any(
            1 in val for val in key_value_pairs.values())  # TODO: sometimes list, sometimes dict
    else:
        ego_already_in_matrix = any(1 in val for key, val in key_value_pairs)
    for actor in actors:
        if "vehicle" in actor.type_id:  # and actor.id != ego_vehicle.id:
            if actor.id == ego_vehicle.id and ego_already_in_matrix:
                continue
            actor_location = actor.get_location()
            actor_waypoint = world_map.get_waypoint(actor_location)
            if junction_id == 1368 and np.sign(ego_waypoint.lane_id) != np.sign(
                    actor_waypoint.lane_id) and actor_waypoint.road_id in [40, 41]:
                continue
            for road in junction_roads:
                distance_to_actor = actor_location.distance(road[2].transform.location)
                different_road_distance = None

                if (actor_waypoint.is_junction) and (
                        actor_waypoint.get_junction().id == junction_id
                ):
                    actor_outside_junction = False
                else:
                    actor_outside_junction = True

                if (
                        distance_to_actor <= distance_to_junc * 1.2
                ) and actor_outside_junction:  # add extra 20% because distance_to_actor is calculated with road[2] waypoint, which can be on other lane
                    included = True
                    if actor_waypoint.road_id == road[0]:
                        different_road_distance = None
                    elif (
                        actor_waypoint.next(int(distance_to_junc / 2))[0].road_id
                        == road[0]
                    ):
                        different_road_distance = int(distance_to_junc / 2)
                    elif (
                        actor_waypoint.previous(int(distance_to_junc / 2))[0].road_id
                        == road[0]
                    ) and (not actor_waypoint.is_junction):
                        different_road_distance = (
                                int(distance_to_junc / 2) * -1
                        )  # negative bc. look back from actor
                    elif (
                        actor_waypoint.next(int(distance_to_junc / 3))[0].road_id
                        == road[0]
                    ):
                        different_road_distance = int(distance_to_junc / 3)
                    elif (
                        actor_waypoint.previous(int(distance_to_junc / 3))[0
                        ].road_id== road[0]
                    ):
                        different_road_distance = (
                                int(distance_to_junc / 3) * -1
                        )  # negative bc. look back from actor
                    else:
                        included = False
                    if included:
                        surrounding_cars[road[1]].append(
                            (actor, different_road_distance)
                        )

    for road in junction_roads:
        for actor, different_road_distance in surrounding_cars[road[1]]:
            actor_location = actor.get_location()
            actor_waypoint = world_map.get_waypoint(actor_location)

            if different_road_distance is not None:
                if different_road_distance > 0:
                    actor_waypoint_lane_id = actor_waypoint.next(
                        different_road_distance
                    )[0].lane_id
                elif different_road_distance < 0:
                    actor_waypoint_lane_id = actor_waypoint.previous(
                        different_road_distance * -1
                    )[0].lane_id
            else:
                actor_waypoint_lane_id = actor_waypoint.lane_id

            # sort list of lane ID's
            if (int(road[3]) < 0 and junction.id != 1368) or int(road[3]) > 0 and junction.id == 1368:
                lanes_all[road[1]].sort(reverse=True)
            else:
                lanes_all[road[1]].sort()

            # determine lane of actor, i=0: lane most out of lanes incoming the junction
            for i in range(len(lanes_all[road[1]])):
                if lanes_all[road[1]][i] == actor_waypoint_lane_id:
                    break

            # determine number of cells/columns in matrix outside the inner junction
            if (road[1] == "ego") or (road[1] == "straight"):
                if len(lanes_all["left"]) == 0:
                    columns = int((8 - len(lanes_all["right"])) / 2)
                elif len(lanes_all["right"]) == 0:
                    columns = int((8 - len(lanes_all["left"])) / 2)
                else:
                    columns = int(
                        (8 - max([len(lanes_all["left"]), len(lanes_all["right"])])) / 2
                    )  # max number of lanes of right/left
            elif (road[1] == "left") or (road[1] == "right"):
                if len(lanes_all["ego"]) == 0:
                    columns = int((8 - len(lanes_all["straight"])) / 2)
                elif len(lanes_all["straight"]) == 0:
                    columns = int((8 - len(lanes_all["ego"])) / 2)
                else:
                    columns = int(
                        (8 - max([len(lanes_all["ego"]), len(lanes_all["straight"])]))
                        / 2
                    )  # max number of lanes of ego/straight

            # determine cell of actor in matrix
            if ((int(road[3]) > 0) and (actor_waypoint_lane_id > 0)) or (
                    (int(road[3]) < 0) and (actor_waypoint_lane_id < 0)
            ):  # actor on outgoing lane
                # location.distance(waypoints[i].transform.location
                actor_distance_junction = actor_waypoint.transform.location.distance(
                    road[2].transform.location
                )
                if actor_distance_junction < (
                        distance_to_junc / columns
                ):  # doesn't matter how many columns: write "2" in the cell clostest to junction inner part
                    c = columns - 1
                elif (columns == 2) or (
                        actor_distance_junction < (distance_to_junc / columns) * 2
                ):  # if 2 columns then it must be the cell farthest away && if 3 columns check if junction is closer than 2/3 of DISTANCE_TO_JUNCTION, then middle cell
                    c = columns - 2
                else:  # if 3 columns and further away, then cell farthest away
                    c = columns - 3
            else:  # incoming actor
                if actor_waypoint.next(int(distance_to_junc / columns))[
                    0
                ].is_junction:  # doesn't matter how many columns: write "2" in the cell clostest to junction inner part
                    c = columns - 1
                elif (columns == 2) or (
                        actor_waypoint.next(int(distance_to_junc / columns) * 2)[
                            0
                        ].is_junction
                ):  # if 2 columns that it must be the cell farsest away && if 3 columns check if junction is closer than 2/3 of DISTANCE_TO_JUNCTION, then middle cell
                    c = columns - 2
                else:  # if 3 columns and further away than 10m, then cell farsest away
                    c = columns - 3

            # write "2" in identified cell
            if actor.id == ego_vehicle.id:
                cell_val = 1
            else:
                cell_val = 2
            if road[1] == "ego":
                for j in range(8):
                    # ego road
                    if key_value_pairs[-1 - j][1][c] != 3:
                        # in case ego vehicle is already in that matrix cell
                        if key_value_pairs[-1 - j - i][1][c] == 1:
                            # Calculate dot_product (similarity between the vectors)
                            dot_product = check_car_in_front_or_behind(
                                ego_vehicle.get_location(),
                                actor.get_location(),
                                ego_vehicle.get_transform().rotation,
                            )
                            if dot_product > 0:  # other car infront
                                if (columns != 1) and (
                                        c == columns - 1
                                ):  # already in front cell
                                    key_value_pairs[-1 - j - i][1][c - 1] = 1
                                    key_value_pairs[-1 - j - i][1][c] = cell_val
                                elif (
                                        columns != 1
                                ):  # not in front cell but more than 1 cells available
                                    key_value_pairs[-1 - j - i][1][c + 1] = 2
                            else:  # other car behind
                                if (columns != 1) and (c == 0):  # already in last cell
                                    key_value_pairs[-1 - j - i][1][c + 1] = 1
                                    key_value_pairs[-1 - j - i][1][c] = cell_val
                                elif (
                                        columns != 1
                                ):  # not in last cell but more than 1 cells available
                                    key_value_pairs[-1 - j - i][1][c - 1] = cell_val
                        else:
                            key_value_pairs[-1 - j - i][1][c] = cell_val
                        break
            elif road[1] == "left":
                for j in range(8):
                    # left road
                    if key_value_pairs[c][1][j] != 3:
                        key_value_pairs[c][1][j + i] = cell_val
                        break
            elif road[1] == "straight":
                for j in range(8):
                    # straight road
                    if key_value_pairs[j][1][-1 - c] != 3:
                        key_value_pairs[j + i][1][-1 - c] = cell_val
                        break
            elif road[1] == "right":
                for j in range(8):
                    # right road
                    if key_value_pairs[-1 - c][1][-1 - j] != 3:
                        key_value_pairs[-1 - c][1][-1 - j - i] = cell_val
                        break

    if junction.id == 1368:
        key_value_pairs[2][1][-3:], key_value_pairs[5][1][-3:] = key_value_pairs[5][1][-3:], key_value_pairs[2][1][-3:]
        key_value_pairs[3][1][-3:], key_value_pairs[4][1][-3:] = key_value_pairs[4][1][-3:], key_value_pairs[3][1][-3:]

    return key_value_pairs


def getJunctionShape(ego_vehicle, ego_wp, wps, road_lane_ids, direction_angle, world_map):
    """
    Determines the shape of the junction in the city matrix and returns relevant information.

    Parameters:
        ego_vehicle (Vehicle): The ego vehicle.
        ego_wp (Waypoint): Waypoint of the ego vehicle.
        junction (Junction): The junction object.
        road_lane_ids (dict): A dictionary containing lane IDs for different directions.
                             Format: {"ego": lane_id, "left": lane_id, "straight": lane_id, "right": lane_id}.
        direction_angle (float): Angle to determine direction at junction.

    Returns:
        tuple: A tuple containing the following information:
            key_value_pairs (list): A list of key-value pairs representing the city matrix.
            lanes_all (dict): A dictionary containing lane information for different directions.
                              Format: {"ego": [lane_ids], "left": [lane_ids], "straight": [lane_ids], "right": [lane_ids]}.
            junction_roads (list): List of junction roads and lane information.
                                   Format: [road_id, direction, outgoing_lane_wp, lane_id].
            yaw (float): The yaw angle of the ego vehicle's rotation.
    """
    lanes_all, junction_roads = get_all_lanes(
        ego_vehicle, ego_wp, wps, road_lane_ids, direction_angle
    )
    key_value_pairs = [
        ("1", [0, 0, 0, 0, 0, 0, 0, 0]),
        ("2", [0, 0, 0, 0, 0, 0, 0, 0]),
        ("3", [0, 0, 0, 0, 0, 0, 0, 0]),
        ("4", [0, 0, 0, 0, 0, 0, 0, 0]),
        ("5", [0, 0, 0, 0, 0, 0, 0, 0]),
        ("6", [0, 0, 0, 0, 0, 0, 0, 0]),
        ("7", [0, 0, 0, 0, 0, 0, 0, 0]),
        ("8", [0, 0, 0, 0, 0, 0, 0, 0]),
    ]
    left_lanes = int((8 - len(lanes_all["ego"])) / 2)
    left_complete = False
    top_lanes = int((8 - len(lanes_all["left"])) / 2)
    top_complete = False
    right_lanes = int((8 - len(lanes_all["straight"])) / 2)
    right_complete = False
    bottom_lanes = int((8 - len(lanes_all["right"])) / 2)
    bottom_complete = False
    i = 0

    while any(
            [not left_complete, not top_complete, not right_complete, not bottom_complete]
    ):

        # 1. ego/left
        if not top_complete:
            for j in range(left_lanes):
                key_value_pairs[j][1][i] = 3

        # 2. top
        if not right_complete:
            for j in range(top_lanes):
                key_value_pairs[i][1][-1 - j] = 3

        # 3. right
        if not bottom_complete:
            for j in range(right_lanes):
                key_value_pairs[-1 - j][1][-1 - i] = 3

        # 4. bottom
        if not left_complete:
            for j in range(bottom_lanes):
                key_value_pairs[-1 - i][1][j] = 3

        # check if sides of matrix are already complete
        i = i + 1
        if i == 8:
            break
        if i == bottom_lanes:
            bottom_complete = True
        if i == right_lanes:
            right_complete = True
        if i == top_lanes:
            top_complete = True
        if i == left_lanes:
            left_complete = True

    if world_map.get_waypoint(
            ego_vehicle.get_location()).road_id == 23:  # on traffic light junction, use yaw of ghost not ego
        if world_map.get_waypoint(ego_vehicle.get_location()).lane_id == -3:  # yaw, in case we entry to the right
            yaw = 179
        else:
            yaw = 1
    else:
        ego_transform = ego_vehicle.get_transform()
        ego_rotation = ego_transform.rotation
        yaw = ego_rotation.yaw

    return key_value_pairs, lanes_all, junction_roads, yaw


# Inner junction:
def get_closest_starting_waypoint(junction_waypoints, ego_location):
    """
    From a list of junction waypoint tuples (start_wp, end_wp), find the closest starting waypoint to the ego vehicle.

    Parameters:
        junction_waypoints (list): List of tuples containing waypoint and lane ID pairs.
                                   Format: [(start_wp, end_wp), ...]
        ego_vehicle (carla.Location): The ego location.

    Returns:
        carla.Waypoint: The closest starting waypoint to the ego vehicle.
    """
    closest_start_wp = junction_waypoints[0][0]
    # get the closest start waypoint to ego
    for start_wp, _ in junction_waypoints:
        if (distance(start_wp.transform.location, ego_location)
            < distance(closest_start_wp.transform.location, ego_location)):
            closest_start_wp = start_wp

    return closest_start_wp


def get_all_lanes(ego_vehicle, ego_wp, junction_waypoints, road_lane_ids, direction_angle):
    """
    Get all lanes related to the junction and the corresponding directions from the ego vehicle's perspective.

    Parameters:
        ego_vehicle (Vehicle): The ego vehicle.
        ego_wp (Waypoint): The waypoint associated with the ego vehicle.
        junction (Junction): The junction of interest.
        road_lane_ids (list): List of road and lane IDs in the world map.
        direction_angle (float): The angle used to determine directions from the ego vehicle.
        world_map (carla.Map): The map of the world in which the waypoints are located.

    Returns:
        dict: A dictionary containing a list for each direction from ego perspective (key) of lane ids of the roads going into the junction object.
                Format: {"ego": [lane_ids], "left": [lane_ids], "straight": [lane_ids], "right": [lane_ids]}.
        list: For all roads going into the junction object one sublist containing the following information:
                Format: [road_id of road after junction, direction from ego perspective, end_wp of junction road, lane_id of road after junction end wp].
    """
    
    ego_location = ego_wp.transform.location
    road_id_ego = ego_wp.road_id

    #lane_id_ego = ego_wp.lane_id
    #start_wps = [[], [], []]
    end_wps = [[], [], [], []]
    closest_start_wp = get_closest_starting_waypoint(junction_waypoints, ego_location)

    # pre processing of junction_waypoints to get necessary information
    for i, (_, end_wp) in enumerate(junction_waypoints):
        # get road id and lane id of the road after the end_wp
        if junction_waypoints[0][0].get_junction().id == 1368 and ((i < 2) or (i >= len(junction_waypoints) - 2)):
            road_id_end_wp = end_wp.previous(2)[0].road_id
            lane_id_end_wp = end_wp.previous(2)[0].lane_id
        else:
            # end
            road_id_end_wp = end_wp.next(1)[0].road_id
            lane_id_end_wp = end_wp.next(1)[0].lane_id

        end_wps[0].append(end_wp) # end_wp of junction road
        end_wps[1].append(road_id_end_wp) # road id of road after junction end wp

        # get direction from ego perspective
        # catch special case of gas station junction objects
        if ((road_id_end_wp != road_id_ego and end_wp.next(10)[0].road_id != road_id_ego)
            and (   not ((road_id_end_wp in [2, 3] and int(road_id_ego) in [467, 468, 477])
                        or road_id_ego in [12, 13, 879, 880, 886])
                 or not ((road_id_end_wp in [12, 13] and int(road_id_ego) in [12, 13, 879, 880, 886])
                        or road_id_ego in [467, 468, 477]))):
            end_wps[2].append(
                get_waypoint_direction(
                    ego_vehicle, closest_start_wp, end_wp, direction_angle #  TODO: comments
                )
            )

        else:
            end_wps[2].append("ego")

        # get lane id of road after junction end wp
        end_wps[3].append(lane_id_end_wp)

    # get distinct road id (of road after junction) + corresponding direction from ego + end_wp
    junction_roads = []
    for i in range(len(end_wps[0])):
        if end_wps[1][i] not in [x[0] for x in junction_roads]:
            junction_roads.append(
                [end_wps[1][i], end_wps[2][i], end_wps[0][i], end_wps[3][i]]
            )

    # get for all directions the lane ids of the roads that go into the junction
    lanes_all = {
        "ego": [],
        "left": [],
        "straight": [],
        "right": [],
    }  # direction from ego perspective
    for lane_id in road_lane_ids:  # iterate through all lanes of map
        for road in junction_roads:  # for each road that goes into the junction
            if road[0] == lane_id[0]:
                if (junction_waypoints[0][0].get_junction().id == 1368) and lane_id[1] * np.sign(
                        ego_wp.lane_id) < 0 and road[0] != 23:
                    continue
                else:
                    lanes_all[road[1]].append(lane_id[1]) # append lane id
    
    return lanes_all, junction_roads


def remove_elements(lst):
    """
    Filters out elements from the list that have another element in the list within a distance of 1.5.

    Args:
        lst (list): A list of numeric values (ints or floats) to be filtered.

    Returns:
        list: A list containing the filtered elements of 'lst'.
    """
    result = []
    for i in range(len(lst)):
        should_remove = False
        for j in range(i + 1, len(lst)):
            if abs(lst[i] - lst[j]) <= 1.5:
                should_remove = True
                break
        if not should_remove:
            result.append(lst[i])
    return result


def build_grid(boxes):
    """
    Build a grid from the list of boxes. All boxes with the same x value are grouped together in a row.

    Parameters:
        boxes (list): A list of boxes, where each box is represented as a list containing a carla.BoundingBox object and an integer value.

    Returns:
        list: A 2D grid representation of the boxes.
            Format: [[carla.BoundingBox, carla.BoundingBox, carla.BoundingBox, ...], [carla.BoundingBox, carla.BoundingBox, carla.BoundingBox, ...], ...]
    """
    x = boxes[0][0].location.x
    grid = []
    row = [boxes[0]]
    for i in range(1, len(boxes)):
        if boxes[i][0].location.x == x:
            row.append(boxes[i])
        else:
            grid.append(row)
            row = []

            row.append(boxes[i])
            x = boxes[i][0].location.x
    grid.append(row)
    return grid


def transpose_2d_array(array):
    transposed_array = [list(row) for row in zip(*array[::-1])]
    return transposed_array


def rotate_grid(grid, yaw):
    """
    Rotate the grid based on the yaw angle of the ego vehicle.

    Parameters:
        grid (list): A 2D grid representation of the boxes.
        yaw (float): The yaw angle in degrees.

    Returns:
        list: The rotated grid.
    """
    if 45 <= yaw <= 135:
        return transpose_2d_array(transpose_2d_array(grid))
    elif (135 <= yaw <= 180) or (-180 <= yaw <= -135):
        # Rotate 90 degrees to the left
        return transpose_2d_array(grid)
    elif -135 <= yaw <= -45:
        # Rotate 180 degrees
        return grid
    elif -45 <= yaw <= 45:
        # Rotate 90 degrees to the right
        return transpose_2d_array(transpose_2d_array(transpose_2d_array(grid)))


def check_flipping_rows_and_columns(ego_vehicle):
    ego_transform = ego_vehicle.get_transform()
    ego_rotation = ego_transform.rotation
    yaw = ego_rotation.yaw

    if (yaw >= -45 and yaw <= 45) or (
            (yaw >= -180 and yaw < -135) or (yaw >= 135 and yaw <= 180)
    ):
        return True


# NOTE: sub function of detect_cars_inside_junction
def get_grid_corners(junction_shape):
    """
    Find the corner coordinates of the inner junction in the given grid representation.

    Parameters:
        key_value_pairs (list): A list of key-value pairs representing the city matrix.
            Format: [("1", [0, 0, 0, 0, 0, 0, 0, 0]), ("2", [0, 0, 0, 0, 0, 0, 0, 0]), ...].

    Returns:
        list: A list containing the coordinates of the four corners of the inner junction.
            Format: [[row, column], [row, column], [row, column], [row, column]] in the grid format.

    Notes:
        - The grid representation must be a 2D list with 8 rows and 8 columns.
        - The function handles the possibility of a 90-degree rotation in the grid,
          ensuring correct corner identification regardless of the junction's orientation.
    """
    # get top y coordinate: y1
    global x_1, x_2, y_2
    y_1 = None
    for i in range(8):
        if junction_shape[i][1][0] != 3:
            y_1 = i
            break

    # get bottom y coordinate: y2
    for j in range(7, -1, -1):
        if junction_shape[j][1][0] != 3:
            y_2 = j
            break

    # if left from ego perspective is no street: check in last row
    if sum(junction_shape[0][1]) == 8 * 3: # all 8 value of value 3
        row = 7
    # else: left from ego perspective is a street: check in first row
    else:
        row = 0
    # get left x coordinate: x1
    for k in range(8):
        if junction_shape[row][1][k] != 3:
            x_1 = k
            break
    # get right x coordinate: x2
    for n in range(7, -1, -1):
        if junction_shape[row][1][n] != 3:
            x_2 = n
            break

    return [[y_1, x_1], [y_1, x_2], [y_2, x_1], [y_2, x_2]]

# NOTE: sub function update_matrix
def insert_in_matrix(matrix, car, ego_vehicle, col, row):
    if car.id == ego_vehicle.id:
        matrix[row][1][col] = 1
    else:
        if matrix[row][1][col] == 1:
            # check if car is behind or in front of ego vehicle: dot_product > 0 ==> in front, dot_product < 0 ==> behind
            dot_product = check_car_in_front_or_behind(
                ego_vehicle.get_location(),
                car.get_location(),
                ego_vehicle.get_transform().rotation,
            )
            if dot_product > 0:
                if row == 6 or row == 7:
                    matrix[row - 1][1][col] = 2
                elif row == 5 and col < 7:
                    matrix[row][1][col + 1] = 2
            else:
                if row == 6:
                    matrix[row + 1][1][col] = 2
                elif row == 5 and col > 0:
                    matrix[row][1][col - 1] = 2
        else:
            matrix[row][1][col] = 2


def get_right_lane_wp(wps):
    """
    Iterates over grouped highway junction waypoints and returns the waypoint of the right (most out) lane.

    Args:
        wps (list): List of one waypoint cluster of grouped highway junction waypoints.
            Format: [(start_wp, "start"), (start_wp, "start"), ..]

    Returns:
        carla.Waypoint: Waypoint with highest absolute lande_id -> right (most out) lane
    """
    right_lane_wp = wps[0][0]  # initialize = first wp of group
    for wp in wps:
        if abs(wp[0].lane_id) > abs(right_lane_wp.lane_id):
            right_lane_wp = wp[0]
    return right_lane_wp


def get_road(lane_start):
    waypoints = [lane_start]
    next_wp = lane_start.next(2)[0]
    while next_wp.road_id == waypoints[-1].road_id:
        waypoints.append(next_wp)
        next_wp = next_wp.next(2)[0]
    return waypoints


# NOTE: sub function of check_ego_exit_highway
def angle_between_vectors(a, b):
    """Calculates the angle between to forward vectors.
    
    Args:
        a (carla.Vector3D): First forward vector
        b (carla.Vector3D): Second forward vector
    
    Returns:
        float: Angle between a and b in degree.
    """
    dot = a.x * b.x + a.y * b.y
    mag_a = math.sqrt(a.x ** 2 + a.y ** 2)
    mag_b = math.sqrt(b.x ** 2 + b.y ** 2)
    cos_theta = dot / (mag_a * mag_b)
    theta = math.acos(cos_theta)
    return math.degrees(theta)
