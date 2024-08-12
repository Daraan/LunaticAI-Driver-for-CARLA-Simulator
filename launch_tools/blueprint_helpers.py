from typing import List, Optional, Tuple, TYPE_CHECKING

from launch_tools import CarlaDataProvider, Literal

if TYPE_CHECKING:
    import carla


create_blueprint = CarlaDataProvider.create_blueprint

def get_blueprint_library(world: Optional["carla.World"]=None):
    """
    Get the blueprint library of the given world.
    
    .. deprecated:: 
        Consider using :py:attr:`.CarlaDataProvider._blueprint_library` 
        or :py:meth:`.CarlaDataProvider.create_blueprint` instead.
    """
    if CarlaDataProvider._blueprint_library:
        return CarlaDataProvider._blueprint_library
    elif world is None:
        world = CarlaDataProvider.get_world()
    return world.get_blueprint_library()

def get_contrasting_blueprints(world: "carla.World", ego_vehicle="vehicle.lincoln.mkz_2020", ego_color: str="255,0,0") \
    -> Tuple["carla.ActorBlueprint", "carla.ActorBlueprint"]:
    """
    Sets the color of NPC vehicles and marks the ego vehicle red.

    Parameters:
    world : carla.World
        The world object.
    ego_vehicle : str, optional
        The name of the ego vehicle, by default "vehicle.lincoln.mkz_2020"
    ego_color : str, optional
        The color of the ego vehicle in RGB format, by default "255,0,0"

    Returns:
    tuple
        A tuple containing the ego vehicle blueprint and the NPC vehicle blueprint.
    """
    blueprint_library: carla.BlueprintLibrary = get_blueprint_library()
    car_blueprint = blueprint_library.filter('vehicle')[0]

    if car_blueprint.has_attribute('color'):
        color = car_blueprint.get_attribute('color').recommended_values[-1]
        car_blueprint.set_attribute('color', color)

    ego_bp = blueprint_library.find(ego_vehicle)
    if ego_bp.has_attribute('color'):
        color = ego_bp.get_attribute('color').recommended_values[0]
        ego_bp.set_attribute('color', ego_color)

    ego_bp.set_attribute('role_name', 'hero')
    return ego_bp, car_blueprint


def get_actor_blueprints(world: "carla.World", filter: str,
                         generation: "Literal[1, 2, 'all']") -> List["carla.ActorBlueprint"]:
    """
    Returns a list of actor blueprints filtered by the given filter and generation.

    Args:
        world : The world to get the blueprints from.
        filter : The filter to apply to the blueprints.
        generation : The generation of the blueprints to return. Can be "all", "1", or "2".

    Returns:
        List of carla.ActorBlueprint: The list of actor blueprints that match the given filter and generation.
    """
    bps = get_blueprint_library().filter(filter)

    if isinstance(generation, str) and generation.lower() == "all":
        return bps

    # If the filter returns only one bp, we assume that this one needed
    # and therefore, we ignore the generation
    if len(bps) == 1:
        return bps

    try:
        int_generation = int(generation)
        # Check if generation is in available generations
        if int_generation in [1, 2]:
            bps = [x for x in bps if int(x.get_attribute('generation')) == int_generation]
            return bps
        else:
            print("   Warning! Actor Generation is not valid. No actor will be spawned.")
            return []
    except Exception:
        print("   Warning! Actor Generation is not valid. No actor will be spawned.")
        return []
