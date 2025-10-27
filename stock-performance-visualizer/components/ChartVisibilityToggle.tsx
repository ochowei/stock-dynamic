import React from 'react';

export interface ChartVisibilityState {
  return: boolean;
  performance: boolean;
  kd: boolean;
  table: boolean;
}

interface ChartVisibilityToggleProps {
  visibility: ChartVisibilityState;
  onVisibilityChange: (chartKey: keyof ChartVisibilityState) => void;
}

const chartOptions: { key: keyof ChartVisibilityState; label: string }[] = [
    { key: 'return', label: 'Investment Return' },
    { key: 'performance', label: 'Performance Indicators' },
    { key: 'kd', label: 'KD Indicator' },
    { key: 'table', label: 'Data History' },
];

const ChartVisibilityToggle: React.FC<ChartVisibilityToggleProps> = ({ visibility, onVisibilityChange }) => {
  return (
    <div className="flex flex-wrap items-center justify-center gap-4 my-4 p-4 bg-gray-800 rounded-lg shadow-md">
      {chartOptions.map(({ key, label }) => (
        <div key={key} className="flex items-center">
          <input
            type="checkbox"
            id={`toggle-${key}`}
            checked={visibility[key]}
            onChange={() => onVisibilityChange(key)}
            className="w-4 h-4 text-indigo-600 bg-gray-700 border-gray-600 rounded focus:ring-indigo-500"
            aria-labelledby={`label-${key}`}
          />
          <label
            id={`label-${key}`}
            htmlFor={`toggle-${key}`}
            className="ml-2 text-sm font-medium text-gray-300"
          >
            {label}
          </label>
        </div>
      ))}
    </div>
  );
};

export default ChartVisibilityToggle;
