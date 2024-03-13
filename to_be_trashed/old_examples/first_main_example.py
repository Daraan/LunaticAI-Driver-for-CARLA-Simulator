import __allow_imports_from_root
import time

import carla

import launch_tools
from classes.carla_service import CarlaService
# TODO: maybe we can merge these or make them more unified & marge with agent
from classes.driver import Driver

vehicles = []


def main(args):
    global client
    carlaService = CarlaService("Town04", args.host, args.port)
    client = carlaService.client

    world = carlaService.getWorld()
    level = world.get_map()
    ego_bp, car_bp = launch_tools.blueprint_helpers.get_contrasting_blueprints(world)  # ego is red the others default colors

    driver1 = Driver("config/default_driver.json")
    car1 = carlaService.createCar("model3")

    driver2 = Driver("config/default_driver.json")
    car2 = carlaService.createCar("coupe")

    driver3 = Driver("config/default_driver.json")
    car3 = carlaService.createCar("mustang")

    carlaService.assignDriver(car1, driver1)
    carlaService.assignDriver(car2, driver2)
    carlaService.assignDriver(car3, driver3)

    spawnPoint = carlaService.getWorld().get_map().get_spawn_points()[123]
    driver1.spawn(spawnPoint)
    spawnPoint.location.y += 8
    driver2.spawn(spawnPoint)
    spawnPoint.location.y -= 16
    driver3.spawn(spawnPoint)

    # driver1.vehicle.focusCamera()
    car3.setThrottle(0.2)
    driver1.drive(carlaService.vehicleList)
    # car2.setThrottle(2)

    time.sleep(1)
    # car1.setBrake(2)
    # car1.setSteering(3)
    # car1.setHandbrake(True)
    time.sleep(5)

    if args.interactive:
        # goes into interactive mode here
        import code
        v = globals().copy()
        v.update(locals())
        code.interact(local=v)
    input("press any key to end...")


if __name__ == '__main__':
    import launch_tools.argument_parsing as parse
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
