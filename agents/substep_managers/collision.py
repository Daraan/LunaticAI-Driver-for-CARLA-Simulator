import carla


"""
carla.CollisionEvent

Inherited from carla.SensorData
    frame
    timestamp
    transform

Class that defines a collision data for sensor.other.collision. The sensor creates one of these for every collision detected. Each collision sensor produces one collision event per collision per frame. Multiple collision events may be produced in a single frame by collisions with multiple other actors. Learn more about this here.
Instance Variables

    actor (carla.Actor)
    The actor the sensor is attached to, the one that measured the collision.
    other_actor (carla.Actor)
    The second actor involved in the collision.
    normal_impulse (carla.Vector3D - N*s)
    Normal impulse resulting of the collision.
"""

from typing_extensions import TYPE_CHECKING
if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent

PRINTED_WARNING = False

def collision_manager(self : "LunaticAgent", event: carla.CollisionEvent):
    """
    What to do in case of a collision
    """
    global PRINTED_WARNING
    if not PRINTED_WARNING:
        PRINTED_WARNING = True
        print("WARNING: Collision manager not implemented yet!")
        print("Collision detected!", event, "during", self.current_phase)
