from __future__ import annotations

import signal
import threading
import time
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set

import carla
import matplotlib
import numpy as np
import pygame
import pylab
from typing_extensions import TypedDict

from agents.tools.logging import logger

#from classes.constants import StreetType
from data_gathering.car_detection_matrix.informationUtils import (
    RoadLaneId,
    check_ego_on_highway,
    create_city_matrix,
    detect_surrounding_cars,
    get_all_road_lane_ids,
)
from launch_tools import CarlaDataProvider

matplotlib.use('Agg')
import matplotlib.backends.backend_agg as agg

__all__ = [
    'DetectionMatrix',
    'AsyncDetectionMatrix',
    'wrap_matrix_functionalities',
]

def wrap_matrix_functionalities(ego_vehicle : carla.Actor,
                                world : carla.World,
                                world_map : carla.Map,
                                road_lane_ids: "set[RoadLaneId]",
                                radius: float =100.0,
                                highway_shape=None):
    """
    Parameters:
        ego_vehicle: The ego vehicle
        highway_shape (tuple): Tuple containing highway_type, number of straight highway lanes, entry waypoint tuple and/ exit waypoint tuple.
            Format: (highway_type: string, straight_lanes: int, entry_wps: ([wp,..], [wp,..]), exit_wps: ([wp,..], [wp,..]))
    """
    ego_location = ego_vehicle.get_location()
    #ego_waypoint = world_map.get_waypoint(ego_location)
    ego_on_highway = check_ego_on_highway(ego_location, road_lane_ids, world_map)

    #current_lanes = [rl_id[1] for rl_id in road_lane_ids if rl_id[0] == ego_waypoint.road_id]

    # Normal Road; TODO: Check if this is useful
    #if ego_on_highway:
    #    street_type = StreetType.ON_HIGHWAY
    #else:
    #    street_type = StreetType.NON_HIGHWAY_STREET
    
    # NOTE: in rare unsupported cases, the function will return None
    matrix = create_city_matrix(ego_location, road_lane_ids, world_map)

    if matrix:
        matrix, _ = detect_surrounding_cars(
            ego_location, ego_vehicle, matrix, road_lane_ids, world, radius, ego_on_highway, highway_shape
        )
    else:
        return None
    # Removes the information about "left_outer_lane" by replacing it with numeric values.
    # TODO: Should possibly revert this.
    new_matrix = dict(enumerate(matrix.values()))
    matrix = new_matrix
    return matrix


class DetectionMatrix:
    """Create a matrix representing the lanes around the ego vehicle."""
    
    matrix : Dict[int, List[int]]
    """
    A :py:class:`collections.OrderedDict`: An ordered dictionary representing the city matrix. The keys for existing lanes are the lane IDs in the format "road_id_lane_id".
    For non-existing lanes different placeholder exist, e.g.  left_outer_lane, left_inner_lane, No_4th_lane, No_opposing_direction
    The values indicate whether a vehicle is present: 0 - No vehicle, 1 - Ego vehicle, 3 - No road.
    Format example:
    
    .. code-block:: python
        
        {
            "left_outer_lane": [3, 3, 3, 3, 3, 3, 3, 3],
            "left_inner_lane": [3, 3, 3, 3, 3, 3, 3, 3],
            "1_2": [0, 0, 0, 0, 0, 0, 0, 0],
            "1_1": [0, 0, 0, 0, 0, 0, 0, 0],
            "1_-1": [0, 0, 0, 0, 0, 0, 0, 0],
            "1_-2": [0, 0, 0, 0, 0, 0, 0, 0],
            "right_inner_lane": [3, 3, 3, 3, 3, 3, 3, 3],
            "right_outer_lane": [3, 3, 3, 3, 3, 3, 3, 3],
        }
            
    Attention:
        Currently the keys are replaces by numbers.
    """
    
    def __init__(self, ego_vehicle : carla.Actor, road_lane_ids: Optional[Set[RoadLaneId]]=None):
        self._ego_vehicle = ego_vehicle
        self._world = CarlaDataProvider.get_world()
        self._world_map = CarlaDataProvider.get_map()
        self.running = True
        """If the matrix will perform updates."""
        self._sync = True
        self._road_lane_ids = road_lane_ids or get_all_road_lane_ids(CarlaDataProvider._map)
        """A set containing unique road and lane identifiers in the format "roadId_laneId"."""
        self.matrix = None  # type: ignore[assignment]
        self._add_signal_handler()

    def _calculate_update(self):
        return wrap_matrix_functionalities(self._ego_vehicle, self._world, self._world_map,
                                                         self._road_lane_ids)
    
    def update(self) -> "Dict[int, List[int]] | None":
        """
        If the matrix is :py:attr:`running`, it will update the matrix and return it,
        otherwise returns :python:`None`.
        """
        if self.running:
            self.matrix = self._calculate_update()
            return self.matrix

    def getMatrix(self) -> Dict[int, List[int]]:
        return self.matrix
        
    def to_list(self) -> "None | list[list[int]]":
        """
        Returns the values of :py:attr:`matrix` as a list.
        """
        if self.matrix is None:
            return None
        return list(self.matrix.values())
    
    def to_numpy(self) -> "None | np.ndarray[int, Any]":
        """
        Returns the values of :py:attr:`matrix` as a numpy array.
        """
        if self.matrix is None:
            return None
        return np.array(self.to_list())
    
    if TYPE_CHECKING:
        class RenderOptions(TypedDict, total=False, closed=True):
            """Signature for :py:meth:`.DetectionMatrix.render`."""
            imshow_settings: dict[str, Any]
            vertical : bool
            draw_values : bool
            text_settings : dict[str, Any]
            draw : bool
    
    def render(self,
               display: pygame.Surface,
               imshow_settings: dict[str, Any]={'cmap':'jet'},  # noqa: B006
               vertical: bool=True,
               draw_values: bool=True,
               text_settings: dict[str, Any]={'color':'orange'},  # noqa: B006
               *,
               draw: bool=True):
        """
        Renders the matrix on the given surface.
        
        :meta private:
        """
        if not draw:
            return
        matrix = self.to_numpy() # lanes are horizontal, OneLane: left to right, Left Lane at the top.
        if matrix is None:
            return
        ax : pylab.Axes
        fig, ax = pylab.subplots(figsize=(2, 2), dpi=100)
        if vertical:
            matrix = np.rot90(matrix) # 1st/3rd perspective
        ax.imshow(matrix, **imshow_settings)
        if draw_values:
            for (i, j), val in np.ndenumerate(matrix):
                ax.text(j, i, val, ha='center', va='center', **text_settings)
        ax.axis('off')
        fig.tight_layout(pad=0)
        
        canvas: agg.FigureCanvasAgg = fig.canvas  # type: ignore[assignment]
        canvas.draw()
        buffer_data : memoryview = canvas.buffer_rgba()
        
        size = canvas.get_width_height()
        surf = pygame.image.frombuffer(buffer_data, size, "RGBA")
        
        display.blit(surf, (220, display.get_height() - surf.get_height()- 40 ))
        pylab.close(fig)

    @property
    def sync(self):
        """
        Weather the matrix is synchronous or not.
        
        :meta private:
        """
        return self._sync
    
    def start(self):
        """Allows the matrix to update."""
        self.running = True

    def stop(self):
        """Prevents the matrix from updating."""
        self.running = False
        self.matrix = None # prevent rendering # type: ignore[assignment]
         
    def __del__(self):
        if self.running:
            try:
                self.stop()
            except Exception:
                pass

    def _signal_handler(self, signum: int, _):
        """
        Signal handler for stopping the simulation, e.g. when pressing Ctrl+C
        in the terminal.
        
        Calls :py:meth:`.stop`.
        
        :meta private:
        """
        from classes.keyboard_controls import RSSKeyboardControl
        logger.info(f"DetectionMatrix: signal {signum} received. Stopping.")
        self.stop()
        # Can only have one signal handler!
        RSSKeyboardControl._signal_handler(signum, _) 
        
    def _add_signal_handler(self):
        """
        Adds the signal handler for stopping the simulation.
        
        :meta private:
        """
        signal.signal(signal.SIGINT, self._signal_handler)

class AsyncDetectionMatrix(DetectionMatrix):
    def __init__(self, ego_vehicle : carla.Actor, *, road_lane_ids=None, sleep_time=0.1):
        """
        Asynchronous version of the :py:class:`DetectionMatrix`.
        
        Will calculate the matrix update in a separate thread.
        """
        super().__init__(ego_vehicle, road_lane_ids)
        self._sync = False
        self.sleep_time = sleep_time
        self.lock = threading.Lock()
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        
    # TODO: add signal handler to interrupt the thread faster
    
    def update(self) -> None:
        """Not available in the async version."""

    def _worker(self) -> None:
        while self.running:
            try:
                new_matrix = self._calculate_update()
                with self.lock:
                    self.matrix = new_matrix
            except (RuntimeError, OSError) as e:
                print(f"Error in matrix calculation: {e}")
                raise
            except Exception as e:
                print(f"Error in matrix calculation: {e}")
            if self.sleep_time:
                time.sleep(self.sleep_time)

    def getMatrix(self):
        with self.lock:
            return self.matrix

    def start(self):
        self.running = True
        self.worker_thread.start() # NOTE: This does not allow restart

    def stop(self, timeout: float | None=None):
        """
        See Also:
            :meth:`threading.Thread.join`
            
        Raises:
            RuntimeError: if **timeout** is not None and the thread is still alive after the time.
        """
        self.running = False
        if self.worker_thread.is_alive():
            self.worker_thread.join(timeout)
        else:
            from agents.tools.logging import logger
            logger.info("DetectionMatrix.stop called multiple times.")
        self.matrix = None # prevent rendering # type: ignore[assignment]
    
    def __del__(self):
        self.running = False
        try:
            self.worker_thread.join(3.0)
        except Exception:
            pass
        self.matrix = None  # type: ignore[assignment]


def get_car_coords(matrix) -> tuple[int, int]:
    """
    Position of the ego vehicle in the matrix.
    Should be a constant value for non-junctions.
    """
    (i_car, j_car) = (0, 0)
    for lane, occupations in matrix.items():
        try:
            return (lane, occupations.index(1)) # find the 1 entry in a efficient way
        except ValueError:
            continue

    return i_car, j_car
