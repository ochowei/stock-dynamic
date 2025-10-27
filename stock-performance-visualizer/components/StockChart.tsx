
import React from 'react';
import {
  ComposedChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
  ReferenceLine
} from 'recharts';
import { StockDataPoint } from '../types';
import ChartCard from './ChartCard';

interface StockChartProps {
  data: StockDataPoint[];
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="p-2 bg-gray-700 border border-gray-600 rounded-md shadow-lg text-sm">
        <p className="label text-white">{`${new Date(label).toLocaleString()}`}</p>
        <p className="text-green-400">{`Open: ${data.open.toFixed(2)}`}</p>
        <p className="text-blue-400">{`High: ${data.high.toFixed(2)}`}</p>
        <p className="text-yellow-400">{`Low: ${data.low.toFixed(2)}`}</p>
        <p className="text-red-400">{`Close: ${data.close.toFixed(2)}`}</p>
        <p className="text-purple-400">{`Volume: ${data.volume.toLocaleString()}`}</p>
      </div>
    );
  }
  return null;
};

const StockChart: React.FC<StockChartProps> = ({ data }) => {
  const chartData = data.map(d => ({
    ...d,
    // data for floating bar
    body: [d.open, d.close].sort((a,b) => a-b)
  }));
  
  return (
    <ChartCard title="Price and Volume">
      <div className="w-full h-[500px]">
        <ResponsiveContainer width="100%" height="70%">
          <ComposedChart
            data={chartData}
            margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
            syncId="stockSync"
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#4A5568" />
            <XAxis dataKey="datetime" tickFormatter={(time) => new Date(time).toLocaleDateString()} stroke="#A0AEC0" />
            <YAxis yAxisId="left" orientation="left" stroke="#A0AEC0" domain={['dataMin - 5', 'dataMax + 5']} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Bar dataKey="range" yAxisId="left" fill="#6B7280" barSize={1} name="High-Low Range"/>
            <Bar dataKey="body" yAxisId="left" name="Open-Close">
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.close > entry.open ? '#10B981' : '#EF4444'} />
              ))}
            </Bar>
          </ComposedChart>
        </ResponsiveContainer>
        <ResponsiveContainer width="100%" height="30%">
          <ComposedChart
            data={data}
            margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
            syncId="stockSync"
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#4A5568" />
            <XAxis dataKey="datetime" tickFormatter={(time) => new Date(time).toLocaleDateString()} stroke="#A0AEC0" />
            <YAxis yAxisId="left" orientation="left" stroke="#A0AEC0" />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="volume" yAxisId="left" name="Volume" fill="#4C51BF" />
             <ReferenceLine y={0} stroke="#E2E8F0" yAxisId="left"/>
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  );
};

export default StockChart;
