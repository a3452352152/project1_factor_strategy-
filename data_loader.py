import pandas as pd
from FinMind.data import DataLoader

def get_stock_data(stock_id, start_date='2022-01-01', end_date='2024-12-31'):
    dl = DataLoader()
    dl.login_by_token(api_token='你的 FinMind Token')  # 請替換為你自己的 API Token
    df = dl.taiwan_stock_daily(
        stock_id=stock_id,
        start_date=start_date,
        end_date=end_date
    )
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

