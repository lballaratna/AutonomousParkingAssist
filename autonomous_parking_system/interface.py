from abc import ABC, abstractmethod
from .state import CarState

class ParkingAssistantInterface(ABC):
    STREET_LENGTH = 500
    STRETCH_REQUIRED = 5

    @abstractmethod
    def where_is(self) -> CarState:
        '''
        Description: return current position and parked/unparked status.
        Pre-condition: none.
        Post-condition: state is unchanged, just reported back.
        Test-cases: a, b, c, d (tests/test_where_is.py)
        '''

    @abstractmethod
    def move_forward(self) -> CarState:
        '''
        Description: move 1 m forward, query is_empty(), record the result.
        Must not move past STREET_LENGTH.
        Pre-condition: none.
        Post-condition: if position < STREET_LENGTH, position goes up by 1
        and a new reading gets recorded; if position == STREET_LENGTH,
        nothing changes (rejected, no-op).
        Test-cases: a, b, c, d (tests/test_move_forward.py)
        '''

    @abstractmethod
    def move_backward(self) -> CarState:
        '''
        Description: move 1 m backward, query is_empty(), record the result.
        Must not move before postion 0.
        Pre-condition: none.
        Post-condition: if position > 0, position goes down by 1 and a new
        reading gets recorded; if position == 0, nothing changes (rejected,
        no-op).
        Test-cases: a, b, c, d (tests/test_move_backward.py)
        '''

    @abstractmethod
    def is_empty(self) -> int:
        '''
        Description: query both sensors >=5 times, filter noise, disregard a
        continously noisy sensor, return distance in cm (0-200).
        Pre-condition: none.
        Post-condition: returns an int in 0-200 if at least one sensor is
        not noisy; raises an error if both sensors are noisy at the same
        time (not mentioned in the requirement - our own decision).
        Test-cases: a, b, c, d, e, f, g, and the call-count case (f)
        (tests/test_is_empty.py) - the call-count case is covered in Phase 2.
        '''

    @abstractmethod
    def park(self) -> CarState:
        '''
        Description: park at the current position if it's at a free stretch
        of STRETCH_REQUIRED meters, otherwise drive forward searching for
        one, then park.
        Pre-condition: car must not already be parked.
        Post-condition: status becomes "parked" once a qualifying stretch is
        found; raises an error if park() is called while already parked
        (not mentioned in the requirement - our own decision, same
        reasoning as unpark() below).
        Test-cases: case 20, case 25 (tests/test_park.py) - built for Phase
        1. Cases 21-24 (searching forward, the exact 5m boundary, no
        stretch found anywhere) are skipped for now, covered in Phase 2.
        '''

    @abstractmethod
    def unpark(self) -> CarState:
        '''
        Description: move forward (and left) to the front of the parking
        place. Only valid while status=="parked".
        Pre-condition: car must be parked.
        Post-condition: position moves forward by 1 and status becomes
        "unparked"; raises an error if unpark() is called while not parked
        (the requirement only says what happens "if it is parked" - it
        doesn't say what to do otherwise, so this is our own decision).
        Test-cases: case 26, 27, 28 (tests/test_unpark.py)
        '''



    