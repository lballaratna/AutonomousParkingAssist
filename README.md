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
├── sensor.py              fake sensors (fixed, random, noisy, scripted, counting) standing in for real hardware
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
are implemented. All 33 test cases pass - none skipped. The project
instructions originally define 29 of those; the other 4 are our own
additions (proving the reverse-parking distance, the two "wall" scenarios,
and that `RandomSensor` behaves), folded into the same 1-33 numbering
rather than kept as an unnumbered side list - see `tests/README.md` for
exactly which case number is which.

**Decisions we made that aren't in the project instructions** (documented
assumptions, not requirements we missed):
- isEmpty: what happens if both sensors are noisy at once, and what
  happens if a sensor gives an out-of-range reading.
- Park: a free stretch is measured as consecutive whole metres where
  isEmpty() reads 0, since the project instructions describe the 5m
  requirement but not how a single-position sensor reading (max 2m range)
  is meant to add up to that over multiple metres.
- Park: once a qualifying stretch is found, the car reverses
  `STRETCH_REQUIRED - 1` metres back into it before parking - modelling
  the "standard parallel reverse parking maneuver" the project
  instructions mention, but don't spell out in terms of exact distance.
- UnPark: because of the above, UnPark now drives forward by
  `STRETCH_REQUIRED - 1` (not a flat 1) to reach the front of the space -
  the distance a straight `+1` covered before Park actually reversed into
  the space.
- The car only senses forward/backward along the street; there's no
  lateral state, so an obstacle on the *opposite* side of the car from the
  parking space isn't modelled at all.

**On mocking:** no mocking library (`pytest-mock`/`unittest.mock`) is used
anywhere in this test suite. Sensors are all small hand-written fakes:
`FixedSensor`, `RandomSensor`, `NoisySensor`, `SequenceSensor` (returns a
scripted list of readings, used to prove Park's search-forward logic and
5m boundary), and `CountingSensor` (wraps another sensor and counts its
`read()` calls, used to prove isEmpty's 5-queries-per-sensor requirement).
Every official test case now passes without a mocking framework. See
`tests/README.md` for the full breakdown.
