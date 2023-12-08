from config import config


import hourly_data_download
import daily_data_download

import indicators.stock_indicator_calculation as sic
import trend_indicator.trend_indicator_calculation as tic
import strength_indicator.strength_calculation as sc


def lagging_indicator_function(end_date, n, n_daily):

    #### Download Data
    hourly_data = hourly_data_download.hourly_data(end_date, n, configuration = config)
    daily_data = daily_data_download.daily_download(end_date, n_daily, configuration = config)

    #### Indicators Function
    st_daily = sic.trend_calculation(daily_data)
    st_one_min = sic.trend_calculation(hourly_data)

    st_last_date_daily = sic.time_series_last_date(st_daily)
    st_last_date_one_min = sic.time_series_last_date(st_one_min)
    ###################
    vix_df = sic.VIX()
    ###################

    #### Strength Functions

    hourly_strength_calc = sc.strength_calculation(st_one_min, 70, 30)
    daily_strength_calc = sc.strength_calculation(st_daily, 70, 30)

    #### Trend Function


    hourly_trend_calc = tic.trend_calculation(hourly_strength_calc)
    daily_trend_calc = tic.trend_calculation(daily_strength_calc)

    #### CSV
    hourly_trend_calc.to_csv("time_series_data/final_data/hourly_trend_calc.csv")
    daily_trend_calc.to_csv("time_series_data/final_data/daily_trend_calc.csv")

    st_last_date_daily.to_csv("time_series_data/final_data/st_last_date_daily.csv")
    st_last_date_one_min.to_csv("time_series_data/final_data/st_last_date_one_min.csv")

    vix_df.to_csv("time_series_data/final_data/vix_df.csv")

    # return hourly_trend_calc, daily_trend_calc, st_last_date_daily, st_last_date_one_min, vix_df
