import math
import time
from cmath import sqrt

import carla
from carla import Vector3D

import plotly.graph_objs as go
import plotly.subplots
import random
import time
import matplotlib
matplotlib.use('TkAgg')

def calculateDistance(location1, location2):
    return sqrt(
        (location1.x ** 2 - location2.x ** 2) +
        (location1.y ** 2 - location2.y ** 2) +
        (location1.z ** 2 - location2.z ** 2)
    ).real

from carla import Vector3D

class Vehicle:
    # TODO would be nice if we could derive this from carla.Vehicle
    # should be able to use some functions directly without using functions for all

    instances : list = [] # for easier destruction later

    def __init__(self, world, make=""):
        self.actor = None
        self.world = world
        self.control = carla.VehicleControl()
        blueprint_library = world.get_blueprint_library()
        if isinstance(make, carla.ActorBlueprint):
            self.actorBlueprint = make
        else:
            self.actorBlueprint = blueprint_library.filter(make)[0]
        Vehicle.instances.append(self) # access all instances over the class

    def __eq__(self, other):
        return not (
                self.getLocation().x != other.getLocation().x
                or self.getLocation().y != other.getLocation().y
                or self.getLocation().z != other.getLocation().z
        )


    def spawn(self, transform):
        self.actor = self.world.spawn_actor(self.actorBlueprint, transform)
        self.actor.apply_control(self.control)

    def focusCamera(self):
        self.world.get_spectator().set_transform(self.actor.get_transform())

    def setThrottle(self, value):
        self.control.brake = 0
        self.control.throttle = value
        self.actor.apply_control(self.control)

    def setVelocity(self, speed : Vector3D =3):
        if not isinstance(speed, Vector3D):
            self.actor.enable_constant_velocity(Vector3D(x=speed))
        else:
            self.actor.enable_constant_velocity(speed)

    def setBrake(self, value):
        self.control.throttle = 0
        self.control.brake = value
        self.actor.apply_control(self.control)

    def setSteering(self, value):
        self.control.steer = value
        self.actor.apply_control(self.control)

    def setHandbrake(self, value):
        self.control.hand_brake = value
        self.actor.apply_control(self.control)

    def getLocation(self):
        return self.actor.get_transform().location

    def getRotation(self):
        return self.actor.get_transform().rotation

    def calculateRelativeCoordinates(self, other_car_location):
        currentLocation = self.getLocation()
        currentRotation = self.getRotation()

        relative_x = other_car_location.x - currentLocation.x
        relative_y = other_car_location.y - currentLocation.y

        # Convert relative position to ego car's coordinate system based on its rotation
        relative_x_rotated = (
                relative_x * math.cos(math.radians(-currentRotation.yaw)) -
                relative_y * math.sin(math.radians(-currentRotation.yaw))
        )
        relative_y_rotated = (
                relative_x * math.sin(math.radians(-currentRotation.yaw)) +
                relative_y * math.cos(math.radians(-currentRotation.yaw))
        )

        return relative_x_rotated, relative_y_rotated

    def distanceToCarAhead(self, vehicles: []):
        closestCar = None
        closestDistance = float('inf')  # Initialize with a very large value

        for car in vehicles:
            if car != self:
                car_location = car.getLocation()

                # Calculate relative coordinates using the separate function
                relative_x_rotated, relative_y_rotated = self.calculateRelativeCoordinates(car_location)

                # Check if the car is ahead based on relative y-coordinate
                if relative_y_rotated > 0:
                    distance = calculateDistance(self.getLocation(), car_location)
                    if distance < closestDistance:
                        closestDistance = distance
                        closestCar = car  # Store the closest car object

        # Return the distance to the closest car ahead
        if closestCar is not None:
            return closestDistance
        else:
            return None

    def distanceToCarBehind(self, vehicles: []):
        closestCar = None
        closestDistance = float('inf')  # Initialize with a very large value

        for car in vehicles:
            if car != self:
                car_location = car.getLocation()

                # Calculate relative coordinates using the separate function
                relative_x_rotated, relative_y_rotated = self.calculateRelativeCoordinates(car_location)

                # Check if the car is behind based on relative y-coordinate
                if relative_y_rotated < 0:
                    distance = calculateDistance(self.getLocation(), car_location)
                    if distance < closestDistance:
                        closestDistance = distance
                        closestCar = car  # Store the closest car object

        # Return the distance to the closest car behind
        if closestCar is not None:
            return closestDistance
        else:
            return None

    def drive(self, carList):
        # Define the desired safe distance between cars
        safe_distance = 5.0  # You can adjust this value as needed

        # Set the loop rate (e.g., 10 times per second)
        loop_rate = 5  # Hz
        loop_interval = 1.0 / loop_rate

        fig = plotly.subplots.make_subplots()
        trace = go.Scatter(x=[], y=[], mode='lines+markers')
        fig.add_trace(trace)
        fig.update_layout(
            xaxis=dict(range=[0, 10]),  # Adjust the x-axis limits as needed
            yaxis=dict(range=[0, 100])  # Adjust the y-axis limits as needed
        )


        while True:

            # Check the distance to the car ahead
            # vehicles_in_world = self.world.get_actors().filter('vehicle.*')
            distance_to_car_ahead = self.distanceToCarAhead(carList)
            if distance_to_car_ahead is not None:

                if distance_to_car_ahead < 54:
                    self.setBrake(1)
                else:
                    # Calculate the speed difference between the two cars
                    # speed_difference = self.actor.get_velocity().x - vehicles_in_world[0].get_velocity().x
                    print(distance_to_car_ahead)

                    # Calculate the desired speed to maintain the safe distance
                    desired_speed = -(1/(math.e**distance_to_car_ahead))+1
                    # print("Desired speed:", desired_speed)

                    # Calculate the desired acceleration
                    desired_acceleration = (desired_speed - self.actor.get_velocity().y) / (safe_distance)

                    # Adjust throttle and brake based on the desired acceleration
                    if desired_acceleration > 0:
                        self.setThrottle(min(1.0, desired_acceleration))
                    else:
                        self.setBrake(min(1.0, -desired_acceleration))

                    # print("Desired acc:", desired_acceleration)

            # Sleep for the specified interval
            time.sleep(loop_interval)
