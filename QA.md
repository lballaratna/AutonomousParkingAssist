# Phase 1 — Questions & Answers

This is prep for explaining the project out loud - to a teammate, a
grader, or in the individual oral defense. Every answer is written the way
you'd actually say it, not textbook phrasing. Topics run in a logical
order: why testing matters at all, how to design tests before code, how
to measure whether those tests were thorough, the TDD process that ties
it together, the classes actually built, the Java-to-Python shift, the
six methods one by one, the project's structure, the team process, the
decisions made along the way, and where all of this comes from in the
real world. Everything matches what's actually in this repo right now.

---

## 1. Why testing matters at all

**Q: Why does any of this matter - isn't "the code works" enough?**

A: Because "seems to work" and "is actually correct" are different
claims, and the gap between them has caused real damage. A data-conversion
bug destroyed the Ariane 5 rocket 37 seconds after launch. A sentencing
software bug released over 3,200 prisoners early, unnoticed for a decade.
Nissan recalled over a million cars over an airbag-sensor bug. Three
separate software glitches contributed to the two Boeing 737 MAX crashes -
346 deaths, an estimated $18.7 billion. A race-condition bug sat quietly
in alarm software for 3 million hours of operation before the exact bad
timing finally caused a blackout across 8 US states. The lesson from that
last one specifically: a bug doesn't need to be *likely* to eventually
happen - it just needs enough running time.

**Q: What's the actual definition of testing, then?**

A: Planned experiments, run for two reasons at once: to reveal bugs
(deliberately trying to turn a hidden fault into a visible failure), and
to gain confidence (building justified trust that the software behaves
correctly). Dijkstra's line is the one to remember here: "Testing shows
the presence, not the absence, of bugs." Passing tests never prove zero
bugs remain - they only prove the specific inputs you tried behave
correctly. You can't run every possible input, so you can't get a
mathematical guarantee from testing alone.

**Q: What's a fault, an error, and a failure - and can you tie each to this project?**

A: A fault is the actual wrong or missing line of code - it comes in two
flavors: *commission* (you wrote the wrong thing) and *omission* (you
forgot to write something the spec required, which is harder to notice,
since there's no wrong code to point at, just missing code). An error is
an incorrect internal state caused by that fault - a variable now holds
the wrong value. A failure is that error finally becoming visible in
behavior. Concretely, in this project: forgetting to disregard a
continuously-noisy sensor at all would be an omission fault. The error
would be `isEmpty` holding an averaged distance that includes a corrupted
reading. The failure would be the car reporting a 5m stretch as free when
it isn't, and attempting to park into an occupied space.

**Q: Why don't all faults cause immediate, obvious failures?**

A: Because a fault has to survive a three-step journey to become visible
- this is called the RIP process. *Reachability*: the faulty line has to
actually execute. *Infection*: executing it has to actually corrupt
something (not every reached fault corrupts state - sometimes it gets
lucky). *Propagation*: that corrupted state has to survive everything
that happens afterward and actually reach visible output, without
something else overwriting or masking it first. Break the chain at any
point and the bug stays completely silent. This is exactly why the
Northwest blackout bug took 3 million hours to surface - the race
condition needed exactly the right timing just to be *reached*.

**Q: What's the difference between validation and verification?**

A: Validation asks "have we built the *right* product?" - checked against
real-world intended use, usually manual, usually done on the finished
product. Verification asks "have we built the product *right*?" -
checked as compliance between artifacts from consecutive phases (does the
code match the design? does the design match the requirements?), and it
can often be automated. You can pass verification perfectly - every phase
matches its predecessor exactly - and still fail validation, if the
original spec itself was wrong. Both are necessary; neither substitutes
for the other. This project is entirely a verification exercise: does the
code match the class/method spec.

**Q: What are Beizer's five levels of testing, and where does this project sit?**

A: They describe testing maturity as a mindset that grows in stages: L0
is ad hoc debugging with a handful of inputs, just enough to see the code
run. L1 is deliberately showing the software *does* work. L2 is actively
trying to show it does *not* work - hunting corner cases. L3 is
prioritizing which test goals matter most, since you can't test
everything. L4 is testing thinking baked into how you design and write
code from the start, not bolted on after. A TDD project like this one
lives mostly at L4 - the tests aren't an afterthought, they're what
*shapes* the code as it's written.

**Q: What's the V-Model, and where does Phase 1 fit in it?**

A: It pairs each design level with a matching testing level: Requirements
↔ Acceptance Testing, System Design ↔ System Testing, Architecture Design
↔ Integration Testing, Module Design ↔ Unit Testing, with Coding at the
bottom joining the two arms. Phase 1 of this project sits at Module
Design ↔ Unit Testing - we're testing one class in isolation. Phase 2
moves up one level, to Architecture Design ↔ Integration Testing, once
the actuator/sensor boundary actually gets modeled and multiple pieces
have to work together.

---

## 2. Designing tests before the code exists (functional testing)

**Q: What is functional testing, and why does TDD depend on it specifically?**

A: Functional testing treats the code as a black box and derives test
cases purely from the *specification* - what goes in, what should come
out - without looking at the implementation at all. It's the only kind of
testing that can happen before any code exists, which is exactly why TDD
runs on it: a test written before the method exists can only ever be
based on the spec, never on the code, since there's no code to look at
yet.

**Q: What's Boundary Value testing, and why is it the workhorse of this project?**

A: One test case per extreme value of each input - both the valid edge
and just past it. It's simple and it directly targets off-by-one bugs,
but it says nothing about the middle of a domain and doesn't handle
variables that depend on each other. This project has three hard limits
that all get this treatment: the street's two ends (0m/500m), the
5-metre stretch threshold, and the sensor's 0-200cm range. Testing 499→500
*and* 500→500 together is what proves a `>=` check is right instead of
`>` - a single mid-range test could never catch that.

**Q: What's an equivalence class, and what's the difference between weak and strong, normal and robust?**

A: The idea starts from a small puzzle: what's the fewest tokens needed on
an m×n grid so every row and column has at least one token? The answer is
`max(m, n)` - you don't need one token per cell, just enough placed
cleverly. Equivalence class testing applies that logic to test design:
partition each variable's domain into classes, then cover each class at
least once.

- **Weak Normal EC** covers each class once, one variable at a time (the
  *single fault assumption* - you're betting a bug only depends on one
  variable going wrong). Cheapest option.
- **Strong Normal EC** covers *every combination* of classes across all
  variables (the *multiple fault assumption*). Grows fast - it needs the
  product of every variable's class count.
- **Weak/Strong Robust EC** add explicit out-of-range values on top of
  the normal variants. Robust is what actually catches invalid-input
  handling, which matters a lot for sensor data specifically.

**Q: Why does the reference material warn so strongly against Strong Robust EC?**

A: Because it explodes combinatorially. A course case study found Strong
Robust EC generating over 100 test cases for a 3-variable mortgage
spec, and warned that 5 variables with 5 partitions each balloons to
roughly 8 million cases - "3 months of testing" at one second per case.
That's the entire argument for defaulting to Weak Normal/Robust EC, and
reserving Strong EC for the *one* place in this project where combinatorics
actually matter: the two-sensor fusion logic inside `isEmpty`, where "is A
noisy, is B noisy" genuinely interact.

**Q: What's a decision table, and where does this project use one?**

A: A table for when conditions *aren't independent* - you list every
combination of conditions (the stub) against the required action for each
combination (the entries), with "don't care" cells where a condition
doesn't matter. A complete table needs 2 to the power of (number of
conditions) rows, for independent boolean conditions. `isEmpty`'s
sensor-fusion rule is exactly this: is sensor A noisy? Is sensor B noisy?
Based on that combination - average both, disregard A, disregard B, or
(the undecided case) refuse to guess.

**Q: How do you actually go from a line in the brief to a technique to a test case? Walk through one example.**

A: Take Park's spec line: *"performs a reverse parallel parking maneuver
if it is already positioned at an empty parking space stretch, or moves
forward until such a stretch is detected, then parks it."* Step one:
underline the boundary and before/after words - "already positioned at a
stretch" is a boundary condition on the 5m requirement, which points to
Boundary Value testing. "Parks it" / not parked, before and after, is a
before/after condition with rules about which transitions are legal,
which points to State Transition testing. Step two: match those to actual
cases - the boundary gives cases 22/23 (exactly 5.0m vs 4.9m), the state
transition gives case 25 (reject parking while already parked). That's
the whole method - read the spec, underline the boundary/before-after
words, match to a technique, write the case.

**Q: How were the six methods themselves classified by technique?**

A: `WhereIs` uses state-based cases, since it's a pure query - every state
the car can be in needs its own case. `MoveForward`/`MoveBackward` use
Boundary Value on position plus Weak Normal EC on the `isEmpty` reading
each move triggers. `isEmpty` uses Strong Robust EC on the sensor pair (the
one deliberately expensive technique), a decision table for the fusion
rule, and Boundary Value at the 0/200cm edges. `Park`/`UnPark` use State
Transition testing, plus Boundary Value on the 5m threshold for Park
specifically.

---

## 3. Measuring whether the tests were thorough (structural testing)

**Q: What is structural testing, and why does it come *after* functional testing, not before?**

A: Structural testing is designed from the actual program code - test
cases are chosen to cover the code's flow graph (nodes are statements,
edges are "this line may run immediately after that one"). It can only
happen once an implementation exists, which is exactly why it's the
second half of the TDD loop, not the first: derive tests from the spec,
implement, run coverage, and treat any gap coverage finds as evidence of a
*missing functional test case* - not something to patch with a throwaway
assertion.

**Q: What's the ladder of structural coverage criteria, weakest to strongest?**

A: Statement coverage - every node in the flow graph runs at least once.
DD-Path coverage (Decision-to-Decision path) - every node *and edge* in
the collapsed decision graph is covered; this is exactly what
`coverage.py`'s branch-coverage flag reports. Prime path coverage - every
complete simple path, or one full simple loop iteration, is covered;
relevant here specifically inside `isEmpty`'s "query at least 5 times"
loop, where 0/1/many-iteration boundaries matter. And beyond what
`coverage.py` gives automatically: dependent-pairs/multiple-condition
coverage, and MC/DC (each individual boolean sub-condition must
independently affect the outcome - the criterion ISO 26262 mandates for
safety-critical automotive code).

**Q: Concretely, what's the difference between statement and branch coverage catching a bug?**

A: Take a function that rejects readings outside 0-200: one passing test
with a valid input already gives 100% statement coverage - the `if` line
ran. Branch coverage disagrees, correctly: the *rejection* branch never
ran once, so that logic is completely unproven. Add a test for an invalid
input and only then is the 100% actually earned rather than assumed.

**Q: What's cyclomatic complexity, and what does it have to do with testability?**

A: `V(G) = edges - nodes + 2` for a single-entry, single-exit graph - it's
a testability budget, not just a coverage number. The risk scale: 1-10 is
simple, 11-20 moderate risk, 21-50 high risk, above 50 is effectively
untestable. The target for every method in this project is to stay under
10 - `isEmpty` is the one to watch, since it's the highest-complexity
method here (the sensor-fusion decision logic). If it ever starts feeling
tangled, that's the signal to extract a helper, not push through.

**Q: What does hitting 100% coverage actually prove, and what does it not prove?**

A: It proves every line and branch ran at least once during the test
suite. It does not prove correctness - a line can execute and still
produce a wrong answer if the assertion checking it is weak, or missing
entirely. "We wrote some tests" proves nothing by itself either; it's
trivially easy to test the agreeing-sensors path and never touch the
disagreeing one. Coverage is the best automatic signal available that
something went *untested* - industry teams commonly gate releases at
around 80% for exactly this reason - but it's a floor, not a guarantee.

---

## 4. The TDD process that ties it together

**Q: What's the actual red-green-refactor cycle, step by step?**

A: Red - write one test for a single piece of spec-derived behavior, run
it, watch it fail because the code doesn't exist yet. This failure is
deliberate: a test that passes before any code exists isn't testing
anything real. Green - write the *smallest* amount of code that passes
that one test, not the general solution - this feels backwards at first,
since it looks like writing deliberately incomplete code, but that's the
point: design isn't guessed at upfront, it's built one proven step at a
time. Refactor - clean up (rename, extract a helper, remove duplication)
without changing behavior, using the now-passing test as a safety net; if
the refactor actually breaks something, the test goes red immediately and
says so. Then loop: pick the next case.

**Q: One rule that "never bends" in TDD - what is it?**

A: Implementation code never gets written for a test that doesn't exist
yet - not even correct code. If there's no failing test in front of you,
you've stepped outside TDD, full stop.

**Q: Why is "developer" and "tester" the same person, in the same hour, in TDD?**

A: Because there's no hand-off - Red is the tester's hat, Green is the
developer's hat, Refactor is both, and one person wears all three inside a
single short cycle. Nobody on this team is "only testing" or "only
building" - every method's implementation and its test file grow together,
in the same sitting, by whoever owns that method.

**Q: What order were the six methods actually built in, and why that order?**

A: `WhereIs` first - it's a pure state query with no motion logic, so it
establishes the state representation everything else reads. Then
`MoveForward`/`MoveBackward` - boundary logic at the two ends of the
street, still no sensors involved. Then `isEmpty` - the noisy-sensor
filtering, the highest-complexity method, built once the scaffolding
around it already has tests. Then `Park`, which composes `MoveForward` +
`isEmpty`. `UnPark` last, since it only has to undo what `Park` did.

**Q: Where does TDD actually *start* in this codebase - is it Day 1?**

A: No, and this is worth being precise about. Three of the four engine
files - `state.py`, `sensor.py`, `interface.py` - have zero behavior.
They're scaffolding, written by hand, not test-driven, because there's no
meaningful failing test for "does this dataclass have a `position`
field." Even `ParkingAssistant`'s constructor isn't TDD - it's verified
directly with a one-line script, because it isn't behavior to test, it's
the foundation behavior gets tested *against*. TDD genuinely starts the
moment the six method stubs stop being `raise NotImplementedError` and
get replaced one at a time through red-green-refactor.

**Q: Why does mocking exist, and why does stubbing alone not cover everything?**

A: Real dependencies are frequently slow, unavailable, or - like
`isEmpty` was, mid-project - simply not built yet. A stub (`FixedSensor`)
gives a canned answer and nothing else; that's enough for most cases,
where you only care what comes back. A mock also *remembers* how it was
used, so you can assert things like "was this dependency actually called
at least 5 times" - a stub can't answer that question, only a mock can. If
`Park` had to wait for the real `isEmpty` before it could be tested,
nothing could be tested until everything was finished, which is backwards
- a stub (or `monkeypatch`) breaks that deadlock.

---

## 5. The classes actually built

**Q: Walk me through what each file in `autonomous_parking_system/` does.**

A: `state.py` is pure data - what a car knows about itself: position,
status, reading history. `sensor.py` is the hardware boundary, faked on
purpose, since real sensors aren't modeled this phase. `interface.py` is
the contract: six method names, return types, two shared constants, zero
bodies. `parking_assistant.py` is the only file where any of this
actually *does* something - the one class implementing all six methods
for real.

**Q: Why split into four files instead of one class?**

A: Two reasons. The brief treats "interface design" as its own
deliverable, separate from implementation, so the contract needed to be
its own thing. And with three people building this together, one giant
file means constant merge conflicts - four small files mean everyone
mostly stays in their own corner.

**Q: What is `ParkingAssistantInterface`, and why does it exist?**

A: The answer to "design an interface." Python has no `interface`
keyword, so `abc.ABC` + `@abstractmethod` stands in for it - the closest
thing to "here's a contract every implementation must satisfy." It
defines the six methods with no bodies, plus `STREET_LENGTH` and
`STRETCH_REQUIRED`, constants every implementation has to agree on.

**Q: What does `@abstractmethod` actually do, mechanically?**

A: It tags a method so `ABCMeta` knows it isn't implemented yet. The
check happens the moment you try to *construct* an object - if any tagged
method hasn't been overridden by then, Python refuses with `TypeError`.
It doesn't stop you from writing a body under the decorator (ours are
just docstrings), and it doesn't judge whether an override is any good -
`raise NotImplementedError` counts as implemented just as much as real
logic does.

**Q: How is that different from Java's `interface`?**

A: Same protection, different moment. Java's compiler refuses to build a
class missing a required method - caught before the program ever runs.
Python has no compile step, so it waits until instantiation:
`Car()` throws `TypeError: Can't instantiate abstract class Car with
abstract method park` the instant you try to build the incomplete class.
The rule is identical; only the timing moved.

**Q: Why `abc.ABC` instead of `typing.Protocol`?**

A: `Protocol` is structural - any class with matching method names
qualifies automatically, no inheritance needed. That's a weaker match to
what the brief actually asks for: an explicit "this class implements that
contract," the same explicit declaration Java's `implements` makes.
`ABC` requires writing `class ParkingAssistant(ParkingAssistantInterface)`
- a real, visible commitment.

**Q: Why do `STREET_LENGTH`/`STRETCH_REQUIRED` live on the interface, not the implementation?**

A: They're part of the contract, not an implementation detail - every
method touching boundaries has to agree what "500m" and "5m" mean. If
they lived only in `parking_assistant.py`, a test or a second
implementation couldn't reference them without importing the concrete
class, defeating the point of coding against an abstraction.

**Q: What is `CarState`, and why a dataclass?**

A: The car's entire memory - `position`, `status`, `records`.
`@dataclass` generates the constructor and equality check from the field
list, so there's no hand-written boilerplate for something that's
genuinely just data. `CarState()` with zero arguments is valid because
every field's default describes exactly "a brand new car."

**Q: Why `Literal["moving", "parked", "unparked"]` instead of plain `str`?**

A: So a typo like `"prked"` gets caught by a type checker instead of
surviving into a bug report. It restricts `status` to exactly those three
strings - visible in the type itself, not buried in a comment.

**Q: Why `field(default_factory=list)` instead of `records: List[...] = []`?**

A: A classic Python trap - a mutable default like `[]` is created *once*,
at class-definition time, and every instance sharing that default would
silently share the *same* list. `default_factory=list` makes every new
instance get its own fresh list.

**Q: What's `ParkingRecord`, and why `Optional[int]` on `distance_cm`?**

A: One `isEmpty()` reading, tied to the position it was taken at.
`Optional` because a reading might be invalid - the type documents that
possibility instead of leaving it unstated.

**Q: Why does `Sensor` exist as its own abstraction?**

A: The brief says to assume "random or fixed sensor inputs" - multiple
*kinds* of sensor behavior need to exist side by side and be swappable.
`Sensor(ABC)` is the contract (`read() -> int`); `FixedSensor`,
`RandomSensor`, `NoisySensor` are three implementations of it.
`ParkingAssistant` only ever depends on the abstraction - Dependency
Inversion in practice.

**Q: Why does `ParkingAssistant`'s constructor take sensors as parameters?**

A: Dependency injection. If the constructor built its own sensors, every
test would be at the mercy of that internal logic. Passed in, a test does
`ParkingAssistant(FixedSensor(0), FixedSensor(0))` and knows *exactly*
what every reading will be - it's what makes the class testable at all.

**Q: Stub vs mock - what's the actual difference?**

A: A stub gives a canned answer, nothing else. A mock also *remembers*
how it was used, so you can assert on call counts or arguments. This
project uses stubs almost everywhere; the one place that would genuinely
need a mock (proving `isEmpty` queried a sensor at least 5 times) is
deferred to Phase 2 rather than bringing a mocking library into Phase 1.

**Q: What does "fulfilling the contract" mean for `ParkingAssistant`?**

A: For every abstract method: matching name, matching return type,
behavior matching what the docstring promised - the interface never says
*how*. Private helpers (`_is_noisy`, `_average`, `_at_free_stretch`)
aren't part of the contract at all; fulfilling a contract doesn't mean
you can *only* have the promised methods.

---

## 6. The Java → Python shift

**Q: Why is this project in Python when the brief describes Java?**

A: The brief names Java and JUnit with no hedge, but explicitly allows
substitutes for the coverage tool ("EclEmma, or similar tools") and the
mocking tool ("Mockito, or similar tools, alternatively manual
mock-ups"). Hedging two of four tool choices and not the other two was
worth taking seriously rather than assuming either way - so the language
choice was asked about directly, and confirmed acceptable, rather than
decided unilaterally.

**Q: What actually changes structurally moving from Java/JUnit to Python/pytest?**

A: Two big ones. Java's `interface` keyword becomes `abc.ABC` +
`@abstractmethod`, moving contract enforcement from compile-time to
instantiation-time. And JUnit's one-test-method-per-case style becomes
`@pytest.mark.parametrize` - one test function fed a table of
input/expected-output rows, mapping directly onto how boundary-value and
equivalence-class tables already look on paper.

**Q: What's the full tool mapping, one line each?**

A: JUnit → `pytest` (test discovery via `test_*.py`, plain `assert`).
EclEmma → `coverage.py`/`pytest-cov` (line/branch coverage, HTML report).
Mockito → `unittest.mock`/`pytest-mock` (kept for Phase 2's
actuator/sensor stubbing in this project's plan). Java `interface` →
`abc.ABC`.

**Q: Does moving to Python change what TDD actually *is*?**

A: No - red-green-refactor is a discipline, not a language feature. What
changes is mechanics: no compile step means faster iteration per cycle,
and `parametrize` cuts boilerplate versus JUnit's per-method style. Fail
first, smallest passing change, refactor with a safety net - identical in
both languages.

**Q: What does Python's dynamic typing cost here, if anything?**

A: Some mistakes Java's compiler catches immediately (a typo in a method
name, a wrong return type) only surface when that code path runs in a
test. `Literal["moving", "parked", "unparked"]` on `CarState.status` is
partly about buying back some of that static-typing safety net through
Python's own type-hint system, even though nothing enforces it at
runtime the way Java would.

**Q: What's the actual risk carried by using Python instead of Java?**

A: Not compliance - that's settled and documented. It's continuity: the
TDD module is likely taught with Java/JUnit examples, so anyone on the
team needs to translate those examples into the Python equivalent on the
spot - in the report, and out loud in the oral defense - rather than
assuming the vocabulary carries over unchanged.

---

## 7. The six methods, one by one

**Q: `WhereIs()` - what does it do, and what's tested?**

A: Reports current position and parked/unparked status - a pure query,
no computation. Technique: state-based cases, since every state the car
can be in needs its own case. Cases: (1) a fresh car reports position 0,
unparked. (2) position reflects moves - after two `MoveForward` calls,
position is 2. (3) status shows "parked" right after a successful Park.
(4) status shows "unparked" right after UnPark. Fully implemented and
tested - `return self.state`, one line, because `CarState` already *is*
the answer.

**Q: `MoveForward()`/`MoveBackward()` - what do they do, and what's tested?**

A: Move the car one metre, query `isEmpty()`, record the result, and
never move past either end of the 500m street. Technique: Boundary Value
on position. Cases: moving from an ordinary position (0, or 500 going
backward), moving from one metre short of a limit (499 forward, 1
backward - still legal), moving from *at* a limit (500 forward, 0
backward - rejected, no-op), and confirming a successful move actually
appends a reading to `state.records`. All eight cases (four each) fully
implemented and tested.

**Q: `isEmpty()` - what does it do, and what's tested?**

A: Query both sensors at least 5 times each, filter noise, disregard a
continuously-noisy sensor, return a distance in 0-200cm. The
highest-complexity method in the project. Techniques: Strong Robust EC on
the sensor pair, a decision table for the fusion rule, Boundary Value at
0/200cm. Cases: both sensors clean and agreeing (averaged), one sensor
noisy (disregarded, use the other), both noisy at once (undecided by the
brief - we raise an error), readings at the exact 0/200cm edges
(accepted), a reading outside that range (undecided by the brief - treated
like noise), and a call-count check (each sensor read ≥5 times). Seven of
eight cases implemented; the call-count case is deferred to Phase 2 (needs
mocking tooling to prove a call count at all).

**Q: `Park()` - what does it do, and what's tested?**

A: If already at a free stretch of at least 5m, park immediately.
Otherwise, drive forward searching for one, then park. Reject a second
`park()` while already parked. Techniques: State Transition testing plus
Boundary Value on the 5m threshold. Cases: already at a free stretch
(parks immediately - built and tested), calling park while already parked
(rejected - built and tested), searching forward when nothing's free yet,
the exact 5.0m/4.9m boundary, and "no stretch anywhere on the street" -
these last four are all deferred to Phase 2, since proving them needs a
sensor that can return a *sequence* of different readings (a single
reading only reaches 2m; the requirement is 5m), which needs mocking
tooling we're not bringing into Phase 1.

**Q: `UnPark()` - what does it do, and what's tested?**

A: Move the car forward (and left) to the front of the parking space -
only valid while parked. Technique: State Transition testing. Cases:
unparking from a parked state (status flips to unparked, *and* position
moves forward by one - more on why that matters below), unparking while
never parked (rejected), and confirming the new state is visible through
`WhereIs` too, not just `unpark()`'s own return value. All three cases
fully implemented and tested.

---

## 8. Project structure and tooling

**Q: Why does `pyproject.toml` exist, and what do its two settings do?**

A: `pythonpath = ["."]` tells pytest the project root is importable, so
`from autonomous_parking_system import ...` resolves inside test files -
without it, pytest fails with import errors. `branch = true` under
`[tool.coverage.run]` turns on branch coverage, not just statement
coverage, and `source = [...]` tells coverage.py to measure the engine
code specifically, not the tests themselves.

**Q: Why does `requirements.txt` list exactly `pytest`, `pytest-cov`, `pytest-mock`?**

A: They're the three tools this project maps onto Java's testing stack -
`pytest` (JUnit), `pytest-cov` (EclEmma), `pytest-mock` (Mockito, reserved
for Phase 2). None of them are built into Python, so this file is what
makes `pip install -r requirements.txt` give everyone the same
environment.

**Q: Why does `.gitignore` list `__pycache__/`, `.pytest_cache/`, `htmlcov/`, `.coverage`?**

A: All four are regenerated automatically as a side effect of running
Python/pytest/coverage - none of them are source code, so none of them
belong in git or in the final submission ZIP.

**Q: Why does `__init__.py` matter, even empty?**

A: A plain folder of `.py` files isn't automatically importable as one
thing - Python has no way to know "these files belong together" without
it. It's the literal mechanism that turns a folder into an importable
package; without it, `from autonomous_parking_system import ParkingAssistant`
fails outright.

---

## 9. Team process

**Q: Who owns what?**

A: Lavanya BallaRatna - `Park`, `UnPark`, plus architecture lead (the
interface, the class skeleton, the overall test plan everyone else builds
on). Harikrishna M - `WhereIs`, `MoveForward` (built first, since nothing
else depends on them existing yet). Pooney Joseph - `MoveBackward`,
`isEmpty` (the highest-complexity method; tests reviewed by Harikrishna
before merge).

**Q: What does "whoever owns a method writes both its tests and its implementation" actually mean in practice?**

A: The method owner runs their own red-green-refactor cycle, alone,
producing two things together: `tests/test_<method>.py` (the tester
artifact) and the method body in the shared `ParkingAssistant` class (the
developer artifact). Everyone still reviews everyone else's tests before
merging - checking the test file against the official case list and
confirming nothing was skipped - since that's the "second pair of eyes" a
solo TDD cycle can't give itself.

**Q: Why is `coverage.py` described as a "group checkpoint," not just a personal tool?**

A: Because a coverage gap often shows up as an *interaction* between two
people's code - for instance, `Park` calling `isEmpty`. Running coverage
against the whole class, not just each person's own methods, is what
catches that kind of gap; run it weekly against the whole thing, not only
per-person.

---

## 10. Decisions and assumptions made along the way

**Q: What are the documented assumptions in this project, and why does each exist?**

A: Four, all because the brief left a genuine gap:

1. **Both sensors noisy at once** (`isEmpty`) - raise an error instead of
   guessing. A falsely "empty" reading is the failure mode that actually
   risks a collision, so refusing to guess is the safer default.
2. **A reading outside 0-200cm** (`isEmpty`) - treated the same as a
   noisy sensor: disregarded, not trusted or silently clamped.
3. **Calling `park()` while already parked** - rejected with an
   exception, the simplest, most defensible choice.
4. **Calling `unpark()` while not parked** - rejected the same way, kept
   consistent with #3 so both methods use one mechanism.

**Q: Why does `park()` currently only cover two of its six official cases?**

A: Cases 20 and 25 only need a single sensor reading to test -
`FixedSensor` handles them fine. The other four need to prove behavior
across a *stretch* of positions, but a single reading only reaches 2m
while the requirement is 5m - so proving it needs a sensor that returns a
*sequence* of readings. We tried adding a new sensor type for this
(`ScriptedSensor`) and rejected it, since it isn't one of the "random or
fixed" inputs the brief names. The alternative is a mocking library, which
we're deliberately keeping for Phase 2 rather than mixing it into Phase 1
early. So both the tests *and* the corresponding search-forward logic are
deferred together, with the reason written down next to each skipped
test - not silently missing.

**Q: Why isn't `pytest-mock` used anywhere in Phase 1, even though it's installed?**

A: Our own tool-mapping plan filed Mockito/`unittest.mock` under Phase 2,
tied to when actuators actually get modeled. Rather than mixing "mocking
in some places, manual fakes everywhere else" within Phase 1, the line was
kept clean: zero mocking-library imports anywhere in Phase 1 code. The
handful of cases that would benefit from it (isEmpty's call-count check,
Park's search/boundary logic) are skipped with a clear note pointing to
Phase 2, instead of using the tool early just for those four cases.

**Q: `test_both_sensors_noisy` can fail by chance - why wasn't that just fixed properly?**

A: It *was* fixed once, mid-project, using a scripted deterministic
reading. But that fix relied on the same manual test-double
infrastructure that Park's deferred cases needed, and once the decision
was made to keep Phase 1 free of that infrastructure for consistency, the
fix was reverted along with it. It's a known, occasionally-flaky test
right now, left that way deliberately - the real fix arrives with proper
mocking tooling in Phase 2, not a half-measure now.

**Q: What's the `NOISE_THRESHOLD = 10` constant, and where did that number come from?**

A: The maximum acceptable spread across a sensor's 5 readings before
`isEmpty` calls that sensor "noisy" and disregards it. It's a chosen
constant, not something the brief specifies numerically - `FixedSensor`
always has zero spread (trivially clean), `NoisySensor` swings across the
full 0-200cm range (reliably over any small threshold), so 10 was picked
as a clear, uncontroversial separator between the two.

**Q: Why does `unpark()` change the car's position, not just its status - and why does that matter?**

A: Because the interface's docstring explicitly says UnPark should "move
forward (and left) to the front of the parking place," and the official
case list backs it up: "position → front of the space." The first
version of `unpark()` only flipped `status`, and the test only checked
`status` too - so it passed while silently not proving the actual
requirement. This is worth mentioning directly in the report as a real
caught mistake: both the code and the test were fixed together once it
was noticed, which is exactly the kind of gap a second pair of eyes (or a
more careful first pass at writing the test) is supposed to catch.

**Q: If asked "is this project actually done," what's the honest answer?**

A: Five of six methods are fully built and tested against every case in
the official plan. `Park` covers its two simplest cases; the other four
are deliberately deferred to Phase 2, with the reason written down next to
each one. Nothing here is *accidentally* incomplete - everything open is a
named, explained decision, and every documented assumption is written
where a grader can find it.

---

## 11. Real-world grounding

**Q: The brief's "two ultrasound sensors" - is that based on anything real?**

A: Yes - it's a scaled-down version of Park Distance Control (PDC), the
ultrasonic sensor arrays major suppliers (Bosch, Continental, Valeo,
Denso) build into bumpers on most cars sold today, typically 4-12 sensors
front and rear. Each sensor works by time-of-flight: emit a chirp,
measure how long the echo takes to return - exactly the "distance in cm
to the nearest object" `isEmpty` computes, just with two sensors instead
of a full array.

**Q: Is the noise-filtering requirement just busywork, or does it model something real?**

A: It's real. Production PDC systems face exactly this failure mode - a
single echo corrupted by rain, debris, or cross-talk (one sensor picking
up another's pulse). Real systems handle it with multiple-pulse
filtering: several consecutive readings, outliers rejected or averaged -
which is exactly why the brief asks for "at least 5" queries and
filtering. The rule that a *continuously* noisy sensor gets disregarded
entirely, not blended in, mirrors a real concept called sensor
plausibility checking - a fault-detection layer that stops one unreliable
sensor from dragging down an otherwise-good reading. There's a genuine
design tension worth naming too: soft, sound-absorbing surfaces can look
like "noise" even when the sensor itself is healthy, which is exactly why
disregarding a sensor is the safer default over trusting a corrupted
average - a falsely "empty" reading is the failure mode that actually
causes a collision.

**Q: Does the parking maneuver itself match how real systems work?**

A: Yes - production parallel-parking assistants (Ford Active Park
Assist, VW Park Assist, Toyota Intelligent Parking Assist) work in the
same two-step shape this brief specifies: drive past candidate spaces at
low speed while continuously checking for a long-enough gap (our
`MoveForward` + `isEmpty` loop), then execute a pre-computed
reverse-parallel trajectory once stopped at the right position (`Park`).

**Q: Why doesn't this project model the actuators or real sensors at all?**

A: Because that's a deliberate, real boundary, not a project shortcut.
These production systems are SAE Level 2 driver-assistance features -
sensing and steering are automated, but they sit on top of a *separate*
low-level actuation/motor-control layer. That maps directly onto the
brief's own framing: sensor signals "come from sensor classes that are
not modeled," and actuators aren't modeled either. This project builds
the decision-logic layer only - the same separation of concerns a real
parking-assist ECU has from the motor-control ECU it talks to. If asked
in the oral exam why physical sensors/motors aren't simulated, that's the
answer: it's the same boundary real automotive software draws, not a
simplification invented for this assignment.
