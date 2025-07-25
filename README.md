# evolution-simulator
A biologically-inspired evolution simulator with a Python backend and interactive web frontend.

## Features
- Predator/Prey dynamics
- Asexual reproduction with mutation
- Real-time charting of population and trait evolution
- Adjustable simulation parameters (initial population, mutation rate, food spawn rate, tick speed, etc.)
- Play/pause, reset, and speed controls

## Simulation Details
There are two types of organisms: predators and prey. Each has a position, energy level, inheritable traits (just speed and size for now), and other parameters (movement cost, reproduction rate, etc.). During each tick of the simulation, food is spawned, every alive organism moves, those that find food eat, and some reproduce. Movement is determined by randomly choosing a direction and moving a certain number of steps, based on the speed stat. Organisms will consume any food available between their start and end points during this movement. Prey only eat the food that is spawned every tick, while predators only eat prey that are smaller than themselves. This puts evolutionary pressure on organisms to become larger, as larger prey are less likely to be eaten and larger predators can consume more of the prey they find. Similarly, there is a pressure for organisms to become faster, as the more distance covered during each tick, the greater the chance of finding food. These pressures are counterbalanced by the fact that larger and faster organisms require more energy to move, and organisms die when they run out of energy. To simulate (asexual) reproduction, organisms with enough energy have a chance to reproduce during each tick. Their child inherits traits sampled from a Gaussian distribution with the parent's trait value as the mean and the mutation rate as the standard deviation.

<img width="1897" height="926" alt="Screenshot 2025-07-23 at 2 38 30 PM" src="https://github.com/user-attachments/assets/9be67213-e995-4b40-bbfd-d23d514df4c5" />
<img width="1518" height="806" alt="Screenshot 2025-07-23 at 2 38 51 PM" src="https://github.com/user-attachments/assets/2286d6ad-8aef-4e17-864a-0677f3992374" />

## Installation
### 1. Clone the repo
```bash
git clone https://github.com/ANewRag/evolution-simulator.git
cd evolution-simulator
```
### 2. Setup Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn api:app --reload
```
### 3. Setup Frontend
In a separate terminal window, navigate to the `evolution-simulator` folder.
```bash
cd frontend
npm install
npm run dev
```

### 4. Visit http://localhost:5173/


## Usage
```markdown
1. Adjust the sliders to configure the simulation parameters.
2. Click play to begin ticking.
3. View population and trait charts in real-time.
4. Reset and tweak parameters anytime.
```
