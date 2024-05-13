from pydantic import BaseModel
from typing import List, Dict

from pydantic import BaseModel

class Flight(BaseModel):
    flight_num: str
    capacity: int
    estimated_flight_duration: int

class Airline(BaseModel):
    name: str
    flights: List[Flight]