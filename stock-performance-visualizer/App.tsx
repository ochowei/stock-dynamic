import React, { useState, useEffect } from 'react';
import { StockDataPoint } from './types';
import { parseAndProcessStockData } from './services/dataService';
import Header from './components/Header';
import StockChart from './components/StockChart';
import IndicatorChart from './components/IndicatorChart';
import DataTable from './components/DataTable';
import ChartCard from './components/ChartCard';
import DateRangePicker from './components/DateRangePicker';
import ChartVisibilityToggle, { ChartVisibilityState } from './components/ChartVisibilityToggle';
import CsvUploader from './components/CsvUploader';


const formatDateForInput = (date: Date): string => {
  return date.toISOString().split('T')[0];
};

const App: React.FC = () => {
  const [data, setData] = useState<StockDataPoint[]>([]);
  const [filteredData, setFilteredData] = useState<StockDataPoint[]>([]);
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [minDate, setMinDate] = useState<string>('');
  const [maxDate, setMaxDate] = useState<string>('');

  const [chartVisibility, setChartVisibility] = useState<ChartVisibilityState>({
    return: true,
    performance: true,
    kd: true,
    table: true,
  });

  const handleDataLoaded = (parsedData: any[]) => {
    try {
      const processedData = parseAndProcessStockData(parsedData);
      setData(processedData);

      if (processedData.length > 0) {
        const firstDate = new Date(processedData[0].datetime);
        const lastDate = new Date(processedData[processedData.length - 1].datetime);

        const formattedFirstDate = formatDateForInput(firstDate);
        const formattedLastDate = formatDateForInput(lastDate);

        setStartDate(formattedFirstDate);
        setEndDate(formattedLastDate);
        setMinDate(formattedFirstDate);
        setMaxDate(formattedLastDate);
      }
    } catch (error) {
      console.error("Failed to process stock data:", error);
      // Optionally, provide user feedback here
    }
  };

  useEffect(() => {
    if (data.length > 0 && startDate && endDate) {
      const start = new Date(startDate);
      start.setUTCHours(0, 0, 0, 0);

      const end = new Date(endDate);
      end.setUTCHours(23, 59, 59, 999);

      const filtered = data.filter(d => {
        const pointDate = d.datetime;
        return pointDate >= start && pointDate <= end;
      });
      setFilteredData(filtered);
    } else {
      setFilteredData([]);
    }
  }, [data, startDate, endDate]);

  const handleVisibilityChange = (chartKey: keyof ChartVisibilityState) => {
    setChartVisibility(prev => ({ ...prev, [chartKey]: !prev[chartKey] }));
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-200 font-sans">
      <Header />
      <main className="p-4 sm:p-6 lg:p-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="md:col-span-1">
            <CsvUploader onDataLoaded={handleDataLoaded} />
          </div>
          <div className="md:col-span-2">
            <DateRangePicker
              startDate={startDate}
              endDate={endDate}
              onStartDateChange={setStartDate}
              onEndDateChange={setEndDate}
              minDate={minDate}
              maxDate={maxDate}
              disabled={data.length === 0}
            />
          </div>
        </div>
        <ChartVisibilityToggle
            visibility={chartVisibility}
            onVisibilityChange={handleVisibilityChange}
        />

        {data.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-2xl text-gray-500">No data available. Please upload a CSV file to begin.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 mt-6">
            <StockChart data={filteredData} />

            {chartVisibility.return && (
              <ChartCard title="Investment Return">
                  <IndicatorChart
                    data={filteredData}
                    lines={[
                      { dataKey: 'return', color: '#A78BFA', name: 'Return' },
                    ]}
                    height={300}
                    isPercentage={true}
                  />
              </ChartCard>
            )}

            {chartVisibility.performance && (
              <ChartCard title="Performance Indicators">
                <IndicatorChart 
                  data={filteredData}
                  lines={[
                    { dataKey: 'pBuy', color: '#34D399', name: 'Buy Price' },
                    { dataKey: 'pSell', color: '#F87171', name: 'Sell Price' },
                  ]}
                  height={300}
                />
              </ChartCard>
            )}

            {chartVisibility.kd && (
              <ChartCard title="KD Indicator">
                  <IndicatorChart
                      data={filteredData}
                      lines={[
                          { dataKey: 'k', color: '#FBBF24', name: 'K' },
                          { dataKey: 'd', color: '#818CF8', name: 'D' },
                      ]}
                      height={300}
                      domain={[0, 100]}
                  />
              </ChartCard>
            )}

            {chartVisibility.table && (
              <DataTable data={filteredData} />
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default App;