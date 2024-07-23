"""
Leaderboard_ 2.0 compatible version of the Lunatic Agent

Attention: 
    Command line overrides are currently not supported for this agent,
    therefore this module allows to define some global constants to 
    that can adjust settings the settings if they are not set to None (default).
    
    These global settings are only used if :py:meth:`LunaticChallenger.setup` 
    is called with a string pointing to a configuration file. Passing a
    :py:class:`.LaunchConfig` directly will skip the Hydra_ setup and the global
    values will not be used.
"""
import operator
import os
from typing import Any, Dict, TYPE_CHECKING, Union
from omegaconf import OmegaConf
from hydra import compose, initialize_config_dir
from hydra.core.utils import configure_log

import carla
import pygame

from agents.tools.debug_drawing import draw_route
from classes.exceptions import UserInterruption

try:
    # Prefer the current submodule version
    from launch_tools import CarlaDataProvider, GameTime, singledispatchmethod
except ModuleNotFoundError:
    from srunner.scenariomanager.timer import GameTime                        # pyright: ignore[reportMissingImports]      
    from srunner.scenariomanager.carla_data_provider import CarlaDataProvider # pyright: ignore[reportMissingImports]
    from functools import singledispatchmethod # If this fails please use Python3.10+
    

try:
    from leaderboard.autoagents.autonomous_agent import AutonomousAgent, Track # pyright: ignore[reportMissingImports]
    from leaderboard.utils.route_manipulation import downsample_route          # pyright: ignore[reportMissingImports]
except ModuleNotFoundError:
    # Leaderboard is not a submodule, cannot use it on readthedocs 
    if "READTHEDOCS" in os.environ and not TYPE_CHECKING:
        class AutonomousAgent: pass # noqa
    else: raise

from agents.lunatic_agent import LunaticAgent

from classes.constants import Phase
from classes.keyboard_controls import RSSKeyboardControl
from classes.worldmodel import GameFramework, WorldModel, AD_RSS_AVAILABLE
from agents.tools.logging import logger
from agents.tools.config_creation import LaunchConfig, LunaticAgentSettings

if TYPE_CHECKING:
    from scenario_runner.srunner.autoagents.sensor_interface import SensorInterface
    from classes.constants import RoadOption
    from data_gathering.car_detection_matrix.run_matrix import DetectionMatrix

import logging
logger.setLevel(logging.DEBUG)


def get_entry_point():
    """Must return the name of the class to be used"""
    return "LunaticChallenger"

# --- DEBUG OVERWRITES ---
# as the leaderboard agent cannot accept command line overrides these can be set here.
DEBUG = False

WORLD_MODEL_DESTROY_SENSORS = True

ENABLE_RSS = AD_RSS_AVAILABLE and True
"""If not :code:`None`, overwrites :py:attr:`LunaticAgentSettings.rss.enabled`"""

ENABLE_DATA_MATRIX = None
"""If not :code:`None`, overwrites :py:attr:`LunaticAgentSettings.detection_matrix.enabled`"""

DATA_MATRIX_ASYNC = False
"""Run the DetectionMatrix update in a separate thread; overwrites :py:attr:`LunaticAgentSettings.detection_matrix.sync`."""

DATA_MATRIX_SYNC_INTERVAL = None
"""When running synchronously how many ticks should be between two updates; overwrites :py:attr:`LunaticAgentSettings.detection_matrix.sync_interval`"""

USE_OPEN_DRIVE_DATA = False

DOWNSAMPLING_FACTOR_OF_ROUTE_COORDINATES = 5
"""
The smaller the the value the more exact will the agent stick to the original route,
BUT ONLY IF the route is provided as a fine-grained route.

NOTE: We should NOT rely on the route to be available in a fine grained manner -> Should work with larger values

Larger values will make the agent cut corners and drive more straight lines.
Needs extra tools to stick to the road.
"""

args: LaunchConfig
"""Global access to the launch config; set in :py:meth:`LunaticChallenger.setup`"""

class LunaticChallenger(AutonomousAgent, LunaticAgent):
    """
    Variant of the :py:class:`.LunaticAgent` that is compatible with the 
    `Leaderboard 2.0 <https://leaderboard.carla.org/>`_ interface.
    
    Attention:
        If the :py:class:`LunaticChallenger` is used without the Leaderboard 2.0 framework
        the :py:meth:`__call__`  method should be used instead of :py:meth:`run_step`
        to acquire the next control. 
    """
    
    sensor_interface: "SensorInterface" #: :meta private:
    
    _global_plan: "list[tuple[Dict[str, float], RoadOption]]" = None
    _global_plan_world_coord: "list[tuple[carla.Transform, RoadOption]]" = None
    _global_plan_waypoints: "list[tuple[carla.Waypoint, RoadOption]]" = None 
    
    _road_matrix_updater : "DetectionMatrix" = None
    
    def __init__(self, carla_host, carla_port, debug=False):
        """
        Initializes the LunaticChallenger. This does not yet load the config or calls :py:meth:`LunaticAgent.__init__ <agents.lunatic_agent.LunaticAgent.__init__>`.
        
        Further initialization is done in :py:meth:`LunaticChallenger.setup`.
        """
        print("Initializing LunaticChallenger")
        self.world_model: WorldModel = None
        self.game_framework: GameFramework = None
        self._destroyed = False
        super().__init__(carla_host, carla_port, debug)
        self.track = Track.MAP
        self._opendrive_data = None
        self._local_planner = None

    def setup(self, path_to_conf_file: Union[str, LaunchConfig]):
        """
        Initializes the underlying :py:class:`.LunaticAgent` as well as instances of :py:class:`.GameFramework` and :py:class:`.WorldModel`.
        
        To some extends initializes the Hydra_ framework and load the configuration.
        
        Parameters:
            path_to_conf_file : Can either be a string pointing to a configuration file to load a :py:class:`.LaunchConfig` or a :py:class:`.LaunchConfig` to be used directly.
                
                Note: 
                    If a :py:class:`.LaunchConfig` is passed directly the Hydra setup will be skipped.
        """
        self._destroyed = False
        self.track = Track.MAP
        if isinstance(path_to_conf_file, str):
            print("Setup with conf file", path_to_conf_file)
            logger.info("Setup with conf file %s", path_to_conf_file)
            config_dir, config_name = os.path.split(path_to_conf_file)
            # TODO: Maybe move to init so its available during set_global_plan 
            global args
            overrides=["agent=leaderboard"]
            if not GameFramework.hydra_initialized():
                initialize_config_dir(version_base=None, 
                                        config_dir=os.path.abspath(config_dir), 
                                        job_name="LeaderboardAgent")
                if ENABLE_DATA_MATRIX is not None:
                    overrides.append("agent.detection_matrix.enabled=" + str(ENABLE_DATA_MATRIX).lower())
                overrides.append("agent.detection_matrix.sync="+str(DATA_MATRIX_ASYNC).lower())
                if ENABLE_RSS is not None:
                    overrides.append("agent.rss.enabled=" + str(ENABLE_RSS).lower())
                args = compose(config_name=config_name, return_hydra_config=True, 
                            overrides=overrides # uses conf/agent/leaderboard
                            )
                args.debug = DEBUG
                # Let scenario manager decide
                if args.map:
                    logger.warning("Map should be set by scenario manager and be None in the config file found map is %s." % args.map)
                if args.handle_ticks:
                    logger.warning("When using the leaderboard agent, `handle_ticks` should be False.")
                    args.handle_ticks = False
                if args.sync is not None:
                    logger.warning("When using the leaderboard agent, `sync` should be None.")
                    args.sync = None
                
                # Setup Hydra
                from hydra.core.hydra_config import HydraConfig
                if OmegaConf.is_missing(args.hydra.runtime, "output_dir"):
                    args.hydra.runtime.output_dir = args.hydra.run.dir
                HydraConfig.instance().set_config(args)
                os.makedirs(args.hydra.runtime.output_dir, exist_ok=True)
                configure_log(args.hydra.job_logging, logger.name) # Assure that our logger works
                
                if DATA_MATRIX_ASYNC is not None:
                    args.agent.detection_matrix.sync = not DATA_MATRIX_ASYNC
                if DATA_MATRIX_SYNC_INTERVAL is not None:
                    args.agent.detection_matrix.sync_interval = DATA_MATRIX_SYNC_INTERVAL
                logger.info(OmegaConf.to_yaml(args))
            else:
                args = compose(config_name=config_name, return_hydra_config=True, 
                    overrides=overrides)
            logger.setLevel(logging.DEBUG)
            self.args = args
            
            config = LunaticAgentSettings.create(self.args.agent, assure_copy=True, as_dictconfig=True)
        else:
            self.args = path_to_conf_file
            config = self.args.agent
        if OmegaConf.is_missing(config.planner, "dt"):
            config.planner.dt = 1/20 # TODO: maybe get from somewhere else
        
        self.game_framework = GameFramework(self.args, config)
        print("Game framework setup")
        # TODO: How to make args optional
        self.world_model = WorldModel(config, args=self.args)
        self.game_framework.world_model = self.world_model
        print("World Model setup")
        self.controller = self.game_framework.make_controller(self.world_model, RSSKeyboardControl, start_in_autopilot=False) # Note: stores weakref to controller
        print("Initializing agent")
        LunaticAgent.__init__(self, config, self.world_model)
        print("LunaticAgent initialized")
        
        from agents.rules.lane_changes.random import RandomLaneChangeRule
        for rules in self.rules.values():
            for rule in rules:
                if isinstance(rule, RandomLaneChangeRule):
                    rule.enabled = False
            
        # Set plan
        if self._global_plan_waypoints:
            self._local_planner_set_plan(self._global_plan_waypoints)
        
        self.game_framework.agent = self # TODO: Remove this circular reference
        self.agent_engaged = False
        # Print controller docs
        try:
            print(self.controller.get_docstring())
        except Exception:
            pass
        
    def sensors(self) -> "list[dict]":
        """
        Define the sensor suite required by the agent
        
            Returns: 
                A list containing the required sensors in the following format
            
                .. code-block:: python
                
                    [
                    {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
                    'width': 300, 'height': 200, 'fov': 100, 'id': 'Left'},

                    {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
                    'width': 300, 'height': 200, 'fov': 100, 'id': 'Right'},

                    {'type': 'sensor.lidar.ray_cast', 'x': 0.7, 'y': 0.0, 'z': 1.60, 'yaw': 0.0, 'pitch': 0.0, 'roll': 0.0,
                    'id': 'LIDAR'}
                    ]
        
        Note:
            The LunaticChallenger does not use any sensors; the usage of 'sensor.opendrive_map' is experimental, however
            there is yet no parsing done for the data.
        """
        sensors: list = super().sensors() # This should be empty
        
        # temp; remove
        try:
            i = [x['type'] for x in args.leaderboard.sensors].index('sensor.opendrive_map')
        except (ValueError, AttributeError):
            pass
        else:
            args.leaderboard.sensors[i].use = USE_OPEN_DRIVE_DATA
        
        # add sensors if they have the use flag in the config
        try:
            sensors.extend(filter(operator.itemgetter('use'), args.leaderboard.sensors))
        except Exception:
            pass
        logger.info("Using sensors: %s", sensors)
        return sensors

    @staticmethod
    def _print_input_data(input_data):
        if not input_data:
            return None
        print("=====================>")
        for key, val in input_data.items():
            if hasattr(val[1], 'shape'):
                shape = val[1].shape
                print("[{} -- {:06d}] with shape {}".format(key, val[0], shape))
            else:
                print("[{} -- {:06d}] ".format(key, val[0]))
        print("<=====================")
        return True
    
    # This allows BlockingRules to pick up the coorect function
    @singledispatchmethod
    def run_step(self, debug:bool=False, second_pass=False) -> carla.VehicleControl:   
        """
        Attention:
            Use :py:meth:`__call__` instead of this method!
        """     
        # TODO: Possibly singledispatch to __call__ instead
        return super(AutonomousAgent, self).run_step(debug=self.args.debug, second_pass=second_pass)

    @run_step.register(dict)
    def _(self, input_data:"Dict[str, tuple[int, Any]]", timestamp=None) -> carla.VehicleControl:
        """Function that is called by leaderboard framework"""
        try:
            if self._print_input_data(input_data) and "OpenDRIVE" in input_data:
                frame, data = input_data["OpenDRIVE"]
                data : str = data["opendrive"]
                if self._opendrive_data != data:
                    if self._opendrive_data is not None:
                        #breakpoint()
                        pass
                    self._opendrive_data = data
                    print(frame, data[:5000])
                    with open("opendrive.xml", "w") as f:
                        f.write(data)
                else:
                    print("OpenDRIVE data unchanged")
            self.agent_engaged = True # remove this, if not used
            
            with self.game_framework:
                control = self.run_step(self.args.debug) # Call Lunatic Agent run_step
            # Handle render updates
            
            self.execute_phase(Phase.APPLY_MANUAL_CONTROLS | Phase.BEGIN, prior_results=control)
            if self.controller.parse_events(self.get_control()):
                print("Exiting by user input.")
                raise UserInterruption("Exiting by user input.")
            self.execute_phase(Phase.APPLY_MANUAL_CONTROLS | Phase.END, prior_results=None)
            
            self.execute_phase(Phase.EXECUTION | Phase.BEGIN, prior_results=control)
            final_controls: carla.VehicleControl = self.get_control()
            
            # TODO: Update HUD controls info
            return final_controls
        except Exception as e:
            if not isinstance(e, UserInterruption):
                logger.error("Error in LunaticChallenger.run_step:", exc_info=True)
            self.destroy()
            raise e
        
    # NOTE: to update the doc use
    #run_step.func.__doc__ += "\n" + LunaticAgent.run_step.__doc__

    # TODO maybe move to misc / tools
    @staticmethod
    def _transform_to_waypoint(transform: "carla.Transform", project_to_road=True, lane_type=carla.LaneType.Driving) -> "carla.Waypoint":
        return CarlaDataProvider.get_map().get_waypoint(transform.location, project_to_road=project_to_road, lane_type=lane_type)
    
    def _local_planner_set_plan(self, plan):
        super(AutonomousAgent, self).set_global_plan(plan, stop_waypoint_creation=True, clean_queue=True)
        if self.game_framework._args.debug:
            draw_route(CarlaDataProvider.get_world(), plan, vertical_shift=0.5, size=0.15, downsample=1, life_time=1000.0)
    
    def set_global_plan(self, global_plan_gps: "tuple[Dict[str, float], RoadOption]", global_plan_world_coord: "tuple[carla.Transform, RoadOption]"):
        """
        Set the plan (route) for the agent
        """
        #super().set_global_plan(global_plan_gps, global_plan_world_coord)
        print("==============Road updated============")
        print("Plan GPS", global_plan_gps[:10])
        print("Plan World Coord", global_plan_world_coord[:10])
        
        ds_ids: "list[int]" = downsample_route(global_plan_world_coord, DOWNSAMPLING_FACTOR_OF_ROUTE_COORDINATES) # Downsample to less distance. TODO: should increase this
        print("Downsampled ids", ds_ids)
        
        # Reduce the global plan to the downsampled ids
        self._global_plan_world_coord = [(global_plan_world_coord[x][0], global_plan_world_coord[x][1]) for x in ds_ids]
        assert self._global_plan_world_coord == [global_plan_world_coord[x] for x in ds_ids]
        self._global_plan = [global_plan_gps[x] for x in ds_ids]
        self._global_plan_waypoints = [(self._transform_to_waypoint(transform), road_option) for transform, road_option in self._global_plan_world_coord]
        if self._local_planner is not None:
             # TODO: maybe waypoints is not necessary as we extract locations
            self._local_planner_set_plan(self._global_plan_waypoints)
    
    def __call__(self) -> carla.VehicleControl:
        """
        Executes the next step and returns the control for the vehicle.
        
        Attention:
            Use this function instead of :py:meth:`run_step`!
        """
        input_data = self.sensor_interface.get_data(GameTime.get_frame())

        timestamp = GameTime.get_time()

        if args.leaderboard.print_time_info:
            if not self.wallclock_t0:
                self.wallclock_t0 = GameTime.get_wallclocktime()
            wallclock = GameTime.get_wallclocktime()
            wallclock_diff = (wallclock - self.wallclock_t0).total_seconds()
            sim_ratio = 0 if wallclock_diff == 0 else timestamp/wallclock_diff

            print('=== [Agent] -- Wallclock = {} -- System time = {} -- Game time = {} -- Ratio = {}x'.format(
                str(wallclock)[:-3], format(wallclock_diff, '.3f'), format(timestamp, '.3f'), format(sim_ratio, '.3f')))

        control = self.run_step(input_data, timestamp)
        control.manual_gear_shift = False

        return control

    def destroy(self):
        self._destroyed = True
        print("Destroying Lunatic Challenger")
        if self._road_matrix_updater is not None:
            self._road_matrix_updater.stop()
            self._road_matrix_updater = None
        super().destroy()
        if self.world_model:
            if not WORLD_MODEL_DESTROY_SENSORS:
                self.world_model.actors.clear()
            self.world_model.destroy()
            self.world_model = None
        if self.game_framework:
            self.game_framework.agent = None
            self.game_framework = None
        pygame.quit()
        print("Destroyed", self)
        
    def __del__(self):
        if not self._destroyed:
            self.destroy()
