import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Legend,
  Tooltip,
} from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Legend, Tooltip);

const PopulationChart = ({ history }) => {
  const data = {
    labels: history.map(h => h.ticks),
    datasets: [
      {
        label: 'Prey',
        data: history.map(h => h.num_prey),
        borderColor: 'green',
        tension: 0.3,
      },
      {
        label: 'Predators',
        data: history.map(h => h.num_predators),
        borderColor: 'red',
        tension: 0.3,
      },
    ],
  };

  return (
    <div>
      <h2>Population Over Time</h2>
      <Line data={data} />
    </div>
  );
};

export default PopulationChart;