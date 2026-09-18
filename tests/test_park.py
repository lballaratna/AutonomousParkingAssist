"""Owner: Lavanya BallaRatna

**Requirement:** if the car is already at a free stretch of at least 5
metres, run the parking maneuver immediately. Otherwise, drive forward
until a long-enough stretch is found, then park. Parking while already
parked should not be allowed.


"""
import pytest

from autonomous_parking_system import FixedSensor, ParkingAssistant, SequenceSensor

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

        


# No stretch right here (1 blocked metre), but one exists further ahead =>
# car drives forward (reusing move_forward + isEmpty) until it finds one,
# then parks at the far end of it. Uses SequenceSensor instead of a
# mocking library - see sensor.py.
def test_park_searches_forward_when_no_stretch_here():
    car = ParkingAssistant(
        SequenceSensor([80, 0, 0, 0, 0, 0]),
        SequenceSensor([80, 0, 0, 0, 0, 0]),
    )  # case 21
    car.park()
    assert car.state.status == "parked"
    assert car.state.position == 5


# Free stretch is exactly 5.0m (boundary) => accepted, and the car stops
# right there instead of continuing to drive through the blocked metre
# that comes right after it.
def test_boundary_five_metre_stretch_is_accepted():
    car = ParkingAssistant(
        SequenceSensor([0, 0, 0, 0, 0, 80]),
        SequenceSensor([0, 0, 0, 0, 0, 80]),
    )  # case 22
    car.park()
    assert car.state.status == "parked"
    assert car.state.position == car.STRETCH_REQUIRED - 1


# Free stretch falls short (4 clear metres, then blocked) => rejected, the
# run resets and the search keeps going until it reaches a real 5m
# stretch further ahead, rather than parking early on the short one.
# (The brief phrases this as "4.9m"; this simulation moves in whole
# metres, so the equivalent is a run that breaks one metre short of 5.)
def test_four_point_nine_metre_stretch_is_rejected():
    car = ParkingAssistant(
        SequenceSensor([0, 0, 0, 0, 80, 0, 0, 0, 0, 0]),
        SequenceSensor([0, 0, 0, 0, 80, 0, 0, 0, 0, 0]),
    )  # case 23
    car.park()
    assert car.state.status == "parked"
    assert car.state.position == 9


# No qualifying stretch exists anywhere on the rest of the street => the
# search has to stop at the street's end rather than looping forever.
def test_no_stretch_found_anywhere_is_rejected():
    car = ParkingAssistant(FixedSensor(80), FixedSensor(80))  # case 24
    with pytest.raises(Exception):
        car.park()
    assert car.state.position == car.STREET_LENGTH
    assert car.state.status != "parked"





