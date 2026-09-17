# Why Hari's commit (`6929662`) was not brought into `master`

## What the commit contained

Branch `origin/referencecopy`, commit `6929662` ("Added functionality to
sensor and implemented test cases for move_forward and where_is"),
authored by `harikrishnamr`, changed three files:

- `autonomous_parking_system/sensor.py` — `FixedSensor` was changed from
  always returning the exact value it was constructed with, to returning
  that value **plus a random jitter of ±2** (`value + random.randint(-2, 2)`,
  clamped to 0–200).
- `tests/test_move_forward.py` — reworded docstring, and rewrote the
  parametrized boundary test as two separate loop-based tests.
- `tests/test_where_is.py` — reworded docstring/comments; test bodies
  otherwise equivalent to what was already there.

## The blocking problem: the sensor jitter breaks `park()`

`park()`'s free-space check is exact:

```python
def _at_free_stretch(self) -> bool:
    return self.is_empty() == 0
```

Every test that needs a guaranteed "free stretch" sets up the car with
`FixedSensor(0)` (6 places, across `test_where_is.py`, `test_park.py`,
`test_unpark.py`), relying on `FixedSensor(0)` reliably returning `0`.

Once `FixedSensor` jitters by ±2, `FixedSensor(0).read()` returns `0`,
`1`, or `2` at random (clamped, so never negative). `is_empty()` averages
5 reads from each sensor, so it is *usually* still `0`, but not always —
which makes `_at_free_stretch()` intermittently `False` when the test
expects the car to park.

Confirmed empirically: running the full suite repeatedly with the jitter
applied produced random, non-deterministic failures in
`test_where_is.py::test_status_parked_after_park` (and, by the same
mechanism, was a latent risk in `test_park.py` and `test_unpark.py`
too) — sometimes 24/24 passing, sometimes one of these failing, purely
depending on the random draw.

This is a flaky test, not a wrong test: the assumption `FixedSensor(0)`
== "guaranteed empty" is baked into the current `park()`/`unpark()`
design and into 6 existing test setups. Fixing it properly would mean
either loosening `_at_free_stretch()` to a tolerance (`is_empty() <= 2`
or similar) or keeping the sensor deterministic — both are real design
decisions, not something to silently pick while pulling in an unrelated
teammate's commit.

## Why "keep it deterministic" is the right call, not just the easy one

Checked against the two authoritative course documents:

- `Project_instructions.pdf` (the actual graded Phase 1 spec) says,
  under sensor inputs: *"You can assume random or fixed sensor inputs in
  this phase... The sensor inputs (for a properly working sensor) are
  integers (in the range of 0 to 200)."* There is no requirement that a
  "fixed" sensor behave with jitter — a `FixedSensor` returning a fixed
  value is exactly what the spec allows, and is what the existing
  `RandomSensor`/`NoisySensor` classes already cover for the
  non-deterministic case.
- `Testing_project.pdf` confirms Phase 1 is TDD/JUnit unit testing of
  exactly these interfaces (`MoveForward`, `isEmpty`, `MoveBackward`,
  `Park`, `UnPark`, `WhereIs`), with **mocking reserved for Phase 2**
  ("Integration Testing (Mocking)", due October 2). Making a previously
  deterministic test double behave probabilistically works against the
  whole point of a fixed test double in Phase 1 — it's the kind of
  scenario Phase 2's mocking tools exist to handle properly, not
  something to bolt onto `FixedSensor` now.

So: `FixedSensor` returning jittered values isn't wrong on its own, but
it directly contradicts the deterministic-sensor-doubles approach the
team already committed to for Phase 1 (see
`CLAUDE_SESSION_HANDOFF.md`), and it introduces flakiness into a test
suite that was previously fully deterministic (`24 passed, 5 skipped, 0
failed`, reliably, every run).

## What was actually done

- Cherry-picked only Hari's own commit's diff (not the rest of the
  `referencecopy` branch, most of which duplicates work already on
  `origin/main`/local `master`), then reverted it in full after the
  regression above was found — `sensor.py`, `test_move_forward.py`, and
  `test_where_is.py` are all back to their pre-Hari state.
- Verified by running `pytest tests/ --ignore=tests/AutonomousParkingAssist`
  five times in a row before the jitter change (stable), and three more
  times after reverting it (stable) — `24 passed, 5 skipped, 0 failed`
  every time.

## If the team still wants Hari's sensor idea

Worth raising with Hari and the team directly (per
`CLAUDE_SESSION_HANDOFF.md`'s existing note about conflicts needing a
real conversation, not a silent pick): the jitter idea is reasonable
*if* `_at_free_stretch()` is deliberately changed to tolerate it (e.g.
"empty" means `is_empty() <= 2`, not `== 0`), and that tolerance itself
becomes a documented, tested requirement rather than an accidental side
effect. That's a design change to production logic, not a drop-in
sensor tweak, so it should be a team decision made together — not
something merged in from one person's branch unreviewed.
