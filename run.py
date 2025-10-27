import pandas as pd
import matplotlib.pyplot as plt
import argparse
import math
import os
import glob

# Import modularized functions
from src.stock_analysis.core import analyze_fixed_time_lag, run_strategy_backtest
from src.stock_analysis.plotting import plot_results, plot_comparison_chart
from src.stock_analysis.data import download_stock_data
from src.stock_analysis.cli import setup_arg_parser


def print_results(results: dict):
    """格式化並印出中英分析結果"""
    if not results:
        return

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

    # print("-" * 40)
    # print(f"價值期望值 (Expected Return %): {results['expected_return']:.4%}")
    # print(f"    (報酬率 > 0 的機率 (Win Rate %): {results['win_rate']:.2%})")

    # print("=" * 70)
    # print("註 (Note): 此分析未考慮交易手續費或滑價成本 (This analysis excludes commissions and slippage.)")


def latest_one_third(df: pd.DataFrame, divid: int) -> pd.DataFrame:
    if df is None or df.empty:
        return df
    n = len(df)
    take = max(1, math.ceil(n / divid))
    return df.tail(take).copy()


# No content


def run_analysis_loops(
    ticker_list_array: list,
    data_short_batch,
    data_long_batch,
    args: argparse.Namespace,
    summary_filename: str,
    interval_short: str,
    filename_suffix: str,
):
    """
    Runs the main analysis loops through all ticker lists and holding periods.
    """

    for ticker_list in ticker_list_array:
        if not ticker_list:
            continue

        all_analysis_data_master = {}
        all_summary_results_master = {}

        for ticker_symbol in ticker_list:
            print("\n=======================================================")
            print(f"======= 正在分析 (Now Analyzing): {ticker_symbol} =======")
            print("=======================================================\n")

            try:
                stock_data_short_interval = data_short_batch[ticker_symbol].dropna()
            except (KeyError, AttributeError):
                stock_data_short_interval = pd.DataFrame()

            if args.save_data and not stock_data_short_interval.empty:
                raw_filename = f"output_data/{ticker_symbol}_{interval_short}_raw.csv"
                stock_data_short_interval.to_csv(raw_filename)
                print(f"原始資料已儲存至 (Raw data saved to): {raw_filename}")

            if stock_data_short_interval.empty:
                print(
                    f"*** {ticker_symbol} 沒有可分析的 {interval_short} 資料。跳過... ***"
                )
                # We don't continue here, to allow for long interval analysis if that data exists

            for x in range(args.iterations):
                holding_hours = args.base_hours * (x + 1)
                print(f"--- 分析 ({interval_short} K線, {holding_hours} 小時) ---")

                stock_data_to_analyze = latest_one_third(
                    stock_data_short_interval, args.iterations / (x + 1)
                )

                analysis_results, detailed_df = analyze_fixed_time_lag(
                    stock_data=stock_data_to_analyze,
                    ticker=ticker_symbol,
                    interval=interval_short,
                    holding_hours=holding_hours,
                    time_anchor=args.time_anchor,
                )

                if (
                    analysis_results
                    and detailed_df is not None
                    and not detailed_df.empty
                ):
                    # --- NEW CODE START ---
                    # 取得當前的迭代次數 (iteration number)
                    iteration_num = x + 1

                    # 1. 正規化「平均期望報酬率」 (analysis_results['expected_return'])
                    # 這個值會用於 summary report 和 plot 上的平均線
                    if "expected_return" in analysis_results:
                        analysis_results["expected_return"] = (
                            analysis_results["expected_return"] / iteration_num
                        )

                    # 2. 正規化「每筆交易的報酬率」 (detailed_df['return'])
                    # 這個 DataFrame column 會用於繪製主圖表 (plot_results) 和
                    # 跨股票比較圖 (plot_comparison_chart)
                    if "return" in detailed_df.columns:
                        detailed_df["return"] = detailed_df["return"] / iteration_num
                    # --- NEW CODE END ---

                    if args.save_data:
                        analysis_filename = f"output_data/{ticker_symbol}_{holding_hours}hr_analysis.csv"
                        detailed_df.to_csv(analysis_filename)
                        print(
                            f"分析資料已儲存至 (Analysis data saved to): {analysis_filename}"
                        )

                    # Initialize dicts if they don't exist
                    if holding_hours not in all_analysis_data_master:
                        all_analysis_data_master[holding_hours] = {}
                    if holding_hours not in all_summary_results_master:
                        all_summary_results_master[holding_hours] = []

                    all_analysis_data_master[holding_hours][ticker_symbol] = detailed_df
                    all_summary_results_master[holding_hours].append(analysis_results)

                    if not args.plot_on_profit or (
                        args.plot_on_profit and analysis_results["expected_return"] > 0
                    ):
                        print_results(analysis_results)
                        plot_results(analysis_results, detailed_df, filename_suffix=filename_suffix)

            print(f"\n======= {ticker_symbol} 分析結束 (Analysis Complete) =======")

        generate_summary_reports(all_summary_results_master, summary_filename)

        generate_comparison_plots(all_analysis_data_master, ticker_list, "output_img", filename_suffix)

    return all_analysis_data_master, all_summary_results_master


def generate_summary_reports(all_summary_results_grouped: dict, summary_filename: str):
    """
    Generates and prints the summary report, and appends it to a file.
    """
    report_header = "\n======= 總結：各持有週期報酬率排行 (Summary: Return Ranking by Holding Period) ======="
    print(report_header)
    with open(summary_filename, "a", encoding="utf-8") as f:
        f.write(report_header + "\n")

        for holding_hours in sorted(all_summary_results_grouped.keys()):
            results_list = all_summary_results_grouped[holding_hours]

            if not results_list:
                continue

            period_header = (
                f"\n--- 持有 {holding_hours} 小時 (Holding {holding_hours} Hours) ---"
            )
            print(period_header)
            f.write(period_header + "\n")

            sorted_list = sorted(
                results_list,
                key=lambda r: r.get("expected_return", -float("inf")),
                reverse=True,
            )

            if not sorted_list:
                no_data_msg = "  (無有效資料 No valid data)"
                print(no_data_msg)
                f.write(no_data_msg + "\n")
                continue

            for result in sorted_list:
                result_line = f"  - {result['ticker']}: {result['expected_return']:.4%}"
                print(result_line)
                f.write(result_line + "\n")


def generate_comparison_plots(
    all_analysis_data: dict, ticker_list: list, output_folder: str, filename_suffix: str
):
    """
    Generates comparison plot charts for each holding period.
    """
    print("\n======= 正在產生比較圖表 (Generating Comparison Charts) =======")

    # Flatten the ticker list array for easier processing
    all_tickers_in_run = ticker_list

    for holding_hours, ticker_data_map in all_analysis_data.items():
        if ticker_data_map:
            # Plot the first 5 tickers from the overall list that are present in the current data map
            tickers_to_plot = [t for t in all_tickers_in_run if t in ticker_data_map][
                :5
            ]
            if tickers_to_plot:
                plot_comparison_chart(
                    data_map=ticker_data_map,
                    holding_hours=holding_hours,
                    tickers_to_plot=tickers_to_plot,
                    output_folder=output_folder,
                    filename_suffix=filename_suffix,
                )


def run_backtest_mode(
    ticker_list_array: list, data_short: dict, args: argparse.Namespace
):
    """
    Runs the backtesting mode for the given tickers.
    """
    print("\n======= 策略回測模式 (Strategy Backtest Mode) =======")
    for ticker_list in ticker_list_array:
        if not ticker_list:
            continue
        for ticker in ticker_list:
            stock_data = data_short.get(ticker)
            if stock_data is None or stock_data.empty:
                print(
                    f"\n--- {ticker}: 無法取得資料，跳過回測 (No data, skipping backtest) ---"
                )
                continue

            results = run_strategy_backtest(stock_data, ticker, args)

            if results:
                print(
                    f"\n======= 回測報告: {ticker} (共 {len(results)} 筆交易) ======="
                )
                for i, result in enumerate(results):
                    print(f"\n--- 交易 #{i + 1} ---")
                    print(
                        f"策略: {result['entry_trail_pct']}% 進場追蹤, {result['exit_trail_pct']}% 出場追蹤"
                    )

                    if result["budget"]:
                        print(f"預算 (Budget): ${result['budget']:.2f}")
                        print(f"部位 (Shares): {result['shares']} 股 (基於預算計算)")
                    else:
                        print(f"部位 (Shares): {result['shares']} 股 (固定)")

                    print(
                        f"買入觸發: ${result['buy_price']:.2f} (於 {result['buy_time'].strftime('%Y-%m-%d %H:%M')})"
                    )
                    print(
                        f"賣出觸發: ${result['sell_price']:.2f} (於 {result['sell_time'].strftime('%Y-%m-%d %H:%M')})"
                    )
                    print("----------------------------------------")
                    print(
                        f"每股獲利: ${result['sell_price'] - result['buy_price']:.2f}"
                    )
                    print(f"每股獲利率 (Profit %): {result['profit_pct']:.2%}")
                    print(f"總損益: ${result['profit_and_loss']:.2f}")
                print("======================================\n")


def main():
    """
    Main function to run the stock analysis script.
    """
    plt.ioff()
    parser = setup_arg_parser()
    args = parser.parse_args()

    # 自動建立輸出資料夾 (Automatically create output folders)
    os.makedirs("output_img", exist_ok=True)
    os.makedirs("output_txt", exist_ok=True)
    os.makedirs("output_data", exist_ok=True)

    if args.clean:
        print("Cleaning output directories...")
        # Clean images
        img_files = glob.glob("output_img/*.png")
        img_count = 0
        for f in img_files:
            try:
                os.remove(f)
                img_count += 1
            except OSError as e:
                print(f"Error removing file {f}: {e}")
        print(f"Removed {img_count} .png file(s) from output_img/.")

        # Clean text reports
        txt_files = glob.glob("output_txt/*.txt")
        txt_count = 0
        for f in txt_files:
            try:
                os.remove(f)
                txt_count += 1
            except OSError as e:
                print(f"Error removing file {f}: {e}")
        print(f"Removed {txt_count} .txt file(s) from output_txt/.")

        # Clean data files
        csv_files = glob.glob("output_data/*.csv")
        csv_count = 0
        for f in csv_files:
            try:
                os.remove(f)
                csv_count += 1
            except OSError as e:
                print(f"Error removing file {f}: {e}")
        print(f"Removed {csv_count} .csv file(s) from output_data/.")

    # Dynamic Date Calculation
    max_lookback_hours = args.base_hours * args.iterations
    max_lookback_timedelta = pd.Timedelta(hours=max_lookback_hours)

    if args.start_date and args.end_date:
        # --- 模式 1：絕對日期 (Absolute Date Mode) ---
        print("模式：使用絕對日期區間 (Mode: Using absolute date range)")
        analysis_start_date = pd.Timestamp(args.start_date)
        analysis_end_date = pd.Timestamp(args.end_date)

        # 下載的開始日期需要包含回測所需的時間
        start_date = analysis_start_date - max_lookback_timedelta
        end_date = analysis_end_date

        # 用於日誌記錄的週期字串
        period_log_str = f"{args.start_date} to {args.end_date}"

    else:
        # --- 模式 2：相對日期 (Relative Date Mode - Current Logic) ---
        print(f"模式：使用相對期間 (Mode: Using relative period '{args.period}')")
        analysis_period_timedelta = pd.Timedelta(args.period)
        total_download_timedelta = max_lookback_timedelta + analysis_period_timedelta
        end_date = pd.Timestamp.now()
        start_date = end_date - total_download_timedelta

        # 用於日誌記錄的週期字串
        period_log_str = args.period

    # --- 建立檔名後綴 (Create Filename Suffix) ---
    if args.start_date and args.end_date:
        period_str = f"{args.start_date}_to_{args.end_date}"
    else:
        period_str = f"period-{args.period}"

    filename_suffix = f"_{args.interval_short}_anchor-{args.time_anchor}_{period_str}"
    # --- 檔名後綴建立完畢 ---

    # 定義報告檔案路徑 (Define report file path) with base hours
    summary_filename = f"output_txt/summary_base-{args.base_hours}_iter-{args.iterations}{filename_suffix}.txt"

    # 在迴圈開始前，清空檔案並寫入標頭 (Before the loop, clear the file and write the header)
    try:
        with open(summary_filename, "w", encoding="utf-8") as f:
            f.write("Stock Dynamic Analysis Report\n")
            f.write("=============================\n")
        print(f"Summary report will be saved to {summary_filename}")
    except IOError as e:
        print(f"Error: Unable to write to file {summary_filename}. {e}")
        # 選擇性地決定是否要因此錯誤而中止程式
        # Optionally, decide if you want to exit the script on this error
        return

    # Import configurations
    from src.stock_analysis.config import INTERVAL_LONG

    # --- Ticker Configuration ---
    # Check if the --tickers argument is provided. If so, override the config.
    if args.tickers:
        print(
            f"模式：使用命令行提供的 Tickers (Mode: Using tickers from command line): {args.tickers}"
        )
        TICKER_SYMBOLS = args.tickers
        TICKER_LIST_ARRAY = [
            args.tickers
        ]  # Analyze all provided tickers as a single group
    else:
        print("模式：使用設定檔中的 Tickers (Mode: Using tickers from config file)")
        from src.stock_analysis.config import TICKER_SYMBOLS, TICKER_LIST_ARRAY

    # Use the global TICKER_SYMBOLS for the download
    data_short, data_long = download_stock_data(
        TICKER_SYMBOLS,
        args.interval_short,
        INTERVAL_LONG,
        start_date,
        end_date,
        period_log_str,
        args,
    )

    # --- Download Only Mode ---
    if args.download_only:
        if args.save_data:
            print("--- 儲存已下載的資料 (Saving downloaded data) ---")
            for ticker in TICKER_SYMBOLS:
                # Save short interval data
                df_short = data_short.get(ticker)
                if df_short is not None and not df_short.empty:
                    filename_short = f"output_data/{ticker}_{args.interval_short}_raw.csv"
                    df_short.to_csv(filename_short)
                    print(f"  - Saved short-interval data for {ticker} to {filename_short}")

                # Save long interval data
                df_long = data_long.get(ticker)
                if df_long is not None and not df_long.empty:
                    filename_long = f"output_data/{ticker}_{INTERVAL_LONG}_raw.csv"
                    df_long.to_csv(filename_long)
                    print(f"  - Saved long-interval data for {ticker} to {filename_long}")

        print("\n資料下載完成，已根據 --download-only 指令跳過分析。")
        print("Data download complete. Skipping analysis as per --download-only flag.")

    elif args.strategy_backtest:
        run_backtest_mode(TICKER_LIST_ARRAY, data_short, args)
    else:
        all_data, all_results = run_analysis_loops(
            TICKER_LIST_ARRAY,
            data_short,
            data_long,
            args,
            summary_filename,
            args.interval_short,
            filename_suffix,
        )

    print("\n======= 程式執行完畢 (Process Finished) =======")


# --- 執行主程式 (Run Main Program) ---
if __name__ == "__main__":
    main()
