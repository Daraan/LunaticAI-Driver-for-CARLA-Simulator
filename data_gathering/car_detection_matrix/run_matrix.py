import matplotlib
matplotlib.use('Agg')

import threading
import time
from typing import Dict, List, TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Literal # For Python 3.8

import asyncio
import threading
import time

import numpy as np
import matplotlib.backends.backend_agg as agg
import pylab

import carla
import pygame

from data_gathering.car_detection_matrix.informationUtils import get_all_road_lane_ids
from data_gathering.car_detection_matrix.matrix_wrap import wrap_matrix_functionalities

from launch_tools import CarlaDataProvider

async def matrix_function(ego_vehicle, world, world_map, road_lane_ids, result_queue):
    while True:
        matrix = wrap_matrix_functionalities(ego_vehicle, world, world_map, road_lane_ids)
        # Put the matrix into the queue for access outside the thread
        await result_queue.put(matrix)
        await asyncio.sleep(1)

class DataMatrix:
    def __init__(self, ego_vehicle : carla.Actor, world : carla.World, road_lane_ids=None):
        self.ego_vehicle = ego_vehicle
        self.world = world
        self.world_map = CarlaDataProvider.get_map()
        self.road_lane_ids = road_lane_ids or get_all_road_lane_ids(world_map=CarlaDataProvider._map)
        self.matrix : Dict[int, List[int]] = None
        self.running = True
        self._sync = True

    def _calculate_update(self):
        return wrap_matrix_functionalities(self.ego_vehicle, self.world, self.world_map,
                                                         self.road_lane_ids)
    
    def update(self):
        if self.running:
            self.matrix = self._calculate_update()
            return self.matrix

    def getMatrix(self):
        return self.matrix

    def start(self):
        self.running = True

    def stop(self):
        self.running = False
         
    def __del__(self):
        if self.running:
            self.stop()
        
    def to_list(self):
        if self.matrix is None:
            return None
        return list(self.matrix.values())
    
    def to_numpy(self):
        if self.matrix is None:
            return None
        return np.array(self.to_list())  
    
    def render(self, display : pygame.Surface, 
               imshow_settings={'cmap':'jet'},
               vertical=True, 
               values=True,
               text_settings={'color':'orange'},
               *,
               draw=True):
        if self.matrix is None or not draw:
            return
        ax : pylab.Axes
        fig, ax = pylab.subplots(figsize=(2, 2), dpi=100)
        matrix = self.to_numpy() # lanes are horizontal, OneLane: left to right, Left Lane at the top.
        if vertical:
            matrix = np.rot90(matrix) # 1st/3rd perspective
        ax.imshow(matrix, **imshow_settings)
        if values:
            for (i, j), val in np.ndenumerate(matrix):
                ax.text(j, i, val, ha='center', va='center', **text_settings)
        ax.axis('off')
        fig.tight_layout(pad=0)
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        
        size = canvas.get_width_height()
        #size = (size[0] //2, size[1] // 2)
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        
        display.blit(surf, (220, display.get_height() - surf.get_height()- 40 ))
        pylab.close(fig)

    @property
    def sync(self):
        return self._sync

class AsyncDataMatrix(DataMatrix):
    def __init__(self, ego_vehicle : carla.Actor, world : carla.World, road_lane_ids=None, *, sleep_time=0.1):
        super().__init__(ego_vehicle, world, road_lane_ids)
        self._sync = False
        self.sleep_time = sleep_time
        self.lock = threading.Lock()
        self.worker_thread = threading.Thread(target=self._worker)
        
    # TODO: add signal handler to interrupt the thread faster
    
    def update(self):
        NotImplemented

    def _worker(self):
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
            time.sleep(self.sleep_time)

    def getMatrix(self):
        with self.lock:
            return self.matrix

    def start(self):
        self.running = True
        self.worker_thread.start() # NOTE: This does not allow restart

    def stop(self):
        self.running = False
        try:
            from agents.tools.logging import logger
            if self.worker_thread.is_alive():
                self.worker_thread.join()
            else:
                logger.info("DataMatrix.stop called multiple times.")
        except ImportError:
            print("Cannot import logger from agents.tools.logging. Stopping data matrix.")
            self.worker_thread.join()
