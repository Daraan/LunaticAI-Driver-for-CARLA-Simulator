from __future__ import print_function

import logging
import random
import sys
import threading

import carla
import numpy.random as random
import pygame

import utils
from DataGathering.informationUtils import follow_car, get_all_road_lane_ids
from DataGathering.matrix_wrap import wrap_matrix_functionalities
from agents.navigation.basic_agent import BasicAgent
from agents.navigation.behavior_agent import BehaviorAgent
from agents.navigation.constant_velocity_agent import ConstantVelocityAgent
from classes.carla_originals.HUD import HUD
from classes.carla_originals.world import World
from classes.traffic_manager_daniel import TrafficManagerD
from classes.vehicle import Vehicle
from utils.keyboard_controls import PassiveKeyboardControl as KeyboardControl


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
        spawn_points = utils.general.csv_to_transformations("doc/highway_example_car_positions.csv")

        # Spawn Ego
        ego_bp, car_bp = utils.blueprint_helpers.get_contrasting_blueprints(sim_world)
        ego = Vehicle(sim_world, ego_bp)
        start: carla.Transform = spawn_points[0]
        ego.spawn(start)

        world = World(client.get_world(), hud, args, player=ego.actor)
        wp_start = world.map.get_waypoint(start.location)
        all_spawn_points = world.map.get_spawn_points()
        controller = KeyboardControl(world)

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

        ego_vehicle = ego.actor
        game_world = client.get_world()
        world_map = game_world.get_map()
        road_lane_ids = get_all_road_lane_ids(world_map=world_map)

        def loop():
            i = 0
            while True:
                clock.tick()

                follow_car(ego_vehicle, game_world)
                matrix = wrap_matrix_functionalities(ego_vehicle, game_world, world_map, road_lane_ids)

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

                control = agent.run_step(debug=True)
                control.manual_gear_shift = False
                world.player.apply_control(control)
                i += 1

        if "-I" in sys.argv:
            thread = threading.Thread(target=loop)
            thread.start()
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


def main():
    args = utils.argument_parsing.automatic_control_example.parse_args()
    args.width, args.height = [int(x) for x in args.res.split('x')]
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)
    logging.info('listening to server %s:%s', args.host, args.port)

    try:
        game_loop(args)
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':
    main()
