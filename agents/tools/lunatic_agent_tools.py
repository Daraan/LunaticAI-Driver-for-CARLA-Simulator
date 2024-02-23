from shapely.geometry import Polygon
from functools import partial

import carla
from agents.navigation.local_planner import RoadOption
from agents.tools.misc import (is_within_distance,
                               compute_distance, ObstacleDetectionResult)



from typing import TYPE_CHECKING, NamedTuple
if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent

# TODO: see if max_distance is currently still necessary
# TODO: move angles to config
#@override
def detect_vehicles(self : "LunaticAgent", vehicle_list=None, max_distance=None, up_angle_th=90, low_angle_th=0,
                                lane_offset=0):
    """
    Method to check if there is a vehicle in front or around the agent blocking its path.

        :param vehicle_list (list of carla.Vehicle): list containing vehicle objects.
            If None, all vehicle in the scene are used
        :param max_distance: max free-space to check for obstacles.
            If None, the base threshold value is used

    The angle between the location and reference transform will also be taken into account. 
    Being 0 a location in front and 180, one behind, i.e, the vector between has to satisfy: 
    low_angle_th < angle < up_angle_th.
    """

    if self.config.obstacles.ignore_vehicles:
        return ObstacleDetectionResult(False, None, -1)
    
    if vehicle_list is None:
        # NOTE: If empty list is passed e.g. for walkers this pulls all vehicles
        # TODO: Propose update to original carla
        vehicle_list = self._world.get_actors().filter("*vehicle*")
    elif len(vehicle_list) == 0: # Case for no pedestrians
        return ObstacleDetectionResult(False, None, -1)

    def get_route_polygon():
        # Note nested functions can access variables from the outer scope
        route_bb = []
        extent_y = self._vehicle.bounding_box.extent.y
        r_ext = extent_y + self.config.controls.offset
        l_ext = -extent_y + self.config.controls.offset
        r_vec = ego_transform.get_right_vector()
        p1 = ego_location + carla.Location(r_ext * r_vec.x, r_ext * r_vec.y)
        p2 = ego_location + carla.Location(l_ext * r_vec.x, l_ext * r_vec.y)
        route_bb.extend([[p1.x, p1.y, p1.z], [p2.x, p2.y, p2.z]])

        for wp, _ in self._local_planner.get_plan():
            if ego_location.distance(wp.transform.location) > max_distance:
                break

            r_vec = wp.transform.get_right_vector()
            p1 = wp.transform.location + carla.Location(r_ext * r_vec.x, r_ext * r_vec.y)
            p2 = wp.transform.location + carla.Location(l_ext * r_vec.x, l_ext * r_vec.y)
            route_bb.extend([[p1.x, p1.y, p1.z], [p2.x, p2.y, p2.z]])

        # Two points don't create a polygon, nothing to check
        if len(route_bb) < 3:
            return None

        return Polygon(route_bb)

    if not max_distance:
        max_distance = self.config.obstacles.base_vehicle_threshold

    ego_transform = self._vehicle.get_transform()
    ego_location = ego_transform.location
    ego_wpt = self._map.get_waypoint(ego_location)

    # Get the right offset
    if ego_wpt.lane_id < 0 and lane_offset != 0:
        lane_offset *= -1

    # Get the transform of the front of the ego
    ego_front_transform = ego_transform
    ego_front_transform.location += carla.Location(
        self._vehicle.bounding_box.extent.x * ego_transform.get_forward_vector())

    opposite_invasion = abs(self.config.controls.offset) + self._vehicle.bounding_box.extent.y > ego_wpt.lane_width / 2
    use_bbs = self.config.unknown.use_bbs_detection or opposite_invasion or ego_wpt.is_junction

    # Get the route bounding box
    route_polygon = get_route_polygon()

    for target_vehicle in vehicle_list:
        if target_vehicle.id == self._vehicle.id:
            continue

        target_transform = target_vehicle.get_transform()
        if target_transform.location.distance(ego_location) > max_distance:
            continue

        target_wpt = self._map.get_waypoint(target_transform.location, lane_type=carla.LaneType.Any)

        # General approach for junctions and vehicles invading other lanes due to the offset
        if (use_bbs or target_wpt.is_junction) and route_polygon:

            target_bb = target_vehicle.bounding_box
            target_vertices = target_bb.get_world_vertices(target_vehicle.get_transform())
            target_list = [[v.x, v.y, v.z] for v in target_vertices]
            target_polygon = Polygon(target_list)

            if route_polygon.intersects(target_polygon):
                return ObstacleDetectionResult(True, target_vehicle, compute_distance(target_vehicle.get_location(), ego_location))

        # Simplified approach, using only the plan waypoints (similar to TM)
        else:

            if target_wpt.road_id != ego_wpt.road_id or target_wpt.lane_id != ego_wpt.lane_id + lane_offset:
                next_wpt = self._local_planner.get_incoming_waypoint_and_direction(steps=3)[0]
                if not next_wpt:
                    continue
                if target_wpt.road_id != next_wpt.road_id or target_wpt.lane_id != next_wpt.lane_id + lane_offset:
                    continue

            target_forward_vector = target_transform.get_forward_vector()
            target_extent = target_vehicle.bounding_box.extent.x
            target_rear_transform = target_transform
            target_rear_transform.location -= carla.Location(
                x=target_extent * target_forward_vector.x,
                y=target_extent * target_forward_vector.y,
            )

            if is_within_distance(target_rear_transform, ego_front_transform, max_distance,
                                    [low_angle_th, up_angle_th]):
                return ObstacleDetectionResult(True, target_vehicle, compute_distance(target_transform.location, ego_transform.location))

    return ObstacleDetectionResult(False, None, -1)

#TODO: UNCLEAR IF CORRECT -> understand angles
detect_vehicles_in_front = partial(detect_vehicles, up_angle_th=90, low_angle_th=0)
detect_vehicles_behind = partial(detect_vehicles, up_angle_th=180, low_angle_th=160)



def generate_lane_change_path(waypoint, direction='left', distance_same_lane=10,
                                   distance_other_lane=25, lane_change_distance=25,
                                   check=True, lane_changes=1, step_distance=2):
    """
    This method generates a path that results in a lane change.
    Use the different distances to fine-tune the maneuver.
    If the lane change is impossible, the returned path will be empty.
    """
    distance_same_lane = max(distance_same_lane, 0.1)
    distance_other_lane = max(distance_other_lane, 0.1)
    lane_change_distance = max(lane_change_distance, 0.1)

    plan = [(waypoint, RoadOption.LANEFOLLOW)]
    option = RoadOption.LANEFOLLOW

    # Same lane
    distance = 0
    while distance < distance_same_lane:
        next_wps = plan[-1][0].next(step_distance)  # follow a path of waypoints
        if not next_wps:
            return []
        next_wp = next_wps[0]
        distance += next_wp.transform.location.distance(plan[-1][0].transform.location)
        plan.append((next_wp, RoadOption.LANEFOLLOW))  # next waypoint to the path

    if direction == 'left':
        option = RoadOption.CHANGELANELEFT
    elif direction == 'right':
        option = RoadOption.CHANGELANERIGHT
    else:
        # ERROR, input value for change must be 'left' or 'right'
        return []

    lane_changes_done = 0
    lane_change_distance = lane_change_distance / lane_changes

    # Lane change
    while lane_changes_done < lane_changes:

        # Move forward
        next_wps = plan[-1][0].next(lane_change_distance)
        if not next_wps:
            return []
        next_wp = next_wps[0]

        # Get the side lane
        if direction == 'left':
            if check and str(next_wp.lane_change) not in ['Left', 'Both']:
                return []
            side_wp = next_wp.get_left_lane()  # get waypoint on other lane
        else:
            if check and str(next_wp.lane_change) not in ['Right', 'Both']:
                return []
            side_wp = next_wp.get_right_lane()

        if not side_wp or side_wp.lane_type != carla.LaneType.Driving:
            return []

        # Update the plan
        plan.append((side_wp, option))
        lane_changes_done += 1

    # Other lane
    # NOTE: Might force it to follow the other lane for some time
    distance = 0
    while distance < distance_other_lane:
        next_wps = plan[-1][0].next(step_distance)
        if not next_wps:
            return []
        next_wp = next_wps[0]
        distance += next_wp.transform.location.distance(plan[-1][0].transform.location)
        plan.append((next_wp, RoadOption.LANEFOLLOW))

    return plan