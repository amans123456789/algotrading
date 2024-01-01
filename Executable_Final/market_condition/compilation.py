from config import config
import indicators.stock_indicator_calculation as sic
import trend_indicator.trend_indicator_calculation as tic
import strength_indicator.strength_calculation as sc

from download_functions.download import daily_data, minute_data

# def lagging_indicator_function(end_date, n, n_daily):

    #### Download Data
fin_min, res_min, vx_min = (minute_data(config["tickers_NS"], "2023-12-21", "2023-12-24"))
fin_day, res_day, vx_day = (daily_data(config["tickers_NS"], "2023-12-21", "2023-12-24"))

#### Indicators Function
st_daily = sic.trend_calculation(fin_day)
st_one_min = sic.trend_calculation(fin_min)

st_last_date_daily = sic.time_series_last_date(st_daily)
st_last_date_one_min = sic.time_series_last_date(st_one_min)


#### Strength Functions

hourly_strength_calc = sc.strength_calculation(st_one_min, 70, 30)
daily_strength_calc = sc.strength_calculation(st_daily, 70, 30)

#### Trend Function


hourly_trend_calc = tic.trend_calculation(hourly_strength_calc)
daily_trend_calc = tic.trend_calculation(daily_strength_calc)

#### CSV
hourly_trend_calc.to_csv("market_data/final_data/hourly_trend_calc.csv")
daily_trend_calc.to_csv("market_data/final_data/daily_trend_calc.csv")

st_last_date_daily.to_csv("market_data/final_data/st_last_date_daily.csv")
st_last_date_one_min.to_csv("market_data/final_data/st_last_date_one_min.csv")


# return hourly_trend_calc, daily_trend_calc, st_last_date_daily, st_last_date_one_min, vix_df
