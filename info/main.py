import logging
import math
import os
import pty
import time

from robot_manager import RobotManager

# _x = 600
# _y = 160
# _theta = 90

# def move_position(distance):
#     global _x
#     global _y
#     global _theta
#     _y += distance * math.sin(math.radians(_theta))
#     _x += distance * math.cos(math.radians(_theta))

# def move_angle(angle):
#     global _theta

#     _theta += angle
#     _theta = _theta % 360

#     # if (_theta >180):
#     #    _theta = 180 - _theta


if __name__ == "__main__":
    rob = RobotManager(log_level=logging.DEBUG)
    rob.wait_until_start()

    rob.move(500, 0)
    time.sleep(3)
    rob.arm.inverted_nazi(True)
    time.sleep(3)
    rob.arm.inverted_nazi(False)
    time.sleep(3)
    rob.go_angle(360)


# Homologation v1

    # if rob.side == "YELLOW" :
    #     rob.move(210, 0)
    #     rob.go_angle(90)
    #     rob.move(940)
    #     rob.arm.inverted_nazi(True)
    #     rob.go_angle(360)
    #     rob.arm.inverted_nazi(False)

    # else :
    #     rob.move(210, 0)
    #     rob.go_angle(-90)
    #     rob.move(940)
    #     rob.arm.inverted_nazi(True)
    #     rob.go_angle(360)
    #     rob.arm.inverted_nazi(False)


# Strat v1 :  dégager la statuette + revenir
    # rob.move(210, 0)
    # rob.go_angle(90)
    # rob.move(940)
    # rob.arm.inverted_nazi(True)
    # rob.go_angle(360)
    # rob.arm.inverted_nazi(False)
    # rob.move(-940)
    # rob.go_angle(90)
    # rob.move(210)


# Strat v2 : dégager la statuette + revenir avec palets
    # rob.move(210, 0)
    # rob.go_angle(90)
    # rob.move(940)
    # rob.arm.inverted_nazi(True)
    # rob.go_angle(360)
    # rob.arm.inverted_nazi(False)
    # rob.go_angle(95)
    # rob.move(-1080)
    # rob.go_angle(95)
    # rob.move(-1080)
    # rob.go_angle(33)
    # rob.move(1650)


