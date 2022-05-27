import logging
import time

from RPi import GPIO


class ArmManager:
    def __init__(self, simulation: bool):
        self.gpio: list[int, int, int, int] = [10, 17, 27, 6]
        self.simulation: bool = simulation
        self.initialize_gpio()

    def initialize_gpio(self):
        if self.simulation:
            logging.debug("Initializing GpioManager")
            return True
        GPIO.setmode(GPIO.BCM)
        for element in range(len(self.gpio)):
            GPIO.setup(self.gpio[element], GPIO.OUT)
            time.sleep(0.1)
            # GPIO.output(self.gpio[element], GPIO.LOW)

    def base_position(self):
        GPIO.output(10, GPIO.LOW)
        GPIO.output(17, GPIO.LOW)
        time.sleep(4)

    def inverted_nazi(self):
        GPIO.output(10, GPIO.HIGH)
        GPIO.output(27, GPIO.HIGH)
        GPIO.output(17, GPIO.LOW)
        time.sleep(4)

    def piedestal(self):
        GPIO.output(10, GPIO.LOW)
        GPIO.output(17, GPIO.HIGH)
        time.sleep(4)

    def suc(self, activation: bool):
        if activation:
            GPIO.output(22, GPIO.HIGH)
        elif not activation:
            GPIO.output(22, GPIO.LOW)
