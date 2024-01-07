import logging
import os
from compilation_functions.compilation_indicator import indicator_func
import pandas as pd

import trend_indicator.trend_indicator_calculation as tic
import strength_indicator.strength_calculation as sc

logging.basicConfig(level=logging.INFO)

def strength_trend_func(end_date, n, n_daily):
    try:

        folder_name = end_date.strftime('%Y-%m-%d')
        base_folder = 'market_data/trend_strength_indicator'

        new_folder_path = os.path.join(base_folder, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        daily_strength_filename = os.path.join(new_folder_path, "daily_trend_strength{}.csv".format(folder_name))
        hourly_strength_filename = os.path.join(new_folder_path, "hourly_trend_strength{}.csv".format(folder_name))


        check = all(os.path.exists(filename) for filename in [daily_strength_filename, hourly_strength_filename ])
        if not check:
            logging.info("Strength Function Started")
            #### Indicator Data
            st_last_date_daily, st_last_date_one_min, st_daily, st_one_min = indicator_func(end_date, n, n_daily)

            #### Strength Function
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
            hourly_trend_calc.to_csv(hourly_strength_filename,  index=False, mode='w')
            logging.info("Writing calculated daily trend data to CSV file")
            daily_trend_calc.to_csv(daily_strength_filename,  index=False, mode='w')

            logging.info(f"CSV files created successfully in {new_folder_path}")

            return hourly_trend_calc, daily_trend_calc
        else:
            logging.info(f"CSV files for the mentioned date already exist. Skipping data fetching and processing.")
            hourly_trend_calc = pd.read_csv(hourly_strength_filename)
            daily_trend_calc = pd.read_csv(daily_strength_filename)

            return hourly_trend_calc, daily_trend_calc

    except Exception as e:
        logging.error(f"An error occurred in indicator_func: {str(e)}", exc_info=True)

