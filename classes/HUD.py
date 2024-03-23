#!/usr/bin/env python

# Copyright (c) 2018 Intel Labs.
# authors: German Ros (german.ros@intel.com)
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""Example of automatic vehicle control from client side."""
import os
import math
from typing import ClassVar, Optional, Union
from datetime import timedelta
import pygame

import carla


from classes.keyboard_controls import RSSKeyboardControl
from classes.rss_visualization import RssStateVisualizer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.worldmodel import WorldModel

FONT_SIZE = 20


def get_actor_display_name(actor, truncate=250):
    """Method to get actor display name"""
    name = ' '.join(actor.type_id.replace('_', '.').title().split('.')[1:])
    return (name[:truncate - 1] + u'\u2026') if len(name) > truncate else name

# ==============================================================================
# -- HUD -----------------------------------------------------------------------
# ==============================================================================


class HUD(object):
    """Class for HUD text"""
    default_font : ClassVar[str] = 'ubuntumono'

    def __init__(self, width:int, height:int, world : carla.World, help_text:Optional[str]=RSSKeyboardControl.__doc__):
        """Constructor method"""
        self.dim = (width, height)
        self._world = world
        self.map_name = world.get_map().name
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        font_name = 'courier' if os.name == 'nt' else 'mono'
        fonts = [x for x in pygame.font.get_fonts() if font_name in x]
        mono = self.default_font if self.default_font in fonts else fonts[0]
        mono = pygame.font.match_font(mono)
        self._font_mono = pygame.font.Font(mono, 12 if os.name == 'nt' else 14)
        self._notifications = FadingText(font, (width, 40), (0, height - 40))
        self.help = HelpText(pygame.font.Font(mono, FONT_SIZE), width, height, 
                             doc=help_text if help_text is not None else False)
        self.server_fps = 0
        self.frame = 0
        self.simulation_time = 0
        self._show_info = True
        self._info_text = []
        self._server_clock = pygame.time.Clock()
        # RSS
        self.original_vehicle_control = None
        self.restricted_vehicle_control = None
        self.allowed_steering_ranges = []
        self.rss_state_visualizer = RssStateVisualizer(self.dim, self._font_mono, self._world)

    def on_world_tick(self, timestamp : carla.Timestamp):
        """Gets informations from the world at every tick"""
        self._server_clock.tick()
        self.server_fps = self._server_clock.get_fps()
        # self.frame = timestamp.frame_count # NON- RSS Example
        self.frame = timestamp.frame
        self.simulation_time = timestamp.elapsed_seconds

    def tick(self, world : "WorldModel", clock):
        """HUD method for every tick"""
        self._notifications.tick(clock)
        if not self._show_info:
            return
        player = world.player
        transform = player.get_transform()
        vel = player.get_velocity()
        control = player.get_control()
        heading = 'N' if abs(transform.rotation.yaw) < 89.5 else ''
        heading += 'S' if abs(transform.rotation.yaw) > 90.5 else ''
        heading += 'E' if 179.5 > transform.rotation.yaw > 0.5 else ''
        heading += 'W' if -0.5 > transform.rotation.yaw > -179.5 else ''
        colhist = world.collision_sensor.get_collision_history()
        collision = [colhist[x + self.frame - 200] for x in range(0, 200)]
        max_col = max(1.0, max(collision))
        collision = [x / max_col for x in collision]
        vehicles = world.world.get_actors().filter('vehicle.*')

        self._info_text = [
            'Server:  % 16.0f FPS' % self.server_fps,
            'Client:  % 16.0f FPS' % clock.get_fps(),
            'Map:     % 20s' % self.map_name, # from rss
            '',
            'Vehicle: % 20s' % get_actor_display_name(player, truncate=20),
            'Map:     % 20s' % world.map.name.split('/')[-1],
            'Simulation time: % 12s' % timedelta(seconds=int(self.simulation_time)),
            '',
            'Speed:   % 15.0f km/h' % (3.6 * math.sqrt(vel.x ** 2 + vel.y ** 2 + vel.z ** 2)),
            u'Heading:% 16.0f\N{DEGREE SIGN} % 2s' % (transform.rotation.yaw, heading),
            #  TODO maybe 'Heading: % 20.2f' % math.radians(transform.rotation.yaw),
            'Location:% 20s' % ('(% 5.1f, % 5.1f)' % (transform.location.x, transform.location.y)),
            'Height:  % 18.0f m' % transform.location.z,]
        if world.gnss_sensor:
            self._info_text.append('GNSS:% 24s' % ('(% 2.6f, % 3.6f)' % (world.gnss_sensor.lat, world.gnss_sensor.lon)))
        self._info_text.append('') # empty line
        if isinstance(control, carla.VehicleControl):
            if self.original_vehicle_control:
                orig_control = self.original_vehicle_control
                restricted_control = self.restricted_vehicle_control
                allowed_steering_ranges = self.allowed_steering_ranges
                self._info_text += [
                    ('Throttle:', orig_control.throttle, 0.0, 1.0, restricted_control.throttle),
                    ('Steer:', orig_control.steer, -1.0, 1.0, restricted_control.steer, allowed_steering_ranges),
                    ('Brake:', orig_control.brake, 0.0, 1.0, restricted_control.brake)]
            else:
                self._info_text += [
                    ('Throttle:', control.throttle, 0.0, 1.0),
                    ('Steer:', control.steer, -1.0, 1.0),
                    ('Brake:', control.brake, 0.0, 1.0),]
            self._info_text += [
                ('Reverse:', control.reverse),
                ('Hand brake:', control.hand_brake),
                ('Manual:', control.manual_gear_shift),
                'Gear:        %s' % {-1: 'R', 0: 'N'}.get(control.gear, control.gear)]
        elif isinstance(control, carla.WalkerControl):
            self._info_text += [
                ('Speed:', control.speed, 0.0, 5.556),
                ('Jump:', control.jump)]
        self._info_text += [
            '',
            'Collision:',
            collision,
            '',
            'Number of vehicles: % 8d' % len(vehicles)]

        if len(vehicles) > 1:
            self._info_text += ['Nearby vehicles:']

        def dist(l):
            return math.sqrt((l.x - transform.location.x) ** 2 + (l.y - transform.location.y)
                             ** 2 + (l.z - transform.location.z) ** 2)

        vehicles = [(dist(x.get_location()), x) for x in vehicles if x.id != world.player.id]

        for dist, vehicle in sorted(vehicles): # TODO TypeError: '<' not supported between instances of 'Vehicle' and 'Vehicle'
            if dist > 200.0:
                break
            vehicle_type = get_actor_display_name(vehicle, truncate=22)
            self._info_text.append('% 4dm %s' % (dist, vehicle_type))

    def toggle_info(self):
        """Toggle info on or off"""
        self._show_info = not self._show_info

    def notification(self, text, seconds=2.0):
        """Notification text"""
        self._notifications.set_text(text, seconds=seconds)

    def error(self, text):
        """Error text"""
        self._notifications.set_text('Error: %s' % text, (255, 0, 0))

    def render(self, display):
        """Render for HUD class"""
        if self._show_info:
            info_surface = pygame.Surface((220, self.dim[1]))
            info_surface.set_alpha(100)
            display.blit(info_surface, (0, 0))
            v_offset = 4
            bar_h_offset = 100
            bar_width = 106
            text_color = (255, 255, 255)
            for item in self._info_text:
                if v_offset + 18 > self.dim[1]:
                    break
                if isinstance(item, list):
                    if len(item) > 1:
                        points = [(x + 8, v_offset + 8 + (1 - y) * 30) for x, y in enumerate(item)]
                        pygame.draw.lines(display, (255, 136, 0), False, points, 2)
                    item = None
                    v_offset += 18
                elif isinstance(item, tuple):
                    if isinstance(item[1], bool):
                        # rect = pygame.Rect((bar_h_offset, v_offset + 8), (6, 6))
                        rect = pygame.Rect((bar_h_offset, v_offset + 2), (10, 10))
                        pygame.draw.rect(display, (255, 255, 255), rect, 0 if item[1] else 1)
                    else:
                        # draw allowed steering ranges
                        if len(item) == 6 and item[2] < 0.0:
                            for steering_range in item[5]:
                                starting_value = min(steering_range[0], steering_range[1])
                                length = (max(steering_range[0], steering_range[1]) -
                                          min(steering_range[0], steering_range[1])) / 2
                                rect = pygame.Rect(
                                    (bar_h_offset + (starting_value + 1) * (bar_width / 2), v_offset + 2), (length * bar_width, 14))
                                pygame.draw.rect(display, (0, 255, 0), rect)

                        # draw border
                        # rect_border = pygame.Rect((bar_h_offset, v_offset + 8), (bar_width, 6))
                        rect_border = pygame.Rect((bar_h_offset, v_offset + 2), (bar_width, 14))
                        pygame.draw.rect(display, (255, 255, 255), rect_border, 1)

                        # draw value / restricted value
                        input_value_rect_fill = 0
                        if len(item) >= 5:
                            if item[1] != item[4]:
                                input_value_rect_fill = 1
                                f = (item[4] - item[2]) / (item[3] - item[2])
                                if item[2] < 0.0:
                                    rect = pygame.Rect(
                                        (bar_h_offset + 1 + f * (bar_width - 6), v_offset + 3), (12, 12))
                                else:
                                    rect = pygame.Rect((bar_h_offset + 1, v_offset + 3), (f * bar_width, 12))
                                pygame.draw.rect(display, (255, 0, 0), rect)

                        f = (item[1] - item[2]) / (item[3] - item[2])
                        rect = None
                        if item[2] < 0.0:
                            #rect = pygame.Rect(
                            #    (bar_h_offset + fig * (bar_width - 6), v_offset + 8), (6, 6))
                            rect = pygame.Rect((bar_h_offset + 2 + f * (bar_width - 14), v_offset + 4), (10, 10))
                        else:
                            #rect = pygame.Rect((bar_h_offset, v_offset + 8), (fig * bar_width, 6))
                            if item[1] != 0:
                                rect = pygame.Rect((bar_h_offset + 2, v_offset + 4), (f * (bar_width - 4), 10))
                        if rect:
                            # pygame.draw.rect(display, (255, 255, 255), rect)
                            pygame.draw.rect(display, (255, 255, 255), rect, input_value_rect_fill)
                    item = item[0]
                if item:  # At this point has to be a str.
                    surface = self._font_mono.render(item, True, text_color)
                    display.blit(surface, (8, v_offset))
                v_offset += 18

            self.rss_state_visualizer.render(display, v_offset)
        self._notifications.render(display)
        self.help.render(display)


# ==============================================================================
# -- FadingText ----------------------------------------------------------------
# ==============================================================================


class FadingText(object):
    """ Class for fading text """

    def __init__(self, font, dim, pos):
        """Constructor method"""
        self.font = font
        self.dim = dim
        self.pos = pos
        self.seconds_left = 0
        self.surface = pygame.Surface(self.dim)

    def set_text(self, text, color=(255, 255, 255), seconds=2.0):
        """Set fading text"""
        text_texture = self.font.render(text, True, color)
        self.surface = pygame.Surface(self.dim)
        self.seconds_left = seconds
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(text_texture, (10, 11))

    def tick(self, clock):
        """Fading text method for every tick"""
        delta_seconds = 1e-3 * clock.get_time()
        self.seconds_left = max(0.0, self.seconds_left - delta_seconds)
        self.surface.set_alpha(500.0 * self.seconds_left)

    def render(self, display):
        """Render fading text method"""
        display.blit(self.surface, self.pos)


# ==============================================================================
# -- HelpText ------------------------------------------------------------------
# ==============================================================================


class HelpText(object):
    """Helper class to handle text output using pygame"""

    def __init__(self, font, width, height, doc:Optional[Union[str, bool]] = None):
        """Constructor method"""
        self.line_space = 18
        self.font = font
        self.seconds_left = 0
        self._width = width
        self._height = height
        if doc != False:
            self.create_surface(doc or __doc__) # Use doc of THIS file, analog to carla examples.
        else:
            self.surface = None
        self._render = False
        
    def create_surface(self, doc):
        """Create surface method"""
        lines = doc.split('\n')
        self.dim = (780, len(lines) * self.line_space + 12)
        #self.dim = (680, len(lines) * 22 + 12)
        self.pos = (0.5 * self._width - 0.5 * self.dim[0], 0.5 * self._height - 0.5 * self.dim[1])
        self.surface = pygame.Surface(self.dim)
        self.surface.fill((0, 0, 0, 0))
        for i, line in enumerate(lines):
            text_texture = self.font.render(line, True, (255, 255, 255))
            self.surface.blit(text_texture, (22, i * self.line_space))
        self.surface.set_alpha(220)

    def toggle(self):
        """Toggle on or off the render help"""
        if self.surface is None:
            print("Warning: No help text available - Initialized with doc=False. Cannot display help. Call create_surface first.")
            return
        self._render = not self._render

    def render(self, display):
        """Render help text method"""
        if self._render:
            display.blit(self.surface, self.pos)
