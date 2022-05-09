class ArmManager:
    def __init__(self, simulation: bool):
        self.gpio: list[int, int, int, int] = [4, 17, 27, 22]
        self.position: dict = {}
        self.simulation: bool = simulation

    def move_arm(self, position: str):
        if self.simulation:
            print("Simulation: ArmManager: arm: " + position)
            return
