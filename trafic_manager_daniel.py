import carla


class TrafficManagerD:

    def __init__(self, client, actor, *,
                 speed_limit_scale=1.3,
                 min_front_distance=0,
                 seed=0):
        # TODO use a settings file
        self.tm : carla.TrafficManager = client.get_trafficmanager()
        self.tm.set_random_device_seed(seed)
        self.min_front_distance=min_front_distance
        self.speed_limit_scale : float = speed_limit_scale
        self.actor = actor
        self.init_lunatic_driver()

    def init_lunatic_driver(self):
        self.tm.auto_lane_change(self.actor, False)
        self.tm.distance_to_leading_vehicle(self.actor, self.min_front_distance)
        self.tm.vehicle_percentage_speed_difference(self.actor, 100 * self.speed_limit_scale)
        self.tm.keep_right_rule_percentage(self.actor, 0)
        self.tm.random_right_lanechange_percentage(self.actor, 20)
        self.tm.random_left_lanechange_percentage(self.actor, 60)

    def force_overtake(self, speed):
        self.force_lane_change(right=False)
        self.actor.setThrottle(7)


    def force_lane_change(self, right=False):
        self.tm.force_lane_change(self.actor, right)










def init_driver(tm : carla.TrafficManager, actor):



