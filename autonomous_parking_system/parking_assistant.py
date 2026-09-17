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
        # case a (test_fresh_car_is_unparked_at_position_zero) / case b
        # (test_position_reflects_moves) / case c (test_status_parked_after_park) /
        # case d (test_status_unparked_after_unpark): a pure query, CarState
        # already holds the answer to all four cases - nothing to compute.
        return self.state

    def move_forward(self) -> CarState:
        # case c (test_move_forward_rejected_at_street_end): at the upper
        # boundary, no-op and return the unchanged state.
        if self.state.position >= self.STREET_LENGTH:
            return self.state
        # case a/b (test_move_forward_advances_one_metre[0-1, 499-500]):
        # ordinary move and the upper-boundary-minus-one move both just
        # advance by 1.
        self.state.position += 1
        # case d (test_move_forward_records_isEmpty_reading): every
        # successful move queries isEmpty() and records the reading.
        reading = self.is_empty()
        self.state.records.append(ParkingRecord(self.state.position, reading))
        return self.state

    # --- Owner: Pooney Joseph --
    def move_backward(self) -> CarState:
        # case c (test_move_backward_rejected_at_street_start): at the lower
        # boundary (position 0), no-op and return the unchanged state.
        if self.state.position <= 0:
            return self.state
        # case a/b (test_move_backward_retreats_one_metre[500-499, 1-0]):
        # ordinary move and the lower-boundary-plus-one move both retreat by 1.
        self.state.position -= 1
        # case d (test_move_backward_records_isEmpty_reading): every
        # successful move queries isEmpty() and records the reading.
        reading = self.is_empty()
        self.state.records.append(ParkingRecord(self.state.position, reading))
        return self.state

    # --- Owner: Pooney Joseph (reviewed by Harikrishna M) --
    def is_empty(self) -> int:
        # case f (test_each_sensor_queried_at_least_five_times, Phase 2):
        # the brief requires >=5 queries per sensor.
        left = [self.sensor_left.read() for _ in range(5)]
        right = [self.sensor_right.read() for _ in range(5)]
        left_noisy = self._is_noisy(left)
        right_noisy = self._is_noisy(right)

        # case b (test_noisy_left_sensor_is_disregarded): left noisy, right
        # clean - disregard left entirely, trust right.
        if left_noisy and not right_noisy:
            return self._average(right)
        # case c (test_noisy_right_sensor_is_disregarded): mirror of case b.
        if right_noisy and not left_noisy:
            return self._average(left)
        # case a (test_both_sensors_clean_returns_filtered_reading): both
        # clean - average the two filtered readings.
        if not left_noisy and not right_noisy:
            return (self._average(left) + self._average(right)) // 2

        # case d (test_both_sensors_noisy): both sensors noisy at once - not
        # specified by the brief; refuse to guess rather than average two
        # untrustworthy readings (documented assumption, see
        # tests/test_is_empty.py, case d).
        raise ValueError("both sensors are continuously noisy - reading unreliable")

    @classmethod
    def _is_noisy(cls, readings) -> bool:
        # case g (test_out_of_range_reading_is_treated_as_invalid): a
        # reading outside the sensor's documented 0-200cm range is treated
        # as noisy (documented assumption - not specified by the brief).
        if any(r < 0 or r > 200 for r in readings):
            return True
        # case e/f (test_boundary_readings_are_valid[0, 200]): readings at
        # exactly the 0/200cm edges must be accepted as valid, not flagged
        # as noisy - the threshold check below only trips on *spread*
        # across the 5 readings, not on the absolute value.
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
        # case 25 (test_park_while_already_parked_is_rejected): reject a
        # second park() call while already parked.
        if self.state.status == "parked":
            raise ValueError("already parked")
        # case 20 (test_parks_immediately_when_already_at_free_stretch): if
        # already at a qualifying free stretch, park immediately.
        if self._at_free_stretch():
            self.state.status = "parked"
        return self.state

    def _at_free_stretch(self) -> bool:
        return self.is_empty() == 0

    def unpark(self) -> CarState:
        # case 27 (test_unpark_while_not_parked_is_rejected): reject
        # unparking a car that isn't parked (documented assumption - the
        # brief only describes what UnPark does "if it is parked").
        if self.state.status != "parked":
            raise ValueError("cannot unpark - car is not parked")
        # case 26 (test_unpark_from_parked_state) / case 28
        # (test_where_is_consistent_after_unpark): move forward to the
        # front of the space and flip status back to unparked.
        self.state.position += 1
        self.state.status = "unparked"
        return self.state