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

    # --- Owner: Pooney Joseph (reviewed by Harikrishna M R) --
    def is_empty(self) -> int:
        # case 20 (test_each_sensor_queried_at_least_five_times, call-count
        # case): the project instructions require >=5 queries per sensor.
        left = [self.sensor_left.read() for _ in range(5)]
        right = [self.sensor_right.read() for _ in range(5)]
        left_noisy = self._is_noisy(left)
        right_noisy = self._is_noisy(right)

        # case b (test_noisy_left_sensor_is_disregarded): left noisy, right
        # clean - disregard left entirely, trust right.
        if left_noisy and not right_noisy:

            return self._average(right)
        # case c (test_noisy_right_sensor_is_disregarded): mirror of case b.
        elif right_noisy and not left_noisy:
     
            return self._average(left)
        # case a (test_both_sensors_clean_returns_filtered_reading): both
        # clean - average the two filtered readings.
        elif not left_noisy and not right_noisy:

            return (self._average(left) + self._average(right)) // 2



        # case d (test_both_sensors_noisy): both sensors noisy at once - not
        # specified by the project instructions; refuse to guess rather than average two
        # untrustworthy readings (documented assumption, see
        # tests/test_is_empty.py, case d).
        raise ValueError("both sensors are continuously noisy - reading unreliable")

    @classmethod
    def _is_noisy(cls, readings) -> bool:
        # case g (test_out_of_range_reading_is_treated_as_invalid): a
        # reading outside the sensor's documented 0-200cm range is treated
        # as noisy (documented assumption - not specified by the project
        # instructions).
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
    # Each is_empty() == 0 reading stands for one clear metre. Cases
    # 22-26 are really one algorithm: keep a running count of *consecutive*
    # clear metres, starting from wherever the car already is; a non-zero
    # reading breaks the run and the count starts over. Once the count
    # reaches STRETCH_REQUIRED the car is sitting at the far end of a
    # qualifying stretch (measurements combined/filtered via is_empty(),
    # accumulated across positions), so it parks right there. If the
    # street runs out first, there was never a long-enough gap (case 26).
    def park(self) -> CarState:
        # case 27 (test_park_while_already_parked_is_rejected): reject a
        # second park() call while already parked.
        if self.state.status == "parked":
            raise ValueError("already parked")

        # case 22/23/24: reading at the current position, before moving -
        # if it's already clear that's the first metre of the stretch.
        consecutive_clear = 1 if self.is_empty() == 0 else 0

        while consecutive_clear < self.STRETCH_REQUIRED:
            # case 26 (test_no_stretch_found_anywhere_is_rejected): ran out
            # of street before finding STRETCH_REQUIRED consecutive clear
            # metres.
            if self.state.position >= self.STREET_LENGTH:
                raise ValueError(
                    "no free stretch of {}m found on the street".format(
                        self.STRETCH_REQUIRED))
            self.move_forward()
            # case 25 (test_four_point_nine_metre_stretch_is_rejected): a
            # blocked reading resets the run; a clear one extends it.
            latest_reading = self.state.records[-1].distance_cm
            consecutive_clear = consecutive_clear + 1 if latest_reading == 0 else 0

        # case 28 (test_park_reverses_into_the_space_after_finding_it): the
        # car is now at the end of the qualifying STRETCH_REQUIRED-metre
        # stretch, having driven past it - that's the standard parallel
        # parking setup, not the finish. Reverse back the length of the
        # stretch (minus the metre already standing on) to land at its
        # start, i.e. actually into the space, before parking. Without
        # this the car would "park" at the space's entrance, and unpark()'s
        # forward-to-the-front step would then drive it straight past the
        # space instead of out of it.
        for _ in range(self.STRETCH_REQUIRED - 1):
            self.move_backward()

        self.state.status = "parked"
        return self.state

    def unpark(self) -> CarState:
        # case 32 (test_unpark_while_not_parked_is_rejected): reject
        # unparking a car that isn't parked (documented assumption - the
        # project instructions only describe what UnPark does "if it is
        # parked").
        if self.state.status != "parked":
            raise ValueError("cannot unpark - car is not parked")
        # case 31 (test_unpark_from_parked_state) / case 33
        # (test_where_is_consistent_after_unpark) / case 29
        # (test_unpark_returns_to_front_of_space_found_by_park): park()
        # leaves the car at the *back* of the STRETCH_REQUIRED-metre space
        # (having reversed into it), so driving to the front means covering
        # the rest of the space's length, not just 1 metre.
        self.state.position += self.STRETCH_REQUIRED - 1
        self.state.status = "unparked"
        return self.state