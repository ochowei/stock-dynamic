
import React from 'react';
import { StockDataPoint } from '../types';
import ChartCard from './ChartCard';

interface DataTableProps {
  data: StockDataPoint[];
}

const DataTable: React.FC<DataTableProps> = ({ data }) => {
  const formatNumber = (num: number | null | undefined, digits = 2) => {
    if (num === null || typeof num === 'undefined') return 'N/A';
    return num.toFixed(digits);
  };
  
  const formatPercentage = (num: number | null | undefined) => {
     if (num === null || typeof num === 'undefined') return 'N/A';
     return `${(num * 100).toFixed(2)}%`;
  }

  const headers = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'P_Buy', 'P_Sell', 'Return', 'K%', 'D%'];

  return (
    <ChartCard title="Data History">
      <div className="overflow-x-auto max-h-[400px]">
        <table className="w-full text-sm text-left text-gray-400">
          <thead className="text-xs text-gray-300 uppercase bg-gray-700 sticky top-0">
            <tr>
              {headers.map(header => (
                <th key={header} scope="col" className="px-4 py-3 whitespace-nowrap">{header}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index} className="border-b border-gray-700 hover:bg-gray-600">
                <td className="px-4 py-2 whitespace-nowrap">{row.datetime.toLocaleString()}</td>
                <td className="px-4 py-2">{formatNumber(row.open)}</td>
                <td className="px-4 py-2">{formatNumber(row.high)}</td>
                <td className="px-4 py-2">{formatNumber(row.low)}</td>
                <td className="px-4 py-2">{formatNumber(row.close)}</td>
                <td className="px-4 py-2">{row.volume.toLocaleString()}</td>
                <td className="px-4 py-2">{formatNumber(row.pBuy)}</td>
                <td className="px-4 py-2">{formatNumber(row.pSell)}</td>
                <td className={`px-4 py-2 ${row.return >= 0 ? 'text-green-400' : 'text-red-400'}`}>{formatPercentage(row.return)}</td>
                <td className="px-4 py-2">{formatNumber(row.k)}</td>
                <td className="px-4 py-2">{formatNumber(row.d)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </ChartCard>
  );
};

export default DataTable;
