"""
This module contains a flexible variant of the local planner provided by CARLA to perform low-level
waypoint following based on PID controllers.
"""

from __future__ import annotations

from collections import deque
from typing import List, Optional, Tuple, TYPE_CHECKING

import carla

from agents.dynamic_planning.dynamic_controller import DynamicVehiclePIDController
from agents.navigation.local_planner import LocalPlanner, PlannedWaypoint
from agents.tools.misc import draw_waypoints, get_speed
from classes.constants import RoadOption
if TYPE_CHECKING:
    from classes.type_protocols import UseableWithDynamicPlanner
    from classes.rss_sensor import RssSensor


class DynamicLocalPlanner(LocalPlanner):
    """
    LocalPlanner implements the basic behavior of following a
    trajectory of waypoints that is generated on-the-fly.

    The low-level motion of the vehicle is computed by using two PID controllers,
    one is used for the lateral control and the other for the longitudinal control (cruise speed).

    When multiple paths are available (intersections) this local planner makes a random choice,
    unless a given global plan has already been specified.
    """
    _waypoints_queue : "deque[Tuple[carla.Waypoint, RoadOption]]"

    @property
    def config(self):
        return self._agent.ctx.config

    def __init__(self,
                 agent : "UseableWithDynamicPlanner",
                 opt_dict: None,
                 map_inst: carla.Map = None,  # type: ignore # keep for compatibility, inform user
                 world: carla.World = None    # type: ignore # keep for compatibility, inform user
                 ):
        """
        :param vehicle: actor to apply to local planner logic onto
        :param opt_dict:
            
            Attention:
                .. deprecated:: _
                    Do not use anymore. The agent's :py:attr:`config<.LunaticAgent.config>`
                    is used instead.
             
            dictionary of arguments with different parameters:
            dt: time between simulation steps
            target_speed: desired cruise speed in Km/h
            sampling_radius: distance between the waypoints part of the plan
            lateral_control_dict: values of the lateral PID controller
            longitudinal_control_dict: values of the longitudinal PID controller
            max_throttle: maximum throttle applied to the vehicle
            max_steering: maximum steering applied to the vehicle
            offset: distance between the route waypoints and the center of the lane
            
        :param map_inst: carla.Map instance to avoid the expensive call of getting it.
        
        Raises:
            ValueError: If the 'opt_dict' parameter is passed.
        """
        if opt_dict:
            raise ValueError("The 'opt_dict' parameter is deprecated. Do not pass")
        
        #self._agent : LunaticAgent = weakref.proxy(agent)
        self._agent = agent
        self._vehicle = self._agent._vehicle
        assert self._vehicle, "The agent must have a vehicle to create a local planner"
        self._world = world or self._vehicle.get_world()
        try:
            if map_inst:
                if isinstance(map_inst, carla.Map):
                    self._map : carla.Map = map_inst
                else:
                    print("Warning: Ignoring the given map as it is not a 'carla.Map'")
                    self._map : carla.Map = self._world.get_map()
            else:
                self._map : carla.Map = self._world.get_map()
        except AttributeError as e:
            print(e)

        # set in _init_controller
        self._vehicle_controller : DynamicVehiclePIDController = None  # type: ignore[assignment]
        self.target_waypoint : carla.Waypoint = None  # type: ignore[assignment]
        """The next waypoint in the queue, as long as it is not empty."""
        self.target_road_option : RoadOption = None  # type: ignore[assignment]
        """The next :py:class:`RoadOption` in the queue, as long as it is not empty."""

        self._waypoints_queue = deque(maxlen=10000)
        self._min_waypoint_queue_length = 100
        self._stop_waypoint_creation = False

        # initializing controller
        self._init_controller()

    @property
    def next_target(self) -> Tuple[carla.Waypoint, RoadOption]:
        """
        The next waypoint and road option in the queue to use this step.
        
        Raises:
            IndexError: If the queue is empty.
        """
        return self._waypoints_queue[0]

    def _init_controller(self):
        """Controller initialization"""
        self._vehicle_controller = DynamicVehiclePIDController(self._agent)

        # Compute the current vehicle waypoint
        current_waypoint = self._map.get_waypoint(self._vehicle.get_location())
        self.target_road_option = RoadOption.VOID
        self.target_waypoint, self.target_road_option = (current_waypoint, RoadOption.LANEFOLLOW)
        self._waypoints_queue.append(PlannedWaypoint(self.target_waypoint, self.target_road_option))

    def set_speed(self, speed):
        """
        Changes the target speed

        :param speed: new target speed in Km/h
        :return:
        """
        if self.config.speed.follow_speed_limits:
            print("WARNING: The max speed is currently set to follow the speed limits. "
                  "Use 'follow_speed_limits' to deactivate this")
        self.config.speed.target_speed = speed

    def follow_speed_limits(self, value=True):
        """
        Activates a flag that makes the max speed dynamically vary according to the speed limits

        :param value: bool
        :return:
        """
        self.config.speed.follow_speed_limits = value

    @property  # allows to use _compute_next_waypoints of parent
    def _sampling_radius(self):
        return self.config.planner.sampling_radius

    # set_global_plan -> parent

    def run_step(self, debug=False):
        """
        Execute one step of local planning which involves running the longitudinal and lateral PID controllers to
        follow the waypoints trajectory.

        :param debug: boolean flag to activate waypoints debugging
        :return: control to be applied
        """
        if self.config.speed.follow_speed_limits:
            self.config.speed.target_speed = self.config.live_info.current_speed_limit

        # Add more waypoints too few in the horizon
        if not self._stop_waypoint_creation and len(self._waypoints_queue) < self._min_waypoint_queue_length:
            self._compute_next_waypoints(k=self._min_waypoint_queue_length)

        # Purge the queue of obsolete waypoints
        veh_location = self._vehicle.get_location()
        vehicle_speed = get_speed(self._vehicle) / 3.6
        self._min_distance = self.config.planner.min_distance_next_waypoint + self.config.planner.next_waypoint_distance_ratio * vehicle_speed

        num_waypoint_removed = 0
        for waypoint, _ in self._waypoints_queue:

            if len(self._waypoints_queue) - num_waypoint_removed == 1:
                min_distance = 1  # Don't remove the last waypoint until very close by
            else:
                min_distance = self._min_distance

            if veh_location.distance(waypoint.transform.location) < min_distance:
                num_waypoint_removed += 1
            else:
                break

        if num_waypoint_removed > 0:
            for _ in range(num_waypoint_removed):
                self._waypoints_queue.popleft()

        # Get the target waypoint and move using the PID controllers. Stop if no target waypoint
        if len(self._waypoints_queue) == 0:
            control = carla.VehicleControl()
            control.steer = 0.0
            control.throttle = 0.0
            control.brake = 1.0
            control.hand_brake = False
            control.manual_gear_shift = False
        else:
            self.target_waypoint, self.target_road_option = self._waypoints_queue[0]
            control = self._vehicle_controller.run_step(self.target_waypoint)

        if debug:
            draw_waypoints(self._vehicle.get_world(), [self.target_waypoint], road_options=[self.target_road_option], z=1.0)

        return control

# def get_incoming_waypoint_and_direction(self, steps=3):
  
class DynamicLocalPlannerWithRss(DynamicLocalPlanner):
    
    def __init__(self, agent,
                 opt_dict: None = None,
                 map_inst: carla.Map = None,  # type: ignore # keep for compatibility, inform user
                 world: carla.World = None,  # type: ignore # keep for compatibility, inform user
                 rss_sensor: Optional[RssSensor] = None):
        super().__init__(agent, opt_dict, map_inst, world)
        self._rss_sensor = rss_sensor
        
        
    def set_global_plan(self, current_plan : List[Tuple[carla.Waypoint, RoadOption]], stop_waypoint_creation=True, clean_queue=True):
        """
        Adds a new plan to the local planner. A plan must be a list of [carla.Waypoint, RoadOption] pairs
        The 'clean_queue` parameter erases the previous plan if True, otherwise, it adds it to the old one
        The 'stop_waypoint_creation' flag stops the automatic creation of random waypoints

        :param current_plan: list of (carla.Waypoint, RoadOption)
        :param stop_waypoint_creation: bool
        :param clean_queue: bool
        :return:
        """
        if clean_queue:
            self._waypoints_queue.clear()
            # NOTE: We clean the RSS routing targets below and fill it with the new/or extended queue. No need to clean it here.

        # Remake the waypoints queue if the new plan has a higher length than the queue
        new_plan_length = len(current_plan) + len(self._waypoints_queue)
        if new_plan_length > self._waypoints_queue.maxlen:  # type: ignore # is bounded
            new_waypoint_queue : deque[Tuple[carla.Waypoint, RoadOption]] = deque(maxlen=new_plan_length)
            for wp in self._waypoints_queue:
                new_waypoint_queue.append(wp)
            self._waypoints_queue = new_waypoint_queue

        if self._rss_sensor:
            self._rss_sensor.sensor.reset_routing_targets()
            assert len(self._rss_sensor.sensor.routing_targets) == 0, f"Routing targets not cleared. Remaining: {self._rss_sensor.sensor.routing_targets}"  # TODO: End remove.
        for elem in current_plan:
            self._waypoints_queue.append(elem)
            if self._rss_sensor:
                self._rss_sensor.sensor.append_routing_target(elem[0].transform)
        if self._rss_sensor:
            self._rss_sensor.drop_route()  # Replans from remaining routing targets

        self._stop_waypoint_creation = stop_waypoint_creation
