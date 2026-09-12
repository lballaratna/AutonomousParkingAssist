"""Owner: Lavanya BallaRatna

**Requirement:** move the car forward (and left) to the front of the
parking space. This is only valid while the car is actually parked.



"""
import pytest

from autonomous_parking_system import FixedSensor, ParkingAssistant

#Car is parked => Status becomes "unparked" 

def test_unpark_from_parked_state():
    car = ParkingAssistant(FixedSensor(0), FixedSensor(0))
    car.park()
    car.unpark()
    assert car.state.status == "unparked" 


#Car is not parked =>unpark is Rejected (unparking should only work if the car is actually parked).
# An error is raised.

def test_unpark_while_not_parked_is_rejected():
    car = ParkingAssistant(FixedSensor(100), FixedSensor(100))
    with pytest.raises(Exception):
        car.unpark()  


# UnPark the car immediately followed by WhereIs(shows unparked status) 
# To do: Park, unpark, then check status through where_is() instead.
# Expected: where_is() also reports "unparked".
def test_where_is_consistent_after_unpark():
    car = ParkingAssistant(FixedSensor(0), FixedSensor(0))
    car.park()
    car.unpark()
    assert car.where_is().status == "unparked"  
