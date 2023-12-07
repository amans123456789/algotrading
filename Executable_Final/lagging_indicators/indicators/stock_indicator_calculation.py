import indicators.stock_indicator_functions as stf
import pandas as pd

import yfinance as yf
from datetime import datetime, timedelta


hourly_data = pd.read_csv("./time_series_data/hour_data.csv")
daily_data = pd.read_csv("./time_series_data/daily_data.csv")


def trend_calculation(df):
    st = pd.DataFrame()

    df_ma = stf.moving_average(df)
    for i in df.Stock.unique():
        num = stf.rsi(df_ma, i)
        num = stf.boll_band(num, i, n=14)
        num = stf.atr(num, i, n=14)
        num = stf.macd(num, i)
        num = stf.adx(num, i)
        num = stf.calculate_stochastic_oscillator(num, i)

        st = pd.concat([st, num])

    return st

def time_series_last_date(st):
    st_last_date = st.groupby('Stock').apply(lambda x: x.iloc[[-1]]).reset_index(drop=True)
    st_last_date = stf.calculate_fibonacci_levels(st_last_date)

    return st_last_date
def VIX():
    vix_ticker = yf.Ticker("^VIX")
    today = datetime.now().strftime('%Y-%m-%d')
    today = datetime.strptime(today, '%Y-%m-%d')

    start_date = today - timedelta(days=1)
    start_date_str = start_date.strftime('%Y-%m-%d')
    vix_data = vix_ticker.history(start=start_date_str, end=today)

    return vix_data


st_daily = trend_calculation(daily_data)
st_one_min = trend_calculation(hourly_data)

st_last_date_daily = time_series_last_date(st_daily)
st_last_date_one_min = time_series_last_date(st_one_min)

vix_df = VIX()
print(vix_df)
#
# vix_df.to_csv("time_series_data/trend_indicator_data/vix_df.csv")
#
# st_daily.to_csv("time_series_data/trend_indicator_data/st_daily.csv")
# st_one_min.to_csv("time_series_data/trend_indicator_data/st_one_min.csv")
#
# st_last_date_daily.to_csv("time_series_data/trend_indicator_data/st_last_date_daily.csv")
# st_last_date_one_min.to_csv("time_series_data/trend_indicator_data/st_last_date_one_min.csv")

