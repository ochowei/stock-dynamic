import argparse

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
    parser.add_argument(
        '--prepost-short',
        action='store_true',
        help='下載短週期資料時包含盤前盤後數據 (Include pre/post market data for short interval download).'
    )
    parser.add_argument(
        '--no-prepost-long',
        dest='prepost_long',
        action='store_false',
        help='下載長週期資料時不包含盤前盤後數據 (Exclude pre/post market data for long interval download).'
    )
    parser.add_argument(
        '--interval-short',
        type=str,
        default='5m',
        help='設定分析用的短週期 K 線間隔 (e.g., "1m", "5m", "15m")'
    )
    parser.add_argument(
        '--save-data',
        action='store_true',
        help='儲存下載的原始 K 線資料與分析後的 DataFrame 為 CSV 檔案。'
    )
    return parser