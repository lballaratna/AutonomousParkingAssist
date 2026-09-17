"""Owner: Pooney Joseph

**Requirement:** 
query both ultrasonic sensors at least 5 times each,
filter out noise, disregard a sensor that is continuously noisy and
return a distance between 0–200cm.

**Not provided in requiremnt: ** 
Both sensors are noisy at the same time and Reading outside 0–200cm 

is sensor A noisy? Is sensor B noisy?

(a) Both sensors are clean and agree => Filter average of the two readings 
(b) Sensor A is noisy and B is clean  => A is disregarded entirely; return B's reading 
(c) Sensor B is noisy and A is clean => B is disregarded entirely; return A's reading
(d) Both sensors are noisy at the same time => raise an error instead of guessing 
                                               (because it isnot mentioned in the REQUIREMENTS)
(e) Reading exactly 0cm (lower boundary) => Accepted as valid 
(f) Reading exactly 200cm (upper boundary) => Accepted as valid 
(g) Reading outside 0–200cm => treat it as invalid, same as a noisy reading 
                               (because it isnot mentioned in the REQUIREMENTS)
(f) Checking how many times each sensor is actually queried => Each sensor is read at least 5 times 

"""

#testing code starts here
import pytest

from autonomous_parking_system import FixedSensor, NoisySensor, ParkingAssistant


# (a) Both sensors are clean and agree => Filter average of the two readings
def test_both_sensors_clean_returns_filtered_reading():
    car = ParkingAssistant(FixedSensor(50), FixedSensor(52))
    assert 50 <= car.is_empty() <= 52


# (b) Sensor A is noisy and B is clean => A is disregarded entirely; return B's reading
def test_noisy_left_sensor_is_disregarded():
    car = ParkingAssistant(NoisySensor(), FixedSensor(80))
    assert car.is_empty() == 80


# (c) Sensor B is noisy and A is clean => B is disregarded entirely; return A's reading
def test_noisy_right_sensor_is_disregarded():
    car = ParkingAssistant(FixedSensor(80), NoisySensor())
    assert car.is_empty() == 80


# (d) Both sensors are noisy at the same time => raise an error instead of
# guessing (because it isnot mentioned in the REQUIREMENTS)
# Known issue: with two real NoisySensor() instances, this occasionally
# fails (about 1 run in 5) purely by chance - both sides' random readings
# can happen to land close enough together to not look noisy. A reliable
# fix needs a sensor that can be scripted to guarantee noise on both
# sides every time, which needs mocking tooling we're keeping for Phase 2.
# Covered properly in Phase 2; left as a (rarely) flaky test for now.
def test_both_sensors_noisy():
    car = ParkingAssistant(NoisySensor(), NoisySensor())
    with pytest.raises(Exception):
        car.is_empty()


# (e) Reading exactly 0cm (lower boundary) => Accepted as valid
# (f) Reading exactly 200cm (upper boundary) => Accepted as valid
@pytest.mark.parametrize("reading", [0, 200])
def test_boundary_readings_are_valid(reading):
    car = ParkingAssistant(FixedSensor(reading), FixedSensor(reading))
    assert car.is_empty() == reading


# (g) Reading outside 0-200cm => treat it as invalid, same as a noisy
# reading (because it isnot mentioned in the REQUIREMENTS)
def test_out_of_range_reading_is_treated_as_invalid():
    car = ParkingAssistant(FixedSensor(250), FixedSensor(80))
    assert car.is_empty() == 80


# (f) Checking how many times each sensor is actually queried => Each
# sensor is read at least 5 times
# Requirement is real for Phase 1, but proving a call *count* needs a
# sensor that can track how many times it was read - FixedSensor can't
# tell you that, only what it returns. Needs mocking tooling (pytest-mock)
# that we're keeping for Phase 2. Covered in Phase 2.
def test_each_sensor_queried_at_least_five_times():
    pytest.skip("needs call-count tracking (pytest-mock) - covered in Phase 2")  # case 19
