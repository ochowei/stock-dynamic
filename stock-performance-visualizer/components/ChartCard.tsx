
import React from 'react';

interface ChartCardProps {
  title: string;
  children: React.ReactNode;
}

const ChartCard: React.FC<ChartCardProps> = ({ title, children }) => {
  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
      <h2 className="text-lg font-semibold text-gray-300 mb-4">{title}</h2>
      <div className="h-full">
        {children}
      </div>
    </div>
  );
};

export default ChartCard;
