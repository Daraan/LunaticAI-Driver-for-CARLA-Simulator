import weakref
from threading import Event, Thread
from typing import TYPE_CHECKING, ClassVar, List, Optional, cast

import carla
import numpy as np
import pygame
from carla import ColorConverter as cc
from carla import AttachmentType
from typing_extensions import Self

from agents.tools import logger
from agents.tools.hints import CameraBlueprint
from classes import MockDummy
from classes._sensor_interface import CustomSensorInterface
from launch_tools import CarlaDataProvider, class_or_instance_method

if TYPE_CHECKING:
    from agents.tools.config_creation import LaunchConfig
    from classes.hud import HUD

# TODO integrate into camera.yaml
CameraBlueprints = {
    'Camera RGB': CameraBlueprint('sensor.camera.rgb', cc.Raw, 'Camera RGB'),
    'Camera Depth (Raw)': CameraBlueprint('sensor.camera.depth', cc.Raw, 'Camera Depth (Raw)'),
    'Camera Depth (Gray Scale)': CameraBlueprint('sensor.camera.depth', cc.Depth, 'Camera Depth (Gray Scale)'),
    'Camera Depth (Logarithmic Gray Scale)': CameraBlueprint('sensor.camera.depth', cc.LogarithmicDepth, 'Camera Depth (Logarithmic Gray Scale)'),
    'Camera Semantic Segmentation (Raw)': CameraBlueprint('sensor.camera.semantic_segmentation', cc.Raw, 'Camera Semantic Segmentation (Raw)'),
    'Camera Semantic Segmentation (CityScapes Palette)': CameraBlueprint('sensor.camera.semantic_segmentation', cc.CityScapesPalette, 'Camera Semantic Segmentation (CityScapes Palette)'),
    'Lidar (Ray-Cast)': CameraBlueprint('sensor.lidar.ray_cast', carla.ColorConverter.Raw, 'Lidar (Ray-Cast)')
}
"""Camera blueprints used by the CARLA examples."""

CameraBlueprintsSimple: List[CameraBlueprint] = [CameraBlueprints['Camera RGB']]
"""Just a single RGB camera. Default for :py:meth:`.CameraManager.sensors`"""


# ==============================================================================
# -- CameraManager -------------------------------------------------------------
# ==============================================================================

_follow_car_event = Event()
"""Use the :py:meth:`treading.Event.set` method to stop the thread."""


# Solutions see: https://stackoverflow.com/questions/69107143/how-to-end-a-while-loop-in-another-thread
def spectator_follow_actor(actor: carla.Actor):
    """
    Continuously follow the ego vehicle with the spectator view.
    
    Attention:
        - Needs to be run in a separate thread.
        - Does not allow for thread.join() to stop the thread, before calling :py:meth:`stop`.
        
    Methods:
        stop: Stop following the actor.
        
    See Also:
        - :py:meth:`CameraManager.follow_actor`
    """
    try:
        while not _follow_car_event.is_set():
            _spectator_to_actor(actor)
    except Exception as e:
        logger.error(f"Error in spectator_follow_actor: {e}")


spectator_follow_actor.stop = lambda: _follow_car_event.set()  # type: ignore[attr-defined]


class CameraManager(MockDummy.CanBeDummy, CustomSensorInterface):
    """ Class for camera management"""

    default_blueprints: ClassVar[List[CameraBlueprint]] = list(CameraBlueprints.values())
    """Cameras that should be attached to the ego vehicle by default."""

    def __init__(self,
                 parent_actor: carla.Actor,
                 hud: "HUD",
                 args: "LaunchConfig",
                 sensors: Optional[List[CameraBlueprint]] = CameraBlueprintsSimple,
                 ):
        """
        Constructor method.
        
        :py:meth:`set_sensor` should be called after init to set :py:attr:`sensor`
        and :py:attr:`index` to a valid value.
        """
        self.sensor: Optional[carla.Sensor] = None  # Needs call to set_sensor
        self.index: Optional[int] = None  # Needs call to set_sensor
        
        self._surface: Optional[pygame.Surface] = None  # set on _parse_image, # type: ignore
        self._parent = parent_actor
        self._hud: "HUD" = hud
        self.current_frame = -1
        self.recording = False
        self._args = args
        self._frame_interval = args.camera.recorder.frame_interval  # todo freeze
        self.outpath = args.camera.recorder.output_path  # todo freeze
        bound_x = 0.5 + self._parent.bounding_box.extent.x
        bound_y = 0.5 + self._parent.bounding_box.extent.y
        bound_z = 0.5 + self._parent.bounding_box.extent.z
        
        # Maybe use args.camera.camera_blueprints
        self._camera_transforms = [
            (carla.Transform(carla.Location(x=-2.0 * bound_x, y=+0.0 * bound_y, z=2.0 * bound_z),
                             carla.Rotation(pitch=8.0)),
                AttachmentType.SpringArmGhost),
            (carla.Transform(carla.Location(x=+0.8 * bound_x, y=+0.0 * bound_y, z=1.3 * bound_z)),
                AttachmentType.Rigid),
            (carla.Transform(carla.Location(x=+1.9 * bound_x, y=+1.0 * bound_y, z=1.2 * bound_z)),
                AttachmentType.SpringArmGhost),
            (carla.Transform(carla.Location(x=-2.8 * bound_x, y=+0.0 * bound_y, z=4.6 * bound_z),
                             carla.Rotation(pitch=6.0)),
                AttachmentType.SpringArmGhost),
            (carla.Transform(carla.Location(x=-1.0, y=-1.0 * bound_y, z=0.4 * bound_z)),
                AttachmentType.Rigid)
        ]

        self.transform_index = 1
        # TODO: These are remnants from the original code, for our purpose most sensors are not relevant
        # -> Move to globals or some config which should be used (also saves resources)
        self.sensors = sensors or self.default_blueprints
        bp_library = CarlaDataProvider._blueprint_library
        for i, item in enumerate(self.sensors):
            try:
                if item.actual_blueprint is not None:
                    continue
            except AttributeError:  # not a named tuple
                pass
            blp = bp_library.find(item[0])
            if item[0].startswith('sensor.camera'):
                blp.set_attribute('image_size_x', str(hud.dim[0]))
                blp.set_attribute('image_size_y', str(hud.dim[1]))
                if blp.has_attribute('gamma'):
                    blp.set_attribute('gamma', str(args.camera.gamma))
            elif item[0].startswith('sensor.lidar'):
                blp.set_attribute('range', '50')
            try:
                # Named tuple
                self.sensors[i] = item._replace(actual_blueprint=blp)  # update with actual blueprint added
            except AttributeError:
                self.sensors[i] = CameraBlueprint(item[0], item[1], item[2], blp)
        
        # Update spectator in UE editor.
        if args.camera.spectator:
            self.follow_actor(self._parent)

    def toggle_camera(self) -> None:
        """Activate a camera"""
        self.transform_index = (self.transform_index + 1) % len(self._camera_transforms)
        self.set_sensor(self.index if self.index is not None else 0, notify=False, force_respawn=True)

    def set_sensor(self, index: Optional[int], notify=True, force_respawn=False) -> None:
        """Set the sensor that should be used for the camera output"""
        index = index or 0
        index = index % len(self.sensors)
        needs_respawn = True if self.index is None else (
                force_respawn or (self.sensors[index][0] != self.sensors[self.index][0]))
        if needs_respawn:
            if self.sensor is not None:
                self.destroy()
                self._surface = None
            self.sensor = cast(carla.Sensor, CarlaDataProvider.get_world().spawn_actor(
                self.sensors[index][-1],  # type: ignore
                self._camera_transforms[self.transform_index][0],
                attach_to=self._parent,
                attachment_type=self._camera_transforms[self.transform_index][1]))

            # We need to pass the lambda a weak reference to
            # self to avoid circular reference.
            weak_self = weakref.ref(self)
            self.sensor.listen(lambda image: CameraManager._parse_image(weak_self, image))  # type: ignore[arg-type]
        if notify:
            self._hud.notification(self.sensors[index][2])
        self.index = index

    def next_sensor(self) -> None:
        """Get the next sensor"""
        self.set_sensor(self.index + 1 if self.index is not None else None)

    def toggle_recording(self) -> None:
        """
        Toggle recording on or off
        
        Note:
            Currently requires :py:attr:`.LaunchConfig.pygame` to be set to :code:`True`.
        
        .. deprecated:
            Superseded by WorldMode.toggle_recording
        
        :meta private:
        """
        self.recording = not self.recording
        self._hud.notification('Recording %s' % ('On' if self.recording else 'Off'))

    def destroy(self) -> None:
        super().destroy()
        _follow_car_event.set()
        self.index = None   # type: ignore
        self._surface = None  # type: ignore

    def render(self, display: pygame.surface.Surface) -> None:
        """Renders method the current camera image"""
        if self._surface is not None:
            display.blit(self._surface, (0, 0))

    @staticmethod
    def _parse_image(weak_self: "weakref.ref[CameraManager]", image: carla.Image):
        self = weak_self()
        if not self:
            return
        index: int = self.index  # type: ignore[assignment]
        if self.sensors[index][0].startswith('sensor.lidar'):
            points = np.frombuffer(image.raw_data, dtype=np.dtype('f4'))
            points = np.reshape(points, (int(points.shape[0] / 4), 4))
            lidar_data = np.array(points[:, :2])
            lidar_data *= min(self._hud.dim) / 100.0
            lidar_data += (0.5 * self._hud.dim[0], 0.5 * self._hud.dim[1])
            lidar_data = np.fabs(lidar_data)  # pylint: disable=assignment-from-no-return
            lidar_data = lidar_data.astype(np.int32)
            lidar_data = np.reshape(lidar_data, (-1, 2))
            lidar_img_size = (self._hud.dim[0], self._hud.dim[1], 3)
            lidar_img = np.zeros(lidar_img_size)
            lidar_img[tuple(lidar_data.T)] = (255, 255, 255)
            self._surface = pygame.surfarray.make_surface(lidar_img)
        else:
            image.convert(self.sensors[index][1])  # apply color converter
            array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
            array = np.reshape(array, (image.height, image.width, 4))
            array = array[:, :, :3]
            array = array[:, :, ::-1]
            self._surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
        # Deprecated: Recording is done on the WorldModel
        if self.recording and (
                (image.frame % self._frame_interval) == 0
                or self.current_frame + self._frame_interval < image.frame):
            print("Saving image to disk", self.outpath % image.frame)
            image.save_to_disk(self.outpath % image.frame)
        self.current_frame = image.frame
     
    _spectator_thread: Thread
    """Thread for the spectator to follow the ego vehicle."""
     
    @class_or_instance_method
    def follow_actor(cls_or_self: "Self | type[Self]",
                     actor: Optional[carla.Actor] = None,
                     updater=spectator_follow_actor) -> None:
        """
        Follows the actor with the spectator view.
        
        Parameters:
            actor: The actor to follow. Defaults to the **parent_actor**.
            updater: The function to update the camera view. Defaults to :py:func:`camera_follow_actor`.
        """
        actor = actor or getattr(cls_or_self, "_parent", None)
        if actor is None:
            raise ValueError("No actor to follow")
        logger.log(0, "Starting spectator thread")
        cls_or_self._spectator_thread = Thread(target=updater, args=(actor, ), daemon=True)
        cls_or_self._spectator_thread.start()
        
    @staticmethod
    def stop_following_actor() -> None:
        _follow_car_event.set()
        
    def stop(self) -> None:
        self.stop_following_actor()
        return super().stop()
        
# ==============================================================================


def _spectator_to_actor(actor: carla.Actor) -> None:
    """
    Set the spectator's view to follow the ego vehicle.

    Parameters:
        ego_vehicle (Vehicle): The ego vehicle that the spectator will follow.
        world (World): The game world where the spectator view is set.

    Description:
        This function calculates the desired spectator transform by positioning the spectator
        10 meters behind the ego vehicle and 5 meters above it. The spectator's view will follow
        the ego vehicle from this transformed position.

    Note:
        To face the vehicle from behind, uncomment the line 'spectator_transform.rotation.yaw += 180'.

    Returns:
        None: The function does not return any value.
    """
    # Calculate the desired spectator transform
    vehicle_transform = actor.get_transform()
    spectator_transform = vehicle_transform
    spectator_transform.location -= (
        vehicle_transform.get_forward_vector() * 10
    )  # Move 10 meters behind the vehicle
    spectator_transform.location += (
        vehicle_transform.get_up_vector() * 5
    )  # Move 5 meters above the vehicle
    # spectator_transform.rotation.yaw += 180 # Face the vehicle from behind

    # Set the spectator's transform in the world
    CarlaDataProvider.get_world().get_spectator().set_transform(spectator_transform)
