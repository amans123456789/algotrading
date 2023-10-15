import pandas as pd
import numpy as np
import Stock_List as sl


import yfinance as yf

def stock_5day_1min(tickers_NS):
    data = []
    for i in tickers_NS:
        df = yf.download(tickers=i, period="5d", interval="1m")
        df["Stock"] = i
        data.append(df)

    return data

def stock_7mo_daily(tickers_NS):
    data_day = []
    for i in tickers_NS:
        df_day = yf.download(tickers=i, period="7mo", interval="1d")
        df_day["Stock"] = i
        data_day.append(df_day)

    return data_day

one_minute_data = stock_5day_1min(sl.tickers_NS)
daily_data = stock_7mo_daily(sl.tickers_NS)


one_minute_data.to_csv("Stock_Performance_Document/Stock_time_series/one_minute_download.csv")
daily_data.to_csv("Stock_Performance_Document/Stock_time_series/daily_download.csv")