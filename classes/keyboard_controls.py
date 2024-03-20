import math
import weakref
import pygame
from pygame.locals import KMOD_CTRL
from pygame.locals import KMOD_SHIFT
from pygame.locals import K_BACKSPACE
from pygame.locals import K_TAB
from pygame.locals import K_DOWN
from pygame.locals import K_ESCAPE
from pygame.locals import K_F1
from pygame.locals import K_F2
from pygame.locals import K_F3
from pygame.locals import K_F4
from pygame.locals import K_F5
from pygame.locals import K_F6
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_SLASH
from pygame.locals import K_SPACE
from pygame.locals import K_UP
from pygame.locals import K_a
from pygame.locals import K_b
from pygame.locals import K_d
from pygame.locals import K_g
from pygame.locals import K_h
from pygame.locals import K_n
from pygame.locals import K_p
from pygame.locals import K_q
from pygame.locals import K_r
from pygame.locals import K_s
from pygame.locals import K_w
from pygame.locals import K_l
from pygame.locals import K_i
from pygame.locals import K_z
from pygame.locals import K_x
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import MOUSEBUTTONUP


import carla

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from classes.worldmodel import WorldModel



# ==============================================================================
# -- KeyboardControl -----------------------------------------------------------
# ==============================================================================


class PassiveKeyboardControl(object):
    # COMMENT I think this only allows to end the script
    def __init__(self, world : "WorldModel"):
        world.hud.notification("Press 'H' or '?' for help.", seconds=4.0)

    def parse_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYUP:
                if self._is_quit_shortcut(event.key):
                    return True

    @staticmethod
    def _is_quit_shortcut(key):
        """Shortcut for quitting"""
        return (key == K_ESCAPE) or (key == K_q and pygame.key.get_mods() & KMOD_CTRL)



class RSSKeyboardControl(object):
    """
    TODO: This documentation is not up to date!

    Use ARROWS or WASD keys for control.

        W            : throttle
        S            : brake
        AD           : steer
        Q            : toggle reverse
        Space        : hand-brake
        P            : toggle autopilot

        TAB          : change view
        Backspace    : change vehicle

        R            : toggle recording images to disk

        F2           : toggle RSS visualization mode
        F3           : increase log level
        F4           : decrease log level
        F5           : increase map log level
        F6           : decrease map log level
        B            : toggle RSS Road Boundaries Mode
        G            : RSS check drop current route
        T            : toggle RSS (NotImplemented)
        N            : pause simulation

        F1           : toggle HUD
        H/?          : toggle help
        ESC          : quit
    """
    @classmethod
    def get_docstring(cls):
        return "======== Controls ===========\n"+cls.__doc__+"\n============================\n"
    
    MOUSE_STEERING_RANGE = 200
    signal_received = False

    # TODO: should be a toggle between None, Autopilot, Agent

    def __init__(self, world_model : "WorldModel", start_in_autopilot : bool, agent_controlled : bool = True, clock:pygame.time.Clock=None, config=None):
        if start_in_autopilot and agent_controlled:
            raise ValueError("Agent controlled and autopilot cannot be active at the same time.")
        self._config = config
        self._autopilot_enabled = start_in_autopilot
        self._agent_controlled = agent_controlled
        self._world_model = world_model
        world_model.controller = weakref.proxy(self)
        self._control : carla.VehicleControl = None
        #self._control = carla.VehicleControl()
        self._lights = carla.VehicleLightState.NONE
        #self._restrictor = carla.RssRestrictor() # Moved to worldmodel
        self._restrictor = None
        self._vehicle_physics = world_model.player.get_physics_control()
        world_model.player.set_light_state(self._lights)
        self._steer_cache = 0.0
        self._mouse_steering_center = None

        self._surface = pygame.Surface((self.MOUSE_STEERING_RANGE * 2, self.MOUSE_STEERING_RANGE * 2))
        self._surface.set_colorkey(pygame.Color('black'))
        self._surface.set_alpha(60)
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

    def render(self, display):
        if self._mouse_steering_center:
            display.blit(
                self._surface, (self._mouse_steering_center[0] - self.MOUSE_STEERING_RANGE, self._mouse_steering_center[1] - self.MOUSE_STEERING_RANGE))

    @staticmethod
    def signal_handler(signum, _):
        print('\nReceived signal {}. Trigger stopping...'.format(signum))
        RSSKeyboardControl.signal_received = True

    def parse_events(self, control:"Optional[carla.VehicleControl]"=None):
        if control:
            self._control = control
        if RSSKeyboardControl.signal_received:
            print('\nAccepted signal. Stopping loop...')
            return True
        if isinstance(self._control, carla.VehicleControl):
            current_lights = self._lights
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYUP:
                if self._is_quit_shortcut(event.key):
                    return True
                elif event.key == K_BACKSPACE:
                    if self._autopilot_enabled:
                        self._world_model.player.set_autopilot(False)
                        self._world_model.restart()
                        self._world_model.player.set_autopilot(True)
                    else:
                        self._world_model.restart()
                elif event.key == K_F1:
                    self._world_model.hud.toggle_info()
                elif event.key == K_h or (event.key == K_SLASH and pygame.key.get_mods() & KMOD_SHIFT):
                    self._world_model.hud.help.toggle()
                elif event.key == K_TAB:
                    self._world_model.rss_unstructured_scene_visualizer.toggle_camera()
                elif event.key == K_n:
                    self._world_model.toggle_pause()
                elif event.key == K_r:
                    self._world_model.toggle_recording()
                elif event.key == K_F2:
                    if self._world_model and self._world_model.rss_sensor:
                        self._world_model.rss_sensor.toggle_debug_visualization_mode()
                elif event.key == K_F3:
                    if self._world_model and self._world_model.rss_sensor:
                        self._world_model.rss_sensor.decrease_log_level()
                        self._restrictor.set_log_level(self._world_model.rss_sensor.log_level)
                elif event.key == K_F4:
                    if self._world_model and self._world_model.rss_sensor:
                        self._world_model.rss_sensor.increase_log_level()
                        self._restrictor.set_log_level(self._world_model.rss_sensor.log_level)
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
                        else:
                            self._world_model.rss_set_road_boundaries_mode(carla.RssRoadBoundariesMode.Off)
                            print("carla.RssRoadBoundariesMode.Off")
                elif event.key == K_g:
                    if self._world_model and self._world_model.rss_sensor:
                        self._world_model.rss_sensor.drop_route()
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
            prev_steer_cache = self._steer_cache
            self._parse_vehicle_keys(pygame.key.get_pressed(), self._clock.get_time())
            if pygame.mouse.get_pressed()[0]:
                self._parse_mouse(pygame.mouse.get_pos())
            self._control.reverse = self._control.gear < 0
            return
            vehicle_control = self._control
            #self._world_model.hud.original_vehicle_control = vehicle_control
            #self._world_model.hud.restricted_vehicle_control = vehicle_control

            # limit speed to 30kmh
            #v = self._world_model.player.get_velocity()
            #if (3.6 * math.sqrt(v.x**2 + v.y**2 + v.z**2)) > 30.0:
            #    self._control.throttle = 0

            # if self._world.rss_sensor and self._world.rss_sensor.ego_dynamics_on_route and not self._world.rss_sensor.ego_dynamics_on_route.ego_center_within_route:
            #    print ("Not on route!" +  str(self._world.rss_sensor.ego_dynamics_on_route))
            if self._restrictor:
                rss_proper_response = self._world_model.rss_sensor.proper_response if self._world_model.rss_sensor and self._world_model.rss_sensor.response_valid else None
                if rss_proper_response:
                    if not (pygame.key.get_mods() & KMOD_CTRL):
                        vehicle_control = self._restrictor.restrict_vehicle_control(
                            vehicle_control, rss_proper_response, self._world_model.rss_sensor.ego_dynamics_on_route, self._vehicle_physics)
                    self._world_model.hud.restricted_vehicle_control = vehicle_control
                    self._world_model.hud.allowed_steering_ranges = self._world_model.rss_sensor.get_steering_ranges()
                    if self._world_model.hud.original_vehicle_control.steer != self._world_model.hud.restricted_vehicle_control.steer:
                        self._steer_cache = prev_steer_cache

            #self._world_model.player.apply_control(vehicle_control)

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
        if not self._mouse_steering_center:
            return

        lateral = float(pos[0] - self._mouse_steering_center[0])
        longitudinal = float(pos[1] - self._mouse_steering_center[1])
        max_val = self.MOUSE_STEERING_RANGE
        lateral = -max_val if lateral < -max_val else max_val if lateral > max_val else lateral
        longitudinal = -max_val if longitudinal < -max_val else max_val if longitudinal > max_val else longitudinal
        self._control.steer = lateral / max_val
        if longitudinal < 0.0:
            self._control.throttle = -longitudinal / max_val
            self._control.brake = 0.0
        elif longitudinal > 0.0:
            self._control.throttle = 0.0
            self._control.brake = longitudinal / max_val

    @staticmethod
    def _is_quit_shortcut(key):
        return (key == K_ESCAPE) or (key == K_q and pygame.key.get_mods() & KMOD_CTRL)
