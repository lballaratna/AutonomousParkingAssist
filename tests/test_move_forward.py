"""Owner: Harikrishna M R

a) MoveForward from position 0 => Position becomes 1 (valid move)
b) MoveForward from position 499 =>Position becomes 500 (valid move)
c) MoveForward from position 500 => Position stays at 500 — rejected
d) Whether valid move record an is_empty reading is recorded

"""
from os import startfile
import pytest

from autonomous_parking_system import FixedSensor, ParkingAssistant


@pytest.fixture
def car():
    return ParkingAssistant(FixedSensor(100), FixedSensor(100))


# a) MoveForward from position 0 => Position becomes 1 (valid move)
def test_move_forward_from_0_to_1(car):
    car.state.position = 0
    car.move_forward()
    assert car.state.position == 1


# b) MoveForward from position 499 => 500 (valid move)
def test_move_forward_from_499_to_500(car):
    car.state.position = 0
    for i in range(499):
        car.move_forward()
    assert car.state.position == 499
    car.move_forward()
    assert car.state.position == 500


# c) MoveForward from position 500 => Position stays at 500 (rejected)
def test_move_forward_rejected_at_street_end(car):
    for i in range(500):
        car.move_forward()
    car.move_forward()
    assert car.state.position == 500
    


# d) Whether valid move record an is_empty reading is recorded
def test_move_forward_records_is_Empty_reading(car):
    car.move_forward()
    assert len(car.state.records) == 1