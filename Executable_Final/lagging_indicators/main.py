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

vix_df = sic.VIX()


hourly_strength_calc = sc.strength_calculation(hourly_data)
daily_strength_calc = sc.strength_calculation(daily_data)


hourly_trend_calc = tic.trend_calculation(hourly_data)
daily_trend_calc = tic.trend_calculation(daily_data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("na")