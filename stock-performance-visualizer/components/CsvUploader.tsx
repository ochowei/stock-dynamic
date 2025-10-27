import React, { useCallback } from 'react';
import Papa from 'papaparse';

interface CsvUploaderProps {
  onDataLoaded: (data: any[]) => void;
}

const CsvUploader: React.FC<CsvUploaderProps> = ({ onDataLoaded }) => {
  const handleFileChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (file) {
        Papa.parse(file, {
          header: true,
          dynamicTyping: true,
          skipEmptyLines: true,
          complete: (results) => {
            onDataLoaded(results.data);
          },
          error: (error: any) => {
            console.error('Error parsing CSV:', error);
          },
        });
      }
    },
    [onDataLoaded]
  );

  return (
    <div className="p-4 bg-gray-800 rounded-lg shadow-md flex items-center gap-4">
        <label htmlFor="csv-upload" className="font-bold text-lg text-gray-300">
            Upload CSV
        </label>
        <input
            id="csv-upload"
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-400
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-violet-50 file:text-violet-700
                hover:file:bg-violet-100"
        />
    </div>
  );
};

export default CsvUploader;