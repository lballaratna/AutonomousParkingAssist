"""Owner: Harikrishna M R

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


# a) Fresh car, before any movement => Position is 0, status is "unparked"
def test_fresh_car_is_unparked_at_position_zero(car):
    result = car.where_is()
    assert result.position == 0
    assert result.status == "unparked"


# b) After calling MoveForward n times =>Position is n
def test_position_reflects_moves(car):
    n = 15
    for i in range(n):
        car.move_forward()
    
    assert car.where_is().position == n
    assert car.where_is().status == "unparked"


# c) Right after a successful Park => Status is "parked"
def test_status_parked_after_park():
    car = ParkingAssistant(FixedSensor(0), FixedSensor(0))
    #Creating a new object because the initial object is created with sensor values 100, so if we call the car.part(),
    #it will not be able to perform the park operation
    car.park()
    assert car.where_is().status == "parked"


# d) Right after UnPark =>Status is "unparked"
def test_status_unparked_after_unpark():
    car = ParkingAssistant(FixedSensor(0), FixedSensor(0))
    car.park()
    car.unpark()
    assert car.where_is().status == "unparked"
