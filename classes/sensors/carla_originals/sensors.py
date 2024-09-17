"""
Sensor classes used by the examples in the CARLA repository.
These classes are true to the original, however might have slight
modifications like type hints and the :py:class:`.CustomSensorInterface`
as base.
"""

import collections
import math
import weakref

import carla

from classes.sensors._sensor_interface import CustomSensorInterface

__all__ = [
    'CollisionSensor',
    'GnssSensor',
    'IMUSensor',
    'LaneInvasionSensor',
    'RadarSensor'
]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.ui.hud import HUD

# ==============================================================================
# -- CollisionSensor -----------------------------------------------------------
# ==============================================================================


class CollisionSensor(CustomSensorInterface):
    """
    Wrapper class for CARLA collision sensors
    
    See Also:
        https://carla.readthedocs.io/en/latest/ref_sensors/#collision-detector
    """

    def __init__(self, parent_actor: carla.Actor, hud: "HUD"):
        """Constructor method"""
        self.history: "list[tuple[int, float]]" = []
        self._parent = parent_actor
        self.hud: "HUD" = hud
        world = self._parent.get_world()
        blueprint = world.get_blueprint_library().find('sensor.other.collision')
        self.sensor = world.spawn_actor(blueprint, carla.Transform(), attach_to=self._parent)  # type: ignore
        # We need to pass the lambda a weak reference to
        # self to avoid circular reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(lambda event: CollisionSensor._on_collision(weak_self, event))  # pyright: ignore[reportArgumentType]

    def get_collision_history(self):
        """Gets the history of collisions"""
        history: dict[int, float] = collections.defaultdict(float)
        for frame, intensity in self.history:
            history[frame] += intensity
        return history

    @staticmethod
    def _on_collision(weak_self: "weakref.ref[CollisionSensor]", event: carla.CollisionEvent):
        """On collision method"""
        self = weak_self()
        if not self:
            return
        from classes.ui.hud import get_actor_display_name  # lazy import to avoid circular import  # noqa: PLC0415
        actor_type = get_actor_display_name(event.other_actor)
        self.hud.notification(f'Collision with {actor_type!r}')
        impulse = event.normal_impulse
        intensity = math.sqrt(impulse.x ** 2 + impulse.y ** 2 + impulse.z ** 2)
        self.history.append((event.frame, intensity))
        if len(self.history) > 4000:
            self.history.pop(0)


# ==============================================================================
# -- LaneInvasionSensor --------------------------------------------------------
# ==============================================================================


class LaneInvasionSensor(CustomSensorInterface):
    """
    Wrapper class for CARLA lane invasion sensors
    
    See Also:
        https://carla.readthedocs.io/en/latest/ref_sensors/#lane-invasion-detector
    """

    def __init__(self, parent_actor: carla.Actor, hud: "HUD"):
        """Constructor method"""
        self._parent = parent_actor
        self.hud = hud
        world = self._parent.get_world()
        bp = world.get_blueprint_library().find('sensor.other.lane_invasion')
        self.sensor = world.spawn_actor(bp, carla.Transform(), attach_to=self._parent)  # type: ignore
        # We need to pass the lambda a weak reference to self to avoid circular
        # reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(lambda event: LaneInvasionSensor._on_invasion(weak_self, event))  # pyright: ignore[reportArgumentType]

    @staticmethod
    def _on_invasion(weak_self: "weakref.ref[LaneInvasionSensor]", event: carla.LaneInvasionEvent):
        """On invasion method"""
        self = weak_self()
        if not self:
            return
        lane_types = {x.type for x in event.crossed_lane_markings}
        text = [repr(str(x).split()[-1]) for x in lane_types]
        self.hud.notification('Crossed line {}'.format(' and '.join(text)))


# ==============================================================================
# -- GnssSensor --------------------------------------------------------
# ==============================================================================


class GnssSensor(CustomSensorInterface):
    """
    Wrapper class for CARLA GNSS sensors
    
    See Also:
        https://carla.readthedocs.io/en/latest/ref_sensors/#gnss-sensor
    """

    def __init__(self, parent_actor: carla.Actor):
        """Constructor method"""
        self._parent = parent_actor
        self.lat = 0.0
        self.lon = 0.0
        world = self._parent.get_world()
        blueprint = world.get_blueprint_library().find('sensor.other.gnss')
        self.sensor = world.spawn_actor(blueprint, carla.Transform(carla.Location(x=1.0, z=2.8)),  # type: ignore
                                        attach_to=self._parent)
        # We need to pass the lambda a weak reference to
        # self to avoid circular reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(lambda event: GnssSensor._on_gnss_event(weak_self, event))  # pyright: ignore[reportArgumentType]

    @staticmethod
    def _on_gnss_event(weak_self: "weakref.ref[GnssSensor]", event: carla.GnssMeasurement):
        """GNSS method"""
        self = weak_self()
        if not self:
            return
        self.lat = event.latitude
        self.lon = event.longitude
        
# ==============================================================================
# -- RadarSensor ---------------------------------------------------------------
# ==============================================================================


class RadarSensor(CustomSensorInterface):
    """
    Wrapper class for CARLA radar sensors
    
    See Also:
        https://carla.readthedocs.io/en/latest/ref_sensors/#radar-sensor
    """
    
    def __init__(self, parent_actor: carla.Actor):
        self._parent = parent_actor
        bound_x = 0.5 + self._parent.bounding_box.extent.x
        #bound_y = 0.5 + self._parent.bounding_box.extent.y
        bound_z = 0.5 + self._parent.bounding_box.extent.z

        self.velocity_range = 7.5  # m/s
        world = self._parent.get_world()
        self.debug = world.debug
        bp = world.get_blueprint_library().find('sensor.other.radar')
        bp.set_attribute('horizontal_fov', str(35))
        bp.set_attribute('vertical_fov', str(20))
        self.sensor = world.spawn_actor(  # type: ignore
            bp,
            carla.Transform(
                carla.Location(x=bound_x + 0.05, z=bound_z + 0.05),
                carla.Rotation(pitch=5)),
            attach_to=self._parent)
        # We need a weak reference to self to avoid circular reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(
            lambda radar_data: RadarSensor._Radar_callback(weak_self, radar_data))  # pyright: ignore[reportArgumentType]

    @staticmethod
    def _Radar_callback(weak_self: "weakref.ref[RadarSensor]", radar_data: carla.RadarMeasurement):
        self = weak_self()
        if not self:
            return
        # To get a numpy [[vel, altitude, azimuth, depth],...[,,,]]:
        # points = np.frombuffer(radar_data.raw_data, dtype=np.dtype('f4'))
        # points = np.reshape(points, (len(radar_data), 4))

        current_rot = radar_data.transform.rotation
        for detect in radar_data:
            azi = math.degrees(detect.azimuth)
            alt = math.degrees(detect.altitude)
            # The 0.25 adjusts a bit the distance so the dots can
            # be properly seen
            fw_vec = carla.Vector3D(x=detect.depth - 0.25)
            carla.Transform(
                carla.Location(),
                carla.Rotation(
                    pitch=current_rot.pitch + alt,
                    yaw=current_rot.yaw + azi,
                    roll=current_rot.roll)).transform(fw_vec)

            def clamp(min_v, max_v, value):
                return max(min_v, min(value, max_v))

            norm_velocity = detect.velocity / self.velocity_range  # range [-1, 1]
            r = int(clamp(0.0, 1.0, 1.0 - norm_velocity) * 255.0)
            g = int(clamp(0.0, 1.0, 1.0 - abs(norm_velocity)) * 255.0)
            b = int(abs(clamp(- 1.0, 0.0, - 1.0 - norm_velocity)) * 255.0)
            self.debug.draw_point(
                radar_data.transform.location + fw_vec,  # pyright: ignore[reportArgumentType]
                size=0.075,
                life_time=0.06,
                persistent_lines=False,
                color=carla.Color(r, g, b))
            

# ==============================================================================
# -- IMUSensor -----------------------------------------------------------------
# ==============================================================================

class IMUSensor(CustomSensorInterface):
    """
    Wrapper class for CARLA IMU sensors
    
    See Also:
        https://carla.readthedocs.io/en/latest/ref_sensors/#imu-sensor
    """
    
    def __init__(self, parent_actor: carla.Actor):
        self._parent = parent_actor
        self.accelerometer = (0.0, 0.0, 0.0)
        self.gyroscope = (0.0, 0.0, 0.0)
        self.compass = 0.0
        world = self._parent.get_world()
        bp = world.get_blueprint_library().find('sensor.other.imu')
        self.sensor = world.spawn_actor(                                             # type: ignore
            bp, carla.Transform(), attach_to=self._parent)
        # We need to pass the lambda a weak reference to self to avoid circular
        # reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(
            lambda sensor_data: IMUSensor._IMU_callback(weak_self, sensor_data))  # pyright: ignore[reportArgumentType]

    @staticmethod
    def _IMU_callback(weak_self: "weakref.ref[IMUSensor]", sensor_data: carla.IMUMeasurement):
        self = weak_self()
        if not self:
            return
        limits = (-99.9, 99.9)
        self.accelerometer = (
            max(limits[0], min(limits[1], sensor_data.accelerometer.x)),
            max(limits[0], min(limits[1], sensor_data.accelerometer.y)),
            max(limits[0], min(limits[1], sensor_data.accelerometer.z)))
        self.gyroscope = (
            max(limits[0], min(limits[1], math.degrees(sensor_data.gyroscope.x))),
            max(limits[0], min(limits[1], math.degrees(sensor_data.gyroscope.y))),
            max(limits[0], min(limits[1], math.degrees(sensor_data.gyroscope.z))))
        self.compass = math.degrees(sensor_data.compass)
