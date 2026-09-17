# Phase 1 Report — Autonomous Parking Assist

Course: DT8067, Networks and Testing for Embedded Systems
Phase 1 deadline: September 18, 2026
This report follows the structure asked for in the Phase 1 instructions
(Objectives, Part 1: Interface and Test Design, Part 2: Test-Driven
Development) and is checked only against the two official documents:
the course slide deck (`Testing_project.pdf`) and the detailed Phase 1
instructions (`Project_instructions.pdf`).

---

## Objectives

The instructions list four things Phase 1 is meant to apply:

- Interface design
- Test-Driven Development
- Functional test design
- Unit Testing and the JUnit tool

The brief asks for Java and jUnit specifically. We built this in Python
with pytest instead. This was checked with the instructor and approved -
**this needs a screenshot/record of that approval added here**, since the
brief's own wording is Java-only with no hedge.

**Evidence:** _[screenshot: instructor approval for Python/pytest]_

---

## Description of the Unit

Straight from the instructions: the car moves along a 500m straight
street and registers free parking places on its right-hand side using
two ultrasound sensors. The readings are combined and filtered to find a
free stretch of 5 metres, then the car parks with a standard reverse
parallel maneuver.

Six methods, exactly as named in the instructions:

- **MoveForward** - moves 1m forward, queries isEmpty, returns a data
  structure with the current position and the parking situation so far.
  Cannot move past the end of the street.
- **isEmpty** - queries both sensors at least 5 times, filters the
  noise, returns the distance in cm to the nearest object on the right.
  A continuously noisy sensor gets completely disregarded.
- **MoveBackward** - same as MoveForward, backward. Cannot move behind
  the start of the street.
- **Park** - runs the parking maneuver if already at a free stretch, or
  drives forward until one is found, then parks.
- **UnPark** - moves forward (and left) to the front of the space, if
  parked.
- **WhereIs** - returns current position and (un)parked status.

Sensors and actuators are not modeled - we assume random or fixed
sensor inputs, integers in 0-200cm.

---

## Part 1: Interface and Test Design

### Data structures

Two small data classes, no logic in either:

```python
Status = Literal["moving", "parked", "unparked"]

class ParkingRecord:
    position: int
    distance_cm: Optional[int]   # one isEmpty() reading, tied to a position

class CarState:
    position: int = 0
    status: Status = "unparked"
    records: List[ParkingRecord] = []
```

`CarState` is the class's internal state - position, whether it's
parked, and the history of readings. This is what needs to be available
at all times for the class to work.

### The class and its methods

```python
class ParkingAssistant:
    def __init__(self, sensor_left: Sensor, sensor_right: Sensor):
        ...
```

No method takes any extra parameters beyond `self` - the constructor is
the only place inputs come in (the two sensors), everything else reads
or updates `self.state`.

| Method | Parameters | Return type |
|---|---|---|
| WhereIs | none | CarState |
| MoveForward | none | CarState |
| MoveBackward | none | CarState |
| isEmpty | none | int |
| Park | none | CarState |
| UnPark | none | CarState |

### Interface specification

For each method: Description, Pre-condition, Post-condition, Test-cases -
as asked for in the instructions. These now live directly in
`autonomous_parking_system/interface.py` as docstrings on each abstract
method. Reproduced here for the report:

**WhereIs**
- Description: return current position and parked/unparked status.
- Pre-condition: none.
- Post-condition: state is unchanged, just reported back.
- Test-cases: a, b, c, d (tests/test_where_is.py)

**MoveForward**
- Description: move 1m forward, query is_empty(), record the result.
  Must not move past STREET_LENGTH.
- Pre-condition: none.
- Post-condition: if position < 500, position goes up by 1 and a new
  reading gets recorded; if position == 500, nothing changes (rejected,
  no-op).
- Test-cases: a, b, c, d (tests/test_move_forward.py)

**MoveBackward**
- Description: move 1m backward, query is_empty(), record the result.
  Must not move before position 0.
- Pre-condition: none.
- Post-condition: if position > 0, position goes down by 1 and a new
  reading gets recorded; if position == 0, nothing changes (rejected,
  no-op).
- Test-cases: a, b, c, d (tests/test_move_backward.py)

**isEmpty**
- Description: query both sensors >=5 times, filter noise, disregard a
  continuously noisy sensor, return distance in cm (0-200).
- Pre-condition: none.
- Post-condition: returns an int in 0-200 if at least one sensor is not
  noisy; raises an error if both sensors are noisy at the same time
  (not mentioned in the requirement - our own decision).
- Test-cases: a, b, c, d, e, f, g, and the call-count case (tests/test_is_empty.py)
  - the call-count case is covered in Phase 2.

**Park**
- Description: park at the current position if it's at a free stretch of
  5 meters, otherwise drive forward searching for one, then park.
- Pre-condition: car must not already be parked.
- Post-condition: status becomes "parked" once a qualifying stretch is
  found; raises an error if Park is called while already parked (not
  mentioned in the requirement - our own decision).
- Test-cases: case 20, case 25 (tests/test_park.py) - built for Phase 1.
  Cases 21-24 (searching forward, the exact 5m boundary, no stretch found
  anywhere) are skipped for now, covered in Phase 2.

**UnPark**
- Description: move forward (and left) to the front of the parking
  place. Only valid while status=="parked".
- Pre-condition: car must be parked.
- Post-condition: position moves forward by 1 and status becomes
  "unparked"; raises an error if UnPark is called while not parked (the
  requirement only says what happens "if it is parked" - it doesn't say
  what to do otherwise, so this is our own decision).
- Test-cases: case 26, 27, 28 (tests/test_unpark.py)

### Functional test design technique

The instructions say to use one of the functional testing methods,
preferably classification tree or decision table.

We used a decision table for isEmpty, since it has two conditions that
aren't independent (is sensor A noisy, is sensor B noisy) - a decision
table is the natural fit there. For the other five methods we used
boundary value testing (MoveForward/MoveBackward have hard limits at
both ends of the street) and state-based/state-transition cases
(WhereIs/Park/UnPark, since they're about what state the car is in and
which transitions are legal). These aren't the two preferred techniques,
but they're a reasonable fit for methods that are really about a single
ordered range with two edges, or about legal/illegal state changes,
rather than several interacting conditions - a classification tree for
MoveForward would really just redraw the same two boundaries.

### Test suite

All 28 official test cases, input values and expected outputs:

**WhereIs**
| Case | Input / scenario | Expected output |
|---|---|---|
| a | fresh car, before any movement | position=0, status="unparked" |
| b | after 2x MoveForward | position=2 |
| c | right after a successful Park | status="parked" |
| d | right after UnPark | status="unparked" |

**MoveForward**
| Case | Input / scenario | Expected output |
|---|---|---|
| a | position=0 | position=1 |
| b | position=499 | position=500 |
| c | position=500 (already at end) | position stays 500 |
| d | any successful move | a reading gets recorded |

**MoveBackward**
| Case | Input / scenario | Expected output |
|---|---|---|
| a | position=500 | position=499 |
| b | position=1 | position=0 |
| c | position=0 (already at start) | position stays 0 |
| d | any successful move | a reading gets recorded |

**isEmpty**
| Case | Input / scenario | Expected output |
|---|---|---|
| a | both sensors clean, e.g. 50cm and 52cm | filtered average (between 50-52) |
| b | left noisy, right=80cm | 80 |
| c | right noisy, left=80cm | 80 |
| d | both noisy | raises an error |
| e | reading=0cm | accepted as valid |
| f | reading=200cm | accepted as valid |
| g | reading=250cm (out of range), other=80cm | 80 (out-of-range one disregarded) |
| call-count | wrap both sensors, call isEmpty once | each sensor read >=5 times (Phase 2) |

**Park**
| Case | Input / scenario | Expected output |
|---|---|---|
| 20 | already at a free stretch (0cm both sensors) | status becomes "parked" |
| 21 | no stretch here, one exists ahead | drives forward until found (Phase 2) |
| 22 | exactly 5.0m free | accepted (Phase 2) |
| 23 | 4.9m free | rejected, search continues (Phase 2) |
| 24 | no stretch anywhere on the street | search stops (Phase 2) |
| 25 | Park called while already parked | raises an error |

**UnPark**
| Case | Input / scenario | Expected output |
|---|---|---|
| 26 | car is parked | status="unparked", position moves forward by 1 |
| 27 | car is not parked | raises an error |
| 28 | UnPark then WhereIs | WhereIs shows the same updated status and position |

---

## Part 2: Test-Driven Development

Every method below was built the same way: write the test, run it, watch
it fail (red), add just enough code to pass (green), then clean up if
needed (refactor). Each line added is commented in
`parking_assistant.py` with which test case it satisfies.

### WhereIs

**Red:**
```
$ pytest tests/test_where_is.py -v
```
_[screenshot: all four WhereIs tests failing before implementation, error = NotImplementedError]_

**Green** - the whole method is one line, since `CarState` already holds
the answer to all four cases:
```python
def where_is(self) -> CarState:
    # case a/b/c/d: a pure query, CarState already holds the answer.
    return self.state
```

**Refactor:** nothing to clean up - already as simple as it gets.

**Result:**
```
$ pytest tests/test_where_is.py -v
```
_[screenshot: all four WhereIs tests passing]_

### MoveForward

**Red:** wrote the four cases in `tests/test_move_forward.py`, ran them,
all failed with NotImplementedError.

_[screenshot: test_move_forward.py failing before implementation]_

**Green**, one line at a time, each tied to the case that forced it:
```python
def move_forward(self) -> CarState:
    # case c: at the upper boundary, no-op and return unchanged.
    if self.state.position >= self.STREET_LENGTH:
        return self.state
    # case a/b: ordinary move and boundary-minus-one both advance by 1.
    self.state.position += 1
    # case d: every successful move records an isEmpty() reading.
    reading = self.is_empty()
    self.state.records.append(ParkingRecord(self.state.position, reading))
    return self.state
```

**Refactor:** none needed - the method already reads as one idea per
line.

**Result:**
_[screenshot: test_move_forward.py passing, all 4 tests green]_

### MoveBackward

**Red:** same shape as MoveForward, mirrored at the other end of the
street.

_[screenshot: test_move_backward.py failing before implementation]_

**Green:**
```python
def move_backward(self) -> CarState:
    # case c: at the lower boundary (position 0), no-op.
    if self.state.position <= 0:
        return self.state
    # case a/b: ordinary move and boundary-plus-one both retreat by 1.
    self.state.position -= 1
    # case d: every successful move records an isEmpty() reading.
    reading = self.is_empty()
    self.state.records.append(ParkingRecord(self.state.position, reading))
    return self.state
```

**Result:**
_[screenshot: test_move_backward.py passing, all 4 tests green]_

### isEmpty

**Red:** wrote all 7 cases plus the call-count case in
`tests/test_is_empty.py` - the highest-complexity method, since it has
to combine two sensors and decide which one (if either) to trust.

_[screenshot: test_is_empty.py failing before implementation]_

**Green**, built up case by case:
```python
def is_empty(self) -> int:
    # call-count case: >=5 queries per sensor.
    left = [self.sensor_left.read() for _ in range(5)]
    right = [self.sensor_right.read() for _ in range(5)]
    left_noisy = self._is_noisy(left)
    right_noisy = self._is_noisy(right)

    # case b: left noisy, right clean - disregard left.
    if left_noisy and not right_noisy:
        return self._average(right)
    # case c: mirror of case b.
    if right_noisy and not left_noisy:
        return self._average(left)
    # case a: both clean - average the two.
    if not left_noisy and not right_noisy:
        return (self._average(left) + self._average(right)) // 2

    # case d: both noisy at once - not specified by the brief, our own
    # decision: refuse to guess rather than average two bad readings.
    raise ValueError("both sensors are continuously noisy - reading unreliable")

def _is_noisy(self, readings) -> bool:
    # case g: out-of-range reading treated as noisy - not specified by
    # the brief, our own decision.
    if any(r < 0 or r > 200 for r in readings):
        return True
    # case e/f: exact 0/200cm edges must NOT be flagged as noisy - only
    # the spread across the 5 readings matters here, not the raw value.
    return max(readings) - min(readings) > self.NOISE_THRESHOLD
```

**Refactor:** pulled the noise check and the averaging into
`_is_noisy()`/`_average()` helpers once the four branches above were all
green, so the decision logic reads as one idea per line instead of one
long conditional.

**Result:**
_[screenshot: test_is_empty.py passing - 7 of 8 tests green, 1 skipped (call-count, Phase 2)]_

### Park

**Red:** wrote case 20 and case 25 in `tests/test_park.py`.

_[screenshot: test_park.py failing before implementation]_

**Green:**
```python
def park(self) -> CarState:
    # case 25: reject a second park() call while already parked.
    if self.state.status == "parked":
        raise ValueError("already parked")
    # case 20: if already at a qualifying free stretch, park immediately.
    if self._at_free_stretch():
        self.state.status = "parked"
    return self.state

def _at_free_stretch(self) -> bool:
    return self.is_empty() == 0
```

**Refactor:** named the free-stretch check as its own method
(`_at_free_stretch`) once case 20 was green, so the behaviour is easier
to read and easier to extend later.

**Not built yet:** cases 21-24 (search forward, the exact 5m boundary,
no stretch found anywhere) - the instructions describe Park as "runs the
maneuver if already at a stretch, **or** moves forward until one is
detected." We've only built the first half. Testing the second half
needs a sensor that can give a *sequence* of different readings over
time (a single reading only reaches 200cm, but the stretch requirement
is 500cm) - which needs mocking tooling we're keeping for Phase 2, per
the actual course schedule (Phase 2 is explicitly "Integration Testing
(Mocking)").

**Result:**
_[screenshot: test_park.py - 2 passing, 4 skipped, 0 failing]_

### UnPark

**Red:** wrote all three cases in `tests/test_unpark.py`.

_[screenshot: test_unpark.py failing before implementation]_

**Green:**
```python
def unpark(self) -> CarState:
    # case 27: reject unparking a car that isn't parked - the brief only
    # says what UnPark does "if it is parked," so this is our own decision.
    if self.state.status != "parked":
        raise ValueError("cannot unpark - car is not parked")
    # case 26/28: move forward to the front of the space, flip status back.
    self.state.position += 1
    self.state.status = "unparked"
    return self.state
```

**A mistake we caught along the way, worth noting here:** the first
version of this method only flipped `status` and never actually moved
`position`, even though the requirement explicitly says "moves the car
forward... to front of the parking place." The test only checked
`status` too at first, so it passed without proving the actual
requirement. Once noticed, both the test and the code were fixed
together - the test now checks `position` moved forward by 1 as well as
`status`.

**Result:**
_[screenshot: test_unpark.py passing, all 3 tests green]_

---

## Assumptions we made (not specified in the requirement)

Four places where the brief doesn't say what should happen, and we made
a call:

1. **isEmpty, both sensors noisy at once** - raise an error instead of
   guessing. A falsely "empty" reading is the failure mode that could
   actually cause a collision.
2. **isEmpty, a reading outside 0-200cm** - treated the same as a noisy
   reading, disregarded.
3. **Park, called while already parked** - rejected with an error.
4. **UnPark, called while not parked** - rejected with an error, same
   reasoning as #3 for consistency.

---

## Where things stand right now

```
$ pytest -v
```
_[screenshot: full test run - 24 passed, 5 skipped, 0 failed]_

```
$ python -m coverage run -m pytest
$ python -m coverage report -m
```
_[screenshot: coverage report]_

5 test cases are skipped, all deliberately, all for the same reason -
they need scripted/counted sensor control that needs a mocking tool
(pytest-mock/unittest.mock), and the course's own schedule puts mocking
in Phase 2, not Phase 1:

- isEmpty's call-count check
- Park's search-forward, the 5m boundary (both sides), and the
  no-stretch-found case

No mocking library is used anywhere in this Phase 1 code - every
passing test uses only FixedSensor, RandomSensor, or NoisySensor, which
is what the brief itself says we can assume ("random or fixed sensor
inputs").

---

## Still to add before submission

- [ ] Screenshot of the instructor's approval to use Python instead of Java
- [ ] All the `[screenshot: ...]` placeholders above, filled in with real
      terminal output
- [ ] Zip the source (`autonomous_parking_system/`, `tests/`,
      `pyproject.toml`, `requirements.txt`), extract it somewhere clean,
      run `pip install -r requirements.txt && pytest` to confirm nothing's
      missing
