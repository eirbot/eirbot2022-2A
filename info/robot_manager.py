#! /usr/bin/env python3
import logging
import multiprocessing
import struct
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
    def __init__(self, simulation: bool = False, baudrate: int = 115200, port: str = "/dev/ttyACM0",
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
        self.operation: dict[str, bin] = {"SPO": 1,
                                          "RESET": 2,
                                          "SRO": 4,
                                          "SVI": 5,
                                          "STOP": 6}

        self.type: dict[str, bin] = {"int_16": 0,
                                     "int_32": 1}

        self.return_codes: dict[str, bin] = {"KMS": b'\x00',
                                             "RPOOK": b'\x01',
                                             "RROOUT": b'\x02',
                                             "RROOK": b'\x03',
                                             "RPOUT": b'\x04',
                                             "PLS": b'\x05', }

        self.kms_timeout: float = 0.1
        self.move_timeout: int = 10
        logging.getLogger().setLevel(log_level)
        self.camera_url: str = camera_url
        self.initialize_gpio()
        multiprocessing.Process(target=end_of_world).start()

    def serial_read(self):
        data = self.ser.read()
        logging.info("Reading from serial: {}".format(data))
        return data

    def serial_write(self, op, int_type, param_array):
        header = op << 4 | int_type << 3 | len(param_array)
        data = []

        for param in param_array:
            if int_type == type["int_16"]:
                if param < -32768 or param > 32767:
                    raise ValueError
                data += struct.pack("!h", param)
            elif int_type == type["int_32"]:
                if param < -2147483648 or param > 2147483647:
                    raise ValueError
                data += struct.pack("!i", param)

        cmd = [header] + data
        logging.info("Writing to serial: {}".format(cmd))

        self.ser.write(cmd)

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
        if self.simulation:
            logging.debug("Moving to distance: {}, angle: {}".format(dist, theta))
            return True

        if theta is not None:
            self.serial_write(self.operation["SPO"], self.type["int_16"], [dist, theta])
        else:
            self.serial_write(self.operation["SPO"], self.type["int_16"], [dist])

        self.ser.timeout = self.kms_timeout
        output = self.serial_read()
        if output != self.return_codes["KMS"]:
            self.move(dist, theta)
        elif output == self.return_codes["KMS"]:
            self.ser.timeout = self.move_timeout
            output = self.serial_read()
            if output == self.return_codes["RPOOK"]:
                return True
            elif output == self.return_codes["RPOOUT"]:
                return False

    def go_angle(self, theta):
        if self.simulation:
            logging.debug("Going to angle: {}".format(theta))
            return True

        self.serial_write(self.operation["SRO"], self.type["int_16"], [theta])
        self.ser.timeout = self.kms_timeout
        output = self.serial_read()
        if output != self.return_codes["KMS"]:
            self.go_angle(theta)
        elif output == self.return_codes["KMS"]:
            self.ser.timeout = self.move_timeout
            output = self.serial_read()
            if output == self.return_codes["RROOK"]:
                return True
            elif output == self.return_codes["RROOUT"]:
                return False

    def reset(self):
        if self.simulation:
            logging.debug("Resetting")
            return True

        self.serial_write(self.operation["RESET"], self.type["int_16"], [])

        self.ser.timeout = self.kms_timeout
        output = self.serial_read()
        if output != self.return_codes["KMS"]:
            self.reset()
        elif output == self.return_codes["KMS"]:
            time.sleep(1)
            return True

    def go_speed(self):
        message = self.operation["SVI"] + self.type["int_16"] + "000"
        if self.simulation:
            logging.debug("Going to speed")
            return True

        self.serial_write(self.operation["SVI"], self.type["int_16"], [])
        self.ser.timeout = self.kms_timeout
        output = self.serial_read()
        if output != self.return_codes["KMS"]:
            self.go_speed()
        elif output == self.return_codes["KMS"]:
            return True

    def stop(self):
        message = self.operation["STOP"] + self.type["int_16"] + "000"
        if self.simulation:
            logging.debug("Stopping")
            return True

        self.serial_write(self.operation["STOP"], self.type["int_16"], [])
        self.ser.timeout = self.kms_timeout
        output = self.serial_read()
        if output != self.return_codes["KMS"]:
            self.stop()
        elif output == self.return_codes["KMS"]:
            time.sleep(1)
            return True

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
