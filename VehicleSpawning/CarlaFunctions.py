import utils
from Rules.ApplyRules import RuleInterpreter
from classes.carla_service import CarlaService
from classes.driver import Driver
from classes.traffic_manager import TrafficManager
from classes.vehicle import Vehicle

vehicles = []


def initialize_carla_service():
    global client
    carla_service = CarlaService("Town04", "127.0.0.1", 2000)
    client = carla_service.client
    return carla_service


def setup_world(carla_service):
    world = carla_service.getWorld()
    world_map = world.get_map()
    return world, world_map


def prepare_vehicles(world):
    ego_bp, car_bp = utils.prepare_blueprints(world)
    driver1 = Driver("../config/default_driver.json", traffic_manager=client)
    spawn_points = utils.csv_to_transformations("../doc/highway_example_car_positions.csv")
    rule_interpreter = RuleInterpreter("../Rules/config/yaml/default_rules.yaml")
    return ego_bp, car_bp, driver1, spawn_points, rule_interpreter


def spawn_vehicles(world, ego_bp, spawn_points):
    global vehicles
    ego = Vehicle(world, ego_bp)
    try:
        ego.spawn(spawn_points[0])
    except Exception as e:
        print(e.__str__())
    vehicles.append(ego)
    return ego


def assign_drivers(carla_service, ego, driver1):
    carla_service.assignDriver(ego, driver1)
    return ego.actor


def spawn_traffic(world, car_bp, spawn_points, driver1, ego_vehicle):
    global client, vehicles
    for sp in spawn_points[1:5]:
        v = Vehicle(world, car_bp)
        v.spawn(sp)
        vehicles.append(v)
        ap = TrafficManager(client, v.actor, speed_limit_scale=-driver1.speed_range[1],
                            min_front_distance=driver1.distance_range[0])
        ap.init_lunatic_driver()
        ap.start_drive()

    for sp in spawn_points[5:]:
        v = Vehicle(world, car_bp)
        v.spawn(sp)
        vehicles.append(v)
        ap = TrafficManager(client, v.actor, speed_limit_scale=60, min_front_distance=8)
        ap.init_passive_driver()
        ap.start_drive()

    tm = TrafficManager(client, ego_vehicle,
                        speed_limit_scale=-driver1.speed_range[1],
                        min_front_distance=driver1.distance_range[0])
    tm.init_lunatic_driver()
    tm.start_drive()

    return vehicles, tm
