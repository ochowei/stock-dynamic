
export interface StockDataPoint {
  datetime: Date;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  pBuy: number;
  pSell: number;
  priceDiff: number;
  return: number;
  // For candlestick chart
  ohlc: [number, number, number, number];
  range: [number, number];
  // For KD indicator
  k?: number | null;
  d?: number | null;
}
