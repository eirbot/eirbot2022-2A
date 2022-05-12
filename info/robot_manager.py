#! /usr/bin/env python3
import logging
import multiprocessing
import time

import requests
import serial

import arm_manager


def end_of_world():
    begin = time.time()
    while time.time() - begin < 80:
        pass
    logging.getLogger().error("END")


class RobotManager:
    def __init__(self, simulation: bool = False, baudrate: int = 9600, port: str = "/dev/ttyACM0",
                 log_level: int = logging.INFO, camera_url: str = "http://0.0.0.0"):
        self.simulation: bool = simulation
        self.usb: str = port
        self.baudrate: int = baudrate
        OUT = 0
        IN = 1
        if not self.simulation:
            import RPi.GPIO as GPIO
            OUT = GPIO.OUT
            IN = GPIO.IN
            self.ser = serial.Serial(self.usb, self.baudrate)
            self.ser.flush()
        self.GPIO: dict[str, dict[str | int, str]] = {"bulldozer": {"pin": 5, "direction": OUT},
                                                      "display": {"pin": 6, "direction": OUT},
                                                      "limit_switch_forward": {"pin": 13, "direction": IN},
                                                      "limit_switch_backward": {"pin": 26, "direction": IN},
                                                      "start": {"pin": 18, "direction": IN},
                                                      "side": {"pin": 23, "direction": IN},
                                                      "gp2_forward": {"pin": 24, "direction": IN},
                                                      "gp2_backward": {"pin": 25, "direction": IN},
                                                      "showcase": {"pin": 12, "direction": OUT}}
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
        self.return_codes: dict[str, bin] = {"KMS": "\x00",
                                             "RPOOK": "\x10",
                                             "RROOUT": "\x20",
                                             "RROOK": "\x30",
                                             "RPOUT": "\x40", }
        self.ksm_timeout: int = 1
        self.move_timeout: int = 10
        logging.getLogger().setLevel(log_level)
        self.camera_url: str = camera_url
        self.initialize_gpio()
        multiprocessing.Process(target=end_of_world).start()

    def serial_read(self):
        data = self.ser.read()
        logging.info("Reading from serial: {}".format(data))
        return data

    def serial_write(self, data: bytes):
        logging.info("Writing to serial: {}".format(data))
        self.ser.write(data)

    def initialize_gpio(self):
        if self.simulation:
            logging.debug("Initializing GPIO")
            return True
        from RPi import GPIO
        GPIO.setmode(GPIO.BCM)
        for key in self.GPIO:
            logging.debug("Initializing {} GPIO with pin {} and direction {}".format(key, self.GPIO[key]["pin"],
                                                                                     self.GPIO[key]["direction"]))
            GPIO.setup(self.GPIO[key]["pin"], self.GPIO[key]["direction"])
            time.sleep(0.1)
        self.side = "BLUE" if GPIO.input(self.GPIO["side"]["pin"]) else "YELLOW"

    def move(self, dist, theta=None):
        if theta is None:
            arg = "001"
        else:
            arg = "010"

        message = self.operation["SPO"] + self.type["int_16"] + arg
        if self.simulation:
            logging.debug("Moving to distance: {}, angle: {}".format(dist, theta))
            return True

        self.serial_write(bytes(message, "utf-8"))
        self.serial_write(bytes(str(dist), "utf-8"))
        if theta is not None:
            self.serial_write(bytes(str(theta), "utf-8"))
        self.ser.timeout = self.ksm_timeout
        output = self.serial_read()
        if output != bytes(self.return_codes["KMS"], "utf-8"):
            self.move(dist, theta)
        elif output == bytes(self.return_codes["KMS"], "utf-8"):
            self.ser.timeout = self.move_timeout
            output = self.serial_read()
            if output == bytes(self.return_codes["RPOOK"], "utf-8"):
                return True
            elif output == bytes(self.return_codes["RPOUT"], "utf-8"):
                return False

    def go_angle(self, theta):
        message = self.operation["SRO"] + self.type["int_16"] + "001"
        if self.simulation:
            logging.debug("Going to angle: {}".format(theta))
            return True
        self.serial_write(bytes(message, "utf-8"))
        self.serial_write(bytes(str(theta), "utf-8"))
        self.ser.timeout = self.ksm_timeout
        output = self.serial_read()
        if output != bytes(self.return_codes["KMS"], "utf-8"):
            self.go_angle(theta)
        elif output == bytes(self.return_codes["KMS"], "utf-8"):
            self.ser.timeout = self.move_timeout
            output = self.serial_read()
            if output == bytes(self.return_codes["RROOK"], "utf-8"):
                return True
            elif output == bytes(self.return_codes["RROOUT"], "utf-8"):
                return False

    def reset(self):
        message = self.operation["RESET"] + self.type["int_16"] + "000"
        if self.simulation:
            logging.debug("Resetting")
            return True
        self.serial_write(bytes(message, "utf-8"))
        self.ser.timeout = self.ksm_timeout
        output = self.serial_read()
        if output != bytes(self.return_codes["KMS"], "utf-8"):
            time.sleep(0.1)
            return True
        else:
            return False

    def go_speed(self):
        message = self.operation["SVI"] + self.type["int_16"] + "000"
        if self.simulation:
            logging.debug("Going to speed")
            return True
        self.serial_write(bytes(message, "utf-8"))
        self.ser.timeout = self.ksm_timeout
        output = self.serial_read()
        if output != bytes(self.return_codes["KMS"], "utf-8"):
            return True

    def stop(self):
        message = self.operation["STOP"] + self.type["int_16"] + "000"
        if self.simulation:
            logging.debug("Stopping")
            return True
        self.serial_write(bytes(message, "utf-8"))
        self.ser.timeout = self.ksm_timeout
        output = self.serial_read()
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

    def get_position(self):
        logging.error("Getting position from url: {}".format(self.camera_url))
        position = requests.get(self.camera_url + "/pos_robot").text
        return position

    def wait_until_start(self):
        import RPi.GPIO as GPIO
        while GPIO.input(self.GPIO["start"]["pin"]) != 1:
            time.sleep(0.1)
        logging.error("Started")
        return True
