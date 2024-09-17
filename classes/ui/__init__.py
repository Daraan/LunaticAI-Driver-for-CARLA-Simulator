"""
This package implements tools to allow the user to interact with the simulation.
This includes cameras, keyboard inputs, and the HUD.

Most features are only available from the :py:mod:`pygame` when using :py:attr:`.LaunchConfig.pygame`.
"""


# Solutions see: https://stackoverflow.com/questions/69107143/how-to-end-a-while-loop-in-another-thread
from threading import Event
import carla
from agents.tools import logger
from launch_tools import CarlaDataProvider

__all__ = [
    'spectator_follow_actor'
]

_follow_car_event = Event()
"""Use the :py:meth:`treading.Event.set` method to stop the thread."""


def spectator_follow_actor(actor: carla.Actor):
    """
    Continuously follow the ego vehicle with the spectator view.

    Attention:
        - Needs to be run in a separate thread.
        - Does not allow for thread.join() to stop the thread, before calling :py:meth:`stop`.

    Methods:
        stop: Stop following the actor.

    See Also:
        - :py:meth:`.CameraManager.follow_actor`
    """
    try:
        while not _follow_car_event.is_set():
            spectator_to_actor(actor)
    except Exception as e:
        logger.error(f"Error in spectator_follow_actor: {e}")


spectator_follow_actor.stop = lambda: _follow_car_event.set()  # type: ignore[attr-defined]


def spectator_to_actor(actor: carla.Actor) -> None:
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
