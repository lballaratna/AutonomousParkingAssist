"""Owner: Harikrishna M


**Requirements** :report the car's current position and whether it is parked or not.

Since this method does not calculate anything — it just reports the current
state — every test case here is about checking that it reports the
*correct* state at a specific point in time.

a) Fresh car, before any movement =>Position is 0, status is "unparked"
b) After calling MoveForward twice =>Position is 2
c) Right after a successful Park => Status is "parked"
d) Right after UnPark =>Status is "unparked"

"""
import pytest

from autonomous_parking_system import FixedSensor, ParkingAssistant


@pytest.fixture
def car():
    return ParkingAssistant(FixedSensor(100), FixedSensor(100))


# a) Fresh car, before any movement =>Position is 0, status is "unparked"
def test_fresh_car_is_unparked_at_position_zero(car):
    result = car.where_is()
    assert result.position == 0
    assert result.status == "unparked"


# b) After calling MoveForward twice =>Position is 2
def test_position_reflects_moves(car):
    car.move_forward()
    car.move_forward()
    assert car.where_is().position == 2


# c) Right after a successful Park => Status is "parked"
# using a separate car here, since the fixture above always reads
# "occupied" (100cm) and park() would never actually succeed on it
def test_status_parked_after_park():
    car = ParkingAssistant(FixedSensor(0), FixedSensor(0))
    car.park()
    assert car.where_is().status == "parked"


# d) Right after UnPark =>Status is "unparked"
def test_status_unparked_after_unpark():
    car = ParkingAssistant(FixedSensor(0), FixedSensor(0))
    car.park()
    car.unpark()
    assert car.where_is().status == "unparked"
