from download_functions.dwnld_functions import market_data, VIX
import pandas as pd
from datetime import  timedelta
import logging
logging.basicConfig(level=logging.INFO)
import os

#
from download_functions.dwnld_functions import market_data, VIX
import pandas as pd
from datetime import timedelta
import logging
import os

def daily_minute_data(mkt_symb, freq, n, n_daily, end_date):
    try:
        if freq == "daily":
            start_date_n = end_date - timedelta(days=n_daily)
        elif freq == "minute":
            start_date_n = end_date - timedelta(days=n)
        else:
            logging.error("Invalid frequency specified. Supported frequencies are 'daily' and 'minute'.")
            return None

        logging.info(f"Received end_date: {end_date}")
        logging.info(f"Received start_date for {freq} data: {start_date_n}")

        folder_name = (end_date).strftime('%Y-%m-%d')
        base_folder = 'market_data/final_download'

        new_folder_path = os.path.join(base_folder, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        filename = os.path.join(new_folder_path, f"fin_{freq}{folder_name}.csv")

        # check = os.path.exists(filename)
        check = all(os.path.exists(file) for file in [filename])
        if not check:
            #             res = market_data(mkt_symb,"minute",start_date_n, end_date)
            #             if res is None or res.empty:
            #                 logging.error("No minute wise market data available for the given dates.")
            #                 return
            #             vx = VIX("minute",start_date_n, end_date)
            #             if vx is None or vx.empty:
            #                 logging.error("No minute wise vx market data available for the given dates.")
            #                 return
            #             fin = pd.merge(vx, res, on=['Date','Time'])
            #             fin.to_csv(minute_filename)

            res = market_data(mkt_symb, freq, start_date_n, end_date)
            if res is None or res.empty:
                logging.error(f"No {freq} market data available for the given dates.")
                return

            vx = VIX(freq, start_date_n, end_date)
            if vx is None or vx.empty:
                logging.error(f"No {freq} vx market data available for the given dates.")
                return

            if freq == "daily":
                fin = pd.merge(vx, res, on='Date')
            elif freq == "minute":
                fin = pd.merge(vx, res, on=['Date', 'Time'])

            fin.to_csv(filename)
            return fin
        else:
            logging.info(f"CSV file for the mentioned date already exists. Skipping data fetching and processing.")
            fin = pd.read_csv(filename)
            return fin
    except Exception as e:
        logging.error(f"An error occurred in fetch_and_save_data: {str(e)}", exc_info=True)
        return None

# def daily_data(mkt_symb,n_daily, end_date):
#     try:
#         # start_date_n = end_date - timedelta(days=n)
#         start_date_n_daily = end_date - timedelta(days=n_daily)
#
#         logging.info(f"Received end_date: {end_date}")
#         # logging.info(f"Received start_date for minute data: {start_date_n}")
#         logging.info(f"Received start_date for daily data: {start_date_n_daily}")
#
#         folder_name = (end_date).strftime('%Y-%m-%d')
#         base_folder = 'market_data/final_download'
#
#         new_folder_path = os.path.join(base_folder, folder_name)
#         os.makedirs(new_folder_path, exist_ok=True)
#
#         daily_filename = os.path.join(new_folder_path, "fin_daily{}.csv".format(folder_name))
#
#         check = all(os.path.exists(filename) for filename in [daily_filename])
#         if not check:
#
#             res = market_data(mkt_symb,"daily",start_date_n_daily, end_date)
#             if res is None or res.empty:
#                 logging.error("No market data available for the given dates.")
#                 return
#             vx = VIX("daily",start_date_n_daily, end_date)
#             if vx is None or vx.empty:
#                 logging.error("No vx market data available for the given dates.")
#                 return
#             fin = pd.merge(vx, res, on='Date')
#             fin.to_csv(daily_filename)
#
#             return fin
#         else:
#             logging.info(f"CSV files for the mentioned date already exist. Skipping data fetching and processing.")
#             fin = pd.read_csv(daily_filename)
#
#             return fin
#     except Exception as e:
#         logging.error(f"An error occurred in daily_data: {str(e)}", exc_info=True)
#         return None
#
#
# def minute_data(mkt_symb,n, end_date):
#     try:
#         start_date_n = end_date - timedelta(days=n)
#         # start_date_n_daily = end_date - timedelta(days=n_daily)
#
#         logging.info(f"Received end_date: {end_date}")
#         logging.info(f"Received start_date for minute data: {start_date_n}")
#         # logging.info(f"Received start_date for daily data: {start_date_n_daily}")
#
#
#         folder_name = (end_date).strftime('%Y-%m-%d')
#         base_folder = 'market_data/final_download'
#
#         new_folder_path = os.path.join(base_folder, folder_name)
#         os.makedirs(new_folder_path, exist_ok=True)
#
#         minute_filename = os.path.join(new_folder_path, "fin_minute{}.csv".format(folder_name))
#
#         check = all(os.path.exists(filename) for filename in [minute_filename])
#         if not check:
#
#             res = market_data(mkt_symb,"minute",start_date_n, end_date)
#             if res is None or res.empty:
#                 logging.error("No minute wise market data available for the given dates.")
#                 return
#             vx = VIX("minute",start_date_n, end_date)
#             if vx is None or vx.empty:
#                 logging.error("No minute wise vx market data available for the given dates.")
#                 return
#             fin = pd.merge(vx, res, on=['Date','Time'])
#             fin.to_csv(minute_filename)
#
#             return fin
#
#         else:
#             logging.info(f"CSV files for the mentioned date already exist. Skipping data fetching and processing.")
#             fin = pd.read_csv(minute_filename)
#             return fin
#     except Exception as e:
#         logging.error(f"An error occurred in minute_data: {str(e)}", exc_info=True)
#         return None