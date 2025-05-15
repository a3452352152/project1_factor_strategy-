import pandas as pd

def compute_factors(df: pd.DataFrame, momentum_window=20, mean_reversion_window=5):
    df = df.copy()
    # 動量因子：過去 N 日報酬率
    df['momentum'] = df['close'] / df['close'].shift(momentum_window) - 1
    # 均值回復因子：收盤價 / 過去 N 日最高價 − 1
    df['max_high_5d'] = df['high'].rolling(window=mean_reversion_window).max()
    df['mean_reversion'] = df['close'] / df['max_high_5d'] - 1
    df.dropna(inplace=True)
    return df[['close', 'momentum', 'mean_reversion']]

