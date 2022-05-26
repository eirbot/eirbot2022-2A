import logging
import math
import time

from RPi import GPIO

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
    rob.move(155)
    time.sleep(1)
    rob.go_angle(300)
    time.sleep(1)
    rob.arm.inverted_nazi(True)
    rob.move(470)
    time.sleep(1)
    time.sleep(1)
    rob.go_angle(400)
    time.sleep(1)
    rob.arm.inverted_nazi(False)
    time.sleep(1)
    rob.go_angle(180)
    rob.move(470)
    rob.go_angle(90)
    rob.move(105)

# #Tests
#     rob.move(500, 0)
#     time.sleep(3)
#     rob.arm.inverted_nazi(True)
#     time.sleep(3)
#     rob.arm.inverted_nazi(False)
#     time.sleep(3)
#     rob.go_angle(360)


# # Homologation v1
#
#     if rob.side == "YELLOW":
#         rob.move(105)
#         time.sleep(1)
#         rob.go_angle(90)
#         time.sleep(1)
#         rob.move(470)
#         time.sleep(1)
#         rob.arm.inverted_nazi(True)
#         time.sleep(1)
#         rob.go_angle(360)
#         time.sleep(1)
#         rob.arm.inverted_nazi(False)
#         # rob.go_angle(180)
#         # rob.move(470)
#         # rob.go_angle(270)
#         # rob.move(105)
#
#     else:
#         rob.move(105)
#         time.sleep(1)
#         rob.go_angle(270)
#         time.sleep(1)
#         rob.move(470)
#         time.sleep(1)
#         rob.arm.inverted_nazi(True)
#         time.sleep(1)
#         rob.go_angle(360)
#         time.sleep(1)
#         rob.arm.inverted_nazi(False)
#         time.sleep(1)
#         # rob.go_angle(180)
#         # rob.move(470)
#         # rob.go_angle(90)
#         # rob.move(105)


# Strat v1
    # rob.move(105)
    # rob.go_angle(90)
    # rob.move(470)
    # rob.arm.inverted_nazi(True)
    # rob.go_angle(360)
    # rob.arm.inverted_nazi(False)
    # rob.move(-470)
    # rob.go_angle(90)
    # rob.move(105)


