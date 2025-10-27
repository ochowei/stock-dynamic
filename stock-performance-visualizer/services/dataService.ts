import { StockDataPoint } from '../types';

function calculateKD(data: StockDataPoint[], period: number = 14, dPeriod: number = 3): StockDataPoint[] {
  const dataWithK = data.map((point, index, arr) => {
    if (index < period - 1) {
      return { ...point, k: null, d: null };
    }

    const lookback = arr.slice(index - period + 1, index + 1);
    const lowestLow = Math.min(...lookback.map(p => p.low));
    const highestHigh = Math.max(...lookback.map(p => p.high));

    const kValue = highestHigh === lowestLow ? 0 : ((point.close - lowestLow) / (highestHigh - lowestLow)) * 100;
    return { ...point, k: kValue, d: null };
  });

  return dataWithK.map((point, index, arr) => {
    if (index < period - 1 + dPeriod - 1) {
      return point;
    }
    const kValues = arr.slice(index - dPeriod + 1, index + 1).map(p => p.k).filter(k => k !== null) as number[];
    if(kValues.length < dPeriod) return point;

    const dValue = kValues.reduce((sum, val) => sum + val, 0) / dPeriod;
    return { ...point, d: dValue };
  });
}

export const parseAndProcessStockData = (parsedData: any[]): StockDataPoint[] => {
    const formattedData = parsedData.map(item => ({
        datetime: new Date(item.Datetime),
        open: item.Open,
        high: item.High,
        low: item.Low,
        close: item.Close,
        volume: item.Volume,
        pBuy: item.P_buy,
        pSell: "P_sell" in item ? item.P_sell : 0,
        priceDiff: "price_diff" in item ? item.price_diff : 0,
        return: "return" in item ? item.return : 0,
    }));

    // Add candlestick specific fields
    let processed = formattedData.map(d => ({
        ...d,
        ohlc: [d.open, d.high, d.low, d.close] as [number, number, number, number],
        range: [d.low, d.high] as [number, number]
    }));
    
    // Calculate KD
    processed = calculateKD(processed);

    return processed;
};
