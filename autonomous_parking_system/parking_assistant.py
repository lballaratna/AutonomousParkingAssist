from .interface import ParkingAssistantInterface
from .sensor import Sensor
from .state import CarState, ParkingRecord

class ParkingAssistant(ParkingAssistantInterface):

    NOISE_THRESHOLD = 10  # cm - max acceptable spread across 5 readings

    def __init__(self, sensor_left: Sensor, sensor_right: Sensor):
        self.sensor_left = sensor_left
        self.sensor_right = sensor_right
        self.state = CarState()

   # --- Owner: Harikrishna M --
    def where_is(self) -> CarState:
        return self.state

    def move_forward(self) -> CarState:
        if self.state.position >= self.STREET_LENGTH:
            return self.state
        self.state.position += 1
        reading = self.is_empty()
        self.state.records.append(ParkingRecord(self.state.position, reading))
        return self.state

    # --- Owner: Pooney Joseph --
    def move_backward(self) -> CarState:
        if self.state.position <= 0:
            return self.state
        self.state.position -= 1
        reading = self.is_empty()
        self.state.records.append(ParkingRecord(self.state.position, reading))
        return self.state

    # --- Owner: Pooney Joseph (reviewed by Harikrishna M) --
    def is_empty(self) -> int:
        left = [self.sensor_left.read() for _ in range(5)]
        right = [self.sensor_right.read() for _ in range(5)]
        left_noisy = self._is_noisy(left)
        right_noisy = self._is_noisy(right)

        if left_noisy and not right_noisy:
            return self._average(right)
        if right_noisy and not left_noisy:
            return self._average(left)
        if not left_noisy and not right_noisy:
            return (self._average(left) + self._average(right)) // 2

        # both sensors noisy at once - not covered by the brief; refuse to
        # guess rather than average two untrustworthy readings (see the
        # note in tests/test_is_empty.py, case d)
        raise ValueError("both sensors are continuously noisy - reading unreliable")

    @classmethod
    def _is_noisy(cls, readings) -> bool:
        if any(r < 0 or r > 200 for r in readings):
            return True
        return max(readings) - min(readings) > cls.NOISE_THRESHOLD

    @staticmethod
    def _average(readings) -> int:
        return sum(readings) // len(readings)

    # --- Owner: Lavanya BallaRatna --
    # NOTE: only cases 20 and 25 are built here for Phase 1. Cases 21
    # (search forward for a stretch), 22/23 (the exact 5m boundary), and
    # 24 (no stretch found anywhere) need a way to measure a multi-metre
    # free stretch, which needs sensor test-doubles beyond what
    # FixedSensor/RandomSensor/NoisySensor can give - deferred to Phase 2,
    # where pytest-mock/unittest.mock is the planned tool for exactly this
    # kind of sensor stubbing. See tests/test_park.py for the requirement
    # notes kept against each deferred case.
    def park(self) -> CarState:
        if self.state.status == "parked":
            raise ValueError("already parked")
        if self._at_free_stretch():
            self.state.status = "parked"
        return self.state

    def _at_free_stretch(self) -> bool:
        return self.is_empty() == 0

    def unpark(self) -> CarState:
        if self.state.status != "parked":
            raise ValueError("cannot unpark - car is not parked")
        self.state.position += 1
        self.state.status = "unparked"
        return self.state