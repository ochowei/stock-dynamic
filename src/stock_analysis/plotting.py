import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

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