from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import io
from population_manager import PopulationManager
from environment import Environment
import config


app = FastAPI()
PM = None


origins = [
    "http://localhost:5173",  # React dev server URL
    "http://127.0.0.1:5173",  # IP form
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationConfig(BaseModel):
    num_organisms: int
    percent_prey: float
    mutation_strength: float
    food_spawn_rate: int


@app.post("/start")
def start_simulation(config_input: SimulationConfig):
    global PM

    # Update config values before simulation
    config.NUM_ORGANISMS = config_input.num_organisms
    config.PERCENT_PREY = config_input.percent_prey
    config.MUTATION_STRENGTH = config_input.mutation_strength
    config.FOOD_SPAWN_RATE = config_input.food_spawn_rate

    env = Environment()
    PM = PopulationManager(env)

    return {"message": "Simulation started"}


@app.post("/tick")
def tick():
    if PM is None:
        return {"error": "Simulation not started"}
    for i in range(10): PM.tick()
    PM.record_history()
    # print(PM.history[-1])
    return PM.history[-1]  # Return the most recent stats


@app.post("/reset")
def reset_simulation():
    global PM
    PM = None
    return {"message": "Simulation reset"}


# For debugging purposes, return the history of generations
@app.get("/history")
def get_history():
    if PM is None:
        return {"error": "Simulation not started"}
    return PM.history