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


# No stretch right here, but one exists further ahead => car drives
# forward (reusing move_forward + isEmpty) until it finds one, then parks.
# Requirement is real for Phase 1 (case 21), but testing it needs a sensor
# that can give a *sequence* of different readings - FixedSensor/
# RandomSensor can't do that, and Phase 1 is keeping mocking tools
# (pytest-mock/unittest.mock) for Phase 2's sensor/actuator stubbing.
# Covered in Phase 2.
def test_park_searches_forward_when_no_stretch_here():
    pytest.skip("needs sequenced sensor control (pytest-mock) - covered in Phase 2")  # case 21


# Free stretch is exactly 5.0m (boundary) => accepted
# Same reason as above - covered in Phase 2.
def test_boundary_five_metre_stretch_is_accepted():
    pytest.skip("needs sequenced sensor control (pytest-mock) - covered in Phase 2")  # case 22


# Free stretch is 4.9m (just short) => rejected, search continues
# Same reason as above - covered in Phase 2.
def test_four_point_nine_metre_stretch_is_rejected():
    pytest.skip("needs sequenced sensor control (pytest-mock) - covered in Phase 2")  # case 23


# No qualifying stretch exists anywhere on the rest of the street => the
# search has to stop somewhere, rather than looping forever.
# Same reason as above - covered in Phase 2.
def test_no_stretch_found_anywhere_is_rejected():
    pytest.skip("needs sequenced sensor control (pytest-mock) - covered in Phase 2")  # case 24


# Park called while already parked => Rejected
# Park the car once (succeeds), then call park() again and  second call raises an error. 
def test_park_while_already_parked_is_rejected():
    car = ParkingAssistant(FixedSensor(0), FixedSensor(0))
    car.park()
    with pytest.raises(Exception):
        car.park()  


