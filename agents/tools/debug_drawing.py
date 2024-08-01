# Most errors are from covariant
# pyright: reportArgumentType=information
# pyright: reportOptionalMemberAccess=information
import math
import carla

from typing import TYPE_CHECKING, Optional

from agents.tools import lane_explorer
from classes.constants import RoadOption, RoadOptionColor

if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent
    from classes.worldmodel import GameFramework
    from agents.tools.misc import get_trafficlight_trigger_location # imported correctly from end of misc, to avoid circular import
    


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


def draw_waypoints(world : carla.World, waypoints: "list[carla.Waypoint]", z=0.5, *, road_options: Optional["list[RoadOption]"]=None, **kwargs):
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


def debug_drawing(agent:"LunaticAgent", game_framework : "GameFramework", destination: carla.Waypoint):
    #from agents.tools.misc import get_trafficlight_trigger_location # pylint: disable=import-outside-toplevel # is a circular import

    world_model = game_framework.world_model
    assert world_model, "GameFramework has no world_model"

    # Debug drawing of the route
    try:
        loc = agent._local_planner._waypoints_queue[-1][0].transform.location # TODO find a nicer way
        loc = loc + carla.Vector3D(0, 0, 1.5) # elevate to be not in road
    except IndexError:
        pass
    game_framework.debug.draw_point(loc, life_time=0.5)   # type: ignore[arg-type]
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