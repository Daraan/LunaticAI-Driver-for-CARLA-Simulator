#!/usr/bin/env python
"""
This file tests the agent.
Based on German Ros (german.ros@intel.com) example of automatic_control shipped with carla.
"""
from __future__ import print_function # for python 2.7 compatibility

import _fix_imports
from utils.blueprint_helpers import get_actor_blueprints
import utils.general 


"""Example of automatic vehicle control from client side."""

import argparse
import logging
import numpy.random as random

import glob
import os
import sys
import random
import time

from classes.traffic_manager_daniel import TrafficManagerD

import threading

try:
    import pygame
    from pygame.locals import KMOD_CTRL
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_q
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError(
        'cannot import numpy, make sure numpy package is installed')

# ==============================================================================
# -- Find CARLA module ---------------------------------------------------------
# ==============================================================================
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

# ==============================================================================
# -- Add PythonAPI for release mode --------------------------------------------
# ==============================================================================
try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/carla')
except IndexError:
    pass

import carla

from classes.carla_service import CarlaService # TODO integrate or scrap
from classes.driver import Driver # TODO integrate or scrap
from classes.vehicle import Vehicle

from agents.navigation.behavior_agent import BehaviorAgent  # pylint: disable=import-error
from agents.navigation.basic_agent import BasicAgent  # pylint: disable=import-error
from agents.navigation.constant_velocity_agent import ConstantVelocityAgent  # pylint: disable=import-error

from classes.carla_originals.world import World
from classes.carla_originals.HUD import HUD
from classes.carla_originals.camera_manager import CameraManager

# ==============================================================================
# -- Global functions ----------------------------------------------------------
# ==============================================================================



from utils import get_actor_display_name

from utils.keyboard_controls import PassiveKeyboardControl as KeyboardControl


# ==============================================================================
# -- Game Loop ---------------------------------------------------------
# ==============================================================================


def game_loop(args):
    """
    Main loop of the simulation. It handles updating all the HUD information,
    ticking the agent and, if needed, the world.
    """

    pygame.init()
    pygame.font.init()
    world = None

    try:
        vehicle = []
        if args.seed:
            random.seed(args.seed)

        client = carla.Client(args.host, args.port)
        client.set_timeout(60.0)

        traffic_manager = client.get_trafficmanager()
        sim_world = client.get_world()

        if args.sync:
            logging.log(logging.DEBUG, "Using synchronous mode.")
            # apply synchronous mode if wanted
            settings = sim_world.get_settings()
            settings.synchronous_mode = True
            settings.fixed_delta_seconds = 0.05
            sim_world.apply_settings(settings)

            traffic_manager.set_synchronous_mode(True)
        else:
            logging.log(logging.DEBUG, "Might be using asynchronous mode if not changed.")

        display = pygame.display.set_mode(
            (args.width, args.height),
            pygame.HWSURFACE | pygame.DOUBLEBUF)

        hud = HUD(args.width, args.height)

        #carlaService = CarlaService("Town04", "127.0.0.1", 2000)

        # Set the agent destination
        try:
            spawn_points = utils.general.csv_to_transformations("../examples/highway_example_car_positions.csv")
        except FileNotFoundError:
            spawn_points = utils.general.csv_to_transformations("examples/highway_example_car_positions.csv")
        # car1 = carlaService.createCar("model3")

        # Spawn Ego
        ego_bp, car_bp = utils.blueprint_helpers.get_contrasting_blueprints(sim_world)
        ego = Vehicle(sim_world, ego_bp)
        start : carla.Transform = spawn_points[0]
        ego.spawn(start)

        world = World(client.get_world(), hud, args, player=ego.actor)
        wp_start = world.map.get_waypoint(start.location)
        all_spawn_points = world.map.get_spawn_points()
        #destination = random.choice(all_spawn_points).location

        controller = KeyboardControl(world)
        #world.set_actor(ego.actor)

        #carlaService.assignDriver(ego, driver1)
        if args.agent == "Basic":
            agent = BasicAgent(world.player, 30)
            agent.follow_speed_limits(True)
        elif args.agent == "Constant":
            agent = ConstantVelocityAgent(world.player, 30)
            ground_loc = world.world.ground_projection(world.player.get_location(), 5)
            if ground_loc:
                world.player.set_location(ground_loc.location + carla.Location(z=0.01))
            agent.follow_speed_limits(True)
        elif args.agent == "Behavior":
            agent = BehaviorAgent(world.player, behavior=args.behavior)
            from pprint import pprint
            pprint(vars(agent._behavior))
        else:
            raise ValueError(args.agent)


        next_wps: list = wp_start.next(50)
        last = next_wps[-1]
        left = last.get_left_lane()

        destination = left.transform.location

        agent.set_destination(destination)
        agent.ignore_vehicles(agent._behavior.ignore_vehicles)

        clock = pygame.time.Clock()

        # spawn others
        for sp in spawn_points[1:]:
            v = Vehicle(world, car_bp)
            v.spawn(sp)
            world.actors.append(v)
            # v.setVelocity(1)
            print(v.actor)
            ap = TrafficManagerD(client, v.actor)
            ap.init_passive_driver()
            ap.start_drive()

        ego.set_target_velocity(carla.Vector3D(-7.5, 0, 0))

        def loop():

            i = 0
            while True:
                    clock.tick()
                    if args.sync:
                        world.world.tick()
                    else:
                        world.world.wait_for_tick()
                    if controller.parse_events():
                        return

                    world.tick(clock)
                    world.render(display)
                    pygame.display.flip()

                    if agent.done():
                        if args.loop:
                            agent.set_destination(random.choice(spawn_points).location)
                            world.hud.notification("Target reached", seconds=4.0)
                            print("The target has been reached, searching for another target")
                        else:
                            print("The target has been reached, stopping the simulation")
                            break

                    control = agent.run_step()
                    control.manual_gear_shift = False
                    world.player.apply_control(control)
                    #if i % 50 == 0:
                    #    print("Tailgate Counter", agent._behavior.tailgate_counter)
                    i += 1

        if "-I" in sys.argv:
            thread = threading.Thread(target=loop)
            thread.start()
            # goes into interactive mode here
            import code
            v = globals().copy()
            v.update(locals())
            code.interact(local=v)
            thread.join()
        else:
            loop()


    finally:

        if world is not None:
            settings = world.world.get_settings()
            settings.synchronous_mode = False
            settings.fixed_delta_seconds = None
            world.world.apply_settings(settings)
            traffic_manager.set_synchronous_mode(True)

            world.destroy()

        pygame.quit()


# ==============================================================================
# -- main() --------------------------------------------------------------
# ==============================================================================


def main():
    """Main method"""

    argparser = argparse.ArgumentParser(
        description='CARLA Automatic Control Client')
    argparser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='debug',
        help='Print debug information')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '--res',
        metavar='WIDTHxHEIGHT',
        default='1280x720',
        help='Window resolution (default: 1280x720)')
    argparser.add_argument(
        '--sync',
        action='store_true',
        help='Synchronous mode execution')
    argparser.add_argument(
        '--filter',
        metavar='PATTERN',
        default='vehicle.*',
        help='Actor filter (default: "vehicle.*")')
    argparser.add_argument(
        '--generation',
        metavar='G',
        default='2',
        help='restrict to certain actor generation (values: "1","2","All" - default: "2")')
    argparser.add_argument(
        '-l', '--loop',
        action='store_true',
        dest='loop',
        help='Sets a new random destination upon reaching the previous one (default: False)')
    argparser.add_argument(
        "-a", "--agent", type=str,
        choices=["Behavior", "Basic", "Constant"],
        help="select which agent to run",
        default="Behavior")
    argparser.add_argument(
        '-b', '--behavior', type=str,
        #choices=["cautious", "normal", "aggressive"],
        help='Choose one of the possible agent behaviors (default: normal) ',
        default='normal')
    argparser.add_argument(
        '-s', '--seed',
        help='Set seed for repeating executions (default: None)',
        default=None,
        type=int)
    argparser.add_argument(
        '-I', '--interactive',
        help='Enter interactive mode after initialization',
        action="store_true")

    args = argparser.parse_args()

    args.width, args.height = [int(x) for x in args.res.split('x')]

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    logging.info('listening to server %s:%s', args.host, args.port)

    print(__doc__)

    try:
        game_loop(args)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':
    main()
