import logging
import time

from RPi import GPIO


class ArmManager:
    def __init__(self, simulation: bool):
        self.gpio: list[int, int, int, int] = [4, 17, 27, 22]
        self.position: dict = {"nazi_inverted": 4}
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

    def inverted_nazi(self, activation: bool):
        if activation:
            GPIO.output(4, GPIO.HIGH)
            time.sleep(3)
        elif not activation:
            GPIO.output(4, GPIO.LOW)
            time.sleep(3)
