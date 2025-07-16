import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PopulationChart from './components/PopulationChart';
import TraitChart from './components/TraitChart';

function App() {
  const [history, setHistory] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [simulationStarted, setSimulationStarted] = useState(false);
  const [isConfigurable, setIsConfigurable] = useState(true); // for sliders

  // Config values to be adjusted by the user
  const [numOrganisms, setNumOrganisms] = useState(500);
  const [percentPrey, setPercentPrey] = useState(0.7);
  const [mutationStrength, setMutationStrength] = useState(0.5);
  const [foodSpawnRate, setFoodSpawnRate] = useState(100);

  const [tickSpeedSetting, setTickSpeedSetting] = useState(10); // higher = faster, lower = slower
  const tickSpeed = 2000 / tickSpeedSetting;



  // Function to start the simulation (used both on mount and manually if needed)
  const startSimulation = async () => {
    try {
      const configData = {
        num_organisms: numOrganisms,
        percent_prey: percentPrey,
        mutation_strength: mutationStrength,
        food_spawn_rate: foodSpawnRate,
      };
      await axios.post('http://127.0.0.1:8000/start', configData);
      console.log("SIMULATION STARTED!!")
      setSimulationStarted(true);
      setIsConfigurable(false); // lock sliders after starting
    } catch (error) {
      console.error('Failed to start simulation:', error);
    }
  };

  const resetSimulation = async () => {
    try {
      await axios.post('http://127.0.0.1:8000/reset');
      setHistory([]);
      setIsRunning(false);
      setSimulationStarted(false);
      setIsConfigurable(true); // allow changing sliders after reset
    } catch (error) {
      console.error('Failed to reset simulation:', error);
    }
  };

  const handlePlayPause = async () => {
    if (!simulationStarted) {
      await startSimulation(); // locks sliders
    }
    setIsRunning(prev => !prev);
  };  

  // Automatically start the simulation on mount
/*   useEffect(() => {
    startSimulation();
    setIsConfigurable(false);
  }, []); */

  // Tick the simulation while running
  useEffect(() => {
    let intervalId;

    if (isRunning) {
      intervalId = setInterval(async () => {
        try {
          const res = await axios.post('http://127.0.0.1:8000/tick');
          setHistory(prev => [...prev, res.data]);
        } catch (error) {
          console.error("Tick failed:", error);
        }
      }, tickSpeed);
    }

    return () => clearInterval(intervalId);
  },  [isRunning, tickSpeed]);

  return (
    <div 
      className="App"
      style={{
        padding: 20,
        width: '100vw',  // Full viewport width
        height: '100vh', // Optional for full screen
        boxSizing: 'border-box',
        backgroundColor: '#1e1e1e',
        color: 'white',
      }}
      >
      <h1>Evolution Simulator Dashboard</h1>
  
      <div 
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          width: '100%',
          marginTop: 20,
          gap: 40, // space between charts and settings
        }}
      >
        {/* Left side: Charts */}
        <div style={{ flex: 1 }}>
          <PopulationChart history={history} />
          <TraitChart history={history} />
        </div>
  
        {/* Right side: Settings Panel */}
        <div
          style={{
            width: 300,
            padding: 20,
            border: '1px solid #ccc',
            borderRadius: 10,
            backgroundColor: '#f0f0f0',
            color: '#333',
            height: 'fit-content',
          }}
        >
          <h3>Settings</h3>
  
          {/* Play/Pause + Reset */}
          <button
            onClick={handlePlayPause}
            style={{
              backgroundColor: isRunning ? '#ff6666' : '#4caf50',
              color: 'white',
              border: 'none',
              borderRadius: 5,
              padding: '8px 16px',
              marginBottom: 10,
              cursor: 'pointer',
            }}
          >
            {isRunning ? "Pause" : "Play"}
          </button>
  
          <button
            onClick={resetSimulation}
            style={{
              backgroundColor: '#2196f3',
              color: 'white',
              border: 'none',
              borderRadius: 5,
              padding: '8px 16px',
              marginLeft: 10,
              cursor: 'pointer',
            }}
          >
            Reset
          </button>
  
          {/* Sliders */}
          <div style={{ marginTop: 20, opacity: !isConfigurable ? 0.5 : 1, pointerEvents: !isConfigurable ? 'none' : 'auto' }}>
            <label>Initial Population: {numOrganisms}</label>
            <input
              type="range"
              min="200"
              max="1000"
              value={numOrganisms}
              onChange={(e) => setNumOrganisms(Number(e.target.value))}
              style={{ width: '100%' }}
              disabled={!isConfigurable}
            />
            <br />
  
            <label>Prey Percentage: {Math.round(percentPrey * 100)}%</label>
            <input
              type="range"
              min="0.1"
              max="0.9"
              step="0.05"
              value={percentPrey}
              onChange={(e) => setPercentPrey(parseFloat(e.target.value))}
              style={{ width: '100%' }}
              disabled={!isConfigurable}
            />
            <br />

            <label>Food Spawned per Tick: {foodSpawnRate}</label>
            <input
              type="range"
              min="10"
              max="1000"
              step="10"
              value={foodSpawnRate}
              onChange={(e) => setFoodSpawnRate(Number(e.target.value))}
              style={{ width: '100%' }}
              disabled={!isConfigurable}
            />
  
            <label>Mutation Strength: {mutationStrength.toFixed(2)}</label>
            <input
              type="range"
              min="0.0"
              max="2.0"
              step="0.1"
              value={mutationStrength}
              onChange={(e) => setMutationStrength(parseFloat(e.target.value))}
              style={{ width: '100%' }}
              disabled={!isConfigurable}
            />

          
          </div>
  
          <div style={{ marginTop: 20 }}>
            <label>Tick Speed: {tickSpeedSetting}</label>
            <input
              type="range"
              min="1"
              max="20"
              step="1"
              value={tickSpeedSetting}
              onChange={(e) => setTickSpeedSetting(Number(e.target.value))}
              style={{ width: '100%' }}
            />
          </div>
        </div>
      </div>
    </div>
  );  
}

export default App;
