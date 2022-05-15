import logging
import time

from RPi import GPIO

import flags


class GpioManager:
    def __init__(self, simulation):
        OUT = 0
        IN = 1
        self.simulation = simulation
        if not self.simulation:
            OUT = GPIO.OUT
            IN = GPIO.IN
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

    def initialize_gpio(self):
        if self.simulation:
            logging.debug("Initializing GpioManager")
            return True
        GPIO.setmode(GPIO.BCM)
        for key in self.GPIO:
            logging.debug("Initializing {} GpioManager with pin {} and direction {}".format(key, self.GPIO[key]["pin"],
                                                                                            self.GPIO[key][
                                                                                                "direction"]))
            GPIO.setup(self.GPIO[key]["pin"], self.GPIO[key]["direction"])
            time.sleep(0.1)