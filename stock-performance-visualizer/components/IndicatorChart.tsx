
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import { StockDataPoint } from '../types';

interface LineInfo {
    dataKey: keyof StockDataPoint;
    color: string;
    name: string;
}

interface IndicatorChartProps {
  data: StockDataPoint[];
  lines: LineInfo[];
  height?: number;
  domain?: [number | string, number | string];
  isPercentage?: boolean;
}

const CustomTooltip = ({ active, payload, label }: any, isPercentage: boolean) => {
    if (active && payload && payload.length) {
      return (
        <div className="p-2 bg-gray-700 border border-gray-600 rounded-md shadow-lg text-sm">
          <p className="label text-white">{`${new Date(label).toLocaleString()}`}</p>
          {payload.map((pld: any) => (
            <p key={pld.name} style={{ color: pld.color }}>
              {`${pld.name}: ${isPercentage ? (pld.value * 100).toFixed(2) + '%' : pld.value.toFixed(2)}`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

const IndicatorChart: React.FC<IndicatorChartProps> = ({ data, lines, height = 300, domain, isPercentage = false }) => {
  return (
    <div style={{ width: '100%', height }}>
      <ResponsiveContainer>
        <LineChart 
          data={data}
          margin={{ top: 5, right: 20, left: -10, bottom: 5 }}
          syncId="stockSync"
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#4A5568" />
          <XAxis dataKey="datetime" tickFormatter={(time) => new Date(time).toLocaleDateString()} stroke="#A0AEC0" />
          <YAxis stroke="#A0AEC0" domain={domain} tickFormatter={isPercentage ? (val) => `${(val * 100).toFixed(0)}%` : undefined} />
          <Tooltip content={(props) => CustomTooltip(props, isPercentage)} />
          <Legend />
          {lines.map(line => (
             <Line key={line.dataKey as string} type="monotone" dataKey={line.dataKey} stroke={line.color} dot={false} name={line.name} />
          ))}
          {domain && <ReferenceLine y={domain[0]} stroke="#A0AEC0" />}
          {domain && <ReferenceLine y={domain[1]} stroke="#A0AEC0" />}
          {domain && <ReferenceLine y={20} stroke="#FBBF24" strokeDasharray="3 3"/>}
          {domain && <ReferenceLine y={80} stroke="#FBBF24" strokeDasharray="3 3"/>}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default IndicatorChart;
