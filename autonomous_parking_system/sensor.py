import random
from abc import ABC, abstractmethod

class Sensor(ABC):
    '''Ultrasound sensor contract. A real reading is 0-200 cm'''
    @abstractmethod
    def read(self) -> int: ...

class FixedSensor(Sensor):
    '''always returns the same value-deterministic test cases'''
    def __init__(self,value: int):
        self._value=value
    def read(self) -> int:
        return self._value 

class RandomSensor(Sensor):
    def read(self) -> int:
        return random.randint(0,200)

class NoisySensor(Sensor):
    '''wildy varying values, to stimulate a continously nosiy sensor'''
    def read(self) -> int:
        return random.choice([0,200,random.randint(0,200)])

class CountingSensor(Sensor):
    '''Wraps another sensor and counts how many times read() was called,
    so a test can prove a call count without a mocking library.'''
    def __init__(self, wrapped: Sensor):
        self._wrapped = wrapped
        self.call_count = 0

    def read(self) -> int:
        self.call_count += 1
        return self._wrapped.read()

class SequenceSensor(Sensor):
    '''Returns a pre-set list of values, one block per metre, so a test can
    script a sensor whose reading changes as the car drives forward -
    without a mocking library. is_empty() reads a sensor 5 times per check
    (to filter noise), so each value in `values` is repeated `repeat`
    times in a row before moving on to the next one. Once the list runs
    out, the last value repeats forever.'''
    def __init__(self, values, repeat: int = 5):
        self._values = list(values)
        self._repeat = repeat
        self._calls = 0

    def read(self) -> int:
        index = min(self._calls // self._repeat, len(self._values) - 1)
        self._calls += 1
        return self._values[index]
