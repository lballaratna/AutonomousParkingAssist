from .interface import ParkingAssistantInterface
from .sensor import Sensor
from .state import CarState

class ParkingAssistant(ParkingAssistantInterface):
    def __init__(self, sensor_left: Sensor, sensor_right: Sensor):
        self.sensor_left = sensor_left
        self.sensor_right = sensor_right
        self.state = CarState()
    # --- Owner: Harikrishna M --
    def where_is(self) -> CarState:
        raise NotImplementedError
    def move_forward(self) -> CarState:
        raise NotImplementedError
    # --- Owner: Pooney Joseph --
    def move_backward(self) -> CarState:
        raise NotImplementedError
    # --- Owner: Pooney Joseph (reviewed by Harikrishna M) --
    def is_empty(self) -> int:
        raise NotImplementedError
    # --- Owner: Lavanya BallaRatna --
    def park(self) -> CarState:
        raise NotImplementedError
    def unpark(self) -> CarState:
        raise NotImplementedError
        