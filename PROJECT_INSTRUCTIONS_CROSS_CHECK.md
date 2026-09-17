# Cross-Check: Actual Phase 1 Instructions vs. Current Implementation

**Date:** 2026-09-17
**Source:** `E:\Masters\SoftwareTesting&Networking\Testing\Project_instructions.pdf` — "Phase 1: Test-Driven Development and Unit Testing." Two pages, no more (confirmed by direct page-count check on the PDF).

**Why this document matters more than anything checked so far:** this is the actual, literal, detailed Phase 1 brief — not the team's own interpretation of it. Everything in `BRIEF_AND_PLAN_CROSS_CHECK.md` that was flagged as "unverifiable — I don't have the Blackboard document" is now checkable directly against this file. Some things check out exactly. Others reveal real, concrete gaps that the team's own reference document did not fully carry through into the actual deliverable.

---

## Part 1 — Numeric parameters: now fully confirmed

Every number the codebase relies on is stated explicitly in this document, and every one matches:

| Parameter | Brief text (this document) | Code | Match? |
|---|---|---|---|
| Street length | "a perfectly straight street which is 500 meters long" | `STREET_LENGTH = 500` | **Yes** |
| Free stretch required | "reliably find a free parking stretch of 5 meters" | `STRETCH_REQUIRED = 5` | **Yes** |
| Sensor range | "integers (in the range of 0 to 200) indicating the distance in cm" | Enforced in `_is_noisy` (`r < 0 or r > 200`) | **Yes** |
| Minimum queries per `isEmpty` call | "queries the two ultrasound sensors at least 5 times" | `range(5)` per sensor | **Yes** |
| Sensor count | "two ultrasound sensors" | Constructor takes exactly `sensor_left`, `sensor_right` | **Yes** |
| Noisy-sensor rule | "If one sensor is detected to continuously return very noisy output, it should be completely disregarded" | Matches — `is_empty()`'s branching disregards a noisy sensor entirely | **Yes** |
| Sensor/actuator modeling | "the actuators are not modeled in this phase... all the sensor signals come from sensor classes that are not modeled" | Matches — `Sensor(ABC)` + fakes only, no real hardware modeled | **Yes** |
| Assumed sensor inputs | "You can assume random or fixed sensor inputs in this phase" | `FixedSensor`, `RandomSensor` both exist | **Yes** |

**This resolves the open caveat in `BRIEF_AND_PLAN_CROSS_CHECK.md` Part A.2 and §14** — the numbers in `Testing_Stack_Rationale.pdf` accurately reflect the real brief. No discrepancy found here.

---

## Part 2 — Method specifications: mostly matches, two unspecified behaviors confirmed

The brief's own method descriptions, compared directly against the code:

| Method | Brief's exact requirement | Code behavior | Match? |
|---|---|---|---|
| `MoveForward` | "moves the car 1 meter forward, queries the two sensors through the isEmpty method... returns a data structure that contains the current position... and the situation of the detected parking places... cannot be moved forward beyond the end of the street" | `move_forward()` — increments position, calls `is_empty()`, appends to `records`, returns `CarState`; no-ops at `STREET_LENGTH` | **Match** |
| `isEmpty` | "queries the two ultrasound sensors at least 5 times and filters the noise... returns the distance in cm to the nearest object... If one sensor is detected to continuously return very noisy output, it should be completely disregarded. You can use averaging or any other statistical method" | `is_empty()` — 5 reads per sensor, disregards a noisy one entirely, averages the rest | **Match** |
| `MoveBackward` | "The same as MoveForward... only it moves 1 meter backwards. Cannot be moved behind if already at the beginning of the street" | `move_backward()` — matches, no-ops at position 0 | **Match** |
| `Park` | "performs a pre-programmed reverse parallel parking maneuver, if it is already positioned at an empty parking space stretch, or moves the car forwards towards the end of the street until such a stretch is detected, and then parks it" | Current `park()` only handles the first half ("already positioned at a stretch") — the search-forward half is not implemented, tests for it are skipped | **Partial — see Part 4 below** |
| `UnPark` | "moves the car forward (and to left) to front of the parking place, **if it is parked**" | `unpark()` raises `ValueError` if *not* parked | **Interpretation, not literal requirement — see below** |
| `WhereIs` | "returns the current position of the car in the street as well as its (un)parked status" | `where_is()` returns `self.state` (position + status + records) | **Match** (returns a superset — includes `records` too, which is harmless) |

### A genuinely important nuance: `UnPark`'s "if it is parked" wording

The brief says `UnPark` "moves the car forward... **if it is parked**." Read literally, this describes *when the method's action happens* — it does not say what should happen if it's called while *not* parked. A no-op (do nothing, return the state unchanged) is just as literal a reading as raising an exception.

The current implementation raises `ValueError("cannot unpark - car is not parked")` — which is a **reasonable design choice**, and it is what `test_unpark_while_not_parked_is_rejected` already expects and passes against. But it should be labeled honestly as an **interpretation of an underspecified case**, exactly the same category as the two assumptions already documented for `isEmpty` (both-sensors-noisy, out-of-range reading) — not as something the brief explicitly mandates. The same applies to `Park`'s "called while already parked" behavior (case 25) — the brief describes what `Park` does when *not yet* parked; it says nothing about a second call while already parked.

**Recommendation:** add these two as explicitly logged assumptions in the report, phrased the same way as the other two (e.g., *"The brief does not specify UnPark's behavior when the car is not parked. We chose to raise an exception rather than silently no-op, for the same reasoning as Park's reject-while-parked case: a silent no-op could mask a logic error elsewhere in the calling code."*). This isn't a code change — it's making an already-reasonable choice visibly deliberate rather than implicit.

---

## Part 3 — The interface specification format: a concrete, checkable gap

This is the most specific, most checkable requirement in the whole document, and it is not currently met.

**The brief's exact words:**
> "For the interface, you need to specify the signature of the methods: name, input argument types, and output return type. For each interface method, you need to give its specification in the following form:
> ```
> /**
>  Description
>  Pre-condition:
>  Post-condition:
>  Test-cases:
> */
> ```

**What this means concretely:** every one of the six methods needs a specification block with four explicit labeled parts — Description, Pre-condition, Post-condition, Test-cases — not just a prose docstring.

**Checked against `interface.py` as it currently exists:** each method has a one-line or two-line docstring (e.g., `"""Return current position and parked/unparked status."""`) with no explicit **Pre-condition**, **Post-condition**, or **Test-cases** labels anywhere.

**Status: Gap.** This is not a Python-code problem to fix in `interface.py` necessarily — the brief's judging criteria ("soundness: whether the interfaces have been correctly specified... completeness: whether all requirements have been considered and all test-cases necessary to cover them have been given") describes this as a **report deliverable**, Part 1 of the PDF, separate from the ZIP of source code. But it needs to exist *somewhere*, in this exact structured form, for all six methods, before submission — and right now it doesn't exist anywhere in this repo.

**Recommendation:** for each of the six methods, write a block like:
```
/**
  Description: Moves the car 1 metre forward and records the parking-space
    reading at the new position.
  Pre-condition: none (may be called from any position 0-500).
  Post-condition: if position < STREET_LENGTH, position increases by 1 and
    a new ParkingRecord is appended to state.records; if position ==
    STREET_LENGTH, the call is a no-op and state is unchanged.
  Test-cases: 5, 6, 7, 11 (see tests/test_move_forward.py)
*/
```
...for `WhereIs`, `MoveForward`, `MoveBackward`, `isEmpty`, `Park`, `UnPark`. This is report content, not code — it belongs in the PDF, referencing the actual test file/case numbers already established in `tests/README.md`.

**Evidence:** _[screenshot: the finished specification section of the report PDF, once written]_

---

## Part 4 — Preferred functional test technique: classification tree or decision table

**The brief's exact words:**
> "To design your tests, first use one of the functional testing methods (**preferably: classification tree or decision table**) to partition the domain of different inputs (or output) using the above-given requirements."

**Checked against the actual technique mix used across the 28 test cases** (per `tests/README.md` and `Testing_Stack_Rationale.pdf` §9):

| Method | Technique actually used |
|---|---|
| `WhereIs` | State-based cases |
| `MoveForward`/`MoveBackward` | Boundary Value |
| `isEmpty` | Strong Robust Equivalence Class + **Decision table** (this one matches the brief's preference) |
| `Park`/`UnPark` | State Transition + Boundary Value |

**Status: Partial gap.** Only `isEmpty` uses one of the two explicitly *preferred* techniques (decision table). The other five methods use Boundary Value, Equivalence Class, or State Transition — all legitimate, well-established functional testing techniques, but not the ones the brief calls out as preferred. The word "preferably" means this isn't a hard requirement, but a grader specifically looking for classification trees or decision tables across the whole test plan (not just `isEmpty`) may find the rest of the plan under-using the recommended approach.

**Recommendation:** this doesn't necessarily require redesigning the test suite. Two lower-cost options:
1. Add a **classification tree** for at least one more method (e.g., `Park`, which has multiple interacting conditions — already-at-stretch vs. not, already-parked vs. not — that a classification tree would represent well) as a supplementary artifact in the report, alongside the existing Boundary Value reasoning.
2. In the report, explicitly justify *why* Boundary Value/State Transition were chosen over classification tree/decision table for the other five methods (e.g., "MoveForward/MoveBackward's domain is a single ordered numeric range with two hard edges — a textbook Boundary Value case — a classification tree would only re-describe the same two partitions without adding insight").

Either approach directly answers a question an examiner is likely to ask: *"the instructions said classification tree or decision table — why did you use boundary value instead?"*

---

## Part 5 — Line-by-line TDD commenting: a real, checkable gap

**The brief's exact words (Part 2: Test Driven Development):**
> "For each and every method, apply the principles of test-driven development to implement the interfaces in order to satisfy each and every test-case. **Each line of code should be augmented with the reason why it has been added (which test case it is supposed to satisfy).** Before you start each step in the implementation, implement a test-case as a JUnit test, observe how it fails, add the line(s) of code necessary to satisfy it, observe that all tests pass afterwards and **comment the line(s) of code to specify why they have been added.** In your report, **describe in a step-wise manner how each piece of implementation has been added to fulfill a test-case.**"

This is three distinct, explicit instructions:
1. Every line of production code needs a comment saying which test case it satisfies.
2. This has to happen *as part of the TDD process itself* — comment each line at the moment it's added, not retroactively.
3. The report needs a step-wise narrative — for every method, not just one — showing test case → failing test → line(s) added → why.

**Checked against `parking_assistant.py` as it currently exists:** the file has **method-level** comments (`# --- Owner: Harikrishna M --`) and a few explanatory blocks (e.g., the note above `park()` explaining what's deferred to Phase 2), but **no line-by-line "this line satisfies case N" comments** anywhere in any of the six method bodies. For example:
```python
def move_forward(self) -> CarState:
    if self.state.position >= self.STREET_LENGTH:
        return self.state
    self.state.position += 1
    reading = self.is_empty()
    self.state.records.append(ParkingRecord(self.state.position, reading))
    return self.state
```
None of these five lines say which of cases 5/6/7/11 they satisfy.

**Checked against the report-level walkthrough requirement:** `Testing_Stack_Rationale.pdf` §9 does this **once**, for `Park` case 20 only ("Park(), worked end to end — the pattern to copy for every other method"). No equivalent step-wise walkthrough exists for the other five methods anywhere in this repo's documentation.

**Status: Confirmed gap, and probably the most consequential one in this whole cross-check** — this is stated as an explicit judging mechanism in the brief (Part 2's own process), not a stylistic nicety.

**Recommendation, two parts:**
1. **Code:** go back through each method and add a short inline comment at each line (or small group of lines) that names the case it satisfies, in the exact style already used in `Testing_Stack_Rationale.pdf`'s Park example (`# case 20`, `# case 21`, etc.). This is mechanical — the case numbers already exist in `tests/README.md`; it's a matter of tying them to the specific lines that satisfy each one.
2. **Report:** write the "worked end to end" walkthrough — red test, failing run, line(s) added, why, green run — for every method, not just Park. The template already exists in the reference document; it just needs to be applied five more times.

**Evidence:** _[screenshot: the updated parking_assistant.py with case-number comments on each line, and the report's step-wise section for all six methods]_

---

## Part 6 — Deliverable shape

**The brief's exact words:** "There are two main deliverables for this phase: a single PDF file documenting the outcome of each and every of the following steps and a ZIP file containing the source code of the software implemented as the final outcome of this phase."

| Deliverable | What it needs to contain | Current state |
|---|---|---|
| PDF | Part 1 (data structures/methods discussion, interface spec blocks, functional test design technique, test suite) **and** Part 2 (step-wise TDD narrative for every method) | **Not yet assembled as a single PDF.** The content exists scattered across `README.md`, `tests/README.md`, `QA.md`, and the reference document, but the specific structured pieces required (spec blocks per Part 3 above, step-wise narrative per Part 5 above) are largely missing, not just unassembled. |
| ZIP | Source code | The `autonomous_parking_system/` and `tests/` folders, `pyproject.toml`, `requirements.txt` — all present and working (24 passed, 5 skipped, 0 failed) |

**Status:** the code-side deliverable is close to ready. The PDF-side deliverable has real, identified content gaps (Parts 3 and 5 above) that need to be written before assembly, not just formatted.

---

## Summary — what actually needs to happen before submission

Ordered by how directly each is called out as a judging criterion in this document:

| # | Gap | Where it lives | Priority |
|---|---|---|---|
| 1 | No Description/Pre-condition/Post-condition/Test-cases spec block for any of the six methods | Report (Part 1 deliverable) | **High** — explicitly named as a judged item ("soundness") |
| 2 | No line-by-line "which test case this satisfies" comments in `parking_assistant.py` | Code | **High** — explicitly required by name in Part 2 |
| 3 | No step-wise TDD narrative in the report for 5 of the 6 methods (only Park case 20 has one) | Report (Part 2 deliverable) | **High** — explicitly required by name in Part 2 |
| 4 | Classification tree / decision table used for only 1 of 6 methods, despite being the brief's stated preference | Report, possibly test design | **Medium** — "preferably," not mandatory, but worth a justification either way |
| 5 | `UnPark`'s and `Park`'s rejection behavior (exception vs. no-op) not explicitly logged as an assumption the same way isEmpty's two cases are | Report | **Medium** — easy fix, one paragraph |
| 6 | Park's search-forward logic (the second half of the `Park` requirement: "or moves the car forwards... until such a stretch is detected") is not implemented — confirmed against the actual brief text, not just the team's own case list | Code + tests | **High** — this is literally half of `Park`'s stated requirement, not a nice-to-have extension |
| 7 | Everything already listed in `BRIEF_AND_PLAN_CROSS_CHECK.md`'s summary table (coverage gap at park() line 76->78, missing position checks in WhereIs cases 3/4, no radon/complexity check, etc.) | Various | Carried over, still open |

**Point 6 deserves its own emphasis:** with this document now confirmed as the literal, authoritative brief, `Park`'s requirement is unambiguous — it has two halves ("if already positioned at a stretch" **or** "moves forward... until such a stretch is detected"). The current implementation only satisfies the first half. This was already known and tracked (cases 21–24, deferred to Phase 2 in this session's decisions) — but it's worth being direct about it now: this isn't an optional extension, it's the literal second clause of the one-sentence spec for `Park`. Deferring it to Phase 2 is a real scope decision with a real cost, and should be presented in the report as a conscious, reasoned trade-off (tied to the mocking-tooling boundary established in `BRIEF_AND_PLAN_CROSS_CHECK.md` Part A.3), not glossed over.
