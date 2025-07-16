from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
from .population_manager import PopulationManager
from .environment import Environment
from . import config


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

@app.get("/plot/population")
def plot_population():
    if PM is None or not PM.history:
        return {"error": "No simulation run yet."}

    ticks = [h["ticks"] for h in PM.history]
    num_prey = [h["num_prey"] for h in PM.history]
    num_predators = [h["num_predators"] for h in PM.history]

    plt.figure(figsize=(8, 4))
    plt.plot(ticks, num_prey, label="Prey", color="green")
    plt.plot(ticks, num_predators, label="Predators", color="red")
    plt.title("Population Over Time")
    plt.xlabel("Generation")
    plt.ylabel("Population")
    plt.legend()
    plt.grid(True)

    # Save to memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.get("/plot/traits")
def plot_traits():
    if PM is None or not PM.history:
        return {"error": "No simulation run yet."}

    ticks = [h["ticks"] for h in PM.history]
    avg_speed_prey = [h["avg_speed_prey"] for h in PM.history]
    avg_speed_pred = [h["avg_speed_predator"] for h in PM.history]
    avg_size_prey = [h["avg_size_prey"] for h in PM.history]
    avg_size_pred = [h["avg_size_predator"] for h in PM.history]

    fig, axs = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    axs[0].plot(ticks, avg_speed_prey, label="Prey", color="green")
    axs[0].plot(ticks, avg_speed_pred, label="Predator", color="red")
    axs[0].set_ylabel("Speed")
    axs[0].set_title("Average Speed Over Time")
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(ticks, avg_size_prey, label="Prey", color="green")
    axs[1].plot(ticks, avg_size_pred, label="Predator", color="red")
    axs[1].set_ylabel("Size")
    axs[1].set_xlabel("Generation")
    axs[1].set_title("Average Size Over Time")
    axs[1].legend()
    axs[1].grid(True)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

# For debugging purposes, return the history of generations
@app.get("/history")
def get_history():
    if PM is None:
        return {"error": "Simulation not started"}
    return PM.history


@app.post("/tick")
def tick():
    if PM is None:
        return {"error": "Simulation not started"}
    for i in range(10): PM.tick()
    PM.record_history()
    print(PM.history[-1])
    return PM.history[-1]  # Return the most recent stats

@app.post("/reset")
def reset_simulation():
    global PM
    PM = None
    return {"message": "Simulation reset"}