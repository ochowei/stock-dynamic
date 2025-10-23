import yfinance as yf
import pytz
import argparse
import pandas as pd

def download_stock_data(tickers: list, interval_short: str, interval_long: str, start_date, end_date, period: str, args: argparse.Namespace):
    """
    Downloads stock data for the given tickers and intervals, and handles timezone conversion.
    """
    print("=======================================================")
    print(f"======= 開始批次下載資料 (Starting Batch Download) =======")
    print(f"Tickers: {tickers}")
    print(f"Intervals: {interval_short}, {interval_long}")
    print(f"Period: {period}")
    print(f"Pre/Post Market (Short): {args.prepost_short}")
    print(f"Pre/Post Market (Long): {args.prepost_long}")
    print("=======================================================\n")

    data_short_interval_batch = yf.download(
        tickers=tickers,
        interval=interval_short,
        start=start_date,
        end=end_date,
        progress=True,
        prepost=args.prepost_short,
        group_by='ticker'
    )

    data_long_interval_batch = yf.download(
        tickers=tickers,
        interval=interval_long,
        start=start_date,
        end=end_date,
        progress=True,
        prepost=args.prepost_long,
        group_by='ticker'
    )

    new_york_tz = pytz.timezone('America/New_York')

    if not data_short_interval_batch.empty:
        if data_short_interval_batch.index.tzinfo is None:
            data_short_interval_batch.index = data_short_interval_batch.index.tz_localize('UTC').tz_convert(new_york_tz)
        else:
            data_short_interval_batch.index = data_short_interval_batch.index.tz_convert(new_york_tz)
        print(f"{interval_short} 資料已轉換至 'America/New_York' 時區。")

    if not data_long_interval_batch.empty:
        if data_long_interval_batch.index.tzinfo is None:
            data_long_interval_batch.index = data_long_interval_batch.index.tz_localize('UTC').tz_convert(new_york_tz)
        else:
            data_long_interval_batch.index = data_long_interval_batch.index.tz_convert(new_york_tz)
        print(f"60m 資料已轉換至 'America/New_York' 時區。")

    print("\n======= 資料下載與處理完畢。開始執行分析... =======")

    return data_short_interval_batch, data_long_interval_batch