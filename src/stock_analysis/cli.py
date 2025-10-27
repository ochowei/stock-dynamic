import argparse


def setup_arg_parser():
    """
    Sets up and returns the argument parser for command-line options.
    """
    parser = argparse.ArgumentParser(
        description="執行 stock-dynamic 分析，可自訂分析週期。"
    )
    parser.add_argument(
        "-t",
        "--tickers",
        nargs="+",
        default=None,
        help="Specify one or more ticker symbols to analyze, overriding the config file.",
    )
    parser.add_argument(
        "-p",
        "--period",
        type=str,
        default="5d",
        help="指定 yfinance 下載資料的週期 (例如: '5d', '7d', '1mo')",
    )
    parser.add_argument(
        "-b",
        "--base-hours",
        type=float,
        default=2,
        help="設定分析的基底持有小時 (Base holding hours for analysis)",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=6,
        help="設定分析迴圈的次數 (Number of iterations for the analysis loop)",
    )
    parser.add_argument(
        "--plot-on-profit",
        action="store_true",
        help="僅在價值期望值 (Expected Return) > 0 時才儲存圖表。",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="在執行分析前，清除 output_img/ 資料夾中的所有 .png 檔案 (Clear all .png files in output_img/ before execution).",
    )
    parser.add_argument(
        "--prepost-short",
        action="store_true",
        help="下載短週期資料時包含盤前盤後數據 (Include pre/post market data for short interval download).",
    )
    parser.add_argument(
        "--no-prepost-long",
        dest="prepost_long",
        action="store_false",
        help="下載長週期資料時不包含盤前盤後數據 (Exclude pre/post market data for long interval download).",
    )
    parser.add_argument(
        "--interval-short",
        type=str,
        default="5m",
        help='設定分析用的短週期 K 線間隔 (e.g., "1m", "5m", "15m")',
    )
    parser.add_argument(
        "--save-data",
        action="store_true",
        help="儲存下載的原始 K 線資料與分析後的 DataFrame 為 CSV 檔案。",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default=None,
        help="指定分析的開始日期 (格式: YYYY-MM-DD)。若提供此參數，將忽略 --period。",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=None,
        help="指定分析的結束日期 (格式: YYYY-MM-DD)。若提供此參數，將忽略 --period。",
    )
    parser.add_argument(
        "--time-anchor",
        type=str,
        default="start",
        choices=["start", "end"],
        help="Set the time anchor for analysis: 'start' (X-axis is buy time) or 'end' (X-axis is sell time).",
    )

    # --- Strategy Backtest Arguments ---
    parser.add_argument(
        "--strategy-backtest",
        action="store_true",
        help="啟用追蹤停損策略回測模式 (Enable the trailing stop strategy backtest mode).",
    )
    parser.add_argument(
        "--entry-trail-pct",
        type=float,
        default=5.0,
        help="追蹤停損買單的百分比 (Trailing percentage for the entry order).",
    )
    parser.add_argument(
        "--exit-trail-pct",
        type=float,
        default=3.0,
        help="追蹤停損賣單的百分比 (Trailing percentage for the exit order).",
    )
    parser.add_argument(
        "--shares", type=int, default=100, help="交易股數 (Number of shares to trade)."
    )
    parser.add_argument(
        "--budget",
        type=float,
        default=None,
        help="指定回測的總預算 (美元)。若提供此參數，將忽略 --shares。 (Total budget in USD. If provided, --shares is ignored.)",
    )
    parser.add_argument(
        "--daily-trades",
        action="store_true",
        help="在策略回測中，允許每天重新建立進場條件單 (Allow re-initiating entry conditions daily in strategy backtest mode).",
    )

    return parser
