# stock-dynamic

A Python tool for analyzing fixed-time-lag returns and backtesting trailing-stop strategies for stocks.

## Main Features

*   **Fixed Time Lag Analysis**: Analyzes stock returns over a fixed period (e.g., hours) to calculate expected return and win rates.
*   **Trailing Stop Strategy Backtest**: Simulates a trading strategy using a trailing stop-loss for both entry and exit points.

## Installation

1.  **Python Version**: This project requires Python `3.9.19`.

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

The main entry point for the application is `run.py`. You can run the analysis using various command-line arguments.

### Basic Usage Examples

**Run fixed-time-lag analysis for default tickers over the last 10 days:**
```bash
python run.py --period 10d
```

**Run a strategy backtest for specific tickers:**
```bash
python run.py --strategy-backtest --tickers NVDA AMD --budget 10000
```

**Clean all generated output files:**
```bash
python run.py --clean
```

### Important Command-Line Arguments

*   `--strategy-backtest`: Switch to strategy backtest mode.
*   `--tickers [TICKER ...]`: Specify tickers to analyze, overriding the config.
*   `--period <period>`: Set the data download period (e.g., `5d`, `1mo`).
*   `--start-date <YYYY-MM-DD>` / `--end-date <YYYY-MM-DD>`: Specify an absolute date range for analysis.
*   `--base-hours <hours>`: Set the base holding duration for the fixed-time-lag analysis.
*   `--iterations <count>`: Number of analysis iterations to run (e.g., if base-hours is 2 and iterations is 3, it will run for 2, 4, and 6 hours).
*   `--budget <amount>`: Set a total budget for backtesting, which determines the number of shares based on price.
*   `--shares <count>`: Set a fixed number of shares for backtesting (ignored if `--budget` is set).
*   `--save-data`: Save downloaded and analyzed data to CSV files.
*   `--clean`: Remove all files from the output directories before running.

For a full list of arguments, run:
```bash
python run.py --help
```

## Configuration

Default ticker lists are managed in `src/stock_analysis/config.py`. You can modify this file to change the default stock lists for analysis.

## Output

The script generates files in the following directories:

*   `output_img/`: Stores generated plot images (`.png`).
*   `output_txt/`: Stores summary reports (`.txt`).
*   `output_data/`: Stores raw downloaded data and analysis results in CSV format (only if `--save-data` is used).