import asyncio
import threading
import time

from DataGathering.matrix_wrap import wrap_matrix_functionalities


async def matrix_function(ego_vehicle, world, world_map, road_lane_ids, result_queue):
    while True:
        matrix = wrap_matrix_functionalities(ego_vehicle, world, world_map, road_lane_ids)
        # Put the matrix into the queue for access outside the thread
        await result_queue.put(matrix)
        await asyncio.sleep(1)


class DataMatrix:
    def __init__(self, ego_vehicle, world, world_map, road_lane_ids):
        self.ego_vehicle = ego_vehicle
        self.world = world
        self.world_map = world_map
        self.road_lane_ids = road_lane_ids
        self.matrix = None
        self.running = True
        self.lock = threading.Lock()
        self.worker_thread = threading.Thread(target=self._worker)
        self.worker_thread.start()

    def _worker(self):
        while self.running:
            try:
                new_matrix = wrap_matrix_functionalities(self.ego_vehicle, self.world, self.world_map,
                                                         self.road_lane_ids)
                with self.lock:
                    self.matrix = new_matrix
            except Exception as e:
                print(f"Error in matrix calculation: {e}")
            time.sleep(0.1)

    def getMatrix(self):
        with self.lock:
            return self.matrix

    def stop(self):
        self.running = False
        self.worker_thread.join()

    def __del__(self):
        self.stop()
