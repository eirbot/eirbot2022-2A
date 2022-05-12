#! /usr/bin/env python3
import logging
import time

import serial

import arm_manager


class RobotManager:
    def __init__(self, simulation: bool = False, baudrate: int = 9600, port: str = "/dev/ttyACM0",
                 log_level: int = logging.INFO):
        self.simulation: bool = simulation
        self.usb: str = port
        self.baudrate: int = baudrate
        if not self.simulation:
            self.ser = serial.Serial(self.usb, self.baudrate)
        self.GPIO: dict[str, int] = {"bulldozer": 5,
                                     "display": 6,
                                     "limit_switch_forward": 13,
                                     "limit_switch_backward": 26,
                                     "start": 18,
                                     "side": 23,
                                     "gp2_forward": 24,
                                     "gp2_backward": 25,
                                     "showcase": 12}
        self.start: bool = False
        self.side: str = "BLUE"
        self.arm: arm_manager.ArmManager = arm_manager.ArmManager(simulation=self.simulation)
        self.operation: dict[str, bin] = {"SPO": "0010",
                                          "RESET": "0100",
                                          "SRO": "1000",
                                          "SVI": "1010",
                                          "STOP": "1100"}
        self.type: dict[str, bin] = {"int_16": "0",
                                     "int_32": "1"}
        self.return_codes: dict[str, bin] = {"KMS": "00000000",
                                             "RPOOK": "00010000",
                                             "RROOUT": "00100000",
                                             "RROOK": "00110000",
                                             "RPOUT": "01000000", }
        self.ksm_timeout: int = 1
        self.move_timeout: int = 10
        logging.getLogger().setLevel(log_level)

    def initialize_gpio(self):
        if self.simulation:
            logging.debug("Initializing GPIO")
            return True

    def move(self, dist, theta=None):
        if theta is None:
            arg = "001"
        else:
            arg = "010"

        message = self.operation["SPO"] + self.type["int_16"] + arg
        logging.info(bytes(message, "utf-8"))
        if self.simulation:
            logging.debug("Moving to distance: {}, angle: {}".format(dist, theta))
            return True

        self.ser.write(bytes(message, "utf-8"))
        self.ser.write(bytes(str(dist), "utf-8"))
        if theta is not None:
            self.ser.write(bytes(str(theta), "utf-8"))
        self.ser.timeout = self.ksm_timeout
        output = self.ser.read()
        logging.error(output)
        if output != bytes(self.return_codes["KMS"], "utf-8"):
            self.move(dist, theta)
        elif output == bytes(self.return_codes["KMS"], "utf-8"):
            self.ser.timeout = self.move_timeout
            output = self.ser.read()
            if output == bytes(self.return_codes["RPOOK"], "utf-8"):
                return True
            elif output == bytes(self.return_codes["RPOUT"], "utf-8"):
                return False

    def go_angle(self, theta):
        message = self.operation["SRO"] + self.type["int_16"] + "001"
        logging.info(bytes(message, "utf-8"))
        if self.simulation:
            logging.debug("Going to angle: {}".format(theta))
            return True
        self.ser.write(message)
        self.ser.write(bytes(str(theta), "utf-8"))
        self.ser.timeout = self.ksm_timeout
        output = self.ser.read()
        if output != bytes(self.return_codes["KMS"], "utf-8"):
            self.go_angle(theta)
        elif output == bytes(self.return_codes["KMS"], "utf-8"):
            self.ser.timeout = self.move_timeout
            output = self.ser.read()
            if output == bytes(self.return_codes["RROOK"], "utf-8"):
                return True
            elif output == bytes(self.return_codes["RROOUT"], "utf-8"):
                return False

    def reset(self):
        message = self.operation["RESET"] + self.type["int_16"] + "000"
        logging.info(bytes(message, "utf-8"))
        if self.simulation:
            logging.debug("Resetting")
            return True
        self.ser.write(message)
        self.ser.timeout = self.ksm_timeout
        output = self.ser.read()
        if output != bytes(self.return_codes["KMS"], "utf-8"):
            time.sleep(0.1)
            return True
        else:
            return False

    def go_speed(self):
        message = self.operation["SVI"] + self.type["int_16"] + "000"
        logging.info(bytes(message, "utf-8"))
        if self.simulation:
            logging.debug("Going to speed")
            return True
        self.ser.write(bytes(message, "utf-8"))
        self.ser.timeout = self.ksm_timeout
        output = self.ser.read()
        if output != bytes(self.return_codes["KMS"], "utf-8"):
            return True

    def stop(self):
        message = self.operation["STOP"] + self.type["int_16"] + "000"
        logging.info(bytes(message, "utf-8"))
        if self.simulation:
            logging.debug("Stopping")
            return True
        self.ser.write(message)
        self.ser.timeout = self.ksm_timeout
        output = self.ser.read()
        if output != bytes(self.return_codes["KMS"], "utf-8"):
            return True
        else:
            return False

    def buldozer(self, move="open"):
        if self.simulation:
            logging.debug("Bulldozer: {}".format(move))
            return True

    def suc(self, state: bool = True):
        if self.simulation:
            logging.debug("Suc: {}".format(state))
            return True

    def showcase(self):
        if self.simulation:
            logging.debug("Showing showcase")
            return True
