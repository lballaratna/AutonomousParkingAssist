from dataclasses import dataclass, field
from typing import List, Literal, Optional

Status=Literal["moving","parked","unparked"]

@dataclass

class ParkingRecord:

    '''one isEmpty() reading, tied to the position it was taken at '''
    position: int
    distance_cm: Optional[int]

@dataclass

class CarState:
    position: int=0
    status: Status = "unparked"
    records: List[ParkingRecord] =field(default_factory=list)
    
    