from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import httpx
import requests
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

app = FastAPI()
load_dotenv()

@app.get("/")
async def root():
    return {"message": "Project root"}

# info received from frontend:
# state (required)
# car year (required)
# car make (required)
# car model (required)
# number of passengers (required)
# trip distance

# info sent back:
# A: list of options of specific cars for user to select
# B: only one option so just get the id for that car

# second API call:
# id from selected car (or only option)
# to fuel economy site, get miles per gallon
# also call state gas price/gallon api and get price for selected state

# return two calculations:
# 1. total owed per passenger
# 2. total owed overall

class Vehicle(BaseModel):
    year: int
    make: str
    model: str | None=None
    
class Trip(BaseModel):
    state: str
    vehicleId: int
    tripDistance: float
    numPassengers: int

@app.post("/find_vehicle")
async def find_vehicle(vehicle: Vehicle):
    params = vehicle.model_dump()
    api_url = "https://www.fueleconomy.gov/ws/rest/vehicle/menu/options"
    
    res = requests.get(api_url, params=params)
    # TODO error handling
    # if(res.status_code != 200):

    root = ET.fromstring(res.content)
    car_options = []
    for car in root.findall('menuItem'):
        carName = car.findtext('text')
        carId = car.findtext('value')
        car_dict = {"name": carName, "id": int(carId)}
        car_options.append(car_dict)
    
    return car_options


@app.post("/calculate_trip")
async def calculate_trip(trip: Trip):

    async with httpx.AsyncClient() as client:
        mpg, gallon_cost = await asyncio.gather(
            get_mpg(client, trip.vehicleId),
            get_state_price(client, trip.state)
        )
    
    gallons_used = (trip.tripDistance)/mpg
    total_cost = gallons_used * gallon_cost
    per_passenger_cost = total_cost / (trip.numPassengers)

    return {"total": total_cost, "per_passenger": per_passenger_cost}

    
async def get_mpg(client: httpx.AsyncClient, id: int):
    car_mpg_url = "https://www.fueleconomy.gov/ws/rest/ympg/shared/ympgVehicle/" + str(id)
    res = await client.get(car_mpg_url)
    # TODO error handling
    res.raise_for_status()
    root = ET.fromstring(res.content)
    avgMpg = root.findtext('avgMpg')
    return float(avgMpg)


async def get_state_price(client: httpx.AsyncClient, state: str):
    params = {"state": state}
    state_url = "https://api.collectapi.com/gasPrice/stateUsaPrice"
    headers = {
        "authorization": # TODO,
        "content-type": "application/json"
    }

    res = await client.get(state_url, headers=headers, params=params)
    res.raise_for_status()
    data = res.json()

    return float(data["result"]["state"]["gasoline"])