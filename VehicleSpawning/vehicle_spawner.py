import yaml

import launch_tools
from classes.rule_interpreter import RuleInterpreter
from classes.carla_service import CarlaService
from classes.driver import Driver
from classes.traffic_manager import TrafficManager
from classes.vehicle import Vehicle
from launch_tools import CarlaDataProvider


class VehicleSpawner:
    def __init__(self, config_file):
        self.config = self.read_config(config_file)
        self.client = None
        self.vehicles = []
        self.carla_service: CarlaService = None

    @staticmethod
    def read_config(file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def initialize_carla_service(self):
        carla_config = self.config['carla_service']
        self.carla_service = CarlaService(carla_config['map'], carla_config['ip'], carla_config['port'])

    def setup_world(self):
        world = self.carla_service.get_world()
        world_map = self.carla_service.get_map()
        return world, world_map

    def prepare_vehicles(self, world):
        driver_config_path = self.config['driver']['config']
        spawn_points_file = self.config['spawn_points']['file']
        rule_interpreter_config = self.config['rule_interpreter']['config']

        ego_bp, car_bp = launch_tools.prepare_blueprints(world)
        driver1 = Driver(driver_config_path, traffic_manager=self.client)
        spawn_points = launch_tools.csv_to_transformations(spawn_points_file)
        rule_interpreter = RuleInterpreter(rule_interpreter_config)
        return ego_bp, car_bp, driver1, spawn_points, rule_interpreter

    def spawn_vehicles(self, world, ego_bp, spawn_points):
        ego = Vehicle(world, ego_bp)
        try:
            ego.spawn(spawn_points[0])
        except Exception as e:
            print(e.__str__())
        else:
            CarlaDataProvider.register_actor(ego.actor, spawn_points[0])
            self.vehicles.append(ego)
        return ego

    def assign_drivers(self, ego, driver1):
        self.carla_service.assignDriver(ego, driver1)
        return ego.actor

    def spawn_traffic(self, world, car_bp, spawn_points, driver1, ego_vehicle):
        # NOTE: Duplicate in CarlaFunction
        client = CarlaDataProvider.get_client()
        for sp in spawn_points[1:5]:
            v = Vehicle(world, car_bp)
            v.spawn(sp)
            self.vehicles.append(v)
            ap = TrafficManager(v.actor, speed_limit_scale=-driver1.speed_range[1],
                                min_front_distance=driver1.distance_range[0])
            ap.init_lunatic_driver()
            ap.start_drive()

        for sp in spawn_points[5:]:
            v = Vehicle(world, car_bp)
            v.spawn(sp)
            self.vehicles.append(v)
            ap = TrafficManager(v.actor, speed_limit_scale=60, min_front_distance=8)
            ap.init_passive_driver()
            ap.start_drive()

        tm = TrafficManager(ego_vehicle,
                            speed_limit_scale=-driver1.speed_range[1],
                            min_front_distance=driver1.distance_range[0])
        tm.init_lunatic_driver()
        tm.start_drive()
        return self.vehicles, tm
