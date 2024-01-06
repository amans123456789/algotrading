from download_functions.dwnld_functions import market_data, VIX
import pandas as pd
# from config import config
import logging
logging.basicConfig(level=logging.INFO)
import os


def daily_data(mkt_symb,start_date, end_date):
    try:
        folder_name = (end_date).strftime('%Y-%m-%d')
        base_folder = 'market_data/final_download'

        new_folder_path = os.path.join(base_folder, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        daily_filename = os.path.join(new_folder_path, "fin_daily{}.csv".format(folder_name))

        check = all(os.path.exists(filename) for filename in [daily_filename])
        if not check:

            res = market_data(mkt_symb,"daily",start_date, end_date)
            vx = VIX("daily",start_date, end_date)
            fin = pd.merge(vx, res, on='Date')
            fin.to_csv(daily_filename)

            return fin
        else:
            logging.info(f"CSV files for the mentioned date already exist. Skipping data fetching and processing.")
            fin = pd.read_csv(daily_filename)

            return fin
    except Exception as e:
        logging.error(f"An error occurred in download_func: {str(e)}", exc_info=True)


def minute_data(mkt_symb,start_date, end_date):
    try:
        folder_name = (end_date).strftime('%Y-%m-%d')
        base_folder = 'market_data/final_download'

        new_folder_path = os.path.join(base_folder, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        minute_filename = os.path.join(new_folder_path, "fin_minute{}.csv".format(folder_name))

        check = all(os.path.exists(filename) for filename in [minute_filename])
        if not check:

            res = market_data(mkt_symb,"minute",start_date, end_date)
            vx = VIX("minute",start_date, end_date)
            fin = pd.merge(vx, res, on=['Date','Time'])
            fin.to_csv(minute_filename)

            return fin

        else:
            logging.info(f"CSV files for the mentioned date already exist. Skipping data fetching and processing.")
            fin = pd.read_csv(minute_filename)
            return fin
    except Exception as e:
        logging.error(f"An error occurred in download_func: {str(e)}", exc_info=True)
