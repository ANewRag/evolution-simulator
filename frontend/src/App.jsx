import React, { useState } from 'react';
import axios from 'axios';
import PopulationChart from './components/PopulationChart';
import TraitChart from './components/TraitChart';

function App() {
  const [history, setHistory] = useState([]);
  const [simulationStarted, setSimulationStarted] = useState(false);

  const startSimulation = async () => {
    try {
      const configData = {
        num_organisms: 100,
        percent_prey: 0.7,
        mutation_strength: 0.5,
        ticks: 100,
      };
      await axios.post('http://127.0.0.1:8000/start', configData);
      setSimulationStarted(true);
    } catch (error) {
      console.error("Failed to start simulation:", error);
    }
  };

  const tick = async () => {
    // console.log("Tick button clicked");

    const res = await axios.post('http://127.0.0.1:8000/tick');
    setHistory(prev => [...prev, res.data]);
  };

  return (
    <div className="App" style={{ padding: 20 }}>
      <h1>Evolution Simulator Dashboard</h1>
      {!simulationStarted ? (
        <button onClick={startSimulation}>Start Simulation</button>
      ) : (
        <>
          <button onClick={tick}>Next Tick</button>
          <PopulationChart history={history} />
          <TraitChart history={history} />
        </>
      )}
    </div>
  );
}


export default App;
