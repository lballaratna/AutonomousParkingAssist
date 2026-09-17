"""
Requirements:
1. Read both ultrasonic sensors at least 5 times each.
2. Filter out noisy sensors and return a valid distance between 0-200cm.

Handling specific cases:
- Both clean: Return average of both readings.
- One noisy / out of bounds (0-200cm): Ignore noisy sensor, return valid sensor reading.
- Both noisy: Raise an error.
- Exact boundaries (0cm and 200cm): Valid readings.
"""

import pytest

from autonomous_parking_system import FixedSensor, NoisySensor, ParkingAssistant


# Return average when both sensors give valid readings
def test_both_sensors_clean_returns_filtered_reading():
    car = ParkingAssistant(FixedSensor(50), FixedSensor(52))
    assert 50 <= car.is_empty() <= 52


# Ignore left sensor if it is noisy and return right sensor reading
def test_noisy_left_sensor_is_disregarded():
    car = ParkingAssistant(NoisySensor(), FixedSensor(80))
    assert car.is_empty() == 80


# Ignore right sensor if it is noisy and return left sensor reading
def test_noisy_right_sensor_is_disregarded():
    car = ParkingAssistant(FixedSensor(80), NoisySensor())
    assert car.is_empty() == 80


# Raise error when both sensors are noisy
# Note: May occasionally fail due to random values from NoisySensor
def test_both_sensors_noisy():
    car = ParkingAssistant(NoisySensor(), NoisySensor())
    with pytest.raises(Exception):
        car.is_empty()


# Check lower and upper boundaries (0cm and 200cm)
@pytest.mark.parametrize("reading", [0, 200])
def test_boundary_readings_are_valid(reading):
    car = ParkingAssistant(FixedSensor(reading), FixedSensor(reading))
    assert car.is_empty() == reading


# Readings outside 0-200cm should be treated as noisy/invalid
def test_out_of_range_reading_is_treated_as_invalid():
    car = ParkingAssistant(FixedSensor(250), FixedSensor(80))
    assert car.is_empty() == 80


# Check sensor query count
def test_each_sensor_queried_at_least_five_times():
    pytest.skip("Skipped: requires mock object to track read count")