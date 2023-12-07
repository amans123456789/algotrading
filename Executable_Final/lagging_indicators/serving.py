import yfinance as yf
from config import config
from datetime import datetime, timedelta
import pickle
import pandas as pd

import hourly_data_download
import daily_data_download

# from indicators import stock_indicator_calculation
# from strength_indicator import strength_calculation
# from trend_indicator import trend_indicator_calculation

import indicators.stock_indicator_calculation as sic
import trend_indicator.trend_indicator_calculation as tic
import strength_indicator.strength_calculation as sc


import pandas as pd


end_date = datetime.now()
n = 5
# end_date = datetime.now()
n_daily = 30

#### Download Data
hourly_data = hourly_data_download.hourly_data(end_date, n, configuration = config)
# hour_data.to_csv("time_series_data/hour_data.csv")

daily_data = daily_data_download.daily_download(end_date, n_daily, configuration = config)
# daily_data.to_csv("time_series_data/daily_data.csv")

#### Indicators Function
st_daily = sic.trend_calculation(daily_data)
st_one_min = sic.trend_calculation(hourly_data)

st_last_date_daily = sic.time_series_last_date(st_daily)
st_last_date_one_min = sic.time_series_last_date(st_one_min)
###################
vix_df = sic.VIX()
###################

#### Strength Functions

hourly_data = pd.read_csv("./time_series_data/trend_indicator_data/st_one_min.csv")
daily_data = pd.read_csv("./time_series_data/trend_indicator_data/st_daily.csv")

hourly_strength_calc = sc.strength_calculation(hourly_data, 70, 30)
daily_strength_calc = sc.strength_calculation(daily_data, 70, 30)

# hourly_strength_calc.to_csv("time_series_data/trend_data/hourly_strength_calc.csv")
# daily_strength_calc.to_csv("time_series_data/trend_data/daily_strength_calc.csv")

#### Trend Function


hourly_trend_calc = tic.trend_calculation(hourly_data)
daily_trend_calc = tic.trend_calculation(daily_data)

print(daily_trend_calc)
# hourly_trend_calc.to_csv("time_series_data/trend_data/hourly_trend_calc.csv")
# daily_trend_calc.to_csv("time_series_data/trend_data/daily_trend_calc.csv")





