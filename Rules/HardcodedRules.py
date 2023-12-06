import random
import time


def go_crazy(driver, matrix, i_car, j_car, tm, chances=1000):
    disable_collision = random.randint(1, chances)
    if disable_collision <= driver.ignore_obstacle_chance:
        driver.vehicle.actor.set_autopilot(False)
        driver.vehicle.setThrottle(20)
        print("Crazy")
        time.sleep(1)
        driver.vehicle.actor.set_autopilot(True)
        driver.vehicle.setThrottle(0)
        print("Crazy over")
        return True


def brake_check(driver, matrix, i_car, j_car, tm, chances=100):
    brake_check_choice = random.randint(1, chances)
    if (brake_check_choice <= driver.brake_check_chance
            and (matrix[i_car][j_car - 1] == 2)):
        driver.vehicle.actor.set_autopilot(False)
        driver.vehicle.setThrottle(0)
        driver.vehicle.setBrake(10)
        time.sleep(1.0)
        print("Brake check")
        driver.vehicle.setBrake(0)
        driver.vehicle.actor.set_autopilot(True)
        return True


def overtake_logic(driver, matrix, i_car, j_car, tm, chances=100):
    overtake_direction = 0
    if matrix[i_car + 1][j_car + 1] == 0:
        # print("can overtake on right")
        overtake_direction = 1
    if matrix[i_car - 1][j_car + 1] == 0:
        # print("can overtake on left")
        overtake_direction = -1

    # Overtake logic
    if matrix[i_car][j_car + 1] == 2 or matrix[i_car][j_car + 2] == 2:
        overtake_choice = random.randint(1, chances)
        if overtake_choice >= driver.overtake_mistake_chance:
            tm.force_overtake(100, overtake_direction)
            print("overtake!")
            return True
        else:
            print("overtake averted by chance")


def brake_logic(driver, matrix, i_car, j_car, tm):
    if matrix[i_car][j_car + 1] == 2:
        driver.vehicle.setBrake(4)
        return True


def random_lane_change(driver, matrix, i_car, j_car, tm, chances=100):
    overtake_choice = random.randint(1, chances)
    if overtake_choice <= driver.risky_overtake_chance:
        if matrix[i_car + 1][j_car + 1] == 3 and matrix[i_car - 1][j_car + 1] == 3:
            return False
        elif matrix[i_car + 1][j_car + 1] == 3:
            tm.force_overtake(100, -1)
        elif matrix[i_car - 1][j_car + 1] == 3:
            tm.force_overtake(100, 1)
        else:
            overtake_direction = random.choice([-1, 1])
            tm.force_overtake(100, overtake_direction)
        print("Random lane change")
        return True
