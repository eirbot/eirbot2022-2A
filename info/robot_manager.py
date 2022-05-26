#! /usr/bin/env python3
import logging
import multiprocessing
import time

import requests
from RPi import GPIO

import arm_manager
import camera_manager
import flags
import gpio_manager
import serial_manager


class RobotManager:
    def __init__(self, simulation: bool = False, baudrate: int = 115200, port: str = "/dev/ttyACM0",
                 log_level: int = logging.INFO, camera_url: str = "http://0.0.0.0"):
        self.simulation: bool = simulation

        self.camera_url: str = camera_url

        self.arm: arm_manager.ArmManager = arm_manager.ArmManager(simulation=self.simulation)
        self.gpio: gpio_manager.GpioManager = gpio_manager.GpioManager(simulation=self.simulation)
        self.serial: serial_manager.SerialManager = serial_manager.SerialManager(baudrate=baudrate, port=port)
        # self.camera: camera_manager.CameraManager = camera_manager.CameraManager(camera_url=self.camera_url)

        if not self.simulation:
            self.gpio.initialize_gpio()

        self.start: bool = False
        self.side: str = "YELLOW"
        flags.SIDE = self.side

        self.operation: dict[str, bin] = {"SPO": 1,
                                          "RESET": 2,
                                          "SRO": 4,
                                          "SVI": 5,
                                          "STOP": 6}

        self.return_codes: dict[str, bin] = {"KMS": b'\x00',
                                             "RPOOK": b'\x01',
                                             "RROOUT": b'\x02',
                                             "RROOK": b'\x03',
                                             "RPOOUT": b'\x04',
                                             "PLS": b'\x05', }

        self._length: int = 3000
        self._width: int = 2000
        self._robot_width:int = 150
        
        if self.side == "YELLOW" :
            self._x: int = 700
            self._y: int = 150
            self._theta: int = 0
        else :
            self._x: int = 700
            self._y: int = 2850
            self._theta: int = 0
        
        

        logging.getLogger().setLevel(log_level)
        multiprocessing.Process(target=self.__end_of_world).start()

        GPIO.add_event_detect(self.gpio.GPIO["gp2_forward"]["pin"], GPIO.RISING,
                              callback=self.__gp2_forward_callback,
                              bouncetime=100)
        GPIO.add_event_detect(self.gpio.GPIO["gp2_backward"]["pin"], GPIO.RISING,
                              callback=self.__gp2_backward_callback,
                              bouncetime=100)
        GPIO.add_event_detect(self.gpio.GPIO["limit_switch_forward"]["pin"], GPIO.RISING,
                              callback=self.__limit_switch_forward_callback,
                              bouncetime=100)
        GPIO.add_event_detect(self.gpio.GPIO["limit_switch_backward"]["pin"], GPIO.FALLING,
                              callback=self.__limit_switch_backward_callback,
                              bouncetime=100)

    def __gp2_forward_callback(self, channel):
        logging.error("GP2 backward callback rise")
        self.stop()
        flags.BLOCKED = True
        time.sleep(1)
        flags.BLOCKED = False

    def __gp2_backward_callback(self, channel):
        logging.error("GP2 forward callback rise")
        self.stop()
        flags.BLOCKED = True
        time.sleep(1)
        flags.BLOCKED = False

    def __limit_switch_forward_callback(self, channel):
        logging.error("Limit switch forward callback rise")
        self.stop()
        flags.BLOCKED = True
        time.sleep(1)

        if self.side == "YELLOW" :
            if self._theta <= 45 and self._theta >= -45:
                self._y = self._length - self._robot_width
            elif self._theta > 45 and self._theta <= 135:
                self._x = self._width - self._robot_width
            elif self._theta < -45 and self._theta >= -135:
                self._x = self._robot_width
            elif (self._theta < -135 and self._theta >= -180) or (self._theta > 135 and self._theta <= 180) :
                self._y = self._robot_width
    
        else :
            if self._theta <= 45 and self._theta >= -45:
                self._y = self._robot_width
            elif self._theta > 45 and self._theta <= 135:
                self._x = self._robot_width
            elif self._theta < -45 and self._theta >= -135:
                self._x = self._width - self._robot_width
            elif (self._theta < -135 and self._theta >= -180) or (self._theta > 135 and self._theta <= 180) :
                self._y = self._length - self._robot_width

        flags.BLOCKED = False

    def __limit_switch_backward_callback(self, channel):
        logging.error("Limit switch backward callback rise")
        self.stop()
        flags.BLOCKED = True
        time.sleep(1)

        if self.side != "YELLOW" :
            if self._theta <= 45 and self._theta >= -45:
                self._y = self._length - self._robot_width
            elif self._theta > 45 and self._theta <= 135:
                self._x = self._width - self._robot_width
            elif self._theta < -45 and self._theta >= -135:
                self._x = self._robot_width
            elif (self._theta < -135 and self._theta >= -180) or (self._theta > 135 and self._theta <= 180) :
                self._y = self._robot_width
        
        else :
            if self._theta <= 45 and self._theta >= -45:
                self._y = self._robot_width
            elif self._theta > 45 and self._theta <= 135:
                self._x = self._robot_width
            elif self._theta < -45 and self._theta >= -135:
                self._x = self._width - self._robot_width
            elif (self._theta < -135 and self._theta >= -180) or (self._theta > 135 and self._theta <= 180) :
                self._y = self._length - self._robot_width

        flags.BLOCKED = False

    def __end_of_world(self):
        """
        This function is called when the time is up.
        """
        begin = time.time()
        while time.time() - begin < 80:
            pass
        self.stop()
        logging.getLogger().error("END")

    def __kms_is_dead(self, output):
        """
        This function check if the output on serial is KMS, if not count the number of time and reset nucleo if
        necessary.
        """
        # if output != b'\x00':
        #     self.serial.kms_dead_count += 1
        #     if self.serial.kms_dead_count >= 10:
        #         self.serial.kms_dead_count = 0
        #         self.serial.reset_soft_count += 1
        #         self.reset()
        #         if self.serial.reset_soft_count >= 3:
        #             self.serial.reset_soft_count = 0
        #             GPIO.output(self.gpio.GPIO["reset"]["pin"], GPIO.HIGH)
        #     return False
        # else:
        #     self.serial.kms_dead_count = 0
        #     self.serial.reset_soft_count = 0
        return True

    def move(self, dist, theta=0):
        if self.simulation:
            logging.debug("Moving to distance: {}, angle: {}".format(dist, theta))
            return True
        self.serial.serial_write(self.operation["SPO"], self.serial.type["int_16"], [int(dist), int(theta)])

        self.serial.ser.timeout = self.serial.kms_timeout
        output = self.serial.serial_read()
        if not self.__kms_is_dead(output):
            self.move(dist, theta)
        else:
            self.serial.ser.timeout = self.serial.move_timeout
            output = self.serial.serial_read()
            if output == self.return_codes["RPOOK"]:
                return True
            elif output == self.return_codes["RPOOUT"]:
                return False

        self.move_position(dist)

    def go_angle(self, theta):

        if self.side != "YELLOW" :
        theta = - theta

        if self.simulation:
            logging.debug("Going to angle: {}".format(theta))
            return True

        self.serial.serial_write(self.operation["SRO"], self.serial.type["int_16"], [theta])
        self.serial.ser.timeout = self.serial.kms_timeout
        output = self.serial.serial_read()
        if not self.__kms_is_dead(output):
            self.go_angle(theta)
        else:
            self.serial.ser.timeout = self.serial.move_timeout
            output = self.serial.serial_read()
            if output == self.return_codes["RROOK"]:
                return True
            elif output == self.return_codes["RROOUT"]:
                return False
        
        self.move_angle(theta)

    def reset(self):
        if self.simulation:
            logging.debug("Resetting")
            return True

        self.serial.serial_write(self.operation["RESET"], self.serial.type["int_16"], [])

        GPIO.output(self.gpio.GPIO["reset"]["pin"], GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.gpio.GPIO["reset"]["pin"], GPIO.LOW)

        self.serial.ser.timeout = self.serial.kms_timeout
        output = self.serial.serial_read()
        if not self.__kms_is_dead(output):
            self.reset()
        else:
            time.sleep(1)
            return True

    def go_speed(self):
        if self.simulation:
            logging.debug("Going to speed")
            return True

        self.serial.serial_write(self.operation["SVI"], self.serial.type["int_16"], [])
        self.serial.ser.timeout = self.serial.kms_timeout
        output = self.serial.serial_read()
        if not self.__kms_is_dead(output):
            self.go_speed()
        else:
            return True

    def stop(self):
        if self.simulation:
            logging.debug("Stopping")
            return True

        self.serial.serial_write(self.operation["STOP"], self.serial.type["int_16"], [])
        self.serial.ser.timeout = self.serial.kms_timeout
        output = self.serial.serial_read()
        if not self.__kms_is_dead(output):
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
        multiprocessing.Process(target=self.__showcase_thread).start()
        # GPIO.output(12, GPIO.HIGH)

    def __showcase_thread(self):
        while True:
            GPIO.output(12, GPIO.HIGH)
            time.sleep(0.2)

    def get_position(self):
        logging.error("Getting position from url: {}".format(self.camera_url))
        position = requests.get(self.camera_url + "/pos_robot").text
        return position

    def wait_until_start(self):
        while GPIO.input(self.gpio.GPIO["start"]["pin"]) != 0:
            # logging.debug("Waiting for start" + str(GPIO.input(self.gpio.GPIO["start"]["pin"])))
            time.sleep(0.1)
        logging.error("Started")
        return True
        # while True:
        #     logging.error("Switch forward: {}".format(GPIO.input(self.gpio.GPIO["limit_switch_forward"]["pin"])))
        #     logging.error("Switch backward: {}".format(GPIO.input(self.gpio.GPIO["limit_switch_backward"]["pin"])))
        #     logging.error("GP2 forward: {}".format(GPIO.input(self.gpio.GPIO["gp2_forward"]["pin"])))
        #     logging.error("GP2 backward: {}".format(GPIO.input(self.gpio.GPIO["gp2_backward"]["pin"])))
        #     time.sleep(0.5)


    def go_until_wall(self):
        self.go_speed()
        while GPIO.input(self.gpio.GPIO["limit_switch_forward"]["pin"]) != 1:
            time.sleep(0.1)
        self.stop()


    def move_position(distance):
        x = distance * math.sin(math.radians(self._theta))
        y = distance * math.cos(math.radians(self._theta))

        if self.side != "YELLOW" :
            y = - y
            x = - x
        
        self._y += y
        self._x += x

    def move_angle(angle):
        # _theta += angle
        # _theta = _theta % 360

        self._theta += angle

        if self._theta < -360:
            self._theta = self._theta % -360
        elif self._theta > 360:
            self._theta = self._theta % 360
        if self._theta > 180:
           self._theta = self._theta - 360
        elif self._theta < -180:
            self._theta = 360 + self._theta

