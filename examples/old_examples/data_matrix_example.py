import sys

import carla

import launch_tools
from data_gathering.car_detection_matrix.run_matrix import DataMatrix
from launch_tools.carla_service import initialize_carla
# TODO: maybe we can merge these or make them more unfied
from classes.driver import Driver
from classes.traffic_manager import TrafficManager
from classes.vehicle import Vehicle

vehicles = []


def main():
    global client
    client, world, world_map = initialize_carla("Town04", "127.0.0.1", 2000)

    ego_bp, car_bp = launch_tools.prepare_blueprints(world)

    driver1 = Driver("config/default_driver.json", traffic_manager=client)

    spawn_points = launch_tools.csv_to_transformations("examples/highway_example_car_positions.csv")
    # car1 = carla_service.createCar("model3")

    # Spawn Ego
    ego = Vehicle(world, ego_bp)
    ego.spawn(spawn_points[0])
    vehicles.append(ego)
    #carla_service.assignDriver(ego, driver1)

    # TODO: let Driver class manage autopilot and not the TrafficMangerD class

    matrix = DataMatrix(ego, world)

    # spawn others
    for sp in spawn_points[1:]:
        v = Vehicle(world, car_bp)
        v.spawn(sp)
        vehicles.append(v)
        # v.setVelocity(1)
        print(v.actor)
        ap = TrafficManager(v.actor)
        ap.init_passive_driver()
        ap.start_drive()

    tm = TrafficManager(ego.actor,
                         # config="json/driver1.json" # Not implemented yet
                         )
    tm.init_lunatic_driver()
    # ego.setThrottle(1)
    # time.sleep(1)
    tm.start_drive()

    m = matrix.getMatrix()

    for i in m:
        print(i)

    # driver1.spawn(carla_service.getWorld().get_map().get_spawn_points()[123])
    # driver1.vehicle.focusCamera()
    # ego.setThrottle(8)
    # time.sleep(4)
    # ego.setBrake(2)
    if "-I" in sys.argv:
        # goes into interactive mode here
        import code
        v = globals().copy()
        v.update(locals())
        code.interact(local=v)

    input("press any key to end...")

    """
    driver2 = Driver("json/driver1.json")
    car2 = carla_service.createCar("coupe")

    driver3 = Driver("json/driver1.json")
    car3 = carla_service.createCar("mustang")

    carla_service.assignDriver(car1, driver1)
    carla_service.assignDriver(car2, driver2)
    carla_service.assignDriver(car3, driver3)


    spawnPoint = carla_service.getWorld().get_map().get_spawn_points()[123]
    driver1.spawn(spawnPoint)
    spawnPoint.location.x += 8
    driver2.spawn(spawnPoint)
    spawnPoint.location.x -= 16
    driver3.spawn(spawnPoint)

    driver1.vehicle.focusCamera()
    driver1.drive(carla_service.vehicleList)
    # car2.setThrottle(2)
    # car3.setThrottle(2.1)

    time.sleep(1)
    # car1.setBrake(2)
    # car1.setSteering(3)
    # car1.setHandbrake(True)
    time.sleep(5)
    """


if __name__ == '__main__':
    try:
        main()
    finally:
        try:
            client.apply_batch([carla.command.DestroyActor(x.actor) for x in vehicles])
        except NameError:
            # Should be client not defined
            pass
