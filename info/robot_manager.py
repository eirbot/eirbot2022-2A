#! /usr/bin/env python3
import logging
import multiprocessing
import struct
import time

import RPi.GPIO as GPIO
import requests
import serial

import arm_manager


def end_of_world():
    """
    This function is called when the time is up.
    """
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
                                                      "showcase": {"pin": 12, "direction": OUT},
                                                      "red_led": {"pin": 16, "direction": OUT},
                                                      "reset": {"pin": 19, "direction": OUT}, }
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

        self.kms_timeout: float = 1
        self.kms_dead_count: int = 0
        self.reset_soft_count: int = 0
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
            if int_type == self.type["int_16"]:
                if param < -32768 or param > 32767:
                    raise ValueError
                data += struct.pack("!h", param)
            elif int_type == self.type["int_32"]:
                if param < -2147483648 or param > 2147483647:
                    raise ValueError
                data += struct.pack("!i", param)

        cmd = [header] + data
        logging.info("Writing to serial: {}".format(cmd))

        self.ser.write(cmd)

    def kms_is_dead(self, output):
        """
        This function check if the output on serial is KMS, if not count the number of time and reset nucleo if
        necessary.
        """
        if output != self.return_codes["KMS"]:
            self.kms_dead_count += 1
            if self.kms_dead_count >= 10:
                self.kms_dead_count = 0
                self.reset_soft_count += 1
                self.reset()
                if self.reset_soft_count >= 3:
                    self.reset_soft_count = 0
                    GPIO.output(self.gpio_pins["reset"]["pin"], GPIO.HIGH)
            return False
        else:
            self.kms_dead_count = 0
            self.reset_soft_count = 0
            return True

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

    def move(self, dist, theta=0):
        if self.simulation:
            logging.debug("Moving to distance: {}, angle: {}".format(dist, theta))
            return True
        self.serial_write(self.operation["SPO"], self.type["int_16"], [int(dist), int(theta)])

        self.ser.timeout = self.kms_timeout
        output = self.serial_read()
        if not self.kms_is_dead(output):
            self.move(dist, theta)
        else:
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
        if not self.kms_is_dead(output):
            self.go_angle(theta)
        else:
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

        GPIO.output(self.GPIO["reset"]["pin"], GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.GPIO["reset"]["pin"], GPIO.LOW)

        self.ser.timeout = self.kms_timeout
        output = self.serial_read()
        if not self.kms_is_dead(output):
            self.reset()
        else:
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
        if not self.kms_is_dead(output):
            self.go_speed()
        else:
            return True

    def stop(self):
        message = self.operation["STOP"] + self.type["int_16"] + "000"
        if self.simulation:
            logging.debug("Stopping")
            return True

        self.serial_write(self.operation["STOP"], self.type["int_16"], [])
        self.ser.timeout = self.kms_timeout
        output = self.serial_read()
        if not self.kms_is_dead(output):
            self.stop()
        else:
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
        self.reset()
        while GPIO.input(self.GPIO["start"]["pin"]) != 1:
            time.sleep(0.1)
        logging.error("Started")
        return True
