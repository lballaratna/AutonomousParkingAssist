# Tests

One test file per method. Every test case comes from a requirement in the
Phase 1 brief - this document walks through what each file checks and why,
file by file.

---

## test_where_is.py — Owner: Harikrishna M

**Requirement:** report the car's current position and whether it is
parked or not.

Since this method does not calculate anything - it just reports the
current state - every case here is about checking it reports the
*correct* state at a specific point in time.

- a) Fresh car, before any movement => Position is 0, status is "unparked"
- b) After calling MoveForward twice => Position is 2
- c) Right after a successful Park => Status is "parked"
- d) Right after UnPark => Status is "unparked"

Cases c and d build their own car instead of reusing the shared fixture,
since the fixture's sensors always read "occupied" and park() would never
actually succeed on it.

---

## test_move_forward.py — Owner: Harikrishna M

**Requirement:** move the car one metre, check for a parking space while
moving, and never let the car go past either end of the 500m street.

- a) MoveForward from position 0 => Position becomes 1 (valid move)
- b) MoveForward from position 499 (one before the upper limit) => Position becomes 500 (valid move)
- c) MoveForward from position 500 (already at the upper limit) => Position stays at 500 - rejected
- d) Any successful move => A parking-space reading gets recorded

Cases a/b and c exist together on purpose - if we only tested a normal
value like 250 -> 251, an off-by-one bug right at the boundary would never
show up.

---

## test_move_backward.py — Owner: Pooney Joseph

**Requirement:** same as MoveForward, but backward, and the car must never
go below position 0.

- (a) MoveBackward from position 500 => Position becomes 499
- (b) MoveBackward from position 1 => Position becomes 0
- (c) MoveBackward from position 0 (already at the lower limit) => Position stays at 0 - rejected
- (d) Any successful move => A parking-space reading gets recorded

Case (d) starts the car at position 1 first, not 0 - starting at 0 would
make the move a no-op (case c), so it would never actually record anything.

---

## test_is_empty.py — Owner: Pooney Joseph

**Requirement:** query both ultrasonic sensors at least 5 times each,
filter out noise, disregard a sensor that is continuously noisy, and
return a distance between 0-200cm.

**Not provided in the requirement** (we decided these ourselves):
what happens if both sensors are noisy at the same time, and what happens
if a reading falls outside 0-200cm.

- (a) Both sensors are clean and agree => Filtered average of the two readings
- (b) Sensor A is noisy, B is clean => A is disregarded entirely; return B's reading
- (c) Sensor B is noisy, A is clean => B is disregarded entirely; return A's reading
- (d) Both sensors are noisy at the same time => raise an error instead of guessing (not in the requirements - our own decision)
- (e) Reading exactly 0cm (lower boundary) => Accepted as valid
- (f) Reading exactly 200cm (upper boundary) => Accepted as valid
- (g) Reading outside 0-200cm => treated as invalid, same as a noisy reading (not in the requirements - our own decision)
- Checking how many times each sensor is actually queried => Each sensor is read at least 5 times

Cases (d) and (g) are genuine gaps in the brief, not requirements we
missed - we made a call and wrote it down so it can go in the report as a
documented assumption.

The last case (checking the sensor was actually queried 5+ times) is
skipped for now - proving a call *count* needs a sensor that can track how
many times it was read, which needs mocking tooling (`pytest-mock`). We're
keeping that tool for Phase 2's sensor/actuator stubbing, so this one's
covered there instead of in Phase 1.

Also worth a note: `test_both_sensors_noisy` (case d) uses two real
`NoisySensor()` instances, and can occasionally fail purely by chance -
about 1 run in 5 during testing, when both sides' random readings happened
to land close enough together to not look noisy. A reliable fix needs the
same kind of scripted, mocking-based control as case 19, so it's left as a
known, rarely-flaky test for now rather than half-fixed with a workaround.

---

## test_park.py — Owner: Lavanya BallaRatna

**Requirement:** if the car is already at a free stretch of at least 5
metres, run the parking maneuver immediately. Otherwise, drive forward
until a long-enough stretch is found, then park. Parking while already
parked should not be allowed.

- Car is already at a valid free stretch (>=5m) => Maneuver runs immediately; status becomes "parked"
- Park called while already parked => Rejected

Four cases from the official list are written down but skipped for now,
all for the same reason:
- No stretch right here, but one exists further ahead (search forward)
- Free stretch is exactly 5.0m (boundary) => accepted
- Free stretch is 4.9m (just short) => rejected, search continues
- No qualifying stretch exists anywhere on the rest of the street

Measuring "how long is the free stretch ahead" needs more than a single
sensor reading - a single reading only goes up to 2m, but the requirement
is 5m. Proving that in a test needs a sensor that can return a *sequence*
of different readings, which `FixedSensor`/`RandomSensor` can't do. We
tried adding a new fake sensor type for this once (`ScriptedSensor`), then
decided against it - it wasn't one of the "random or fixed" inputs the
brief actually names. The other option is a sensor scripted via
`pytest-mock`, but we're keeping that mocking tool for Phase 2's
sensor/actuator stubbing instead of bringing it into Phase 1 early.
`park()` itself still only handles cases 20 and 25 for the same reason -
the search-forward logic these four tests would prove doesn't exist yet.

---

## test_unpark.py — Owner: Lavanya BallaRatna

**Requirement:** move the car forward (and left) to the front of the
parking space. This is only valid while the car is actually parked.

- Car is parked => status becomes "unparked", **and** the car moves
  forward to the front of the space (position increases by 1)
- Car is not parked => unpark is rejected, an error is raised
- UnPark immediately followed by WhereIs => WhereIs shows the same
  updated status and position, not just unpark()'s own return value

This one caught us out once already: the first version of `unpark()` only
flipped `status` and never actually moved the car, even though the
requirement explicitly says "move forward... to the front of the parking
place." The tests were only checking status too, so it passed without
actually proving the requirement. Both the tests and the code were fixed
together once this was noticed.

---

## Where we stand

24 of the 28 official test cases are implemented and passing. 5 are
skipped, all for the same underlying reason - they need a sensor that can
be scripted (a specific sequence of readings, or a way to count how many
times it was read), and we're deliberately keeping mocking tools
(`pytest-mock`/`unittest.mock`) for Phase 2's sensor/actuator stubbing
rather than bringing them into Phase 1 early:

- isEmpty case 19 (call-count check)
- Park cases 21, 22, 23, 24 (search-forward and the 5m boundary)

No mocking library is imported anywhere in the Phase 1 test suite right
now - every passing test uses only `FixedSensor`, `RandomSensor`, or
`NoisySensor`, exactly what the brief names.
