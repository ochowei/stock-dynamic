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