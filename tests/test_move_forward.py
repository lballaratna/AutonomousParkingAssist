"""Owner: Harikrishna M


**Requirement:** move the car one metre, check for a parking space while
moving and never let the car go past either end of the 500m street.

Because there is a hard limit at both ends of the street, we test both
sides of each limit specifically, not just an ordinary middle value.

a) MoveForward from position 0 => Position becomes 1 (valid move)
b) MoveForward from position 499 (one before the upper limit) =>Position becomes 500 (valid move)
c) MoveForward from position 500 (already at the upper limit) => Position stays at 500 — rejected
d) Any successful move =>A parking-space reading gets recorded

"""
import pytest

from autonomous_parking_system import FixedSensor, ParkingAssistant


@pytest.fixture
def car():
    return ParkingAssistant(FixedSensor(100), FixedSensor(100))


# a) MoveForward from position 0 => Position becomes 1 (valid move)
# b) MoveForward from position 499 (one before the upper limit) =>Position becomes 500 (valid move)
@pytest.mark.parametrize("start,expected", [
    (0, 1),
    (499, 500),
])
def test_move_forward_advances_one_metre(car, start, expected):
    car.state.position = start
    car.move_forward()
    assert car.state.position == expected


# c) MoveForward from position 500 (already at the upper limit) => Position stays at 500 — rejected
def test_move_forward_rejected_at_street_end(car):
    car.state.position = 500
    car.move_forward()
    assert car.state.position == 500


# d) Any successful move =>A parking-space reading gets recorded
def test_move_forward_records_isEmpty_reading(car):
    car.move_forward()
    assert len(car.state.records) == 1