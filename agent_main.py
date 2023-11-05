import carla
from classes.carla_service import CarlaService
# TODO: maybe we can merge these or make them more unified
from classes.driver import Driver
from classes.vehicle import Vehicle

import sys
import random

import utils
# To import a basic agent
from agents.navigation.basic_agent import BasicAgent

# Import Autopilot, # TODO: remove this
from classes.traffic_manager_daniel import TrafficManagerD


# To import a behavior agent

vehicles = []


def main(args):
    global client
    carlaService = CarlaService("Town04", args.host, args.port)
    client = carlaService.client

    world = carlaService.getWorld()
    level = world.get_map()
    ego_bp, car_bp = utils.blueprint_helpers.get_contrasting_blueprints(world)

    driver1 = Driver("config/driver1.json", traffic_manager=client)

    spawn_points = utils.general.csv_to_transformations("examples/highway_example_car_positions.csv")
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

    # ------------- Planning loop ----------------
    i = 0
    while True:
        if agent.done():
            agent.set_destination(random.choice(spawn_points).location)
            print("The target has been reached, searching for another target")
        controls = agent.run_step()
        if (i % 10000) == 0:
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
    import utils.argument_parsing as parse
    from pprint import pprint
    args = parse.client_settings.add(parse.interactive_mode).parse_args()
    pprint(args)
    try:
        main(args)
    finally:
        try:
            client.apply_batch([carla.command.DestroyActor(x.actor) for x in vehicles])
        except NameError as e:
            print(e)
            # likely client not defined yet due to earlier errors, or not globally defined.

