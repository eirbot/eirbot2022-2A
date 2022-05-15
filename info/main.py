import logging
import math
import os
import pty

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
    rob.move(1000)
    move_position(1000)
    # print(_x,_y, _theta)

    rob.go_angle(270)
    move_angle(270)

    rob.move(400)
    move_position(400)
    # print(_x,_y, _theta)

    rob.go_angle(315)
    move_angle(315)

    rob.move(1054)
    move_position(1054)
    # print(_x,_y, _theta)

    rob.arm.move_arm("home")
    rob.suc(1)
    rob.arm.move_arm("home")

    print(_x, _y, _theta)
