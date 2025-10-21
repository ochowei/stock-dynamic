import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import argparse
import math
import pytz # 引入 pytz 函式庫
import os
import glob

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
    print("-" * 30)


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

def print_results(results: dict):
    """格式化並印出中英分析結果"""
    if not results: return

    holding_hours = results['holding_hours']

    # print(f"======= {results['ticker']} 股票 {holding_hours} 小時持有期分析結果 ({holding_hours}-Hour Holding Period Analysis) =======")
    # print(f"總有效交易次數 (Total Trades): {results['total_trades']:,}")
    # print("-" * 40)

    # print(f"下跌機率 (Probability of Loss): {results['loss_probability']:.2%}")
    # print(f"    (定義: {holding_hours} 小時後價格低於 {holding_hours} 小時前價格的機率)")
    # print(f"    (Definition: Probability that P_sell < P_buy)")

    # print("-" * 40)
    # print(f"價差期望值 (Expected Price Difference): ${results['avg_price_diff']:.4f}")
    # print(f"    - 平均獲利價差 (Avg. Gain Amount): ${results.get('avg_gain_diff', 0):.4f}")
    # print(f"    - 平均虧損價差 (Avg. Loss Amount): ${results.get('avg_loss_diff', 0):.4f}")

    print("-" * 40)
    print(f"價值期望值 (Expected Return %): {results['expected_return']:.4%}")
    # print(f"    (報酬率 > 0 的機率 (Win Rate %): {results['win_rate']:.2%})")

    print("=" * 70)
    # print("註 (Note): 此分析未考慮交易手續費或滑價成本 (This analysis excludes commissions and slippage.)")

# --- 這裡開始是修改過的函式 (This function is modified) ---

def plot_results(results: dict, analysis_df: pd.DataFrame, output_folder: str = 'output_img'):
    """
    將分析結果視覺化 (全英文圖表)
    修改：繪製每筆交易的 "報酬率 (%)" 隨時間變化的圖表
    """
    if not results or analysis_df.empty: return

    holding_hours = results['holding_hours']

    sns.set_style("whitegrid")
    plt.figure(figsize=(15, 7))

    # 建立「交易序號」的 X 軸 (Create a numerical index for the x-axis)
    x_values = range(len(analysis_df))

    # --- 核心修改 (Core Modification) ---
    # 1. 繪製 'return' 欄位，並 * 100 轉換為百分比
    #    (Plot the 'return' column and multiply by 100 to convert to percentage)
    plt.plot(x_values, analysis_df['return'].values * 100,
             label='Return (Percentage)', color='dodgerblue', linewidth=0.8)

    # 2. 損益兩平線仍然是 0 (Breakeven line is still 0)
    plt.axhline(y=0, color='red', linestyle='--', label='Breakeven (Return = 0%)')

    # 3. 繪製 "平均報酬率" (Plot the "Average Return")
    avg_return = results['expected_return']
    plt.axhline(y=avg_return * 100, color='orange', linestyle=':',
                label=f'Average Return ({avg_return:.4%})')
    # --- 修改結束 (End of Modification) ---


    # 建立自訂的 X 軸標籤 (Create custom x-axis ticks)
    num_ticks = 10
    tick_indices = np.linspace(0, len(analysis_df) - 1, num_ticks, dtype=int)
    tick_labels = analysis_df.index[tick_indices].strftime('%m-%d %H:%M')

    plt.xticks(ticks=tick_indices, labels=tick_labels, rotation=30, ha='right')

    # 更新標題和 Y 軸標籤 (Update Title and Y-axis Label)
    plt.title(f"{results['ticker']} - {holding_hours}-Hour Holding Return (Per Trade)", fontsize=16)
    plt.xlabel("Date (Skipping Non-Trading Periods)", fontsize=12)
    plt.ylabel("Return (%)", fontsize=12) # Y 軸標籤改為 Return (%)
    plt.legend()

    plt.tight_layout()

    plot_filename = f"{output_folder}/{results['ticker']}_{holding_hours}hr.png"
    plt.savefig(plot_filename)
    print(f"Plot saved as {plot_filename}")
    plt.close()
    # plt.show()

def plot_comparison_chart(data_map: dict, holding_hours: float, tickers_to_plot: list, output_folder: str):
    """
    繪製多支股票在同一個持有週期下的報酬率比較圖。
    Plots a comparison chart of returns for multiple stocks over the same holding period.
    """
    from matplotlib.dates import DateFormatter

    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(15, 8))

    # 1. 建立待合併的 DataFrame 列表
    dfs_to_merge = []
    for ticker in tickers_to_plot:
        df = data_map.get(ticker)
        if df is not None and not df.empty:
            # 選取 'return' 欄位並重新命名
            renamed_df = df[['return']].rename(columns={'return': ticker})
            dfs_to_merge.append(renamed_df)

    # 2. 合併 DataFrame
    if not dfs_to_merge:
        return # 如果沒有可繪製的資料，則返回

    comparison_df = dfs_to_merge[0].join(dfs_to_merge[1:], how='outer')
    comparison_df.sort_index(inplace=True)

    # 3. 修改繪圖邏輯
    x_values = range(len(comparison_df))

    # 獲取 matplotlib 預設的顏色循環
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    # 遍歷 comparison_df 的欄位 (即股票代碼)
    for i, ticker in enumerate(comparison_df.columns):

        # 獲取當前 ticker 的顏色
        ticker_color = colors[i % len(colors)]

        # 繪製主要的報酬率線
        plt.plot(x_values,
                 comparison_df[ticker].values * 100,
                 label=ticker,
                 linewidth=1,
                 color=ticker_color) # 指定顏色

        # --- 新增開始 ---

        # 1. 計算平均值
        avg_return = comparison_df[ticker].mean()

        # 2. 繪製平均線
        if pd.notna(avg_return): # 確保平均值有效
            plt.axhline(y=avg_return * 100,
                        color=ticker_color, # 使用相同顏色
                        linestyle='--',     # 使用虛線
                        linewidth=0.8,
                        label=f'{ticker} Avg ({avg_return:.4%})') # 3. 新增 Label
        # --- 新增結束 ---


    plt.axhline(y=0, color='red', linestyle='--', label='Breakeven (Return = 0%)')

    # 設定圖表標題和標籤
    plt.title(f"Return Comparison for {', '.join(tickers_to_plot)}\nHolding Period: {holding_hours} Hours", fontsize=16)
    plt.ylabel("Return (%)", fontsize=12)
    plt.xlabel("Date (Skipping Non-Trading Periods)", fontsize=12)

    # 4. 新增自訂 X 軸刻度
    # 建立自訂的 X 軸標籤 (Create custom x-axis ticks)
    num_ticks = 10
    tick_indices = np.linspace(0, len(comparison_df) - 1, num_ticks, dtype=int)

    # 確保 tick_indices 不會超出範圍
    tick_indices = tick_indices[tick_indices < len(comparison_df)]

    tick_labels = comparison_df.index[tick_indices].strftime('%m-%d %H:%M')

    plt.xticks(ticks=tick_indices, labels=tick_labels, rotation=30, ha='right')

    plt.legend()
    plt.tight_layout()

    # 儲存圖表
    safe_tickers_str = '_'.join(tickers_to_plot)
    plot_filename = f"{output_folder}/COMP_{safe_tickers_str}_{holding_hours}hr.png"
    plt.savefig(plot_filename)
    print(f"Comparison chart saved as {plot_filename}")
    plt.close()

def latest_one_third(df: pd.DataFrame, divid: int) -> pd.DataFrame:
    if df is None or df.empty:
        return df
    n = len(df)
    take = max(1, math.ceil(n / divid))
    return df.tail(take).copy()

def setup_arg_parser():
    """
    Sets up and returns the argument parser for command-line options.
    """
    parser = argparse.ArgumentParser(
        description="執行 stock-dynamic 分析，可自訂分析週期。"
    )
    parser.add_argument(
        "-p", "--period",
        type=str,
        default="5d",
        help="指定 yfinance 下載資料的週期 (例如: '5d', '7d', '1mo')"
    )
    parser.add_argument(
        "-b", "--base-hours",
        type=float,
        default=2,
        help="設定分析的基底持有小時 (Base holding hours for analysis)"
    )
    parser.add_argument(
        "-i", "--iterations",
        type=int,
        default=6,
        help="設定分析迴圈的次數 (Number of iterations for the analysis loop)"
    )
    parser.add_argument(
        "--plot-on-profit",
        action="store_true",
        help="僅在價值期望值 (Expected Return) > 0 時才儲存圖表。"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="在執行分析前，清除 output_img/ 資料夾中的所有 .png 檔案 (Clear all .png files in output_img/ before execution)."
    )
    return parser

def download_stock_data(tickers: list, interval_short: str, interval_long: str, start_date, end_date, period: str):
    """
    Downloads stock data for the given tickers and intervals, and handles timezone conversion.
    """
    print("=======================================================")
    print(f"======= 開始批次下載資料 (Starting Batch Download) =======")
    print(f"Tickers: {tickers}")
    print(f"Intervals: {interval_short}, {interval_long}")
    print(f"Period: {period}")
    print("=======================================================\n")

    data_short_interval_batch = yf.download(
        tickers=tickers,
        interval=interval_short,
        start=start_date,
        end=end_date,
        progress=True,
        prepost=False,
        group_by='ticker'
    )

    data_long_interval_batch = yf.download(
        tickers=tickers,
        interval=interval_long,
        start=start_date,
        end=end_date,
        progress=True,
        prepost=True,
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

def run_analysis_loops(ticker_list_array: list, data_short_batch, data_long_batch, args: argparse.Namespace):
    """
    Runs the main analysis loops through all ticker lists and holding periods.
    """
    all_analysis_data_master = {}
    all_summary_results_master = {}

    for ticker_list in ticker_list_array:
        if not ticker_list:
            continue

        for ticker_symbol in ticker_list:
            print(f"\n=======================================================")
            print(f"======= 正在分析 (Now Analyzing): {ticker_symbol} =======")
            print(f"=======================================================\n")

            try:
                stock_data_short_interval = data_short_batch[ticker_symbol].dropna()
            except (KeyError, AttributeError):
                stock_data_short_interval = pd.DataFrame()

            if stock_data_short_interval.empty:
                print(f"*** {ticker_symbol} 沒有可分析的 {INTERVAL_SHORT} 資料。跳過... ***")
                # We don't continue here, to allow for long interval analysis if that data exists

            for x in range(args.iterations):
                holding_hours = args.base_hours * (x + 1)
                print(f"--- 分析 ({INTERVAL_SHORT} K線, {holding_hours} 小時) ---")

                stock_data_to_analyze = latest_one_third(stock_data_short_interval, args.iterations / (x + 1))

                analysis_results, detailed_df = analyze_fixed_time_lag(
                    stock_data=stock_data_to_analyze,
                    ticker=ticker_symbol,
                    interval=INTERVAL_SHORT,
                    holding_hours=holding_hours
                )

                if analysis_results and detailed_df is not None and not detailed_df.empty:
                    # Initialize dicts if they don't exist
                    if holding_hours not in all_analysis_data_master:
                        all_analysis_data_master[holding_hours] = {}
                    if holding_hours not in all_summary_results_master:
                        all_summary_results_master[holding_hours] = []

                    all_analysis_data_master[holding_hours][ticker_symbol] = detailed_df
                    all_summary_results_master[holding_hours].append(analysis_results)

                    if not args.plot_on_profit or (args.plot_on_profit and analysis_results['expected_return'] > 0):
                        print_results(analysis_results)
                        plot_results(analysis_results, detailed_df)

            print(f"\n======= {ticker_symbol} 分析結束 (Analysis Complete) =======")

    return all_analysis_data_master, all_summary_results_master

def generate_summary_reports(all_summary_results_grouped: dict):
    """
    Generates and prints the summary report of returns ranked by holding period.
    """
    print("\n======= 總結：各持有週期報酬率排行 (Summary: Return Ranking by Holding Period) =======")

    for holding_hours in sorted(all_summary_results_grouped.keys()):
        results_list = all_summary_results_grouped[holding_hours]

        if not results_list:
            continue

        print(f"\n--- 持有 {holding_hours} 小時 (Holding {holding_hours} Hours) ---")

        sorted_list = sorted(results_list, key=lambda r: r.get('expected_return', -float('inf')), reverse=True)

        if not sorted_list:
            print("  (無有效資料 No valid data)")
            continue

        for result in sorted_list:
            print(f"  - {result['ticker']}: {result['expected_return']:.4%}")

def generate_comparison_plots(all_analysis_data: dict, ticker_list_array: list, output_folder: str):
    """
    Generates comparison plot charts for each holding period.
    """
    print("\n======= 正在產生比較圖表 (Generating Comparison Charts) =======")

    # Flatten the ticker list array for easier processing
    all_tickers_in_run = [ticker for sublist in ticker_list_array for ticker in sublist]

    for holding_hours, ticker_data_map in all_analysis_data.items():
        if ticker_data_map:
            # Plot the first 5 tickers from the overall list that are present in the current data map
            tickers_to_plot = [t for t in all_tickers_in_run if t in ticker_data_map][:5]
            if tickers_to_plot:
                plot_comparison_chart(
                    data_map=ticker_data_map,
                    holding_hours=holding_hours,
                    tickers_to_plot=tickers_to_plot,
                    output_folder=output_folder
                )

def main():
    """
    Main function to run the stock analysis script.
    """
    plt.ioff()
    parser = setup_arg_parser()
    args = parser.parse_args()

    if args.clean:
        print("Cleaning output_img/ directory...")
        files = glob.glob('output_img/*.png')
        count = 0
        for f in files:
            try:
                os.remove(f)
                count += 1
            except OSError as e:
                print(f"Error removing file {f}: {e}")
        print(f"Removed {count} .png file(s) from output_img/.")

    # Dynamic Date Calculation
    max_lookback_hours = args.base_hours * args.iterations
    max_lookback_timedelta = pd.Timedelta(hours=max_lookback_hours)
    analysis_period_timedelta = pd.Timedelta(args.period)
    total_download_timedelta = max_lookback_timedelta + analysis_period_timedelta
    end_date = pd.Timestamp.now()
    start_date = end_date - total_download_timedelta

    # Use the global TICKER_SYMBOLS for the download
    data_short, data_long = download_stock_data(
        TICKER_SYMBOLS, INTERVAL_SHORT, INTERVAL_LONG, start_date, end_date, args.period
    )

    all_data, all_results = run_analysis_loops(
        TICKER_LIST_ARRAY, data_short, data_long, args
    )

    generate_summary_reports(all_results)

    generate_comparison_plots(all_data, TICKER_LIST_ARRAY, 'output_img')

    print("\n======= 程式執行完畢 (Process Finished) =======")

# --- 您可以在這裡修改共用參數 (You can modify parameters here) ---
# 持有小時 (Holding Hours) - 兩項分析共用
# 股票代碼 (Ticker Symbol) - 兩項分析共用
TICKER_SYMBOLS_US_RARE_EARTH = ['MP','UUUU','UAMY']
TICKER_SYMBOLS_US_DRONE = ['ONDS','RCAT'] #AVAV
TICKER_SYMBOLS_US_NUCLEAR = ['LEU','SMR']
TICKER_SYMBOLS_US_POWER = ['BE','VST']
TICKER_SYMBOLS_US_BETTERY = ['EOSE','WWR']
TICKER_SYMBOLS_US_AI_UP = ['ALAB','AMD','NVDA','NVTS','POWI','TSM']
TICKER_SYMBOLS_US_AI_MEDIUM = ['GOOG']
TICKER_SYMBOLS_US_AI_DOWN = ['ADBE','DUOL','FIG','GRAB','RBRK']
TICKER_SYMBOLS_US_OTHER_STABLE = ['CIFR','SOFI','IBIT']
TICKER_SYMBOLS_US_OTHER_GROWTH = ['IONQ','TMDX',]
TICKER_SYMBOLS_US_OTHER_ETF = ['BND','GLD','MGK','VOO']

TICKER_SYMBOLS_US_OTHER = []

TICKER_LIST_ARRAY = [
    TICKER_SYMBOLS_US_RARE_EARTH,
    TICKER_SYMBOLS_US_DRONE,
    TICKER_SYMBOLS_US_OTHER,
    TICKER_SYMBOLS_US_NUCLEAR,
    TICKER_SYMBOLS_US_POWER,
    TICKER_SYMBOLS_US_BETTERY,
    TICKER_SYMBOLS_US_AI_UP,
    TICKER_SYMBOLS_US_AI_MEDIUM,
    TICKER_SYMBOLS_US_AI_DOWN,
    TICKER_SYMBOLS_US_OTHER_STABLE,
    TICKER_SYMBOLS_US_OTHER_GROWTH,
    TICKER_SYMBOLS_US_OTHER_ETF
]

TICKER_SYMBOLS_US = TICKER_SYMBOLS_US_RARE_EARTH + TICKER_SYMBOLS_US_DRONE + TICKER_SYMBOLS_US_OTHER + TICKER_SYMBOLS_US_NUCLEAR + TICKER_SYMBOLS_US_POWER + TICKER_SYMBOLS_US_BETTERY + TICKER_SYMBOLS_US_AI_UP + TICKER_SYMBOLS_US_AI_MEDIUM + TICKER_SYMBOLS_US_AI_DOWN + TICKER_SYMBOLS_US_OTHER_STABLE + TICKER_SYMBOLS_US_OTHER_GROWTH + TICKER_SYMBOLS_US_OTHER_ETF
TICKER_SYMBOLS_TW = ['00635U.TW','2603.TW']
TICKER_SYMBOLS = TICKER_SYMBOLS_US


# --- 參數定義 (Parameter Definitions) ---
# (保留儲存格 5, 6, 7/8 中的所有參數定義)

# 分析 1 參數
INTERVAL_SHORT = '5m'

# 分析 2 & 3 參數
INTERVAL_LONG = '60m'
# (註：原儲存格 7 和 7/8 都使用 '60m' 和 '5d'，我們在批次下載時使用)


# --- 執行主程式 (Run Main Program) ---
if __name__ == "__main__":
    main()
