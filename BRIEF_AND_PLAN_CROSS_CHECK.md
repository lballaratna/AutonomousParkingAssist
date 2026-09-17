# Cross-Check: Original Brief + Reference Document vs. Actual Implementation

**Date:** 2026-09-17
**Sources checked:**
1. `D:\Learning_with_clarity\Testing_project.pdf` — the actual course slide deck (Wojciech Mostowski, DT8067, 2026-09-02). This is the **authoritative brief**.
2. `D:\Learning_with_clarity\AutonomousParkingSystem\Testing_Stack_Rationale.pdf` — the team's own detailed reference document, written to interpret and expand on the brief.
3. The current code and tests in `E:\AutonomousParkingAssist`.

**Important caveat, stated up front:** the actual brief (source 1) is five slides and does not contain the specific numbers this project is built around — no "500m street," no "5m stretch," no "0–200cm sensor range," no method names like `WhereIs`/`Park`/`UnPark`. Slide 2 says the detailed description lives "on Blackboard, the Software Testing Project section" — a document I do not have access to in this session. Everything specific has been cross-checked against the team's own reference document (source 2) instead, since that is the only detailed spec available to me. **I cannot independently verify that source 2 accurately reflects the real Blackboard text** — that verification has to happen on your end, by comparing source 2 against the actual Blackboard page. Screenshots of that Blackboard page would be good evidence to add here.

---

## Part A — Cross-check against the actual brief (`Testing_project.pdf`)

| Brief statement (verbatim or close) | What it requires | Current state | Verdict |
|---|---|---|---|
| "Control software for an autonomous parking system" | Build the decision-logic software | `autonomous_parking_system/` package exists, five files, all working | **Aligned** |
| "test-driven development in Java using jUnit" | TDD, in Java, with jUnit | Built in **Python** with **pytest** instead | **Documented deviation** — see below |
| "integration testing using Mockito" | Mockito for integration testing | No Mockito/mocking library used yet anywhere in this repo | **Not yet due** — this line applies to Phase 2, not Phase 1 (confirmed by the schedule slide, see Part A.3) |
| "Detailed description on Blackboard" | — | Not available to me in this session | **Unverifiable from here** — you have access to Blackboard, I don't |
| Phase 1: "TDD of the autonomous parking module with the following interfaces: Receiving and filtering ultrasound sensor data, Detecting free spaces while moving along a street, Park and Unpark" | Three functional areas | Maps to: `isEmpty` (sensor filtering), `WhereIs`/`MoveForward`/`MoveBackward` (free-space detection while moving), `Park`/`UnPark` | **Aligned** — six methods cleanly group into the brief's three stated areas |
| "Test design, TDD, jUnit" (Phase 1 line) | Functional test design + TDD process, jUnit-equivalent | Test design done (28 official cases derived before code), TDD process followed method-by-method, pytest used as the jUnit-equivalent | **Aligned**, with the Java→Python substitution noted below |
| "Phase 1: TDD of a Unit: September 18" | Deadline | Matches every date referenced in this project's own docs (README, QA.md) | **Aligned** |
| "Phase 2: Integration Testing (Mocking): October 2" | Mocking is explicitly a **Phase 2** activity in the schedule itself | Zero mocking-library imports anywhere in current Phase 1 code; five test cases (isEmpty's call-count check, Park's search/boundary logic) are deliberately deferred to Phase 2 rather than pulling mocking in early | **Strongly aligned** — this is the single clearest piece of evidence that deferring mocking was the right call, not just an internal team decision. The brief's own schedule slide ties "Mocking" to Phase 2 by name. |
| "Project examinations: starting October 5... questions about the project and the testing lectures contents will be asked" | Oral exam covers both the project and lecture material generally | `QA.md` in this repo is structured exactly this way — project-specific sections (5–10) plus lecture-content sections (1–3, testing theory) | **Aligned** |

### A.1 — The Java → Python substitution: what's actually verified vs. asserted

The brief's own words are unambiguous: **"test-driven development in Java using jUnit."** There is no hedge, no "or equivalent," nothing. Every document in this project (the reference doc, the README, `QA.md`) states that this was raised with the instructor and approved. I want to be precise about what I can and can't confirm:

- **I cannot verify the approval actually happened.** No email, Blackboard screenshot, or other artifact showing instructor sign-off exists anywhere in the files I have access to. The reference document simply asserts it ("The instructor has confirmed this is acceptable") without citing evidence.
- **This is the single highest-risk item in the whole project** if the approval is not real or not documented somewhere the grader can see. Every line of Python code, every pytest test, is a direct contradiction of the literal brief text unless that approval is real and demonstrable.

**Recommendation:** before submission, locate and screenshot whatever record exists of this approval (an email thread, a Blackboard announcement, a forum post reply from the instructor) and include it directly in the report. If no such record exists, this needs to be resolved with the instructor before Phase 1 is submitted, not mentioned as an assumption after the fact.

**Evidence:** _[screenshot: the actual approval — email, Blackboard message, or forum thread]_

### A.2 — What the brief does *not* specify, that this project had to invent

Being strict about only what's in `Testing_project.pdf`: it does not mention EclEmma, coverage tools, "or similar tools" hedging language, specific method names, or any numeric parameters. All of that — which this project's tests and code rely on heavily — comes from the team's own reference document. This isn't necessarily a problem (the reference document may accurately reflect the real Blackboard text), but it means:

- If the Blackboard detailed description differs from `Testing_Stack_Rationale.pdf` in any specific number (street length, stretch requirement, sensor range, query count), the current implementation would need to change to match the real numbers, not the reference document's numbers.
- This is worth a direct side-by-side check on your end: open the Blackboard page and confirm the reference document's Requirement Analysis table (§3) and Appendix (§14) match it exactly.

**Evidence:** _[screenshot: the Blackboard "Software Testing Project" detailed description page, for direct comparison against Testing_Stack_Rationale.pdf §3 and §14]_

---

## Part B — Cross-check against the team's own reference document (`Testing_Stack_Rationale.pdf`)

This section checks the actual code and tests against the detailed plan the team wrote for itself. Structured by the reference document's own section numbers.

### §2–3 — Decision record & requirement analysis

The Python decision and its reasoning are recorded in the reference doc and repeated in this repo's `README.md`. **No code-level check applies here** — this is a documentation/process item. Covered by A.1 above.

### §5 — Language & tooling comparison, tool mapping table

| Brief tool | Doc's Python equivalent | Actually used in this repo? |
|---|---|---|
| JUnit | `pytest` | Yes — `requirements.txt`, all test discovery via `test_*.py` |
| EclEmma | `coverage.py` + `pytest-cov` | Yes — `pyproject.toml` has `[tool.coverage.run]` configured, verified working (`python -m coverage report -m`) |
| Mockito | `unittest.mock` / `pytest-mock` — **filed under Phase 2** in the doc's own table | Correctly absent from Phase 1 — confirmed doubly aligned now that Part A.3 shows the actual brief schedule also calls Phase 2 "Integration Testing (Mocking)" |
| Java `interface` | `abc.ABC` | Yes — `interface.py` |

**Status: Fully aligned.**

**One specific item from §5 not yet done:** the doc names `radon cc` / `flake8 --max-complexity=10` as the tool for verifying cyclomatic complexity stays under 10 per method (this is repeated as a target in §7). **This has not been run in this session.** `isEmpty` is the method most likely to be near the limit (it's flagged in the doc itself as "our highest-complexity method"). I did not install or run `radon`/`flake8` without asking first, since that would add a new dependency.

**Recommendation:** run `pip install radon && radon cc autonomous_parking_system/parking_assistant.py -s` (or `flake8 --max-complexity=10`) and add the output here.

**Evidence:** _[screenshot: radon or flake8 complexity output for parking_assistant.py]_

### §6 — Functional testing, technique naming

The doc's own "Report tip" (§6) says explicitly: *"Name the exact technique behind each pytest case — 'Strong Robust EC on the sensor pair' is a stronger oral-defense answer than 'we thought of this case.'"*

**Checked against actual test file docstrings in this repo:** the six `tests/test_*.py` files state the **requirement** and the **scenario/expected result** clearly, but do **not** name the specific technique (Boundary Value, Strong Robust EC, Decision Table, State Transition) inline in the test file comments themselves. That naming currently only exists in `QA.md`, not in the test files a grader would open first.

**Status: Partial gap.** Not incorrect, but the doc's own explicit recommendation isn't fully carried into the test file comments.

**Recommendation:** consider adding a one-line technique tag to each test file's header docstring (e.g., "Technique: Boundary Value + State Transition") to match the doc's own advice.

### §7 — Structural testing, coverage

Current full-suite coverage (`autonomous_parking_system/*`):

```
Name                                             Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------------------------------
autonomous_parking_system\__init__.py                5      0      0      0   100%
autonomous_parking_system\interface.py              17      0      0      0   100%
autonomous_parking_system\parking_assistant.py      59      0     18      1    99%   76->78
autonomous_parking_system\sensor.py                 14      1      0      0    93%   18
autonomous_parking_system\state.py                  12      0      0      0   100%
--------------------------------------------------------------------------------------------
TOTAL                                              107      1     18      1    98%
```

**A specific, concrete finding worth flagging directly:** the one branch gap (`76->78` in `parking_assistant.py`) is inside `park()` — it's the path where `_at_free_stretch()` returns `False` and the car is *not* parked. I checked this precisely: **no pytest test in the current suite exercises this path.** This is exactly the scenario from the original bug report (Issue 1 — `park()` on a car with no free stretch), and while I verified by hand (a standalone script, not a pytest test) that the fix works correctly, **the automated regression suite does not lock this behavior in.** If someone reintroduces the original bug (implicit `None` return) later, the current test suite would not catch it.

**Status: Real, actionable gap.** The doc's own §9 callout says: *"if coverage.py shows a gap after implementing these 28 cases, that's a scenario this table missed, not a case to skip."* This gap should be closed with a real test, not left as a known coverage shortfall.

**Recommendation:** add a test like:
```python
def test_park_does_not_park_when_no_free_stretch():
    car = ParkingAssistant(FixedSensor(100), FixedSensor(100))
    result = car.park()
    assert result.status == "unparked"
```

**Evidence:** _[screenshot: coverage report -m output, and the new test once added, passing]_

Also flagged: `sensor.py` line 18 (`RandomSensor.read()`) is uncovered — no test in the suite exercises `RandomSensor` at all. Low risk (one line, trivial logic), but worth knowing.

### §8 — The TDD process, build order

The doc specifies build order: WhereIs → MoveForward/MoveBackward → isEmpty → Park → UnPark, and its own worked example for Park (case 20) demonstrates using `monkeypatch` to stub `is_empty()` so Park's owner isn't blocked waiting on isEmpty's owner.

**Checked against actual `test_park.py`:** the current test (`test_parks_immediately_when_already_at_free_stretch`) does **not** use `monkeypatch` — it constructs a real `ParkingAssistant` and lets `park()` call the *real* `is_empty()` directly. This works today because `is_empty()` is already fully implemented, but it means the specific technique the reference document highlights as important ("the monkeypatch line matters as much as the test itself") isn't actually demonstrated anywhere in the current test suite.

**Status: Functional but methodologically different from the documented example.** Not a defect — since one person effectively built all six methods in this repo rather than three people in parallel, the original reason for `monkeypatch` (not blocking on a teammate) doesn't apply the same way. But if asked in the oral exam to point at where `monkeypatch`/stubbing-a-not-yet-built-dependency was used, the honest answer is: it wasn't needed in practice here, even though the reference document describes it as the core technique for cross-method dependencies.

### §9 — Complete test plan, case by case

Full case-by-case status, matched precisely against the doc's own numbered table:

| Case(s) | Method | Status |
|---|---|---|
| 1, 2 | WhereIs | PASS |
| 3 | WhereIs | PASS — but only checks `status`, not `position`, despite the doc's case 3 saying "status='parked', **position** = the parking-spot start" |
| 4 | WhereIs | PASS — same gap: only checks `status`, not `position`. (The position check *does* exist, but in `test_unpark.py`'s case 28 instead, not in `test_where_is.py`'s own case 4.) |
| 5, 6, 7 | MoveForward | PASS |
| 8, 9, 10 | MoveBackward | PASS |
| 11 | MoveForward/MoveBackward | PASS (tested once per direction — two test functions for one documented case, which is reasonable but means the physical test count doesn't map 1:1 to the doc's case numbering) |
| 12, 13, 14 | isEmpty | PASS |
| 15 | isEmpty | PASS — but occasionally flaky (~1 run in 5), see below |
| 16, 17, 18 | isEmpty | PASS |
| 19 | isEmpty | **SKIPPED**, deferred to Phase 2 |
| 20 | Park | PASS |
| 21, 22, 23, 24 | Park | **SKIPPED**, deferred to Phase 2 |
| 25 | Park | PASS |
| 26, 27, 28 | UnPark | PASS |

**23 of 28 official cases fully passing; 5 deliberately deferred; 0 failing.**

**On case 3/4's missing position check:** minor, but worth fixing for completeness against the doc's own stated expected results — case 3 and case 4 both explicitly mention position in the doc's table, and `test_where_is.py`'s versions of these two cases only check status.

**On case 15's flakiness:** confirmed during this session — running `test_both_sensors_noisy` repeatedly showed it can fail by chance (~1 in 5 runs) because two independent `NoisySensor()` instances occasionally produce readings that happen to look non-noisy by coincidence. This was fixed once already (with a scripted deterministic sensor), then reverted when Park's search-logic and mocking-dependent tests were rolled back for consistency. It remains a known, accepted flaky test right now.

**On §9's explicit coverage-target callout:** *"Every method above should reach 100% DD-path coverage from this table alone... that's a scenario this table missed, not a case to skip."* The current approach — skipping 5 cases outright rather than implementing them — is a direct, conscious departure from this specific instruction. This was a deliberate scope decision (confirmed with you directly in this session: defer Park's search logic and the mocking-dependent cases to Phase 2), not an oversight, and it's now doubly justified by Part A.3 above (the actual brief's schedule literally puts "Mocking" in Phase 2). Worth stating this reasoning explicitly in the report, since a grader reading the doc's own words might otherwise expect all 28 cases to be green.

**Evidence:** _[screenshot: full `pytest -v` output showing 24 passed, 5 skipped, 0 failed]_

### §10 — Real-world grounding

Documentation-only section; no code to cross-check. Content is reused accurately in `QA.md`.

### §11 — Interface design & class skeleton

| Doc requirement | Current state |
|---|---|
| `abc.ABC` + `@abstractmethod`, not `typing.Protocol` | Matches — `interface.py` |
| Two-class split (interface stays abstract; `ParkingAssistant` implements with `NotImplementedError` stubs initially, so it's instantiable from day one) | Matches the *original* skeleton; all six stubs have since been replaced with real logic, which is the expected next stage, not a deviation |
| `STREET_LENGTH`, `STRETCH_REQUIRED` live on the interface | Matches — `interface.py` lines with `STREET_LENGTH = 500`, `STRETCH_REQUIRED = 5` |
| Folder structure exactly as listed (`autonomous_parking_system/`, `tests/`, `pyproject.toml`, `requirements.txt`, `.gitignore`) | Matches exactly |
| `pyproject.toml` config (`pythonpath`, coverage `branch = true`, `source`) | Matches |
| `requirements.txt` (pytest, pytest-cov, pytest-mock) | Matches |
| Naming note: brief uses PascalCase (`MoveForward`); doc recommends snake_case (`move_forward`) with the choice documented once in the report | Code correctly uses snake_case throughout. **The documented-assumption part is missing** — I did not find this specific naming-convention note written anywhere in `README.md` or `tests/README.md` in this repo. |
| Stub vs Mock definitions (§11) | `FixedSensor`/`RandomSensor`/`NoisySensor` are correctly stubs (canned answers, no call tracking) — consistent throughout |

**Status: Aligned, with one small documentation gap** (the PascalCase→snake_case naming assumption isn't written down anywhere a grader would see it).

**Recommendation:** add one sentence to `README.md`: *"The brief writes method names in PascalCase (e.g. MoveForward); this implementation uses Python's snake_case convention (move_forward) throughout — a naming-convention choice, not a behavioral one."*

### §12 — Risk register

Documentation-level; the risks named (unrecorded TDD lecture, grader unfamiliar with Python substitutes, uneven fluency, over-claiming the "industry uses Python" argument, generic vs. course terminology) are mitigation strategies for the report/oral defense, not something checkable in code. `QA.md` addresses several of these directly (e.g., using exact course terminology like "Strong Robust EC" rather than generic terms).

### §14 — Appendix, system parameters

| Parameter | Doc value | Code value | Match? |
|---|---|---|---|
| Street length | 500m | `STREET_LENGTH = 500` | Yes |
| Movement step | 1m | `position += 1` / `-= 1` per call | Yes |
| Required free stretch | 5m | `STRETCH_REQUIRED = 5` | Yes |
| Sensor reading range | 0–200cm | Enforced in `_is_noisy` (`r < 0 or r > 200`) | Yes |
| Min queries per `isEmpty` call | ≥5 per sensor | `range(5)` per sensor in `is_empty()` | Yes |
| Sensor count | 2 | Constructor takes exactly `sensor_left`, `sensor_right` | Yes |
| Noisy-sensor rule | disregarded entirely, not averaged | Matches — `is_empty()`'s branching logic | Yes |

**Status: Fully aligned** — but remember the caveat from Part A.2: I'm confirming code matches the *reference document's* numbers, not the original Blackboard source directly, since I don't have that document.

---

## Summary of findings

| # | Finding | Severity | Action needed |
|---|---|---|---|
| 1 | Instructor approval for Java→Python switch is asserted but has no evidence artifact in this repo | **High** — foundational to the whole project's legitimacy | Locate and add proof (email/Blackboard screenshot) before submission |
| 2 | Reference document's numeric parameters (500m, 5m, 0-200cm, etc.) haven't been independently checked against the real Blackboard detailed description | Medium | Compare `Testing_Stack_Rationale.pdf` §3/§14 against the actual Blackboard page directly |
| 3 | `park()`'s "not at a free stretch" branch has no dedicated pytest test (coverage gap at line 76->78) | Medium — this is the exact scenario from the original bug report | Add the suggested test |
| 4 | Cyclomatic complexity of `isEmpty` (flagged by the doc as highest-risk) has not been measured with radon/flake8 | Low-Medium | Run the tool, record the number |
| 5 | Test file docstrings don't name the specific testing technique per the doc's own "Report tip" | Low | Add technique tags to test file headers |
| 6 | WhereIs cases 3 and 4 don't check `position`, only `status`, despite the doc's table specifying both | Low | Add position assertions to those two tests |
| 7 | Park's tests don't use `monkeypatch` the way the doc's worked example demonstrates | Low — informational only | Mention in report/oral defense why it wasn't needed here |
| 8 | Naming-convention assumption (PascalCase→snake_case) isn't documented anywhere in this repo | Low | Add one sentence to README.md |
| 9 | `test_both_sensors_noisy` is a known, accepted flaky test (~1 in 5 runs) | Low — already documented in code comments | No action needed beyond what's already written, unless you want it fixed now |

**Strong alignment confirmed:** the decision to keep all mocking-library usage out of Phase 1 is now doubly justified — both by the team's own tool-mapping plan *and* by the actual course schedule slide, which explicitly labels Phase 2 as "Integration Testing (Mocking)." This is the single clearest point of full compliance found in this cross-check.

**Test suite state at time of this report:** 24 passed, 5 skipped, 0 failed, 98% overall coverage.
