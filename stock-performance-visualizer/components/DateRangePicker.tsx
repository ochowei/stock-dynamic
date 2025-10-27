import React from 'react';

interface DateRangePickerProps {
  startDate: string;
  endDate: string;
  onStartDateChange: (date: string) => void;
  onEndDateChange: (date: string) => void;
  minDate: string;
  maxDate: string;
}

const DateRangePicker: React.FC<DateRangePickerProps> = ({
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
  minDate,
  maxDate,
}) => {
  return (
    <div className="flex flex-col sm:flex-row items-center justify-center gap-4 my-4 p-4 bg-gray-800 rounded-lg shadow-md">
      <div>
        <label htmlFor="startDate" className="text-gray-400 text-sm font-medium mr-2">Start Date:</label>
        <input
          type="date"
          id="startDate"
          name="startDate"
          value={startDate}
          min={minDate}
          max={endDate} 
          onChange={(e) => onStartDateChange(e.target.value)}
          className="bg-gray-700 text-white rounded-md p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          aria-label="Start Date"
        />
      </div>
      <div>
        <label htmlFor="endDate" className="text-gray-400 text-sm font-medium mr-2">End Date:</label>
        <input
          type="date"
          id="endDate"
          name="endDate"
          value={endDate}
          min={startDate}
          max={maxDate}
          onChange={(e) => onEndDateChange(e.target.value)}
          className="bg-gray-700 text-white rounded-md p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          aria-label="End Date"
        />
      </div>
    </div>
  );
};

export default DateRangePicker;