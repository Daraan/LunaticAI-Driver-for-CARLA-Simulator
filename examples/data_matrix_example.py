import sys

import carla

import launch_tools
from data_gathering.car_detection_matrix.run_matrix import DetectionMatrix
from launch_tools.carla_service import initialize_carla
#from classes.experimental.driver import Driver
from classes.experimental.traffic_manager import TrafficManager
from classes.experimental.vehicle import Vehicle

vehicles = []


def main():
    global client
    client, world, world_map = initialize_carla("Town04", "127.0.0.1", 2000)

    ego_bp, car_bp = launch_tools.prepare_blueprints()

    spawn_points = launch_tools.csv_to_transformations("examples/highway_example_car_positions.csv")

    # Spawn Ego
    ego = Vehicle(world, ego_bp)
    ego.spawn(spawn_points[0])
    vehicles.append(ego)

    matrix = DetectionMatrix(ego, world)

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


if __name__ == '__main__':
    try:
        main()
    finally:
        try:
            client.apply_batch([carla.command.DestroyActor(x.actor) for x in vehicles])
        except NameError:
            # Should be client not defined
            pass
