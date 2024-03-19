import matplotlib
matplotlib.use('Agg')

import threading
import time
from typing import Dict, List

import asyncio

import numpy as np
import matplotlib.backends.backend_agg as agg
import pylab

import carla
import pygame

from DataGathering.informationUtils import get_all_road_lane_ids
from DataGathering.matrix_wrap import wrap_matrix_functionalities


async def matrix_function(ego_vehicle, world, world_map, road_lane_ids, result_queue):
    while True:
        matrix = wrap_matrix_functionalities(ego_vehicle, world, world_map, road_lane_ids)
        # Put the matrix into the queue for access outside the thread
        await result_queue.put(matrix)
        await asyncio.sleep(1)

# class DataMatrix:
#     def __init__(self, agent, world):
#         self.world = world
#         self.agent = agent
#         self.matrix = None  # Initialize an empty matrix
#         self.streetType = None
#         self.worker_thread = threading.Thread(target=self._worker)
#         self.worker_thread.start()
#
#     def _worker(self):
#         # Define the radius to search for other vehicles
#         radius = 100
#
#         # Initialize speed of ego_vehicle to use as global variable
#         world_map = self.world.get_map()
#         self.world.tick()
#         highway_shape = None
#         road_lane_ids = get_all_road_lane_ids(world_map=self.world.get_map())
#         df = initialize_dataframe()
#         t_end = time.time() + 10
#         while time.time() < t_end:
#             try:
#                 ego_location = ego_vehicle.get_location()
#                 ego_waypoint = world_map.get_waypoint(ego_location)
#                 ego_on_highway = check_ego_on_highway(ego_location, road_lane_ids, world_map)
#
#                 current_lanes = []
#                 for id in road_lane_ids:
#                     if str(ego_waypoint.road_id) == id.split("_")[0]:
#                         current_lanes.append(int(id.split("_")[1]))
#
#                 # Normal Road
#                 if ego_on_highway:
#                     street_type = StreetType.ON_HIGHWAY
#                 else:
#                     street_type = StreetType.NON_HIGHWAY_STREET
#                 matrix = create_city_matrix(ego_location, road_lane_ids, world_map)
#
#                 if matrix:
#                     matrix, _ = detect_surrounding_cars(
#                         ego_location, ego_vehicle, matrix, road_lane_ids, self.world, radius, ego_on_highway,
#                         highway_shape
#                     )
#
#                 df = safe_data(ego_vehicle, matrix, street_type, df)
#
#                 self.streetType = street_type
#                 self.matrix = matrix
#                 time.sleep(0.5)
#                 self.world.tick()
#
#             except Exception as e:
#                 continue
#
#     def getMatrix(self):
#         return self.matrix
#
#     def getStreetType(self):
#         return self.streetType
#
#     def __del__(self):
#         self.worker_thread.join()


class DataMatrix:
    def __init__(self, ego_vehicle : carla.Actor, world : carla.World, world_map : carla.Map, road_lane_ids=None):
        self.ego_vehicle = ego_vehicle
        self.world = world
        self.world_map = world_map
        self.road_lane_ids = road_lane_ids or get_all_road_lane_ids(world_map=world_map)
        self.matrix : Dict[int, List[int]] = None
        self.running = True

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
        self.stop()
        
    def to_list(self):
        if self.matrix is None:
            return None
        return list(self.matrix.values())
    
    def to_numpy(self):
        if self.matrix is None:
            return None
        return np.array(self.to_list())  
    
    def render(self, display : pygame.Surface):
        if self.matrix is None:
            return
        ax : pylab.Axes
        fig, ax = pylab.subplots(figsize=(2, 2), dpi=100)
        ax.imshow(np.rot90(self.to_numpy()), cmap='jet')
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

        

class AsyncDataMatrix(DataMatrix):
    def __init__(self, ego_vehicle : carla.Actor, world : carla.World, world_map : carla.Map, road_lane_ids=None, *, sleep_time=0.1):
        super().__init__(ego_vehicle, world, world_map, road_lane_ids)
        self.sleep_time = sleep_time
        self.lock = threading.Lock()
        self.worker_thread = threading.Thread(target=self._worker)
    
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
                logger.debug("Joining DataMatrix thread")
                self.worker_thread.join()
            else:
                logger.debug("DataMatrix.stop called multiple times.")
        except ImportError:
            print("Cannot import logger from agents.tools.logging. Stopping data matrix.")
            self.worker_thread.join()

    def __del__(self):
        self.stop()
