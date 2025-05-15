import pandas as pd
import numpy as np

def compute_performance_metrics(nav_df, rf_rate=0.01):
    nav = nav_df['portfolio_value']
    returns = nav.pct_change().dropna()
    freq = pd.infer_freq(nav_df.index)
    ann_factor = 12 if freq.startswith('M') else 252

    # 計算 CAGR
    years = (nav.index[-1] - nav.index[0]).days / 365
    cagr = (nav.iloc[-1] / nav.iloc[0])**(1/years) - 1

    # 波動率 & 夏普
    vol = returns.std() * np.sqrt(ann_factor)
    sharpe = (cagr - rf_rate) / vol if vol > 0 else np.nan

    # 最大回撤
    cummax = nav.cummax()
    drawdown = (nav - cummax) / cummax
    max_dd = drawdown.min()

    df = pd.DataFrame({
        '年化報酬率 (%)': [round(cagr*100, 2)],
        '年化波動率 (%)': [round(vol*100, 2)],
        '夏普比率':       [round(sharpe, 2)],
        '最大回撤 (%)':    [round(max_dd*100, 2)]
    }, index=['績效指標'])
    return df

