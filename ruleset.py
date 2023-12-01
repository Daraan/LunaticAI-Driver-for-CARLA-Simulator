import random

from classes.driver import Driver
from classes.rule import Rule
from utils.logging import log


def go_crazy(driver: Driver):
    driver.vehicle.actor.set_autopilot(False)
    driver.vehicle.setThrottle(200)
    log("Crazy")


class Ruleset:
    def __init__(self, driver, matrix):
        self.ruleset = []
        self.driver = driver
        self.matrix = matrix
        # Go Crazy
        self.ruleset.append(
            Rule(random.randint(0, 100) <= driver.ignore_obstacle_chance, go_crazy)
        )