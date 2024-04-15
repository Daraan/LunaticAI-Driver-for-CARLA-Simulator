import weakref

import carla
import numpy as np
import pygame
from carla import ColorConverter as cc

from typing import TYPE_CHECKING, ClassVar, List, NamedTuple, Optional

from classes._custom_sensor import CustomSensor
from launch_tools import CarlaDataProvider

if TYPE_CHECKING:
    from classes.HUD import HUD
    from agents.tools.config_creation import LaunchConfig

class CameraBlueprint(NamedTuple):
    blueprint_path : str
    color_convert : cc
    name : str
    actual_blueprint : Optional[carla.ActorBlueprint] = None

# TODO maybe use camera.yaml
CameraBlueprints = {
    'Camera RGB' : CameraBlueprint('sensor.camera.rgb', cc.Raw, 'Camera RGB'),
    'Camera Depth (Raw)' : CameraBlueprint('sensor.camera.depth', cc.Raw, 'Camera Depth (Raw)'),
    'Camera Depth (Gray Scale)' : CameraBlueprint('sensor.camera.depth', cc.Depth, 'Camera Depth (Gray Scale)'),
    'Camera Depth (Logarithmic Gray Scale)' : CameraBlueprint('sensor.camera.depth', cc.LogarithmicDepth, 'Camera Depth (Logarithmic Gray Scale)'),
    'Camera Semantic Segmentation (Raw)' : CameraBlueprint('sensor.camera.semantic_segmentation', cc.Raw, 'Camera Semantic Segmentation (Raw)'),
    'Camera Semantic Segmentation (CityScapes Palette)' : CameraBlueprint('sensor.camera.semantic_segmentation', cc.CityScapesPalette, 'Camera Semantic Segmentation (CityScapes Palette)'),
    'Lidar (Ray-Cast)' : CameraBlueprint('sensor.lidar.ray_cast', None, 'Lidar (Ray-Cast)')
}

CameraBlueprintsSimple = [CameraBlueprints['Camera RGB']]


# ==============================================================================
# -- CameraManager -------------------------------------------------------------
# ==============================================================================


class CameraManager(CustomSensor):
    """ Class for camera management"""

    default_blueprints: ClassVar[List[CameraBlueprint]] = list(CameraBlueprints.values())

    def __init__(self, parent_actor : carla.Actor, 
                 hud : "HUD",
                 args:"LaunchConfig",
                 sensors:Optional[List[CameraBlueprint]]=CameraBlueprintsSimple,
                 ):
        """Constructor method"""
        self.sensor = None
        self.surface : pygame.Surface = None
        self._parent = parent_actor
        self.hud : "HUD" = hud
        self.current_frame = -1
        self.recording = False
        self._args = args
        self._frame_interval = args.camera.recorder.frame_interval # todo freeze
        self.outpath = args.camera.recorder.output_path # todo freeze
        bound_x = 0.5 + self._parent.bounding_box.extent.x
        bound_y = 0.5 + self._parent.bounding_box.extent.y
        bound_z = 0.5 + self._parent.bounding_box.extent.z
        attachment = carla.AttachmentType
        # Maybe use args.camera.camera_blueprints
        self._camera_transforms = [
            (carla.Transform(carla.Location(x=-2.0 * bound_x, y=+0.0 * bound_y, z=2.0 * bound_z),
                             carla.Rotation(pitch=8.0)), attachment.SpringArmGhost),
            (carla.Transform(carla.Location(x=+0.8 * bound_x, y=+0.0 * bound_y, z=1.3 * bound_z)), attachment.Rigid),
            (carla.Transform(carla.Location(x=+1.9 * bound_x, y=+1.0 * bound_y, z=1.2 * bound_z)),
             attachment.SpringArmGhost),
            (carla.Transform(carla.Location(x=-2.8 * bound_x, y=+0.0 * bound_y, z=4.6 * bound_z),
                             carla.Rotation(pitch=6.0)), attachment.SpringArmGhost),
            (carla.Transform(carla.Location(x=-1.0, y=-1.0 * bound_y, z=0.4 * bound_z)), attachment.Rigid)]

        self.transform_index = 1
        # TODO: These are remnants from the original code, for our purpose most sensors are not relevant
        # -> Move to globals or some config which should be used (also saves ressources)
        self.sensors = sensors if sensors else self.default_blueprints
        world = self._parent.get_world()
        bp_library = CarlaDataProvider._blueprint_library
        for i, item in enumerate(self.sensors):
            try:
                if item.actual_blueprint is not None:
                    continue
            except AttributeError: # not a named tuple
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
                self.sensors[i] = item._replace(actual_blueprint=blp) # update with actual blueprint added
            except AttributeError:
                self.sensors[i] = (item[0], item[1], item[2], blp)
        self.index = None

    def toggle_camera(self):
        """Activate a camera"""
        self.transform_index = (self.transform_index + 1) % len(self._camera_transforms)
        self.set_sensor(self.index, notify=False, force_respawn=True)

    def set_sensor(self, index, notify=True, force_respawn=False):
        """Set a sensor"""
        index = index % len(self.sensors)
        needs_respawn = True if self.index is None else (
                force_respawn or (self.sensors[index][0] != self.sensors[self.index][0]))
        if needs_respawn:
            if self.sensor is not None:
                self.destroy()
                self.surface = None
            self.sensor = CarlaDataProvider.get_world().spawn_actor(
                self.sensors[index][-1],
                self._camera_transforms[self.transform_index][0],
                attach_to=self._parent,
                attachment_type=self._camera_transforms[self.transform_index][1])

            # We need to pass the lambda a weak reference to
            # self to avoid circular reference.
            weak_self = weakref.ref(self)
            self.sensor.listen(lambda image: CameraManager._parse_image(weak_self, image))
        if notify:
            self.hud.notification(self.sensors[index][2])
        self.index = index

    def next_sensor(self):
        """Get the next sensor"""
        self.set_sensor(self.index + 1)

    def toggle_recording(self):
        """Toggle recording on or off"""
        self.recording = not self.recording
        self.hud.notification('Recording %s' % ('On' if self.recording else 'Off'))

    def destroy(self):
        super().destroy()
        self.index = None
        self.surface = None

    def render(self, display):
        """Render method"""
        if self.surface is not None:
            display.blit(self.surface, (0, 0))

    @staticmethod
    def _parse_image(weak_self: "weakref.ref[CameraManager]", image:carla.Image):
        self = weak_self()
        if not self:
            return
        if self.sensors[self.index][0].startswith('sensor.lidar'):
            points = np.frombuffer(image.raw_data, dtype=np.dtype('f4'))
            points = np.reshape(points, (int(points.shape[0] / 4), 4))
            lidar_data = np.array(points[:, :2])
            lidar_data *= min(self.hud.dim) / 100.0
            lidar_data += (0.5 * self.hud.dim[0], 0.5 * self.hud.dim[1])
            lidar_data = np.fabs(lidar_data)  # pylint: disable=assignment-from-no-return
            lidar_data = lidar_data.astype(np.int32)
            lidar_data = np.reshape(lidar_data, (-1, 2))
            lidar_img_size = (self.hud.dim[0], self.hud.dim[1], 3)
            lidar_img = np.zeros(lidar_img_size)
            lidar_img[tuple(lidar_data.T)] = (255, 255, 255)
            self.surface = pygame.surfarray.make_surface(lidar_img)
        else:
            image.convert(self.sensors[self.index][1]) # apply color converter
            array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
            array = np.reshape(array, (image.height, image.width, 4))
            array = array[:, :, :3]
            array = array[:, :, ::-1]
            self.surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
        if self.recording and (
                (image.frame % self._frame_interval) == 0
                or self.current_frame + self._frame_interval < image.frame):
            print("Saving image to disk", self.outpath % image.frame)
            image.save_to_disk(self.outpath % image.frame)
        self.current_frame = image.frame


def follow_car(ego_vehicle : carla.Actor):
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
    vehicle_transform = ego_vehicle.get_transform()
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


# TODO: # CRITICAL: this does not allow thread.join!
# Solutions see: https://stackoverflow.com/questions/69107143/how-to-end-a-while-loop-in-another-thread
def camera_function(ego_vehicle : carla.Actor):
    while True:
        follow_car(ego_vehicle)
