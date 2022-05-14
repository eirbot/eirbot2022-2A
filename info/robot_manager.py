#! /usr/bin/env python3
import logging
import multiprocessing
import time

import RPi.GPIO as GPIO
import requests

import arm_manager
import gpio_manager
import serial_manager


class RobotManager:
    def __init__(self, simulation: bool = False, baudrate: int = 115200, port: str = "/dev/ttyACM0",
                 log_level: int = logging.INFO, camera_url: str = "http://0.0.0.0"):
        self.simulation: bool = simulation

        self.arm: arm_manager.ArmManager = arm_manager.ArmManager(simulation=self.simulation)
        self.gpio: gpio_manager.GpioManager = gpio_manager.GpioManager(simulation=self.simulation)
        self.serial: serial_manager.SerialManager = serial_manager.SerialManager(baudrate=baudrate, port=port)

        self.camera_url: str = camera_url

        if not self.simulation:
            self.gpio.initialize_gpio()

        self.start: bool = False
        self.side: str = "BLUE"

        self.operation: dict[str, bin] = {"SPO": 1,
                                          "RESET": 2,
                                          "SRO": 4,
                                          "SVI": 5,
                                          "STOP": 6}

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
        multiprocessing.Process(target=self.end_of_world).start()

    def end_of_world(self):
        """
        This function is called when the time is up.
        """
        begin = time.time()
        while time.time() - begin < 10:
            pass
        self.stop()
        logging.getLogger().error("END")

    def move(self, dist, theta=0):
        if self.simulation:
            logging.debug("Moving to distance: {}, angle: {}".format(dist, theta))
            return True
        self.serial.serial_write(self.operation["SPO"], self.serial.type["int_16"], [int(dist), int(theta)])

        self.serial.ser.timeout = self.kms_timeout
        output = self.serial.serial_read()
        if not self.serial.kms_is_dead(output):
            self.move(dist, theta)
        else:
            self.serial.ser.timeout = self.move_timeout
            output = self.serial.serial_read()
            if output == self.return_codes["RPOOK"]:
                return True
            elif output == self.return_codes["RPOOUT"]:
                return False

    def go_angle(self, theta):
        if self.simulation:
            logging.debug("Going to angle: {}".format(theta))
            return True

        self.serial.serial_write(self.operation["SRO"], self.serial.type["int_16"], [theta])
        self.serial.ser.timeout = self.kms_timeout
        output = self.serial.serial_read()
        if not self.serial.kms_is_dead(output):
            self.go_angle(theta)
        else:
            self.serial.ser.timeout = self.move_timeout
            output = self.serial.serial_read()
            if output == self.return_codes["RROOK"]:
                return True
            elif output == self.return_codes["RROOUT"]:
                return False

    def reset(self):
        if self.simulation:
            logging.debug("Resetting")
            return True

        self.serial.serial_write(self.operation["RESET"], self.serial.type["int_16"], [])

        GPIO.output(self.gpio.GPIO["reset"]["pin"], GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.gpio.GPIO["reset"]["pin"], GPIO.LOW)

        self.serial.ser.timeout = self.kms_timeout
        output = self.serial.serial_read()
        if not self.serial.kms_is_dead(output):
            self.reset()
        else:
            time.sleep(1)
            return True

    def go_speed(self):
        if self.simulation:
            logging.debug("Going to speed")
            return True

        self.serial.serial_write(self.operation["SVI"], self.serial.type["int_16"], [])
        self.serial.ser.timeout = self.kms_timeout
        output = self.serial.serial_read()
        if not self.serial.kms_is_dead(output):
            self.go_speed()
        else:
            return True

    def stop(self):
        if self.simulation:
            logging.debug("Stopping")
            return True

        self.serial.serial_write(self.operation["STOP"], self.serial.type["int_16"], [])
        self.serial.ser.timeout = self.kms_timeout
        output = self.serial.serial_read()
        if not self.serial.kms_is_dead(output):
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
        self.reset()
        while GPIO.input(self.gpio.GPIO["start"]["pin"]) != 1:
            time.sleep(0.1)
        logging.error("Started")
        return True
