import logging
import sys
import inspect
import signal
import weakref
from typing import TYPE_CHECKING, Any, Optional, Union

import carla
import pygame
from pygame.locals import (
    K_BACKSPACE,
    K_DOWN,
    K_EQUALS,
    K_ESCAPE,
    K_F1,
    K_F2,
    K_F3,
    K_F4,
    K_F5,
    K_F6,
    K_LEFT,
    K_MINUS,
    K_RIGHT,
    K_SPACE,
    K_TAB,
    K_UP,
    KMOD_CTRL,
    KMOD_SHIFT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    K_a,
    K_b,
    K_d,
    K_g,
    K_i,
    K_l,
    K_n,
    K_o,
    K_p,
    K_q,
    K_r,
    K_s,
    K_t,
    K_w,
    K_x,
    K_z,
)
from typing_extensions import Literal

if TYPE_CHECKING:
    from classes.worldmodel import WorldModel



# ==============================================================================
# -- KeyboardControl -----------------------------------------------------------
# ==============================================================================


class KeyboardControl:
    """
    Primitive base for keyboard control classes.
    
        H/?          : toggle help
    """
    
    _world_model : "WorldModel"
    """Reference to the world model that controls the interface."""
    
    # COMMENT I think this only allows to end the script
    def __init__(self, world : "WorldModel", help_notice=True):
        """
        Parameters:
            world : WorldModel
            help_notice : bool
                Show a notice about the help keys.
        """
        self._world_model = world
        if world.hud.help.surface is None:
            world.hud.help.create_surface(self.get_docstring())
        if help_notice:
            world.hud.notification("Press 'H' or '?' for help.", seconds=4.0)
    
    @classmethod
    def get_docstring(cls):
        """Return the docstring of the class"""
        
        doc = cls.__doc__
        # Get doc from parent
        if doc is None:
            doc = inspect.getdoc(cls)
            if doc is not None and doc != object.__doc__:
                cls.__doc__ = doc
            else:
                cls.__doc__ = doc = "No docstring available"
        if doc == "No docstring available":
            return "No docstring available"

        return "======== Controls ===========\n" + doc + "\n============================\n"

    def parse_events(self, events=None) -> Union[Literal[True], Any]:
        """
        Parse the input events and return True if the loop should end.
        """
        events = events if events is not None else pygame.event.get()
        for event in events:  # pylint: disable=unused-variable
            self._check_help_event(event)
    
    @staticmethod
    def _is_quit_shortcut(key : int):
        """Shortcut for quitting"""
        return (key == K_ESCAPE) or (key == K_q and pygame.key.get_mods() & KMOD_CTRL)

    
    def _check_help_event(self, event : pygame.event.Event):
        """Check if the event is a help event"""
        if not hasattr(event, 'unicode'):  # No KEYUP/DOWN event
            return None
        if event.unicode.lower() in ('h', '?'):  # type: ignore[attr-defined]
            self._world_model.hud.help.toggle()
            return True
        return False

class PassiveKeyboardControl(KeyboardControl):
    """
    Does not allow to control the vehicle. Only allows to
    quit the simulation.

       | ESC          : quit
       | H/?          : toggle help
    """

    def parse_events(self) -> "None | Literal[True]":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYUP:
                if self._is_quit_shortcut(event.key):
                    return True
                if self._check_help_event(event):
                    pass
        return None

class RSSKeyboardControl(KeyboardControl):
    """
    Use ARROWS, WASD keys or mouse click and drag for control.

      | W            : throttle
      | S            : brake
      | AD           : steer
      | Q            : toggle reverse
      | Space        : hand-brake
      | P            : toggle autopilot (depends on setup)

      | TAB          : change view
      | Backspace    : change vehicle (will unset externalActor; experimental)

      | R            : toggle recording images to disk

      | F2           : toggle RSS visualization mode
      | F3           : increase log level
      | F4           : decrease log level
      | F5           : increase map log level
      | F6           : decrease map log level
      | B            : toggle RSS Road Boundaries Mode
      | G            : RSS check drop current route (experimental)
      | S            : toggle RSS (NotImplemented)
      | T            : toggle vehicle's telemetry visualization
      | O            : open/close vehicle's doors
      | N            : pause simulation (not in sync mode)

      | -- Experimental, recording --
      |
      | CTRL + R     : toggle recording of simulation (replacing any previous)
      | CTRL + P     : start replaying last recorded simulation (untested)
      | CTRL + +     : increments the start time of the replay by 1 second (+SHIFT = 10 seconds)
      | CTRL + -     : decrements the start time of the replay by 1 second (+SHIFT = 10 seconds)

      | F1           : toggle HUD
      | H/?          : toggle help
      | ESC          : quit
    """

    MOUSE_STEERING_RANGE = 150
    """
    Controls the size of steering area when using the mouse.
    """
    
    signal_received: "bool | int" = False
    """
    Got a signal to stop the simulation. No more events will be parsed if True.
    
    :meta private:
    """

    # TODO: should be a toggle between None, Autopilot, Agent

    def __init__(self, world_model : "WorldModel", start_in_autopilot : bool, agent_controlled : bool = True, clock: pygame.time.Clock = None, config=None):
        if start_in_autopilot and agent_controlled:
            raise ValueError("Agent controlled and autopilot cannot be active at the same time.")
        super().__init__(world_model)
        
        self._world_model = world_model
        self._config = config  # Note: currently unused
        self._autopilot_enabled = start_in_autopilot
        self._agent_controlled = agent_controlled
        world_model.controller = weakref.proxy(self)
        self._control : carla.VehicleControl = None
        #self._control = carla.VehicleControl()
        self._lights = carla.VehicleLightState.NONE
        #self._restrictor = carla.RssRestrictor() # Moved to worldmodel
        self._restrictor : carla.RssRestrictor = None
        self._vehicle_physics = world_model.player.get_physics_control()
        world_model.player.set_light_state(self._lights)
        self._steer_cache = 0.0
        self._mouse_steering_center = None

        self._surface = pygame.Surface((self.MOUSE_STEERING_RANGE * 2, self.MOUSE_STEERING_RANGE * 2))
        self._surface.set_colorkey(pygame.Color('black'))
        self._surface.set_alpha(60)
        assert clock is not None, "Clock must be provided."
        self._clock = clock

        line_width = 2
        pygame.draw.polygon(self._surface,
                            (0, 0, 255),
                            [
                                (0, 0),
                                (0, self.MOUSE_STEERING_RANGE * 2 - line_width),
                                (self.MOUSE_STEERING_RANGE * 2 - line_width,
                                 self.MOUSE_STEERING_RANGE * 2 - line_width),
                                (self.MOUSE_STEERING_RANGE * 2 - line_width, 0),
                                (0, 0)
                            ], line_width)
        pygame.draw.polygon(self._surface,
                            (0, 0, 255),
                            [
                                (0, self.MOUSE_STEERING_RANGE),
                                (self.MOUSE_STEERING_RANGE * 2, self.MOUSE_STEERING_RANGE)
                            ], line_width)
        pygame.draw.polygon(self._surface,
                            (0, 0, 255),
                            [
                                (self.MOUSE_STEERING_RANGE, 0),
                                (self.MOUSE_STEERING_RANGE, self.MOUSE_STEERING_RANGE * 2)
                            ], line_width)

        world_model.hud.notification("Press 'H' or '?' for help.", seconds=4.0)

    @property
    def controlled_externally(self):
        return self._autopilot_enabled or self._agent_controlled

    def render(self, display: pygame.Surface) -> None:
        if self._mouse_steering_center:
            display.blit(
                self._surface, (self._mouse_steering_center[0] - self.MOUSE_STEERING_RANGE, self._mouse_steering_center[1] - self.MOUSE_STEERING_RANGE))

    @staticmethod
    def _signal_handler(signum, _):
        """
        Signal handler for stopping the simulation, e.g. when pressing Ctrl+C
        in the terminal.
        
        Note:
            If DetectionMatrix is used this signal handler will be overwritten,
            but still executed.
        
        :meta private:
        """
        if not RSSKeyboardControl.signal_received:
            print(f'\nReceived signal {signum}. Trigger stopping... In case the program freezes trigger twice more.')
            RSSKeyboardControl.signal_received = True
            return
        # Did not yet terminate
        if RSSKeyboardControl.signal_received is True:
            print(f'\nReceived signal {signum}. Abort a 3rd time to terminate the program immediately')
            RSSKeyboardControl.signal_received = 2
            return
        sys.exit(1)

    def parse_events(self, control: "Optional[carla.VehicleControl]" = None) -> "None | Literal[True]":
        if control:
            self._control = control  # Note this might be the rss updated controls
        if RSSKeyboardControl.signal_received:
            print('\nAccepted signal. Stopping loop...')
            return True
        if isinstance(self._control, carla.VehicleControl):
            current_lights = self._lights
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYUP:
                if self._is_quit_shortcut(event.key):
                    return True
                
                if event.key == K_BACKSPACE:
                    self._world_model.external_actor = None
                    if self._autopilot_enabled:
                        self._world_model.player.set_autopilot(False)
                        self._world_model.restart()
                        self._world_model.player.set_autopilot(True)
                    else:
                        self._world_model.restart()
                elif event.key == K_F1:
                    self._world_model.hud.toggle_info()
                elif self._check_help_event(event):
                    pass
                elif event.key == K_TAB:
                    self._world_model.rss_unstructured_scene_visualizer.toggle_camera()
                elif event.key == K_n:
                    self._world_model.toggle_pause()
                elif event.key == K_r:
                    self._world_model.toggle_recording()
                elif event.key == K_F2:
                    if self._world_model and self._world_model.rss_sensor:
                        self._world_model.rss_sensor.toggle_debug_visualization_mode()
                        _newmode = self._world_model.rss_sensor.debug_visualizer._visualization_mode
                        self._world_model.hud.notification(f"RSS Debug Visualization Mode: {_newmode}")
                elif event.key == K_F3:
                    if self._world_model and self._world_model.rss_sensor:
                        if not self._world_model._restrictor:
                            print("WARNING: No restrictor available")
                        else:
                            self._world_model.rss_sensor.decrease_log_level()
                            assert isinstance(self._world_model.rss_sensor.log_level, (int, carla.RssLogLevel))
                            self._world_model._restrictor.set_log_level(self._world_model.rss_sensor.log_level)  # pyright: ignore[reportArgumentType]
                elif event.key == K_F4:
                    if self._world_model and self._world_model.rss_sensor:
                        if not self._world_model._restrictor:
                            print("WARNING: No restrictor available")
                        else:
                            self._world_model.rss_sensor.increase_log_level()
                            assert isinstance(self._world_model.rss_sensor.log_level, (int, carla.RssLogLevel))
                            self._world_model._restrictor.set_log_level(self._world_model.rss_sensor.log_level)  # pyright: ignore[reportArgumentType]
                elif event.key == K_F5:
                    if self._world_model and self._world_model.rss_sensor:
                        self._world_model.rss_sensor.decrease_map_log_level()
                elif event.key == K_F6:
                    if self._world_model and self._world_model.rss_sensor:
                        self._world_model.rss_sensor.increase_map_log_level()
                elif event.key == K_b:
                    if self._world_model and self._world_model.rss_sensor:
                        if self._world_model.rss_sensor.sensor.road_boundaries_mode == carla.RssRoadBoundariesMode.Off:
                            self._world_model.rss_set_road_boundaries_mode(carla.RssRoadBoundariesMode.On)
                            print("carla.RssRoadBoundariesMode.On")
                            self._world_model.hud.notification("RSS Road Boundaries Mode:  On")
                        else:
                            self._world_model.rss_set_road_boundaries_mode(carla.RssRoadBoundariesMode.Off)
                            print("carla.RssRoadBoundariesMode.Off")
                            self._world_model.hud.notification("RSS Road Boundaries Mode: Off")
                elif event.key == K_g:
                    if self._world_model and self._world_model.rss_sensor:
                        self._world_model.rss_sensor.drop_route()
                # --- Experimental, copied from other locations ---
                elif event.key == K_t:
                    if self._world_model.show_vehicle_telemetry:
                        self._world_model.player.show_debug_telemetry(False)
                        self._world_model.show_vehicle_telemetry = False
                        self._world_model.hud.notification("Disabled Vehicle Telemetry")
                    else:
                        try:
                            self._world_model.player.show_debug_telemetry(True)
                            self._world_model.show_vehicle_telemetry = True
                            self._world_model.hud.notification("Enabled Vehicle Telemetry")
                        except Exception:
                            logging.debug("Could not enable vehicle telemetry")
                elif event.key == K_o:
                    try:
                        # TODO: Should be set on the agent
                        if self._world_model.doors_are_open:
                            self._world_model.hud.notification("Closing Doors")
                            self._world_model.doors_are_open = False
                            self._world_model.player.close_door(carla.VehicleDoor.All)
                        else:
                            self._world_model.hud.notification("Opening doors")
                            self._world_model.doors_are_open = True
                            self._world_model.player.open_door(carla.VehicleDoor.All)
                    except Exception:
                        logging.warning("Could not open/close doors")
                # --- Experimental, recording ----
                elif event.key == K_r and (pygame.key.get_mods() & KMOD_CTRL):
                    if (self._world_model.recording_enabled):
                        self._world_model.get_client().stop_recorder()
                        self._world_model.recording_enabled = False
                        self._world_model.hud.notification("Recorder is OFF")
                    else:
                        self._world_model.get_client().start_recorder("manual_recording.rec")
                        self._world_model.recording_enabled = True
                        self._world_model.hud.notification("Recorder is ON")
                elif event.key == K_p and (pygame.key.get_mods() & KMOD_CTRL):
                    # stop recorder
                    self._world_model.get_client().stop_recorder()
                    self._world_model.recording_enabled = False
                    # work around to fix camera at start of replaying
                    current_index = self._world_model.camera_manager.index
                    self._world_model.destroy_sensors()
                    # disable autopilot
                    self._autopilot_enabled = False
                    self._world_model.player.set_autopilot(self._autopilot_enabled)
                    self._world_model.hud.notification("Replaying file 'manual_recording.rec'")
                    # replayer
                    # TODO: This likely needs more cleanup!
                    replay_logs = self._world_model.get_client().replay_file("manual_recording.rec", self._world_model.recording_start, 0, 0)
                    print("------ Replay logs -------\n", replay_logs)
                    self._world_model.camera_manager.set_sensor(current_index)
                elif event.key == K_MINUS and (pygame.key.get_mods() & KMOD_CTRL):
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        self._world_model.recording_start -= 10
                    else:
                        self._world_model.recording_start -= 1
                    self._world_model.hud.notification("Recording start time is %d" % (self._world_model.recording_start))
                elif event.key == K_EQUALS and (pygame.key.get_mods() & KMOD_CTRL):
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        self._world_model.recording_start += 10
                    else:
                        self._world_model.recording_start += 1
                    self._world_model.hud.notification("Recording start time is %d" % (self._world_model.recording_start))
                
                
                # Modify controls
                if isinstance(self._control, carla.VehicleControl):
                    if event.key == K_q:
                        self._control.gear = 1 if self._control.reverse else -1
                    elif event.key == K_p and not pygame.key.get_mods() & KMOD_CTRL:
                        # TODO: should be a toggle between None, Autopilot, Agent
                        self._autopilot_enabled = not self._autopilot_enabled
                        self._world_model.player.set_autopilot(self._autopilot_enabled)
                        self._world_model.hud.notification(
                            'Autopilot %s' % ('On' if self._autopilot_enabled else 'Off'))
                    elif event.key == K_l and pygame.key.get_mods() & KMOD_CTRL:
                        current_lights ^= carla.VehicleLightState.Special1
                    elif event.key == K_l and pygame.key.get_mods() & KMOD_SHIFT:
                        current_lights ^= carla.VehicleLightState.HighBeam
                    elif event.key == K_l:
                        # Use 'L' key to switch between lights:
                        # closed -> position -> low beam -> fog
                        if not self._lights & carla.VehicleLightState.Position:
                            self._world_model.hud.notification("Position lights")
                            current_lights |= carla.VehicleLightState.Position
                        else:
                            self._world_model.hud.notification("Low beam lights")
                            current_lights |= carla.VehicleLightState.LowBeam
                        if self._lights & carla.VehicleLightState.LowBeam:
                            self._world_model.hud.notification("Fog lights")
                            current_lights |= carla.VehicleLightState.Fog
                        if self._lights & carla.VehicleLightState.Fog:
                            self._world_model.hud.notification("Lights off")
                            current_lights ^= carla.VehicleLightState.Position
                            current_lights ^= carla.VehicleLightState.LowBeam
                            current_lights ^= carla.VehicleLightState.Fog
                    elif event.key == K_i:
                        current_lights ^= carla.VehicleLightState.Interior
                    elif event.key == K_z:
                        current_lights ^= carla.VehicleLightState.LeftBlinker
                    elif event.key == K_x:
                        current_lights ^= carla.VehicleLightState.RightBlinker
            elif event.type == MOUSEBUTTONDOWN:
                # store current mouse position for mouse-steering
                if event.button == 1:
                    self._mouse_steering_center = event.pos
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self._mouse_steering_center = None
        
        if not self._autopilot_enabled:
            #prev_steer_cache = self._steer_cache # NOTE: Not used anymore
            self._parse_vehicle_keys(pygame.key.get_pressed(), self._clock.get_time())
            if pygame.mouse.get_pressed()[0]:
                self._parse_mouse(pygame.mouse.get_pos())
            self._control.reverse = self._control.gear < 0
            return None
            # Moved Code from Carla example to WorldModel
        return None
 

    def _parse_vehicle_keys(self, keys, milliseconds):
        """Handles manual vehicle controls via keyboard."""
        if keys[K_UP] or keys[K_w]:
            self._control.throttle = min(self._control.throttle + 0.2, 1)
            self._control.brake = 0
        #else:
        #    self._control.throttle = max(self._control.throttle - 0.2, 0)

        if keys[K_DOWN] or keys[K_s]:
            self._control.brake = min(self._control.brake + 0.2, 1)
            self._control.throttle = 0
        #else:
        #    self._control.brake = max(self._control.brake - 0.2, 0)

        self._steer_cache = self._control.steer
        steer_increment = 5e-4 * milliseconds
        if keys[K_LEFT] or keys[K_a]:
            if self._steer_cache > 0:
                self._steer_cache = 0
            else:
                self._steer_cache -= steer_increment
        elif keys[K_RIGHT] or keys[K_d]:
            if self._steer_cache < 0:
                self._steer_cache = 0
            else:
                self._steer_cache += steer_increment
        elif self._steer_cache > 0:
            self._steer_cache = max(self._steer_cache - steer_increment, 0.0)
        elif self._steer_cache < 0:
            self._steer_cache = min(self._steer_cache + steer_increment, 0.0)
        else:
            self._steer_cache = 0

        self._steer_cache = min(1.0, max(-1.0, self._steer_cache))
        self._control.steer = round(self._steer_cache, 1)
        self._control.hand_brake = keys[K_SPACE]

    def _parse_mouse(self, pos):
        """Handles steering and throttle/break control via mouse."""
        if not self._mouse_steering_center:
            return

        lateral = float(pos[0] - self._mouse_steering_center[0])
        longitudinal = float(pos[1] - self._mouse_steering_center[1])
        max_val = self.MOUSE_STEERING_RANGE
        lateral = -max_val if lateral < -max_val else min(lateral, max_val)
        longitudinal = -max_val if longitudinal < -max_val else min(longitudinal, max_val)
        self._control.steer = lateral / max_val
        if longitudinal < 0.0:
            self._control.throttle = -longitudinal / max_val
            self._control.brake = 0.0
        elif longitudinal > 0.0:
            self._control.throttle = 0.0
            self._control.brake = longitudinal / max_val

    
# Stops RSS and allows hard kills if the script is stuck
signal.signal(signal.SIGINT, RSSKeyboardControl._signal_handler)
