import pandas as pd
import re

def analyze_fixed_time_lag(stock_data: pd.DataFrame, ticker: str, interval: str, holding_hours: float):
    """
    分析一檔股票在給定數據下，與 {holding_hours} 小時前的 K 線收盤價的價差。
    Analyzes the price difference of a stock based on provided data,
    between the current bar and the close price {holding_hours} hours prior.
    """
    if stock_data.empty:
        print(f"錯誤：{ticker} 沒有提供數據。")
        print(f"ERROR: No data provided for {ticker}.")
        return None, None

    # 數據已預先處理，直接使用
    print(f"Processing {ticker} data. Total bars: {len(stock_data)}.")
    # print("-" * 30)


    # --- 參數計算 (Parameter Calculation) ---
    try:
        minutes_per_bar = int(re.findall(r'(\d+)', interval)[0])
    except Exception:
        print(f"錯誤：無法從 K 線間隔 '{interval}' 提取分鐘數。請使用 '1m', '5m', '15m' 格式。")
        print(f"ERROR: Could not parse minutes from interval '{interval}'. Please use '1m', '5m', '15m' format.")
        return None, None

    total_minutes_to_lag = holding_hours * 60

    if total_minutes_to_lag % minutes_per_bar != 0:
        print(f"錯誤：持有時間 {holding_hours} 小時 ({total_minutes_to_lag} 分鐘) 不是 K 線間隔 {minutes_per_bar} 分鐘的整數倍。")
        print(f"ERROR: Holding period {holding_hours} hours ({total_minutes_to_lag} mins) is not an integer multiple of the K-bar interval ({minutes_per_bar} mins).")
        return None, None

    lag_periods = int(total_minutes_to_lag / minutes_per_bar)

    # print(f"分析參數 (Analysis Parameters)：")
    # print(f"  - K線間隔 (Interval): {interval} ({minutes_per_bar} 分鐘)")
    # print(f"  - 持有時長 (Holding Period): {holding_hours} 小時 (Hours)")
    # print(f"  - 回溯 K 棒 (Lag Periods): {lag_periods} 根 K 棒 (bars)")
    # print("-" * 30)

    # --- 核心計算 (Core Calculation) ---
    stock_data['P_buy'] = stock_data['Close']
    stock_data['P_sell'] = stock_data['Close'].shift(-lag_periods)

    analysis_df = stock_data.dropna().copy()

    if analysis_df.empty:
        print(f"錯誤：數據量不足，無法進行 {holding_hours} 小時的回測分析。")
        print(f"ERROR: Not enough data for a {holding_hours}-hour lookback analysis.")
        return None, None

    analysis_df['price_diff'] = analysis_df['P_sell'] - analysis_df['P_buy']
    analysis_df['return'] = (analysis_df['P_sell'] - analysis_df['P_buy']) / analysis_df['P_buy']

    # --- 統計分析結果 (Statistical Analysis) ---
    total_trades = len(analysis_df)
    losing_trades = (analysis_df['price_diff'] < 0).sum()

    results = {
        "ticker": ticker,
        "holding_hours": holding_hours,
        "total_trades": total_trades,
        "loss_probability": losing_trades / total_trades if total_trades > 0 else 0,
        "avg_price_diff": analysis_df['price_diff'].mean(),
        "avg_gain_diff": analysis_df[analysis_df['price_diff'] > 0]['price_diff'].mean(),
        "avg_loss_diff": analysis_df[analysis_df['price_diff'] < 0]['price_diff'].mean(),
        "expected_return": analysis_df['return'].mean(),
        "win_rate": (analysis_df['return'] > 0).sum() / total_trades if total_trades > 0 else 0,
    }

    return results, analysis_df

import argparse

def run_strategy_backtest(stock_data: pd.DataFrame, ticker: str, args: argparse.Namespace):
    """
    Simulates a trailing stop trading strategy, allowing for multiple trades.
    """
    if stock_data.empty:
        print(f"No data for {ticker}, skipping backtest.")
        return []

    trades = []
    # --- State Machine Initialization ---
    state = 'LOOKING_TO_BUY'
    lowest_price_seen = float('inf')
    highest_price_since_buy = float('-inf')
    buy_price = 0
    buy_time = None
    current_day = None
    day_of_last_trade = None

    # --- Iterate through K-lines ---
    for index, row in stock_data.iterrows():
        current_low = row['Low']
        current_high = row['High']
        bar_date = index.date()

        if state == 'LOOKING_TO_BUY':
            if bar_date == day_of_last_trade:
                continue

            # --- Daily Reset Logic ---
            if args.daily_trades and bar_date != current_day:
                current_day = bar_date
                lowest_price_seen = current_low # Reset on a new day
            # --- End Daily Reset Logic ---
            elif current_low < lowest_price_seen:
                lowest_price_seen = current_low


            buy_trigger_price = lowest_price_seen * (1 + args.entry_trail_pct / 100)

            if current_high >= buy_trigger_price:
                buy_price = buy_trigger_price
                buy_time = index
                # Reset the highest price seen since the new buy
                highest_price_since_buy = buy_price
                state = 'IN_POSITION'
                print(f"[{ticker}] BUY triggered at ${buy_price:.2f} on {buy_time}")


        elif state == 'IN_POSITION':
            if current_high > highest_price_since_buy:
                highest_price_since_buy = current_high

            sell_trigger_price = highest_price_since_buy * (1 - args.exit_trail_pct / 100)

            if current_low <= sell_trigger_price:
                sell_price = sell_trigger_price
                sell_time = index
                print(f"[{ticker}] SELL triggered at ${sell_price:.2f} on {sell_time}")

                # --- Result Compilation for this trade ---
                if args.budget:
                    shares_to_trade = args.budget // buy_price
                else:
                    shares_to_trade = args.shares

                pnl = (sell_price - buy_price) * shares_to_trade
                profit_pct = (sell_price - buy_price) / buy_price

                result = {
                    'ticker': ticker,
                    'buy_price': buy_price,
                    'buy_time': buy_time,
                    'sell_price': sell_price,
                    'sell_time': sell_time,
                    'shares': shares_to_trade,
                    'profit_and_loss': pnl,
                    'profit_pct': profit_pct,
                    'entry_trail_pct': args.entry_trail_pct,
                    'exit_trail_pct': args.exit_trail_pct,
                    'budget': args.budget
                }
                trades.append(result)

                # --- Reset for next trade ---
                day_of_last_trade = bar_date
                state = 'LOOKING_TO_BUY'
                lowest_price_seen = current_low # Start tracking from current bar's low
                highest_price_since_buy = float('-inf')
                buy_price = 0
                buy_time = None


    if not trades:
        print(f"[{ticker}] No complete trade was executed during the backtest period.")

    return trades