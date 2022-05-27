import logging
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
    rob = RobotManager(log_level=logging.DEBUG, sensors=False)
    rob.wait_until_start()
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

    # # Strat v1 :  dégager la statuette + revenir
    if rob.side == "YELLOW":
        rob.move(400, 0)
        time.sleep(1)
        rob.go_angle(90)
        time.sleep(1)
        rob.move(660)
        time.sleep(1)
        rob.go_angle(60)
        time.sleep(1)
        rob.arm.inverted_nazi()
        rob.move(400)
        time.sleep(1)
        rob.move(-200)
        time.sleep(1)
        rob.go_angle(-160)
        rob.arm.base_position()
        time.sleep(1)
        rob.move(400)
        time.sleep(1)
        rob.go_angle(-20)
        time.sleep(1)
        rob.move(550)
        time.sleep(1)
        rob.go_angle(-90)
        time.sleep(1)
        rob.move(330)

    if rob.side == "PURPLE":
        logging.error("PURPLE")
        rob.move(400, 0)
        time.sleep(1)
        rob.go_angle(80)
        time.sleep(1)
        rob.move(660)
        time.sleep(1)
        rob.go_angle(20)
        time.sleep(1)
        rob.arm.inverted_nazi()
        rob.move(330)
        time.sleep(1)
        rob.move(-200)
        rob.go_angle(-90)
        time.sleep(1)
        rob.go_angle(-80)
        rob.arm.base_position()
        time.sleep(1)
        rob.move(400)
        time.sleep(1)
        rob.go_angle(-80)
        time.sleep(1)
        rob.move(650)
        time.sleep(1)
        rob.go_angle(-80)
        time.sleep(1)
        rob.move(430)

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


# # Strat v3 : dégager la statuette + revenir avec palets
# # JAUNE
#     rob.move(350)
#     rob.go_angle(90)
#     rob.move(800)
#     rob.go_angle(45)
#     rob.move(200)
#
#     ## Action avec la statuette
#
#     #positon_bras_statuette
#     #rob.suc(True)
#     #position_bras_haute
#
#     ## OU
#
#     rob.arm.inverted_nazi(True)
#     rob.go_angle(360)
#     rob.arm.inverted_nazi(False)
#
#     ## Fin action avec la statuette
#
#     rob.move(-50)
#
#     # Si replique
#     #rob.go_angle(-90)
#     #activer_bras_replique
#     #rob.go_angle(-145)
#
#     # Sinon
#     #rob.go_angle(-235)
#
#
#     rob.move(-1375)
#     rob.go_angle(10)
#
#     #déposer statuette
#
#     rob.move(-550)
#
#     #BONUS DE L'AMBIANCE
#
#     rob.move(-300)
#     rob.inverted_nazi(True)
#     rob.go_angle(-360)
#     rob.move(300)
