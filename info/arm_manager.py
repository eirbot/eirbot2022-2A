class ArmManager:
    def __init__(self):
        self.gpio: list[int, int, int, int] = [4, 17, 27, 22]
        self.position: dict = {}
