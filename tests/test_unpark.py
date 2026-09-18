"""Owner: Lavanya BallaRatna

**Requirement:** move the car forward (and left) to the front of the
parking space. This is only valid while the car is actually parked.



"""
import pytest

from autonomous_parking_system import FixedSensor, ParkingAssistant

# Car is parked => Status becomes "unparked", and the car moves forward to
# the front of the parking space. park() leaves the car at the back of the
# STRETCH_REQUIRED-metre space (having reversed into it), so reaching the
# front means covering the rest of the space, not just 1 metre.

def test_unpark_from_parked_state():
    car = ParkingAssistant(FixedSensor(0), FixedSensor(0))  # case 31
    car.park()
    start_position = car.state.position
    car.unpark()
    assert car.state.status == "unparked"
    assert car.state.position == start_position + car.STRETCH_REQUIRED - 1


#Car is not parked =>unpark is Rejected (unparking should only work if the car is actually parked).
# An error is raised.

def test_unpark_while_not_parked_is_rejected():
    car = ParkingAssistant(FixedSensor(100), FixedSensor(100))  # case 32
    with pytest.raises(Exception):
        car.unpark()  


# UnPark the car immediately followed by WhereIs(shows unparked status and
# the new position, not just unpark()'s own return value)
def test_where_is_consistent_after_unpark():
    car = ParkingAssistant(FixedSensor(0), FixedSensor(0))  # case 33
    car.park()
    start_position = car.state.position
    car.unpark()
    result = car.where_is()
    assert result.status == "unparked"
    assert result.position == start_position + car.STRETCH_REQUIRED - 1
