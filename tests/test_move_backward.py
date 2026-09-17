"""

Requirements Summary:
- Car moves backward by 1 meter while scanning for parking spaces.
- Street limits are strictly bounded between 0m and 500m.
- Test boundary cases (start of street, end of street, and out-of-bounds attempts).
- Ensure a valid space measurement is recorded after each successful movement.
"""

import pytest

from autonomous_parking_system import FixedSensor, ParkingAssistant


@pytest.fixture
def car():
    return ParkingAssistant(FixedSensor(100), FixedSensor(100))


# Valid backward movement: reduces current position by 1 meter
@pytest.mark.parametrize("start,expected", [
    (500, 499),
    (1, 0),
])
def test_move_backward_retreats_one_metre(car, start, expected):
    car.state.position = start
    car.move_backward()
    assert car.state.position == expected


# Border check: cannot retreat further when already at position 0
def test_move_backward_rejected_at_street_start(car):
    car.state.position = 0
    car.move_backward()
    assert car.state.position == 0


# Ensure parking sensor data is stored in records array after moving
def test_move_backward_records_isEmpty_reading(car):
    car.state.position = 1
    car.move_backward()
    assert len(car.state.records) == 1
