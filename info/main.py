import logging
import math
import os
import pty
import time

from robot_manager import RobotManager

_x = 600
_y = 160
_theta = 90


def move_position(distance):
    global _x
    global _y
    global _theta
    _y += distance * math.sin(math.radians(_theta))
    _x += distance * math.cos(math.radians(_theta))


def move_angle(angle):
    global _theta

    _theta += angle
    _theta = _theta % 360

    # if (_theta >180):
    #    _theta = 180 - _theta


if __name__ == "__main__":
    rob = RobotManager(log_level=logging.DEBUG)
    rob.wait_until_start()
    rob.go_speed()
    rob.move(0, 0)
