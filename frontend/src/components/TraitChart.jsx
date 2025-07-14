import React from 'react';
import { Line } from 'react-chartjs-2';

const TraitChart = ({ history }) => {
  const ticks = history.map(h => h.ticks);
  // console.log(ticks);

  return (
    <div>
      <h2>Traits Over Time</h2>
      <Line
        data={{
          labels: ticks,
          datasets: [
            {
              label: 'Avg Speed (Prey)',
              data: history.map(h => h.avg_speed_prey),
              borderColor: 'blue',
            },
            {
              label: 'Avg Speed (Predators)',
              data: history.map(h => h.avg_speed_predator),
              borderColor: 'purple',
            },
            {
              label: 'Avg Size (Prey)',
              data: history.map(h => h.avg_size_prey),
              borderColor: 'orange',
            },
            {
              label: 'Avg Size (Predators)',
              data: history.map(h => h.avg_size_predator),
              borderColor: 'brown',
            },
          ],
        }}
      />
    </div>
  );
};

export default TraitChart;