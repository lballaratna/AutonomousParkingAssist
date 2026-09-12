from abc import ABC, abstractmethod
from .state import CarState

class ParkingAssistantInterface(ABC):
    STREET_LENGTH = 500
    STRETCH_REQUIRED = 5

    @abstractmethod
    def where_is(self) -> CarState:
        '''return current position and parked/unparked status'''

    @abstractmethod
    def move_forward(self) -> CarState:
        '''move 1 m forward, query is_empty(), record the result.
        Must not move past STREET LENGTH'''

    @abstractmethod 
    def move_backward(self) -> CarState:
        '''move 1 m backward, query is_empty(), record the result.
        Must not move before postion 0'''

    @abstractmethod
    def is_empty(self) -> int:
        '''query both sensors >=5 times, filter noise, disregard a continously 
        noisy sensor, return distance in cm (0-200)'''

    @abstractmethod
    def park(self) -> CarState:
        '''park at the current positionif its state a free stretch of 
        STRETCH_REQUIRED meters, otherwise drive forward searching for one, 
        then park'''

    @abstractmethod
    def unpark(self) -> CarState:
        '''move forward (and left) to the front of the parking place.
        Only valid while status=="parked". '''



    