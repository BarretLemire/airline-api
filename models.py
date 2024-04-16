from pydantic import BaseModel

class Airline(BaseModel):
    name: str
    Flight: dict

class Flight(Airline):
    number: str
    capacity: int
    duration: int