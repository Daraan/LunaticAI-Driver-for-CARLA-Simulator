# Most errors are from covariant
# pyright: reportArgumentType=information
# pyright: reportOptionalMemberAccess=information
import math
import random
import carla


from typing import TYPE_CHECKING, Any, Optional

from classes.constants import RoadOption, RoadOptionColor
from agents.tools import misc # draw_waypoints patched from this module

if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent
    from classes.worldmodel import GameFramework
    

red = carla.Color(255, 0, 0)
green = carla.Color(0, 255, 0)
blue = carla.Color(47, 210, 231)
cyan = carla.Color(0, 255, 255)
yellow = carla.Color(255, 255, 0)
orange = carla.Color(255, 162, 0)
white = carla.Color(255, 255, 255)

trail_life_time = 10
waypoint_separation = 4.0


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




def _draw_route_wp(world: carla.World, waypoints: "list[tuple[carla.Waypoint, RoadOption]]", vertical_shift=0.5, size=0.3, downsample=1, life_time=1.0):
    """
    Draw a list of waypoints at a certain height given in vertical_shift.

    * NOTE: This is based on the function from the Leaderboard_ project.
    """
    for i, w in enumerate(waypoints):
        if i % downsample != 0:
            continue

        color = roadoption_color(w[1])

        wp = w[0].transform.location + carla.Location(z=vertical_shift)
        world.debug.draw_point(wp, size=size, color=color, life_time=life_time)  # type: ignore[arg-type]

    world.debug.draw_point(waypoints[0][0].transform.location + carla.Location(z=vertical_shift), size=2*size, # type: ignore[arg-type]
                                color=carla.Color(0, 0, 128), life_time=life_time)
    world.debug.draw_point(waypoints[-1][0].transform.location + carla.Location(z=vertical_shift), size=2*size,# type: ignore[arg-type]
                                color=carla.Color(128, 128, 128), life_time=life_time)


def _draw_route_trans(world: carla.World, waypoints: "list[tuple[carla.Transform, RoadOption]]", vertical_shift=0.5, size=0.3, downsample=1, life_time=1.0):
    """
    Draw a list of waypoints at a certain height given in vertical_shift.

    * NOTE: This is based on the function from the Leaderboard_ project.
    """
    for i, w in enumerate(waypoints):
        if i % downsample != 0:
            continue

        color = roadoption_color(w[1])

        wp = w[0].location + carla.Location(z=vertical_shift)
        world.debug.draw_point(wp, size=size, color=color, life_time=life_time) 

    world.debug.draw_point(waypoints[0][0].location + carla.Location(z=vertical_shift), size=2*size,  # type: ignore[arg-type]
                                color=carla.Color(0, 0, 128), life_time=life_time)
    world.debug.draw_point(waypoints[-1][0].location + carla.Location(z=vertical_shift), size=2*size, # type: ignore[arg-type]
                                color=carla.Color(128, 128, 128), life_time=life_time)


def draw_route(world: carla.World, waypoints: "list[tuple[carla.Transform | carla.Waypoint, RoadOption]]", vertical_shift=0.5, size=0.3, downsample=1, life_time=1.0):
    """
    Draw a list of waypoints at a certain height given in vertical_shift.

    * NOTE: This is based on the function from the Leaderboard_ project.
    """
    if len(waypoints) == 0:
        return
    if isinstance(waypoints[0][0], carla.Transform):
        _draw_route_trans(world, waypoints, vertical_shift, size, downsample, life_time) # type: ignore[arg-type]
    elif isinstance(waypoints[0][0], carla.Waypoint):
        _draw_route_wp(world, waypoints, vertical_shift, size, downsample, life_time)  # type: ignore[arg-type]
    else:
        print("Drawing of type:", type(waypoints[0][0]), "not supported.")


def draw_waypoints(world : carla.World, waypoints: "list[carla.Waypoint]", z=0.5, *, road_options: Optional["list[RoadOption]"]=None, **kwargs: Any) -> None:
    """
    Draw a list of waypoints at a certain height given in z.

        :param world: carla.world object
        :param waypoints: list or iterable container with the waypoints to draw
        :param z: height in meters
        
    .. NOTE Imported by the local_planner -> circular import problems
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
        world.debug.draw_arrow(begin, end, color=color, **kwargs)  # type: ignore[arg-type]


def debug_drawing(agent:"LunaticAgent", game_framework : "GameFramework", destination: Optional[carla.Location]):
    """
    
    Raises:
        IndexError: If the agent has no more waypoints and no **destination** is given.
    """
    #from agents.tools.misc import get_trafficlight_trigger_location # pylint: disable=import-outside-toplevel # is a circular import

    world_model = game_framework.world_model
    assert world_model, "GameFramework has no world_model"

    # Debug drawing of the route
    if destination:
        loc = destination
    else:
        
        loc = agent._local_planner._waypoints_queue[-1][0].transform.location # TODO find a nicer way
        loc = loc + carla.Vector3D(0, 0, 1.5) # elevate to be not in road
            
    game_framework.debug.draw_point(loc, life_time=0.5)   # type: ignore[arg-type]
    draw_waypoint_info(game_framework.debug, agent._current_waypoint, lt=10)
    if agent._current_waypoint.is_junction:
        junction = agent._current_waypoint.get_junction()
        draw_junction(game_framework.debug, junction, 0.1)
    if not agent._last_traffic_light:
        traffic_light = agent.live_info.next_traffic_light
    else:
        traffic_light = agent._last_traffic_light

    if traffic_light:
        wps = traffic_light.get_stop_waypoints()
        for wp in wps:
            game_framework.debug.draw_point(wp.transform.location + carla.Location(z=2), life_time=0.6)  
            draw_waypoint_info( game_framework.debug, wp)
        trigger_loc = misc.get_trafficlight_trigger_location(traffic_light)
        trigger_wp = game_framework.get_map().get_waypoint(trigger_loc)
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


def draw_transform(debug: carla.DebugHelper, trans: carla.Transform, col: carla.Color=carla.Color(255, 0, 0), lt:float=-1) -> None:
    debug.draw_arrow(
        trans.location, trans.location + trans.get_forward_vector(), # type: ignore[arg-type]
        thickness=0.05, arrow_size=0.1, color=col, life_time=lt)


def draw_junction(debug: carla.DebugHelper, junction : carla.Junction, l_time:float=10):
    """Draws a junction bounding box and the initial and final waypoint of every lane."""
    # draw bounding box
    box = junction.bounding_box
    point1 = box.location + carla.Location(x=box.extent.x, y=box.extent.y, z=2)
    point2 = box.location + carla.Location(x=-box.extent.x, y=box.extent.y, z=2)
    point3 = box.location + carla.Location(x=-box.extent.x, y=-box.extent.y, z=2)
    point4 = box.location + carla.Location(x=box.extent.x, y=-box.extent.y, z=2)
    debug.draw_line(
        point1, point2,
        thickness=0.1, color=orange, life_time=l_time, persistent_lines=False)
    debug.draw_line(
        point2, point3,
        thickness=0.1, color=orange, life_time=l_time, persistent_lines=False)
    debug.draw_line(
        point3, point4,
        thickness=0.1, color=orange, life_time=l_time, persistent_lines=False)
    debug.draw_line(
        point4, point1,
        thickness=0.1, color=orange, life_time=l_time, persistent_lines=False)
    # draw junction pairs (begin-end) of every lane
    junction_w = junction.get_waypoints(carla.LaneType.Any)
    for pair_w in junction_w:
        draw_transform(debug, pair_w[0].transform, orange, l_time)
        debug.draw_point(
            pair_w[0].transform.location + carla.Location(z=0.75), 0.1, orange, l_time, False)
        draw_transform(debug, pair_w[1].transform, orange, l_time)
        debug.draw_point(
            pair_w[1].transform.location + carla.Location(z=0.75), 0.1, orange, l_time, False)
        debug.draw_line(
            pair_w[0].transform.location + carla.Location(z=0.75),
            pair_w[1].transform.location + carla.Location(z=0.75), 0.1, white, l_time, False)


def draw_waypoint_info(debug: carla.DebugHelper, w: carla.Waypoint, lt:float=5):
    w_loc = w.transform.location
    debug.draw_string(w_loc + carla.Location(z=0.5), "lane: " + str(w.lane_id), False, yellow, lt)
    debug.draw_string(w_loc + carla.Location(z=1.0), "road: " + str(w.road_id), False, blue, lt)
    debug.draw_string(w_loc + carla.Location(z=-.5), str(w.lane_change), False, red, lt)


def draw_waypoint_union(debug: carla.DebugHelper, w0: carla.Waypoint, w1: carla.Waypoint, color: carla.Color=carla.Color(255, 0, 0), lt:float=5) -> None:
    debug.draw_line(
        w0.transform.location + carla.Location(z=0.25), # type: ignore[arg-type]
        w1.transform.location + carla.Location(z=0.25),   # type: ignore[arg-type]
        thickness=0.1, color=color, life_time=lt, persistent_lines=False)
    debug.draw_point(w1.transform.location + carla.Location(z=0.25), 0.1, color, lt, False) # type: ignore[arg-type]


def lane_explorer(debug : carla.DebugHelper, current_w: carla.Waypoint, draw_info=True, waypoint_separation=waypoint_separation, trail_life_time:float=0.1):
    """From CARLA lane_explorer.py example"""

    # list of potential next waypoints
    potential_w = list(current_w.next(waypoint_separation))

    # check for available right driving lanes
    if current_w.lane_change & carla.LaneChange.Right:
        right_w = current_w.get_right_lane()
        if right_w and right_w.lane_type == carla.LaneType.Driving:
            potential_w += list(right_w.next(waypoint_separation))

    # check for available left driving lanes
    if current_w.lane_change & carla.LaneChange.Left:
        left_w = current_w.get_left_lane()
        if left_w and left_w.lane_type == carla.LaneType.Driving:
            potential_w += list(left_w.next(waypoint_separation))

    # choose a random waypoint to be the next
    next_w = random.choice(potential_w)
    potential_w.remove(next_w)

    # Render some nice information, notice that you can't see the strings if you are using an editor camera
    if draw_info:
        draw_waypoint_info(debug, current_w, trail_life_time)
    draw_waypoint_union(debug, current_w, next_w, cyan if current_w.is_junction else green, trail_life_time)
    draw_transform(debug, current_w.transform, white, trail_life_time)

    # print the remaining waypoints
    for p in potential_w:
        draw_waypoint_union(debug, current_w, p, red, trail_life_time)
        draw_transform(debug, p.transform, white, trail_life_time)

    # draw all junction waypoints and bounding box
    if next_w.is_junction:
        junction = next_w.get_junction()
        draw_junction(debug, junction, trail_life_time)
    return next_w


# circular import
misc.draw_waypoints = draw_waypoints