from RPi import GPIO


class ArmManager:
    def __init__(self, simulation: bool):
        self.gpio: list[int, int, int, int] = [4, 17, 27, 22]
        self.position: dict = {"nazi_inverted": 4}
        self.simulation: bool = simulation

    def inverted_nazi(self, activation: bool):
        if activation:
            GPIO.output(4, GPIO.HIGH)
        elif not activation:
            GPIO.output(4, GPIO.LOW)
