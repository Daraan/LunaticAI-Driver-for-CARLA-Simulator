import re
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    import carla
    try:
        from typing import Literal  # python 3.8+
    except ImportError:
        try:
            from typing_extensions import Literal
        except ImportError:
            pass

import carla


def get_contrasting_blueprints(world : carla.World, ego_vehicle="vehicle.lincoln.mkz_2020", ego_color="255,0,0") -> Tuple[
    carla.ActorBlueprint, carla.ActorBlueprint]:
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
    blueprint_library = world.get_blueprint_library()
    car_blueprint = blueprint_library.filter('vehicle')[0]

    if car_blueprint.has_attribute('color'):
        color = car_blueprint.get_attribute('color').recommended_values[-1]
        car_blueprint.set_attribute('color', color)

    ego_bp = world.get_blueprint_library().find(ego_vehicle)
    if ego_bp.has_attribute('color'):
        color = ego_bp.get_attribute('color').recommended_values[0]
        ego_bp.set_attribute('color', ego_color)

    ego_bp.set_attribute('role_name', 'hero')
    return ego_bp, car_blueprint


def get_actor_blueprints(world: carla.World, filter: str,
                         generation: "Literal[1, 2, 'all']") -> List[
    carla.ActorBlueprint]:
    """
    Returns a list of actor blueprints filtered by the given filter and generation.

    Args:
        world (carla.World): The world to get the blueprints from.
        filter (str): The filter to apply to the blueprints.
        generation (str): The generation of the blueprints to return. Can be "all", "1", or "2".

    Returns:
        List of carla.ActorBlueprint: The list of actor blueprints that match the given filter and generation.
    """
    bps = world.get_blueprint_library().filter(filter)

    if generation.lower() == "all":
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
    except:
        print("   Warning! Actor Generation is not valid. No actor will be spawned.")
        return []


def find_weather_presets():
    """Method to find weather presets"""
    rgx = re.compile('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)')

    def name(x): return ' '.join(m.group(0) for m in rgx.finditer(x))

    presets = [x for x in dir(carla.WeatherParameters) if re.match('[A-Z].+', x)]
    return [(getattr(carla.WeatherParameters, x), name(x)) for x in presets]
