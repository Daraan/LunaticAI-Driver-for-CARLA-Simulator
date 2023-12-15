import csv
import random


class VehicleSpawner:
    def __init__(self, config_file, vehicle_creator):
        self.spawn_points = self.load_spawn_points(config_file)
        self.vehicle_creator = vehicle_creator

    @staticmethod
    def load_spawn_points(self, filename):
        spawn_points = []
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                spawn_points.append((float(row['x']), float(row['y']), float(row['z'])))
        return spawn_points

    def spawn_vehicle(self, vehicle_params):
        spawn_point = random.choice(self.spawn_points)
        self.vehicle_creator.create_vehicle(spawn_point, vehicle_params)

    def spawn_vehicles(self, vehicles_config):
        for config in vehicles_config:
            self.spawn_vehicle(config)
