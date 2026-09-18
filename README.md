# AutonomousParkingAssist

Control software for an autonomous parking system — a single Python class
that reports the car's position, moves it forward and backward, checks for
a free parking space using two sensors, and can park and unpark the car.
Real sensors and actuators aren't modeled this phase — we're building the
decision-making logic only.

This is built entirely test-first (TDD): for every method, the tests were
written and agreed on before a single line of the real logic was.

## What's in this repo

```
autonomous_parking_system/
├── __init__.py
├── interface.py          the six required methods, as a contract - no logic
├── state.py               what the car knows about itself: position, status, history
├── sensor.py              fake sensors (fixed, random, noisy, scripted) standing in for real hardware
└── parking_assistant.py   the class that actually implements everything

tests/
├── test_where_is.py
├── test_move_forward.py
├── test_move_backward.py
├── test_is_empty.py
├── test_park.py
└── test_unpark.py
```

Each test file has a short explanation at the top of what it's testing and
why, straight from the requirements. `tests/README.md` has the full
breakdown of every case.

## Setup

```
pip install -r requirements.txt
```

## Running the tests

Run everything:
```
pytest -v
```

Run just one file:
```
pytest tests/test_park.py -v
```

Run one specific test, by name:
```
pytest tests/test_park.py::test_parks_immediately_when_already_at_free_stretch -v
```

Run every test whose name contains a keyword (handy when you don't
remember the exact name):
```
pytest -k "park" -v
```

## Generating a coverage report

Coverage tells us whether the tests actually ran through the code, not just
that they passed - if a line or branch never runs during the tests, it
shows up here.

Run the tests with coverage tracking on, then print a summary:
```
python -m coverage run -m pytest
python -m coverage report -m
```

The `-m` shows exactly which line numbers were missed, so you know what to
go test next.

For a proper, click-through report:
```
python -m coverage html
```
This creates an `htmlcov/` folder - open `htmlcov/index.html` in a browser
and every file is shown with covered lines highlighted and missed ones
called out.

## Where we stand

All six methods (WhereIs, MoveForward, MoveBackward, isEmpty, Park, UnPark)
are implemented. 28 of 29 official test cases pass; 1 is skipped for now.

A couple of decisions we made aren't in the original brief - what happens
if both sensors are noisy at once, and what happens if a sensor gives an
out-of-range reading. We picked a reasonable behaviour ourselves and wrote
it down in the tests, so it can go in the report as a documented
assumption.

**On mocking:** no mocking library (`pytest-mock`/`unittest.mock`) is used
anywhere in this test suite. Sensors are all small hand-written fakes:
`FixedSensor`, `RandomSensor`, `NoisySensor`, and `SequenceSensor` (returns
a scripted list of readings, used to prove Park's search-forward logic and
5m boundary without needing a mocking framework). The one remaining
skipped case - isEmpty's sensor call-count check - needs a sensor that can
report how many times it was read, which is a better fit for
`pytest-mock`, kept for Phase 2's sensor/actuator stubbing. See
`tests/README.md` for the full breakdown.
