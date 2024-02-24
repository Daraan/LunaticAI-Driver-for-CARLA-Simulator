import carla

from DataGathering.informationUtils import check_ego_on_highway, create_city_matrix, detect_surrounding_cars, log

def wrap_matrix_functionalities(ego_vehicle : carla.Actor, world : carla.World, world_map : carla.Map, road_lane_ids,
                                radius=100, highway_shape=None):

    matrix = []
    ego_location = ego_vehicle.get_location()
    ego_waypoint = world_map.get_waypoint(ego_location)
    ego_on_highway = check_ego_on_highway(ego_location, road_lane_ids, world_map)

    current_lanes = []
    for id in road_lane_ids:
        if str(ego_waypoint.road_id) == id.split("_")[0]:
            current_lanes.append(int(id.split("_")[1]))

    # Normal Road
    if ego_on_highway:
        street_type = "On highway"
    else:
        street_type = "Non highway street"
    matrix = create_city_matrix(ego_location, road_lane_ids, world_map)

    if matrix:
        matrix, _ = detect_surrounding_cars(
            ego_location, ego_vehicle, matrix, road_lane_ids, world, radius, ego_on_highway, highway_shape
        )
    new_matrix = {}
    i = 0
    for lane in matrix:
        new_matrix[i] = matrix[lane]
        i += 1
    matrix = new_matrix
    log(str(street_type))
    return matrix


def get_car_coords(matrix):
    (i_car, j_car) = (0, 0)
    for lane in matrix:
        for i in range(len(matrix[lane])):
            if matrix[lane][i] == 1:
                (i_car, j_car) = (lane, i)

    return i_car, j_car
