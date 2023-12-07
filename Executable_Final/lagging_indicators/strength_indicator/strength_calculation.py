import pandas as pd
import strength_indicator.strength_functions as sf
import yfinance as yf
import numpy as np

hourly_data = pd.read_csv("./time_series_data/trend_indicator_data/st_one_min.csv")
daily_data = pd.read_csv("./time_series_data/trend_indicator_data/st_daily.csv")

def strength_calculation(df,upper_limit,lower_limit):
    st = pd.DataFrame()
    # df_ma = tc.moving_average(df)
    for i in df.Stock.unique():
        num = df[df["Stock"] == i]
        num["RSI_Strength"] = sf.rsi_strength(num,  upper_limit, lower_limit)
        num["Bollinger_Strength"] = sf.bollinger_strength(num)
        num["ADX_Strength"] = sf.adx_strength(num)

        st = pd.concat([st, num])

    return st


hourly_strength_calc = strength_calculation(hourly_data, 70, 30)
daily_strength_calc = strength_calculation(daily_data, 70, 30)

print(hourly_strength_calc)
# hourly_strength_calc.to_csv("time_series_data/trend_data/hourly_strength_calc.csv")
# daily_strength_calc.to_csv("time_series_data/trend_data/daily_strength_calc.csv")
