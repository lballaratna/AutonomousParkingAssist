# Cross-Check Report: park() / unpark() Issues

**Date:** 2026-09-17
**Scope:** Four specific issues reported against the earlier partial
implementation of `park()` and `unpark()` in
`autonomous_parking_system/parking_assistant.py`. Each is checked against
the current code, verified with a live run, and marked resolved or open.
Screenshots go in the "Evidence" line of each section — replace the
placeholder text with the actual screenshot once captured.

---

## Issue 1 — `park()` implicitly returned `None`, breaking its `-> CarState` contract

**Originally reported code:**
```python
def park(self) -> CarState:
     if self.is_empty() == 0:
        self.state.status = "parked"
        return self.state
     # <- nothing here: if this condition is False, the function
     #    implicitly returns None, breaking its own -> CarState contract
```

**Current code** (`parking_assistant.py`, lines 73-78):
```python
def park(self) -> CarState:
    if self.state.status == "parked":
        raise ValueError("already parked")
    if self._at_free_stretch():
        self.state.status = "parked"
    return self.state
```

**Check performed:** built a car with sensors reading 100cm (occupied, so
the "not at a free stretch" branch is taken — the exact branch that used
to fall through to an implicit `None`), called `park()`, and inspected
the return value.

**Result:**
```
park() returned: CarState(position=0, status='unparked', records=[])
Type: CarState
PASS: park() returns a real CarState even when no free stretch was found.
```

**Status: RESOLVED.** The `return self.state` now sits outside the `if`
block, so every code path through `park()` returns a `CarState`, honoring
its declared return type. There is no path left that falls through to an
implicit `None`.

**Evidence:** _[screenshot: terminal output of the verification script,
Issue 1 section]_

---

## Issue 2 — `park()` did not reject a second call while already parked

**Originally reported:** `test_park_while_already_parked_is_rejected` was
written and waiting, but the implementation had no check for
`self.state.status == "parked"`, so calling `park()` twice in a row did
not raise, and the test was failing.

**Current code:** the very first line of `park()` is now:
```python
if self.state.status == "parked":
    raise ValueError("already parked")
```

**Check performed:** parked a car once (should succeed), then called
`park()` again on the same car and caught the result.

**Result:**
```
After first park(): status = 'parked'
PASS: second park() raised ValueError: already parked
```

**Test suite confirmation:**
```
tests/test_park.py::test_park_while_already_parked_is_rejected PASSED
```

**Status: RESOLVED.** A second `park()` call is rejected with a clear,
documented exception (case 25 from the official test plan), and the
previously-failing test now passes.

**Evidence:** _[screenshot: pytest output showing
`test_park_while_already_parked_is_rejected PASSED`]_

---

## Issue 3 — `_at_free_stretch()` existed but was dead code (refactor left unfinished)

**Originally reported:** `park()` called `self.is_empty() == 0` directly
instead of calling the already-written `self._at_free_stretch()` helper,
meaning the helper was defined but never actually used anywhere — an
unfinished refactor.

**Current code:**
```python
def park(self) -> CarState:
    if self.state.status == "parked":
        raise ValueError("already parked")
    if self._at_free_stretch():
        self.state.status = "parked"
    return self.state

def _at_free_stretch(self) -> bool:
    return self.is_empty() == 0
```

**Check performed:** inspected `park()`'s live source at runtime
(`inspect.getsource`) and confirmed the call site.

**Result:**
```
if self._at_free_stretch():
    self.state.status = "parked"

PASS: park() calls self._at_free_stretch() - helper is live, not dead code.
```

**Status: RESOLVED.** `park()` now calls the helper instead of
duplicating its logic inline. The refactor step (name the check, keep the
behaviour, verify the test still passes) is complete.

**Evidence:** _[screenshot: the verification script's Issue 3 output, or
the source file itself with both lines visible]_

---

## Issue 4 — `unpark()` was still a stub despite three waiting tests

**Originally reported:** `test_unpark.py` had three real test functions
(`test_unpark_from_parked_state`, `test_unpark_while_not_parked_is_rejected`,
`test_where_is_consistent_after_unpark`) already written, but `unpark()`
itself was `raise NotImplementedError`.

**Current code:**
```python
def unpark(self) -> CarState:
    if self.state.status != "parked":
        raise ValueError("cannot unpark - car is not parked")
    self.state.position += 1
    self.state.status = "unparked"
    return self.state
```

**A second bug found and fixed during this work, worth noting explicitly:**
the first working version of `unpark()` only flipped `status` and did not
move `position`, even though the interface's own docstring says UnPark
should *"move forward (and left) to the front of the parking place."*
The test only checked `status` too, so it passed while silently not
proving the actual requirement. Both the test and the code were corrected
together — `unpark()` now increments `position` by 1, and the tests assert
on both `status` and `position`.

**Check performed:** parked a car, recorded its position, called
`unpark()`, and checked both `status` and `position` before/after.

**Result:**
```
Before unpark: position=0, status='parked'
After unpark:  position=1, status='unparked'
PASS: unpark() is implemented, flips status AND moves position forward.
```

**Test suite confirmation:**
```
tests/test_unpark.py::test_unpark_from_parked_state PASSED
tests/test_unpark.py::test_unpark_while_not_parked_is_rejected PASSED
tests/test_unpark.py::test_where_is_consistent_after_unpark PASSED
```

**Status: RESOLVED** (and improved beyond the original report — the
position bug was an additional, real defect caught and fixed in the same
pass).

**Evidence:** _[screenshot: pytest output showing all three
`test_unpark.py` cases PASSED]_

---

## Full test suite state at time of this check

```
$ python -m pytest tests/ -v
tests/test_park.py::test_parks_immediately_when_already_at_free_stretch PASSED
tests/test_park.py::test_park_searches_forward_when_no_stretch_here SKIPPED
tests/test_park.py::test_boundary_five_metre_stretch_is_accepted SKIPPED
tests/test_park.py::test_four_point_nine_metre_stretch_is_rejected SKIPPED
tests/test_park.py::test_no_stretch_found_anywhere_is_rejected SKIPPED
tests/test_park.py::test_park_while_already_parked_is_rejected PASSED
tests/test_unpark.py::test_unpark_from_parked_state PASSED
tests/test_unpark.py::test_unpark_while_not_parked_is_rejected PASSED
tests/test_unpark.py::test_where_is_consistent_after_unpark PASSED
...
24 passed, 5 skipped in 0.08s
```

The 5 skips are unrelated to these four issues - they're Park's
search-forward logic (cases 21-24) and isEmpty's call-count check (case
19), both deliberately deferred to Phase 2 because they need scripted
sensor control that needs mocking tooling not brought into Phase 1. See
`tests/README.md` for the full reasoning.

**Coverage** (whole suite): `parking_assistant.py` at 99% (statement +
branch) - the one uncovered branch (`76->78`, the "not at a free stretch"
path inside `park()`) is exactly the deferred search-forward logic, not a
gap in what's actually built.

**Evidence:** _[screenshot: full `pytest -v` run, and
`coverage report -m` output]_

---

## Summary

| # | Issue | Status |
|---|---|---|
| 1 | `park()` implicitly returns `None` on the false branch | **Resolved** |
| 2 | `park()` doesn't reject a second call while already parked | **Resolved** |
| 3 | `_at_free_stretch()` defined but unused (dead code) | **Resolved** |
| 4 | `unpark()` still a stub | **Resolved** (plus an additional position bug found and fixed) |

All four originally reported issues are confirmed fixed against the
current code in this repo, verified both by the existing test suite and
by a standalone manual check script. No regressions were introduced
elsewhere - the full suite remains at 24 passed / 5 skipped / 0 failed
both before and after this cross-check.
