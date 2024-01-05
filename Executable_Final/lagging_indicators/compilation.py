from config import config
import logging


import hourly_data_download
import daily_data_download

import indicators.stock_indicator_calculation as sic
import trend_indicator.trend_indicator_calculation as tic
import strength_indicator.strength_calculation as sc

logging.basicConfig(level=logging.INFO)




def lagging_indicator_function(end_date, n, n_daily):
    try:
        logging.info("Lagging Indicator Function Started")
        #### Download Data
        logging.info("Initiating hourly data download")
        hourly_data = hourly_data_download.hourly_data(end_date, n, configuration = config)
        logging.info("Hourly data download completed successfully")

        logging.info("Initiating daily data download")
        daily_data = daily_data_download.daily_download(end_date, n_daily, configuration = config)
        logging.info("Daily data download completed successfully")

        #### Indicators Function
        logging.info("Calculating trend indicators for daily data")
        st_daily = sic.trend_calculation(daily_data)
        logging.info("Calculating trend indicators for hourly data")
        st_one_min = sic.trend_calculation(hourly_data)

        st_last_date_daily = sic.time_series_last_date(st_daily)
        st_last_date_one_min = sic.time_series_last_date(st_one_min)
        ###################
        # vix_df = sic.VIX()
        ###################

        #### Strength Functions
        logging.info("Calculating strength indicators for hourly data")
        hourly_strength_calc = sc.strength_calculation(st_one_min, 70, 30)
        logging.info("Calculating strength indicators for daily data")
        daily_strength_calc = sc.strength_calculation(st_daily, 70, 30)

        #### Trend Function
        logging.info("Calculating trend indicators for hourly strength data")
        hourly_trend_calc = tic.trend_calculation(hourly_strength_calc)
        logging.info("Calculating trend indicators for daily strength data")
        daily_trend_calc = tic.trend_calculation(daily_strength_calc)

        #### CSV
        logging.info("Writing calculated hourly trend data to CSV file")
        hourly_trend_calc.to_csv("time_series_data/final_data/hourly_trend_calc.csv")
        logging.info("Writing calculated daily trend data to CSV file")
        daily_trend_calc.to_csv("time_series_data/final_data/daily_trend_calc.csv")

        logging.info("Writing last date of time series for daily data to CSV file")
        st_last_date_daily.to_csv("time_series_data/final_data/st_last_date_daily.csv")

        logging.info("Writing last date of time series for hourly data to CSV file")
        st_last_date_one_min.to_csv("time_series_data/final_data/st_last_date_one_min.csv")

        logging.info("Lagging Indicator Function Completed")

        # vix_df.to_csv("time_series_data/final_data/vix_df.csv")

        # return hourly_trend_calc, daily_trend_calc, st_last_date_daily, st_last_date_one_min, vix_df
    except Exception as e:
        logging.error(f"An error occurred in lagging_indicator_function: {str(e)}", exc_info=True)