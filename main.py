#"""
#Have these endpoints:

#GET / -> list[airline_name]
#GET /:airline_name -> list[flight_num]
#GET /:airline_name/:flight_num -> Flight

#POST /:airline
#PUT /:airline/:flight_num
#DELETE /:airline/:flight_num

#"""
import json
from fastapi import FastAPI, HTTPException
from typing import List, Dict
from models import Airline, Flight


with open("airlines.json", "r") as f:
    airline_data = json.load(f)


airline_names = [airline for airline in airline_data]

app = FastAPI()


@app.get("/airlines")
async def get_airline_names() -> List[str]:
    return airline_names


@app.get("/{airline_name}")
async def get_flight_numbers(airline_name: str) -> List[str]:
    for airline in airline_data:
        if airline["name"] == airline_name:
            return [flight["number"] for flight in airline["flights"]]
    raise HTTPException(status_code=404, detail="Airline not found")


@app.get("/{airline_name}/{flight_num}")
async def get_flight(airline_name: str, flight_num: str) -> Flight:
    for airline in airline_data:
        if airline["name"] == airline_name:
            for flight in airline["flights"]:
                if flight["number"] == flight_num:
                    return Flight(**flight)
    raise HTTPException(status_code=404, detail="Flight not found")


@app.post("/{airline_name}")
async def new_airline(airline: Airline) -> List[str]:
    airline_names.append(airline.name)
    airline_data.append(airline.dict())
    return airline_names


@app.put("/{airline}/{flight_num}")
async def update_flight(airline: str, flight_num: str, flight_details: Dict) -> Flight:
    for airline_data in airline_data:
        if airline_data["name"] == airline:
            for flight in airline_data["flights"]:
                if flight["number"] == flight_num:
                    flight.update(flight_details)
                    return Flight(**flight)
    raise HTTPException(status_code=404, detail="Flight not found")


@app.delete("/{airline}/{flight_num}")
async def delete_flight(airline: str, flight_num: str) -> List[Flight]:
    for airline_data in airline_data:
        if airline_data["name"] == airline:
            for flight in airline_data["flights"]:
                if flight["number"] == flight_num:
                    airline_data["flights"].remove(flight)
                    return airline_data["flights"]
    raise HTTPException(status_code=404, detail="Flight not found")
