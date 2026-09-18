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
    car = ParkingAssistant(FixedSensor(0), FixedSensor(0))  # case 22
    car.park()
    assert car.state.status == "parked"


# Park called while already parked => Rejected
# Park the car once (succeeds), then call park() again and  second call raises an error.
def test_park_while_already_parked_is_rejected():
    car = ParkingAssistant(FixedSensor(0), FixedSensor(0))  # case 27
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
    )  # case 23
    car.park()
    assert car.state.status == "parked"
    # search drove up to position 5 (the end of the stretch), then reversed
    # STRETCH_REQUIRED - 1 metres back into it, landing at its start (1).
    assert car.state.position == 1


# Free stretch is exactly 5.0m (boundary) => accepted, and the car stops
# right there instead of continuing to drive through the blocked metre
# that comes right after it. Equally: a wall/parked car sitting immediately
# after an otherwise-qualifying 5m slot must NOT disqualify it - the search
# only needs to look as far as the 5th clear metre, never the 6th.
def test_boundary_five_metre_stretch_is_accepted():
    car = ParkingAssistant(
        SequenceSensor([0, 0, 0, 0, 0, 80]),
        SequenceSensor([0, 0, 0, 0, 0, 80]),
    )  # case 24
    car.park()
    assert car.state.status == "parked"
    # the stretch starts right where the car already was (0); reversing
    # back into it lands the car back at 0.
    assert car.state.position == 0


# Free stretch falls short (4 clear metres, then blocked) => rejected, the
# run resets and the search keeps going until it reaches a real 5m
# stretch further ahead, rather than parking early on the short one.
# (The project instructions phrase this as "4.9m"; this simulation moves in whole
# metres, so the equivalent is a run that breaks one metre short of 5.)
def test_four_point_nine_metre_stretch_is_rejected():
    car = ParkingAssistant(
        SequenceSensor([0, 0, 0, 0, 80, 0, 0, 0, 0, 0]),
        SequenceSensor([0, 0, 0, 0, 80, 0, 0, 0, 0, 0]),
    )  # case 25
    car.park()
    assert car.state.status == "parked"
    # search drove up to position 9 (the end of the real stretch), then
    # reversed back to its start (5) - the earlier 4-metre near-miss at
    # positions 0-3 never gets parked in.
    assert car.state.position == 5


# No qualifying stretch exists anywhere on the rest of the street => the
# search has to stop at the street's end rather than looping forever.
def test_no_stretch_found_anywhere_is_rejected():
    car = ParkingAssistant(FixedSensor(80), FixedSensor(80))  # case 26
    with pytest.raises(Exception):
        car.park()
    assert car.state.position == car.STREET_LENGTH
    assert car.state.status != "parked"


# Finding a qualifying stretch isn't the finish - a real parallel park
# means driving to the end of the space, then reversing into it. Blocked
# metre first, so the search actually has to drive forward and pass the
# stretch before parking; the parked position must end up behind where
# the search reached, proving a real reverse happened rather than the car
# just parking wherever the forward search stopped.
def test_park_reverses_into_the_space_after_finding_it():
    car = ParkingAssistant(
        SequenceSensor([80, 0, 0, 0, 0, 0]),
        SequenceSensor([80, 0, 0, 0, 0, 0]),
    )  # case 28
    car.park()
    furthest_position_reached = max(r.position for r in car.state.records)
    assert furthest_position_reached == 5  # the search did reach the far end
    assert car.state.position < furthest_position_reached  # then reversed back
    assert car.state.position == furthest_position_reached - (car.STRETCH_REQUIRED - 1)


# Park then UnPark should be a round trip that makes sense: UnPark drives
# forward to the front of the space, which should land back at the far
# end the original search reached - not past it, and not still inside it.
def test_unpark_returns_to_front_of_space_found_by_park():
    car = ParkingAssistant(
        SequenceSensor([80, 0, 0, 0, 0, 0]),
        SequenceSensor([80, 0, 0, 0, 0, 0]),
    )  # case 29
    car.park()
    parked_position = car.state.position
    car.unpark()
    assert car.state.position == parked_position + car.STRETCH_REQUIRED - 1


# A "wall" doesn't have to be another car - the physical end of the
# street (position 500) is one too. If only a few clear metres remain
# before the street runs out, that's not a qualifying stretch even though
# every reading in it is clear - same rejection as case 26, but proving it
# also holds when the street ends mid-search rather than never finding a
# clear metre at all.
def test_park_rejected_when_street_ends_before_stretch_completes():
    car = ParkingAssistant(SequenceSensor([0] * 10), SequenceSensor([0] * 10))  # case 30
    car.state.position = car.STREET_LENGTH - 3  # only 3 clear metres left
    with pytest.raises(Exception):
        car.park()
    assert car.state.position == car.STREET_LENGTH
    assert car.state.status != "parked"





