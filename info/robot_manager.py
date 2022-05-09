#! /usr/bin/env python3
import serial

from . import arm_manager


class RobotManager:
    def __init__(self, simulation: bool = False, baudrate: int = 9600, port: str = "/dev/ttyACM0"):
        self.simulation: bool = simulation

        self.usb: str = port
        self.baudrate: int = baudrate
        if not self.simulation:
            self.ser = serial.Serial(self.usb, self.baudrate)
        self.GPIO: dict[str, int] = {"buldozer": 5,
                                     "display": 6,
                                     "limit_switch_forward": 13,
                                     "limit_switch_backward": 26,
                                     "start": 18,
                                     "side": 23,
                                     "gp2_forward": 24,
                                     "gp2_backward": 25,
                                     "showcase": 12,
                                     }
        self.start: bool = False
        self.side: str = "BLUE"
        self.arm: arm_manager.ArmManager = arm_manager.ArmManager()

    def initialize_gpio(self):
        if self.simulation:
            print("Initializing GPIO")
            return True

    def move(self, dist, theta=None):
        if self.simulation:
            print("Moving to distance: {}, angle: {}".format(dist, theta))
            return True

    def go_angle(self, theta):
        if self.simulation:
            print("Going to angle: {}".format(theta))
            return True

    def buldozer(self, move="open"):
        if self.simulation:
            print("Buldozer: {}".format(move))
            return True

    def arm(self, move="home"):
        if self.simulation:
            print("Moving arm to the {} position".format(move))
            return True

    def suc(self, state: bool = True):
        if self.simulation:
            print("Suc: {}".format(state))
            return True

    def showcase(self):
        if self.simulation:
            print("Showing showcase")
            return True
