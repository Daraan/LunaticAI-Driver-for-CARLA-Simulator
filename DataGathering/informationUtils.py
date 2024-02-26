from typing import Dict
import carla
import math
import itertools
import collections
import pandas as pd
import numpy as np
import random
from copy import deepcopy

from utils.logging import log

# NOTE: TODO: double definition
def get_row(matrix):
    row_data = {}

    keys = [0, 1, 2, 3, 4, 5, 6, 7]
    counter = 0
    for key, values in matrix.items():
        column_names = [f"{keys[counter]}_{i}" for i in range(0, 8)]
        row_data.update(dict(zip(column_names, values)))
        counter += 1

    return row_data

def get_row(matrix : collections.OrderedDict) -> Dict:
    """
    Convert the city matrix into a row of data in the DataFrame.

    Parameters:
        matrix (collections.OrderedDict): The city matrix representing the lanes around the ego vehicle.

    Returns:
        dict: A dictionary representing a row of data to be added to the DataFrame.
    """
    row_data = {}

    keys = [0, 1, 2, 3, 4, 5, 6, 7]
    counter = 0
    if matrix:
        # Iterate over the data dictionary
        for key, values in matrix.items():
            # Get the column names based on the key
            column_names = [f"{keys[counter]}_{i}" for i in range(0, 8)]
            # Create a dictionary with column names as keys and values from data as values
            row_data.update(dict(zip(column_names, values)))
            counter += 1
    else:
        # If no data is available, fill the row with None values
        for i in range(0, 8):
            column_names = [f"{keys[counter]}_{i}" for i in range(0, 8)]
            row_data.update(dict(zip(column_names, [None] * 8)))
            counter += 1

    return row_data

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
    waypoints = []
    ego_waypoint = world_map.get_waypoint(ego_vehicle_location)
    waypoints.append(ego_waypoint)
    if ego_waypoint.get_left_lane() is not None:
        waypoints.append(ego_waypoint.get_left_lane())
    if ego_waypoint.get_right_lane() is not None:
        waypoints.append(ego_waypoint.get_right_lane())
    
    # check for all waypoints if they are on a highway, in case they have different road_id's
    for wp in waypoints:
        ego_vehilce_road_id = wp.road_id
        # get all lanes of the respective road
        lanes = []
        for id in road_lane_ids:
            if str(ego_vehilce_road_id) == id.split("_")[0]:
                lanes.append(id.split("_")[1])
        # cast lane_id's to int and check for highway condition
        lanes = [int(lane) for lane in lanes]
        if len(lanes) >= 6 or (
            sorted(lanes) == list(range(min(lanes), max(lanes) + 1)) and len(lanes) >= 3
        ):
            return True

    return False


def get_all_road_lane_ids(world_map):
    """
    Retrieve a set of unique road and lane identifiers in the format "roadId_laneId" from the given world map.

    Args:
        world_map (carla.Map): The map of the world from which road and lane identifiers are obtained.

    Returns:
        set: A set containing unique road and lane identifiers in the format "roadId_laneId".
    """
    road_lane_ids = set()

    # iterate through all waypoints in the world map
    for waypoint in world_map.generate_waypoints(1.0):
        # extract lane and road id's 
        lane_id = waypoint.lane_id
        road_id = waypoint.road_id
        # add road and lane identifiers to set
        road_lane_ids.add(f"{road_id}_{lane_id}")

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

def create_city_matrix(ego_vehicle_location, road_lane_ids, world_map, ghost=False, ego_on_bad_highway_street=False):
    """
    Create a matrix representing the lanes around the ego vehicle.

    Parameters:
        ego_vehicle_location (carla.Location): The location object of ego vehicle for which to create the city matrix.
        road_lane_ids (list): A list of all road-lane identifiers of the map, where each identifier is a string in the format "roadId_laneId". 
            Format: ["1_2", "2_1", "3_2"].
        world_map (carla.Map): The map representing the environment.
        ghost (bool): Ghost mode when ego is exiting/entrying a highway - fix a location of an imaginary vehicle on highway to correctly build matrix from this ghost perspective.
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
    ego_vehilce_waypoint = world_map.get_waypoint(ego_vehicle_location)
    ego_vehilce_lane_id = str(ego_vehilce_waypoint.lane_id)
    print("ego_vehicle_lane_id: ", ego_vehilce_lane_id)
    ego_vehilce_road_id = str(ego_vehilce_waypoint.road_id)

    # get all lanes of ego's road
    lanes = []
    for id in road_lane_ids:
        if ego_vehilce_road_id == id.split("_")[0]:
            lanes.append(id.split("_")[1])
    lanes.sort()
    lanes = [int(id) for id in lanes]
    
    # split lanes into directions & sort, e.g. [-2,-1,1,2] -> [[-2,-1],[2,1]]
    lanes_splitted = []
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
    key_value_pairs = None
    other_direction = []
    ego_direction = []
    # Identify list of lanes of ego's direction and opposite direction
    for direction in lanes_splitted:
        if int(ego_vehilce_lane_id) in direction:
            ego_direction = direction
        else:
            other_direction = direction
    
    if len(ego_direction) >= 4:
        # ego is on a highway with 4 or more lanes
        key_value_pairs = [
            ("left_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("left_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            (
                ego_vehilce_road_id + "_" + str(ego_direction[3]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                ego_vehilce_road_id + "_" + str(ego_direction[2]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                ego_vehilce_road_id + "_" + str(ego_direction[1]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                ego_vehilce_road_id + "_" + str(ego_direction[0]),
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
                ego_vehilce_road_id + "_" + str(ego_direction[2]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                ego_vehilce_road_id + "_" + str(ego_direction[1]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                ego_vehilce_road_id + "_" + str(ego_direction[0]),
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
                ego_vehilce_road_id + "_" + str(other_direction[0]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                ego_vehilce_road_id + "_" + str(other_direction[1]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                ego_vehilce_road_id + "_" + str(ego_direction[1]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                ego_vehilce_road_id + "_" + str(ego_direction[0]),
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
                ego_vehilce_road_id + "_" + str(ego_direction[1]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                ego_vehilce_road_id + "_" + str(ego_direction[0]),
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
                ego_vehilce_road_id + "_" + str(other_direction[0]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            (
                ego_vehilce_road_id + "_" + str(ego_direction[0]),
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
                ego_vehilce_road_id + "_" + str(ego_direction[0]),
                [0, 0, 0, 0, 0, 0, 0, 0],
            ),
            ("No_own_right_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("right_inner_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
            ("right_outer_lane", [3, 3, 3, 3, 3, 3, 3, 3]),
        ]

    # Update matrix
    if key_value_pairs:
        matrix = collections.OrderedDict(key_value_pairs)
    
    # Insert ego in matrix, in case ego is not entrying/exiting a highway    
    if matrix and not ghost:
        try:
            if ego_on_bad_highway_street:
                if int(ego_vehilce_lane_id) > 0:
                    matrix[str(ego_vehilce_road_id) + "_" + str(int(ego_vehilce_lane_id) + 1)][3] = 1
                else:
                    matrix[str(ego_vehilce_road_id) + "_" + str(int(ego_vehilce_lane_id) - 1)][3] = 1
            else:
                matrix[str(ego_vehilce_road_id) + "_" + str(ego_vehilce_lane_id)][3] = 1
        except KeyError:
            matrix[str(ego_vehilce_road_id) + "_" + str(ego_vehilce_lane_id)][3] = 1
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
        next_road_id = str(next_waypoint.road_id)
        next_lanes = [
            id.split("_")[1]
            for id in road_lane_ids
            if next_road_id == id.split("_")[0]
        ]
        
    # get lanes of ego vehicle's road
    our_lanes = [
        id.split("_")[1]
        for id in road_lane_ids
        if str(ego_vehicle_waypoint.road_id) == id.split("_")[0]
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
    ego_location,
    ego_vehicle,
    matrix,
    road_lane_ids,
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
        ghost (bool): Ghost mode when ego is exiting/entrying a highway - fix a location of an imaginary vehicle on highway to correctly build matrix from this ghost perspective.

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
    world_map = world.get_map()
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
    lanes = []
    for id in road_lane_ids:
        if str(ego_vehicle_road_id) == id.split("_")[0]:
            lanes.append(id.split("_")[1])
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
    if not highway_shape is None:
        entry_wps = highway_shape[2] # Tuple with start and end waypoint of the entry: ([start_wp, start_wp..], [end_wp, end_wp..])
        exit_wps = highway_shape[3] # Tuple with start and end waypoint of the exit: ([start_wp, start_wp..], [end_wp, end_wp..])

        # get all road id's of entry and exit and previous/next road
        entry_road_id = []
        exit_road_id = []
        entry_city_road = [] # road before an entry in city
        exit_city_road = [] # road after an exit in city
        entry_highway_road = [] # road after an entry on highway
        exit_highway_road = [] # road before an exit on highway
        if entry_wps:
            for entry_wp in entry_wps[0]: # entry_wps[0] contains all start waypoints of entry
                entry_city_road.append(entry_wp.previous(3)[0].road_id)
                entry_road_id.append(entry_wp.road_id)
            for entry_wp in entry_wps[1]: # entry_wps[1] contains all end waypoints of entry
                entry_highway_road.append(entry_wp.next(3)[0].road_id)
            if entry_wp.next(3)[0] and entry_wp.next(3)[0].get_left_lane() and entry_wp.next(3)[0].road_id == \
                    entry_wp.next(3)[0].get_left_lane().road_id:
                entry_highway_road = []
        if exit_wps:
            for exit_wp in exit_wps[1]: # exit_wps[1] contains all end waypoints of exit
                exit_city_road.append(exit_wp.next(3)[0].road_id)
                exit_road_id.append(exit_wp.road_id)
            for exit_wp in exit_wps[0]: # exit_wps[0] contains all start waypoints of exit
                exit_highway_road.append(exit_wp.previous(3)[0].road_id)
            if exit_wp.next(3)[0] and exit_wp.next(3)[0].get_left_lane() and exit_wp.next(3)[0].road_id == \
                    exit_wp.next(3)[0].get_left_lane().road_id:
                exit_highway_road = []

    # Update matrix based on the lane and position/distance to ego vehicle of other car
    if (
        on_highway
        and (not highway_shape is None)
        and (
            ego_vehicle_road_id
            in entry_road_id
            + entry_city_road
            + exit_road_id
            + exit_city_road
            + exit_highway_road
            + entry_highway_road
        )
    ):
        surrounding_cars_on_highway_entryExit.append(ego_vehicle)
    
    # Update matrix based on the lane and position/distance to ego vehicle of other car
    for car in surrounding_cars:
        # Get road and lane_id of other car
        other_car_waypoint = world_map.get_waypoint(car.get_location())
        other_car_lane_id = other_car_waypoint.lane_id
        other_car_road_id = other_car_waypoint.road_id
        other_car_road_lane_id = str(other_car_road_id) + "_" + str(other_car_lane_id)

        # ignore car on highway entry / Exit bc. considered in update_matrix()
        if (
            on_highway
            and (not highway_shape is None)
            and (
                other_car_road_id
                in entry_road_id
                + entry_city_road
                + exit_road_id
                + exit_city_road
                + exit_highway_road
                + entry_highway_road
            )
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
            ego_vehicle.get_velocity(),
            ghost,
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
            elif (lanes_exist_further or lanes_existed_before) and str(
                other_car_lane_id
            ) in [str(road_lane.split("_")[1]) for road_lane in matrix.keys()]:
                if car.id == ego_vehicle.id:
                    matrix[str(ego_vehicle_road_id) + "_" + str(other_car_lane_id)][
                        col
                    ] = 1
                else:
                    try:
                        matrix[str(ego_vehicle_road_id) + "_" + str(other_car_lane_id)][
                            col
                        ] = 2
                    except:
                        pass

    return matrix, surrounding_cars_on_highway_entryExit

def check_car_in_front_or_behind(ego_location, other_location, rotation):
    """
    Chek if other car is in front or behind ego vehicle.

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
    ego_forward_vector = carla.Vector3D(
        math.cos(math.radians(rotation.yaw)),
        math.sin(math.radians(rotation.yaw)),
        0,
    )

    # Calculate dot_product (similarity between the vectors): dot_product > 0 ==> in front, dot_product < 0 ==> behind
    dot_product = (
        ego_forward_vector.x * ego_to_other_vector.x
        + ego_forward_vector.y * ego_to_other_vector.y
    )
    return dot_product
def get_forward_vector_distance(ego_vehicle_location, other_car, world_map):
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
        ego_location, ego_vehicle, other_car, matrix, world_map, velocity, ghost=False
):
    """
    Calculate the position of the other car in the city matrix based on its relative location and distance from the ego vehicle.
    Only determines the column, not the row since that is based on the lane_id of the other car.

    Parameters:
        ego_location (carla.Location): The location object of the ego vehicle.
        ego_vehicle (carla.Vehicle): The ego vehicle for reference.
        other_car (carla.Vehicle): The other car whose position is to be determined.
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
                "right_outer_lane": [3, 3, 3, 3, 3, 3, 3, 3],
        world_map (carla.WorldMap): The map representing the environment.
        ghost (bool): Ghost mode when ego is exiting/entrying a highway - fix a location of an imaginary vehicle on highway to correctly build matrix from this ghost perspective.

    Returns:
        int or None: The column index in the city matrix representing the column in the city matrix of the other car,
                    or None if the other car is not within the specified distance range.

    Note:
        The city matrix should be pre-generated using the 'create_basic_matrix' function. Other cars are detected using the detect_surronding cars func.
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
    distance_to_actor = distance(other_location, ego_location)

    # check if car is behind or in front of ego vehicle: dot_product > 0 ==> in front, dot_product < 0 ==> behind
    dot_product = check_car_in_front_or_behind(ego_location, other_location, rotation)

    # Get road_lane_id of other vehicle
    other_car_waypoint = world_map.get_waypoint(other_location)
    other_car_lane_id = other_car_waypoint.lane_id
    other_car_road_id = other_car_waypoint.road_id
    other_car_road_lane_id = str(other_car_road_id) + "_" + str(other_car_lane_id)

    # Get road_lane_id of ego vehicle
    ego_car_waypoint = world_map.get_waypoint(ego_location)
    ego_car_lane_id = ego_car_waypoint.lane_id
    ego_car_road_id = ego_car_waypoint.road_id
    ego_car_road_lane_id = str(ego_car_road_id) + "_" + str(ego_car_lane_id)

    # velocity = ego_vehicle.get_velocity()
    ego_speed = (
            3.6 * (velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2) ** 0.5
    )  # Convert m/s to km/h
    road_lane_ids = get_all_road_lane_ids(world_map)
    
    # if ego is on highway use different speed factor --> we look further ahead/behind on highway
    if check_ego_on_highway(ego_location, road_lane_ids, world_map):
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


def get_row(matrix):
    row_data = {}

    keys = [0, 1, 2, 3, 4, 5, 6, 7]
    counter = 0
    for key, values in matrix.items():
        column_names = [f"{keys[counter]}_{i}" for i in range(0, 8)]
        row_data.update(dict(zip(column_names, values)))
        counter += 1

    return row_data


def get_speed(ego_vehicle):
    velocity = ego_vehicle.get_velocity()
    ego_speed = (
            3.6 * (velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2) ** 0.5
    )  # Convert m/s to km/h

    return ego_speed


def get_steering_angle(ego_vehicle):
    control = ego_vehicle.get_control()
    steering_angle = math.radians(control.steer)
    return steering_angle


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
    ego_rotation_1 = ego_vehicle.get_transform().rotation.yaw
    # ego_rotation = ego_rotation_1
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
    # get closest start waypoint to ego
    for start_wp, _ in junction_waypoints:
        if distance(start_wp.transform.location, ego_location) < distance(
            closest_start_wp.transform.location, ego_location
        ):
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
    road_id_ego = str(ego_wp.road_id)

    lane_id_ego = ego_wp.lane_id
    start_wps = [[], [], []]
    end_wps = [[], [], [], []]
    closest_start_wp = get_closest_starting_waypoint(junction_waypoints, ego_location)

    # pre processing of junction_waypoints to get necessary information
    for i, (start_wp, end_wp) in enumerate(junction_waypoints):
        # get road id and lane id of the road after the end_wp   
        if junction_waypoints[0][0].get_junction().id == 1368 and ((i < 2) or (i >= len(junction_waypoints) - 2)):
            road_id_end_wp = str(end_wp.previous(2)[0].road_id)
            lane_id_end_wp = str(end_wp.previous(2)[0].lane_id)
        else:
            # end
            road_id_end_wp = str(end_wp.next(1)[0].road_id)
            lane_id_end_wp = str(end_wp.next(1)[0].lane_id)

        end_wps[0].append(end_wp) # end_wp of junction road 
        end_wps[1].append(road_id_end_wp) # road id of road after junction end wp

        # get direction from ego perspective
        # catch special case of gas station junction objects
        if (road_id_end_wp != road_id_ego and str(end_wp.next(10)[0].road_id) != road_id_ego) \
                and (not (
                (int(road_id_end_wp) in [2, 3] and int(road_id_ego) in [467, 468, 477]) or int(road_id_ego) in [12, 13,
                                                                                                                879,
                                                                                                                880,
                                                                                                                886]) \
                     or not ((int(road_id_end_wp) in [12, 13] and int(road_id_ego) in [12, 13, 879, 880, 886]) or int(
                    road_id_ego) in [467, 468, 477])):
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
            if road[0] == lane_id.split("_")[0]:
                if (junction_waypoints[0][0].get_junction().id == 1368) and int(lane_id.split("_")[1]) * np.sign(
                        ego_wp.lane_id) < 0 and int(road[0]) != 23:
                    continue
                else:
                    lanes_all[road[1]].append(lane_id.split("_")[1]) # append lane id
    
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
    Rotate the grid based on the yaw angle of ego.

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


def get_grid_corners(junction_shape):
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
    # else: left from ego perspective is a street: ckeck in first row
    else:
        row = 0        
    # get left x coordinate: x1
    for k in range(8):
        if junction_shape[row][1][k] != 3:
            x_1 = k
            break
    # get right x coordinate: x2
    for l in range(7, -1, -1):
        if junction_shape[row][1][l] != 3:
            x_2 = l
            break

    return [[y_1, x_1], [y_1, x_2], [y_2, x_1], [y_2, x_2]]


def is_highway_junction(ego_vehicle, ego_wp, junction, road_lane_ids, direction_angle):
    lanes_all, junction_roads = get_all_lanes(
        ego_vehicle, ego_wp, junction.get_waypoints(carla.LaneType().Driving), road_lane_ids, direction_angle
    )

    highway_junction = False
    for _, lanes in lanes_all.items():
        if len(lanes) >= 8:
            highway_junction = True
            break
    return highway_junction


def get_distance_junction_start(wp):
    x = 1
    while wp.previous(x)[0].is_junction:
        x = x + 1
    return x


def get_distance_junction_end(wp):
    x = 1
    while wp.next(x)[0].is_junction:
        x = x + 1
    return x


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
    mag_a = math.sqrt(a.x**2 + a.y**2)
    mag_b = math.sqrt(b.x**2 + b.y**2)
    cos_theta = dot / (mag_a * mag_b)
    theta = math.acos(cos_theta)
    return math.degrees(theta)

#####################
# Functions not in use
#####################

def get_ego_direction_lanes(ego_vehicle, road_lane_ids, world_map):
    """
    Determine the lanes in the same and opposite direction as the ego vehicle.

    Parameters:
        ego_vehicle (Vehicle): The ego vehicle for which to determine the lane directions.
        road_lane_ids (list of str): List of road and lane IDs in the world map.
        world_map (WorldMap): The map representing the environment.

    Returns:
        tuple: A tuple containing two lists:
            - ego_direction (list of int): A list of lane IDs that are in the same direction as
                                           the ego vehicle's current lane.
            - other_direction (list of int): A list of lane IDs that are in the opposite direction
                                             to the ego vehicle's current lane.
    """
    ego_vehicle_location = ego_vehicle.get_location()
    ego_vehicle_waypoint = world_map.get_waypoint(ego_vehicle_location)
    ego_vehicle_lane_id = str(ego_vehicle_waypoint.lane_id)
    ego_vehicle_road_id = str(ego_vehicle_waypoint.road_id)

    lanes = []
    for id in road_lane_ids:
        if ego_vehicle_road_id == id.split("_")[0]:
            lanes.append(id.split("_")[1])
    lanes.sort()
    lanes = [int(id) for id in lanes]
    lanes_splitted = []
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
    other_direction = []
    ego_direction = []
    for direction in lanes_splitted:
        if int(ego_vehicle_lane_id) in direction:
            ego_direction = direction
        else:
            other_direction = direction

    return ego_direction, other_direction

def get_road(lane_start):
    waypoints = [lane_start]
    next_wp = lane_start.next(2)[0]
    while next_wp.road_id == waypoints[-1].road_id:
        waypoints.append(next_wp)
        next_wp = next_wp.next(2)[0]
    return waypoints

###########################################################
##################### Get Sensor data #####################
###########################################################
 
def get_speed(ego_vehicle):
    # Get the velocity of the ego vehicle
    velocity = ego_vehicle.get_velocity()
    ego_speed = (
            3.6 * (velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2) ** 0.5
    )  # Convert m/s to km/h

    return ego_speed

def get_acceleration(speed, previous_speed, current_time, previous_time):
    time_interval = (current_time - previous_time) / 1_000_000_000
    acceleration = (speed - previous_speed) / time_interval  # Change in speed during one time interval
    return acceleration

def get_steering_angle(ego_vehicle):
    """
    steering_angle < 0: driving left
    steering_angle > 0: driving right
    """
    control = ego_vehicle.get_control()
    steering_angle = math.radians(control.steer)
    return steering_angle

