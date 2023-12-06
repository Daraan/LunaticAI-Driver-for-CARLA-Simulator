import asyncio

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
#                     street_type = "On highway"
#                 else:
#                     street_type = "Non highway street"
#                 matrix = create_city_matrix(ego_location, road_lane_ids, world_map)
#
#                 if matrix:
#                     matrix, _ = detect_surronding_cars(
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
