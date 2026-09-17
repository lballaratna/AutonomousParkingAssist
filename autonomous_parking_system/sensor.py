import random
from abc import ABC, abstractmethod

class Sensor(ABC):
    '''Ultrasound sensor contract. A real reading is 0-200 cm'''
    @abstractmethod
    def read(self) -> int: ...

class FixedSensor(Sensor):
    '''returns values close to the base value (±2) - simulates a clean,
    stable sensor with realistic minor variation'''
    def __init__(self, value: int):
        self._value = value
    def read(self) -> int:
        jittered = self._value + random.randint(-2, 2)
        if 0 <= self._value <= 200:
            return max(0, min(200, jittered))
        return jittered  # out-of-range base: let _is_noisy() catch it

class RandomSensor(Sensor):
    def read(self) -> int:
        return random.randint(0,200)

class NoisySensor(Sensor):
    '''wildy varying values, to stimulate a continously nosiy sensor'''
    def read(self) -> int:
        return random.choice([0,200,random.randint(0,200)])
    