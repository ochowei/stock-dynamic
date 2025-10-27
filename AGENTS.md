# AI Agent Development Guidelines

This document provides essential context, architectural overview, and development guidelines for AI agents assisting with this project.

## 1. Project Architecture Overview

The project is structured into several key modules to ensure separation of concerns:

*   **`run.py`**: The main script entry point. It is responsible for parsing command-line arguments and orchestrating the analysis flow by calling functions from other modules.
*   **`src/stock_analysis/cli.py`**: Defines all command-line arguments using Python's `argparse` library. This is the single source of truth for the application's command-line interface.
*   **`src/stock_analysis/core.py`**: Contains the core business logic for all analysis. This includes the fixed-time-lag calculation (`analyze_fixed_time_lag`) and the strategy backtesting simulation (`run_strategy_backtest`).
*   **`src/stock_analysis/data.py`**: Handles all data downloading and fetching from external sources, primarily the `yfinance` library.
*   **`src/stock_analysis/plotting.py`**: Manages all chart generation and data visualization using `matplotlib` and `seaborn`.
*   **`src/stock_analysis/config.py`**: Stores static configuration, most importantly the default lists of ticker symbols for analysis.

## 2. Development Guidelines for AI Agents

To ensure consistency and maintainability, please adhere to the following guidelines:

*   **Adding New Command-Line Parameters**: When a new command-line parameter is needed, you must first modify `src/stock_analysis/cli.py` to add the argument definition. Then, update `run.py` to pass the parsed `args` value to the relevant function in `core.py` or other modules.
*   **Core Logic**: All core calculation logic, especially `pandas` DataFrame manipulations for financial analysis, should be placed in `src/stock_analysis/core.py`.
*   **Plotting Logic**: All changes related to data visualization (e.g., colors, labels, chart types, saving figures) should be implemented in `src/stock_analysis/plotting.py`.
*   **Code and Commenting Consistency**: Maintain consistency with the existing codebase. Where appropriate, provide both English and Traditional Chinese comments to ensure clarity for all contributors.

## 3. High-Level Goals

The primary goals for the ongoing development of this project are:

*   **Modularity**: Maintain and improve the modularity of the analysis logic. Each module should have a clear and distinct responsibility.
*   **Flexibility**: Increase the application's flexibility by adding command-line parameters for user-configurable settings, which helps reduce the need for hard-coding changes directly in `.py` files.