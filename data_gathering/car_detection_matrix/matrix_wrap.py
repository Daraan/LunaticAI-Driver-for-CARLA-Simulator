import carla

from data_gathering.car_detection_matrix.informationUtils import RoadLaneId, check_ego_on_highway, create_city_matrix, detect_surrounding_cars
from classes.constants import StreetType

def wrap_matrix_functionalities(ego_vehicle : carla.Actor, world : carla.World, world_map : carla.Map, road_lane_ids: "set[RoadLaneId]",
                                radius=100, highway_shape=None):
    ego_location = ego_vehicle.get_location()
    ego_waypoint = world_map.get_waypoint(ego_location)
    ego_on_highway = check_ego_on_highway(ego_location, road_lane_ids, world_map)

    current_lanes = []
    for id in road_lane_ids:
        if ego_waypoint.road_id == id[0]:
            current_lanes.append(id[1])

    # Normal Road
    if ego_on_highway:
        street_type = StreetType.ON_HIGHWAY
    else:
        street_type = StreetType.NON_HIGHWAY_STREET
    matrix = create_city_matrix(ego_location, road_lane_ids, world_map)

    if matrix:
        matrix, _ = detect_surrounding_cars(
            ego_location, ego_vehicle, matrix, road_lane_ids, world, radius, ego_on_highway, highway_shape
        )
    # Removes the information about "left_outer_lane" by replacing it with numeric values.
    # Is this a good idea?
    new_matrix = {i : v for i, v in enumerate(matrix.values())}
    matrix = new_matrix
    return matrix


def get_car_coords(matrix):
    (i_car, j_car) = (0, 0)
    for lane, occupations in matrix.items():
        try:
            return (lane, occupations.index(1)) # find the 1 entry in a efficient way
        except ValueError:
            continue
    
    return i_car, j_car
