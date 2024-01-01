import indicators.stock_indicator_functions as stf
import pandas as pd

import yfinance as yf
from datetime import datetime, timedelta


def trend_calculation(df):
    st = pd.DataFrame()

    df_ma = stf.moving_average(df)
    num = stf.rsi(df_ma)
    num = stf.boll_band(num)
    num = stf.atr(num)
    num = stf.macd(num)
    num = stf.adx(num)
    num = stf.calculate_stochastic_oscillator(num)

    st = pd.concat([st, num])

    return st


def time_series_last_date(st):
    st_last_date = (
        st.apply(lambda x: x.iloc[[-1]]).reset_index(drop=True)
    )
    st_last_date = stf.calculate_fibonacci_levels(st_last_date)

    return st_last_date

