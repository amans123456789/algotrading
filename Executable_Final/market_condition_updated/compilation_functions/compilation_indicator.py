import logging
import os
from compilation_functions.compilation_download import download_func
import pandas as pd

import indicators.stock_indicator_calculation as sic

logging.basicConfig(level=logging.INFO)


def indicator_func(end_date, n, n_daily):
    try:

        folder_name = end_date.strftime('%Y-%m-%d')
        base_folder = 'time_series_data/indicator'

        new_folder_path = os.path.join(base_folder, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        daily_indicator_filename = os.path.join(new_folder_path, "daily_indicator{}.csv".format(folder_name))
        hourly_indicator_filename = os.path.join(new_folder_path, "hourly_indicator{}.csv".format(folder_name))

        daily_indicator_lastdate = os.path.join(new_folder_path, "last_day_fibonacci_lag_indicator_{}.csv".format(folder_name))
        hourly_indicator_lastdate = os.path.join(new_folder_path, "last_hour_fibonacci_lag_indicator_{}.csv".format(folder_name))

        check = all(os.path.exists(filename) for filename in [daily_indicator_filename, hourly_indicator_filename, daily_indicator_lastdate,hourly_indicator_lastdate ])
        if not check:
            logging.info("Indicator Function Started")
            #### Download Data
            hourly_data, daily_data = download_func(end_date, n, n_daily)

            #### Indicator Data
            logging.info("Calculating indicators for daily data")
            st_daily = sic.trend_calculation(daily_data)
            logging.info("Calculating  indicators for hourly data")
            st_one_min = sic.trend_calculation(hourly_data)

            st_last_date_daily = sic.time_series_last_date(st_daily)

            # hourly_data.to_csv(hourly_filename, index=False, mode='w')
            # daily_data.to_csv(daily_filename, index=False, mode='w')

            logging.info("Writing last date of time series for daily data to CSV file")
            st_last_date_daily.to_csv(daily_indicator_lastdate, index=False, mode='w')

            if st_one_min is not None:
                st_last_date_one_min = sic.time_series_last_date(st_one_min)
                logging.info("Writing last date of time series for hourly data to CSV file")
                st_last_date_one_min.to_csv(hourly_indicator_lastdate, index=False, mode='w')

                logging.info("Writing hourly indicator data to CSV file")
                st_one_min.to_csv(hourly_indicator_filename, index=False, mode='w')

            logging.info("Writing daily indicator data to CSV file")
            st_daily.to_csv(daily_indicator_filename,  index=False, mode='w')



            logging.info(f"CSV files created successfully in {new_folder_path}")

            return st_last_date_daily, st_last_date_one_min, st_daily, st_one_min
        else:
            logging.info(f"CSV files for the mentioned date already exist. Skipping data fetching and processing.")
            st_last_date_daily = pd.read_csv(daily_indicator_lastdate)
            st_last_date_one_min = pd.read_csv(hourly_indicator_lastdate)
            st_daily = pd.read_csv(daily_indicator_filename)
            st_one_min = pd.read_csv(hourly_indicator_filename)

            return st_last_date_daily, st_last_date_one_min, st_daily, st_one_min

    except Exception as e:
        logging.error(f"An error occurred in indicator_func: {str(e)}", exc_info=True)

