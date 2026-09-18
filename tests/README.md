# Tests

One test file per method. Every test case comes from a requirement in the
Phase 1 project instructions - this document walks through what each file
checks and why, file by file. Where a test exists to prove something we
decided ourselves rather than something the project instructions state,
that's called out explicitly as a documented assumption.

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
- RandomSensor readings stay within the documented 0-200cm range across many reads (not one of the official cases - added purely to exercise `RandomSensor`, which nothing else in the suite called directly)

Cases (d) and (g) are genuine gaps in the project instructions, not requirements we
missed - we made a call and wrote it down so it can go in the report as a
documented assumption.

The last case (checking each sensor was actually queried 5+ times) isn't
skipped any more. We'd originally assumed proving a call *count* needed a
sensor that could track how many times it was read via a mocking tool
(`pytest-mock`) - on the same reflection that produced `SequenceSensor`,
that turned out to be more than the job needed. `CountingSensor` in
`sensor.py` just wraps another sensor and increments a counter on every
`read()` call; the test wraps two `FixedSensor`s in it and asserts each
counter reaches at least 5 after one `is_empty()` call. No mocking library
involved.

Also worth a note: `test_both_sensors_noisy` (case d) uses two real
`NoisySensor()` instances, and can occasionally fail purely by chance -
about 1 run in 5 during testing, when both sides' random readings happened
to land close enough together to not look noisy. A reliable fix would need
the same kind of scripted control as `SequenceSensor`/`CountingSensor`
give the other tests, just not written yet for this one, so it's left as a
known, rarely-flaky test for now rather than half-fixed with a workaround.

---

## test_park.py — Owner: Lavanya BallaRatna

**Requirement:** if the car is already at a free stretch of at least 5
metres, run the parking maneuver immediately. Otherwise, drive forward
until a long-enough stretch is found, then park. Parking while already
parked should not be allowed.

- Car is already at a valid free stretch (>=5m) => Maneuver runs immediately; status becomes "parked"
- Park called while already parked => Rejected
- No stretch right here, but one exists further ahead => car drives forward (search) until it finds one, then reverses into it
- Free stretch is exactly 5.0m (boundary) => accepted
- Free stretch is 4.9m (just short) => rejected, search continues past it
- No qualifying stretch exists anywhere on the rest of the street => rejected once the street runs out
- A wall (or another car) sitting immediately after a qualifying stretch doesn't disqualify it - covered by the 5.0m boundary case above, since the search never looks past the 5th clear metre
- A wall can also be the physical end of the street itself, cutting a stretch short with only a few clear metres left => same rejection as "no qualifying stretch," proven separately since it's a different reason for running out of road
- The car actually reverses into the space once it's found, rather than just flagging a status - checked by comparing the furthest position the search reached against where the car ends up parked
- Park followed by UnPark is checked as a round trip: UnPark should land back at the far end the original search reached, not past it and not still inside the space

`park()` treats every `is_empty() == 0` reading as one clear metre, and
keeps a running count of *consecutive* clear metres starting from wherever
the car already is (reusing `move_forward()` + `isEmpty()`, one metre at a
time). A non-zero reading resets the count. Once the count reaches
`STRETCH_REQUIRED` (5), the car has driven to the far end of a qualifying
stretch - but that's the entrance to the space, not the finish. A real
parallel park means reversing into it, so `park()` then calls
`move_backward()` `STRETCH_REQUIRED - 1` times, landing the car at the
*start* of the stretch, before setting `status = "parked"`. If `position`
reaches `STREET_LENGTH` before a qualifying run of 5 is found, there was
never a long-enough gap, so `park()` raises instead of looping forever.
This reverse-in distance isn't spelled out anywhere in the project
instructions - it's our own reading of what "runs a standard parallel
reverse parking maneuver" has to mean, given the car only has one axis of
movement to work with.

Measuring "how long is the free stretch ahead" needs more than a single
sensor reading - a single reading only goes up to 2m, but the requirement
is 5m, so proving cases 23-26 needs a sensor that can return a *sequence*
of different readings as the car moves. `FixedSensor`/`RandomSensor` can't
do that. We'd earlier ruled out adding a sensor for this, planning to
reach for `pytest-mock` in Phase 2 instead - on reflection that was overkill
for what's actually needed here: a small hand-written test double
(`SequenceSensor` in `sensor.py`), in the same spirit as `FixedSensor` and
`NoisySensor`, that returns a scripted list of values instead of a fixed
or random one. No mocking library needed.

---

## test_unpark.py — Owner: Lavanya BallaRatna

**Requirement:** move the car forward (and left) to the front of the
parking space. This is only valid while the car is actually parked.

- Car is parked => status becomes "unparked", **and** the car moves
  forward to the front of the space (position increases by `STRETCH_REQUIRED - 1`)
- Car is not parked => unpark is rejected, an error is raised
- UnPark immediately followed by WhereIs => WhereIs shows the same
  updated status and position, not just unpark()'s own return value

This one caught us out twice, actually. First time: the very first version
of `unpark()` only flipped `status` and never actually moved the car, even
though the requirement explicitly says "move forward... to the front of
the parking place." The tests were only checking status too, so it passed
without actually proving the requirement. Both the tests and the code were
fixed together once this was noticed.

Second time, once `park()` started reversing into the space instead of
just flagging it as "parked": `unpark()` was still doing a flat
`position += 1`, a leftover from when `park()` left the car sitting at the
space's entrance rather than its back. With the reverse-in change, +1 was
no longer "the front of the space" - it was one metre further into a 5m
space the car had just backed all the way into. Caught by a test that
checks Park and UnPark together (`test_unpark_returns_to_front_of_space_found_by_park`
in `test_park.py`) rather than by either method's own tests in isolation,
which is exactly why that round-trip test was worth adding.

---

## Where we stand

All 33 test cases are implemented and passing - none skipped any more.
The case numbers run straight through 1-33 rather than stopping at the 29
the project instructions originally define:

- 1-19: the official cases, unchanged (WhereIs, MoveForward, MoveBackward,
  and isEmpty's a-g).
- 20: isEmpty's call-count case - originally left unnumbered in our own
  notes to avoid colliding with Park's official case 20, since it needed
  a sensor that could report how many times it was read. `CountingSensor`
  in `sensor.py` closed it: it just wraps another sensor and counts its
  `read()` calls, no mocking library involved. We've since given it an
  explicit number of its own (20) rather than leaving it as a named
  exception, which pushed every case from here on down by one.
- 21: our own addition - `RandomSensor` stays within its documented
  0-200cm range. Not asked for by the project instructions; added because
  nothing else in the suite exercised `RandomSensor` directly.
- 22-27: Park's official cases (originally numbered 20-25) - already at a
  free stretch, searching forward for one, the exact 5.0m boundary, the
  4.9m near miss, no stretch anywhere on the street, and Park while
  already parked. Cases 23-26 (search-forward and the boundary) needed
  `SequenceSensor`, a hand-written scripted-sequence test double, for the
  same reason `CountingSensor` was needed for case 20 - see the
  `test_park.py` section above.
- 28-30: our own additions - proving Park actually reverses into the
  space rather than just flagging it "parked", proving Park followed by
  UnPark is a sensible round trip, and the street's own end acting as a
  wall that cuts a stretch short.
- 31-33: UnPark's official cases (originally numbered 26-28), unchanged
  in behaviour - just renumbered to follow on from Park's extended range.

No mocking library is imported anywhere in the test suite; every passing
test uses `FixedSensor`, `RandomSensor`, `NoisySensor`, `SequenceSensor`,
or `CountingSensor`.
