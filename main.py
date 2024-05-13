#"""
#Have these endpoints:

#GET / -> list[airline_name]
#GET /:airline_name -> list[flight_num]
#GET /:airline_name/:flight_num -> Flight

#POST /:airline
#PUT /:airline/:flight_num
#DELETE /:airline/:flight_num

#"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from models import Airline, Flight
import json

app = FastAPI()

from models import Airline, Flight

# Load data from JSON
with open('airlines.json', 'r') as file:
    data = json.load(file)

# Create Airline objects
airlines = []
for name, flights in data.items():
    airline = Airline(name=name, flights=[Flight(**flight) for flight in flights])
    airlines.append(airline)


@app.get("/")
def get_airlines() -> List[str]:
    return [airline.name for airline in airlines]


@app.get("/{airline_name}")
def get_flights(airline_name: str) -> List[str]:
    airline = next((airline for airline in airlines if airline.name == airline_name), None)
    if airline:
        return [flight.flight_num for flight in airline.flights]
    else:
        raise HTTPException(status_code=404, detail="Airline not found")


@app.get("/{airline_name}/{flight_num}")
def get_flight(airline_name: str, flight_num: str) -> Flight:
    airline = next((airline for airline in airlines if airline.name == airline_name), None)
    if airline:
        flight = next((flight for flight in airline.flights if flight.flight_num == flight_num), None)
        if flight:
            return flight
        else:
            raise HTTPException(status_code=404, detail="Flight not found")
    else:
        raise HTTPException(status_code=404, detail="Airline not found")


@app.post("/{airline_name}")
def create_flight(airline_name: str, flight: Flight):
    airline = next((airline for airline in airlines if airline.name == airline_name), None)
    if airline:
        airline.flights.append(flight)
        return {"message": "Flight created successfully"}
    else:
        raise HTTPException(status_code=404, detail="Airline not found")


@app.put("/{airline_name}/{flight_num}")
def update_flight(airline_name: str, flight_num: str, flight: Flight):
    airline = next((airline for airline in airlines if airline.name == airline_name), None)
    if airline:
        existing_flight = next((f for f in airline.flights if f.flight_num == flight_num), None)
        if existing_flight:
            existing_flight.capacity = flight.capacity
            existing_flight.estimated_flight_duration = flight.estimated_flight_duration
            return {"message": "Flight updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Flight not found")
    else:
        raise HTTPException(status_code=404, detail="Airline not found")


@app.delete("/{airline_name}/{flight_num}")
def delete_flight(airline_name: str, flight_num: str):
    airline = next((airline for airline in airlines if airline.name == airline_name), None)
    if airline:
        flight_to_delete = next((f for f in airline.flights if f.flight_num == flight_num), None)
        if flight_to_delete:
            airline.flights.remove(flight_to_delete)
            return {"message": "Flight deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Flight not found")
    else:
        raise HTTPException(status_code=404, detail="Airline not found")
