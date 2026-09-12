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
    