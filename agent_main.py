import carla
from carla_service import CarlaService
# TODO: maybe we can merge these or make them more unfied
from driver import Driver
from vehicle import Vehicle

import numpy
import glob
import os
import sys
import random
import time

from useful_scripts import utils
# To import a basic agent
from agents.navigation.basic_agent import BasicAgent

from classes.traffic_manager_daniel import TrafficManagerD

# To import a behavior agent
from agents.navigation.behavior_agent import BehaviorAgent

vehicles = []


def main():
    global client
    carlaService = CarlaService("Town04", "127.0.0.1", 2000)
    client = carlaService.client

    world = carlaService.getWorld()
    level = world.get_map()
    ego_bp, car_bp = utils.prepare_blueprints(world)

    driver1 = Driver("json/driver1.json", traffic_manager=client)

    spawn_points = utils.csv_to_transformations("useful_scripts/highway_example_car_positions.csv")
    # car1 = carlaService.createCar("model3")

    # Spawn Ego
    ego = Vehicle(world, ego_bp)
    ego.spawn(spawn_points[0])
    vehicles.append(ego)
    carlaService.assignDriver(ego, driver1)
    agent = BasicAgent(ego.actor)

    wp_start=level.get_waypoint(ego.actor.get_location())
    next_wps : list = wp_start.next(200)

    destination = next_wps[-1].transform.location
    agent.set_destination(destination)
    agent.ignore_vehicles(active=False)


    # spawn others
    for sp in spawn_points[1:]:
        v = Vehicle(world, car_bp)
        v.spawn(sp)
        vehicles.append(v)
        # v.setVelocity(1)
        print(v.actor)
        ap = TrafficManagerD(client, v.actor)
        ap.init_passive_driver()
        ap.start_drive()


    i = 0
    while True:
        if agent.done():
            agent.set_destination(random.choice(spawn_points).location)
            print("The target has been reached, searching for another target")
        controls = agent.run_step()
        if (i % 1000) == 0:
            print(controls)
        ego.actor.apply_control(controls)

    """
    tm = TrafficManagerD(client, ego.actor,
                         # config="json/driver1.json" # Not implemented yet
                         )
    tm.init_lunatic_driver()
    # ego.setThrottle(1)
    # time.sleep(1)
    tm.start_drive()
    """
    if "-I" in sys.argv:
        # goes into interactive mode here
        import code
        v = globals().copy()
        v.update(locals())
        code.interact(local=v)

    input("press any key to end...")



if __name__ == '__main__':
    try:
        main()
    finally:
        try:
            client.apply_batch([carla.command.DestroyActor(x.actor) for x in vehicles])
        except NameError:
            # Should be client not defined
            pass
