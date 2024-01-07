import logging
import os
import pandas as pd

import indicators.stock_indicator_calculation as sic

logging.basicConfig(level=logging.INFO)


def indicator_func(end_date, n, n_daily):
    try:

        folder_name = end_date.strftime('%Y-%m-%d')
        base_folder = 'market_data/indicator'

        new_folder_path = os.path.join(base_folder, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        daily_indicator_filename = os.path.join(new_folder_path, "daily_indicator{}.csv".format(folder_name))
        hourly_indicator_filename = os.path.join(new_folder_path, "hourly_indicator{}.csv".format(folder_name))

        daily_indicator_lastdate = os.path.join(new_folder_path, "stlast_daily_indicator{}.csv".format(folder_name))
        hourly_indicator_lastdate = os.path.join(new_folder_path, "stlast_hourly_indicator{}.csv".format(folder_name))

        check = all(os.path.exists(filename) for filename in [daily_indicator_filename, hourly_indicator_filename, daily_indicator_lastdate,hourly_indicator_lastdate ])
        if not check:
            logging.info("Indicator Function Started")

            logging.info("Reading data from the latest date folder")
            daily_data, hourly_data = read_data_from_latest_date("market_data/final_download")

            if daily_data is None or hourly_data is None:
                return None, None, None, None  # Return or handle appropriately
            #### Indicator Data
            logging.info("Calculating indicators for daily data")
            st_daily = sic.trend_calculation(daily_data)
            logging.info("Calculating  indicators for hourly data")
            st_one_min = sic.trend_calculation(hourly_data)

            st_last_date_daily = sic.time_series_last_date(st_daily)
            st_last_date_one_min = sic.time_series_last_date(st_one_min)

            # hourly_data.to_csv(hourly_filename, index=False, mode='w')
            # daily_data.to_csv(daily_filename, index=False, mode='w')

            logging.info("Writing last date of time series for daily data to CSV file")
            st_last_date_daily.to_csv(daily_indicator_lastdate, index=False, mode='w')

            logging.info("Writing last date of time series for hourly data to CSV file")
            st_last_date_one_min.to_csv(hourly_indicator_lastdate, index=False, mode='w')

            logging.info("Writing daily indicator data to CSV file")
            st_daily.to_csv(daily_indicator_filename,  index=False, mode='w')

            logging.info("Writing hourly indicator data to CSV file")
            st_one_min.to_csv(hourly_indicator_filename , index=False, mode='w')

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

def get_latest_date_folder(directory):
    subfolders = [f.path for f in os.scandir(directory) if f.is_dir()]
    if not subfolders:
        return None
    latest_date_folder = max(subfolders, key=os.path.basename)
    return latest_date_folder

def get_latest_date_csv(directory):
    date_folder = get_latest_date_folder(directory)
    if not date_folder:
        return None, None
    daily_csv = os.path.join(date_folder, f"fin_daily{os.path.basename(date_folder)}.csv")
    hourly_csv = os.path.join(date_folder, f"fin_minute{os.path.basename(date_folder)}.csv")
    return daily_csv, hourly_csv

def read_data_from_latest_date(directory):
    daily_csv, hourly_csv = get_latest_date_csv(directory)
    if not daily_csv or not hourly_csv or not os.path.isfile(daily_csv) or not os.path.isfile(hourly_csv):
        logging.info("CSV files for the latest date not found. Please run file downloads first.")
        return None, None

    daily_data = pd.read_csv(daily_csv)
    hourly_data = pd.read_csv(hourly_csv)
    return daily_data, hourly_data