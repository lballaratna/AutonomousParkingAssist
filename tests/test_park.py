"""Owner: Lavanya BallaRatna

**Requirement:** if the car is already at a free stretch of at least 5
metres, run the parking maneuver immediately. Otherwise, drive forward
until a long-enough stretch is found, then park. Parking while already
parked should not be allowed.


"""
import pytest

from autonomous_parking_system import FixedSensor, ParkingAssistant

# Car is already at a valid free stretch (≥5m) => Maneuver runs immediately; status becomes "parked" 
# giving both sensors a "free" reading (0cm)

def test_parks_immediately_when_already_at_free_stretch():
    car = ParkingAssistant(FixedSensor(0), FixedSensor(0))
    car.park()
    assert car.state.status == "parked"  



# Park called while already parked => Rejected 
# Park the car once (succeeds), then call park() again and  second call raises an error. 
def test_park_while_already_parked_is_rejected():
    car = ParkingAssistant(FixedSensor(0), FixedSensor(0))
    car.park()
    with pytest.raises(Exception):
        car.park()  


