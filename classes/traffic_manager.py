class TrafficManager:
    tm = None

    def __init__(self, client, actor, *,
                 speed_limit_scale,
                 min_front_distance,
                 seed=1):
        # TODO use a settings file
        if True or TrafficManager.tm is None:
            # TrafficManager.tm : carla.TrafficManager =\
            self.tm = client.get_trafficmanager()
            # TrafficManager.tm.set_random_device_seed(seed)
            self.tm.set_random_device_seed(seed)
        self.min_front_distance = min_front_distance
        self.speed_limit_scale: float = speed_limit_scale
        self.actor = actor

    def init_lunatic_driver(self):
        self.tm.auto_lane_change(self.actor, False)
        self.tm.distance_to_leading_vehicle(self.actor, (self.min_front_distance - 1) % 10 + 0.5)
        self.tm.vehicle_percentage_speed_difference(self.actor, self.speed_limit_scale)
        self.tm.keep_right_rule_percentage(self.actor, 0)
        self.tm.random_right_lanechange_percentage(self.actor, 0)
        self.tm.random_left_lanechange_percentage(self.actor, 0)
        self.tm.ignore_vehicles_percentage(self.actor, 40)
        self.tm.ignore_lights_percentage(self.actor, 100)

    def init_passive_driver(self):
        self.tm.auto_lane_change(self.actor, False)
        self.tm.random_right_lanechange_percentage(self.actor, 0)
        self.tm.random_left_lanechange_percentage(self.actor, 0)
        self.tm.vehicle_percentage_speed_difference(self.actor, self.speed_limit_scale)
        self.tm.distance_to_leading_vehicle(self.actor, self.min_front_distance)
        self.tm.ignore_lights_percentage(self.actor, 100)
        self.actor.set_autopilot(True)

    def force_overtake(self, speed, overtake_direction):
        self.force_lane_change(right=overtake_direction == 1)
        # self.actor.setThrottle(speed)

    def force_lane_change(self, right=False):
        self.tm.force_lane_change(self.actor, right)

    def start_drive(self):
        self.actor.set_autopilot(True)
