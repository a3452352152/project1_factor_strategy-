import pandas as pd
from data_loader import get_stock_data
from factor_calculator import compute_factors

def backtest(stock_list, start_date='2022-01-01', end_date='2024-12-31', top_k=10):
    price_df = pd.DataFrame()
    factor_df = {}

    # 下載並計算因子
    for stock_id in stock_list:
        try:
            df = get_stock_data(stock_id, start_date, end_date)
            df_factors = compute_factors(df)
            factor_df[stock_id] = df_factors
            price_df[stock_id] = df_factors['close']
        except Exception as e:
            print(f"{stock_id} 資料獲取失敗：{e}")

    monthly_dates = price_df.resample('M').last().index
    nav = 1_000_000  # 初始資金
    portfolio_value = []
    dates = []

    for date in monthly_dates[:-1]:
        scores = {}
        # 計算各股票當日得分
        for stock_id, df in factor_df.items():
            if date not in df.index: continue
            mom = df.loc[date, 'momentum']
            rev = df.loc[date, 'mean_reversion']
            score = (mom - mom.mean())/(mom.std()+1e-5) + (rev - rev.mean())/(rev.std()+1e-5)
            scores[stock_id] = score

        # 選前 top_k
        selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        selected_stocks = [s[0] for s in selected]
        weight = 1 / top_k

        # 計算次月收益
        next_date = monthly_dates[monthly_dates.get_loc(date) + 1]
        monthly_return = 0
        for stock_id in selected_stocks:
            try:
                p1 = factor_df[stock_id].loc[date, 'close']
                p2 = factor_df[stock_id].loc[next_date, 'close']
                monthly_return += weight * ((p2 - p1) / p1)
            except:
                continue

        nav *= (1 + monthly_return)
        portfolio_value.append(nav)
        dates.append(next_date)

    result = pd.DataFrame({
        'date': dates,
        'portfolio_value': portfolio_value
    }).set_index('date')
    return result

