"""Owner: Pooney Joseph

**Requirement:** move the car one metre, check for a parking space while
moving and never let the car go past either end of the 500m street.

Because there is a hard limit at both ends of the street, we test both
sides of each limit specifically, not just an ordinary middle value.

(a) MoveBackward from position 500 => Position becomes 499 and it is Valid move
(b) MoveBackward from position 1 => Position becomes 0 and it is valid move
(c) MoveBackward from position 0 (already at the lower limit) =>Position stays at 0 — rejected
(d) Any successful move => A parking-space reading gets recorded
"""
import pytest

from autonomous_parking_system import FixedSensor, ParkingAssistant


@pytest.fixture
def car():
    return ParkingAssistant(FixedSensor(100), FixedSensor(100))


# (a) MoveBackward from position 500 => Position becomes 499 and it is Valid move
# (b) MoveBackward from position 1 => Position becomes 0 and it is valid move
@pytest.mark.parametrize("start,expected", [
    (500, 499),
    (1, 0),
])
def test_move_backward_retreats_one_metre(car, start, expected):
    car.state.position = start
    car.move_backward()
    assert car.state.position == expected


# (c) MoveBackward from position 0 (already at the lower limit) =>Position stays at 0 — rejected
def test_move_backward_rejected_at_street_start(car):
    car.state.position = 0
    car.move_backward()
    assert car.state.position == 0


# (d) Any successful move => A parking-space reading gets recorded
# starting at position 0 would make this a no-op (case c), so this moves
# the car forward one metre first to give move_backward() somewhere valid
# to actually retreat from
def test_move_backward_records_isEmpty_reading(car):
    car.state.position = 1
    car.move_backward()
    assert len(car.state.records) == 1

