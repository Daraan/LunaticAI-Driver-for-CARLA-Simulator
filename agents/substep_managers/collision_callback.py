from typing import TYPE_CHECKING

import carla

if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent

PRINTED_WARNING = False


def collision_manager(self: "LunaticAgent", event: carla.CollisionEvent) -> None:
    """
    What to do in case of a collision
    
    Callback function for the collision event.
    
    Attention:
        This function currently is not yet implemented.
    """
    global PRINTED_WARNING
    if not PRINTED_WARNING:
        PRINTED_WARNING = True
        print("WARNING: Collision manager not implemented yet! Please handle collision in Phase.COLLISION")
        print("Collision detected!", event, "during", self.current_phase)
