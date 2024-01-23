from config import config
import logging
import os

from compilation_functions.hourly_data_download import hourly_download
from compilation_functions.daily_data_download import daily_download

# import hourly_data_download
# import daily_data_download

import pandas as pd

from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)

def download_func(date_daily, date_hourly):
    try:
        folder_name = (date_daily).strftime('%Y-%m-%d')
        base_folder = 'Source_Data/time_series_data'

        new_folder_path = os.path.join(base_folder, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        hourly_filename = os.path.join(new_folder_path, "hourly_data{}.csv".format(folder_name))
        daily_filename = os.path.join(new_folder_path, "daily_date{}.csv".format(folder_name))

        check = all(os.path.exists(filename) for filename in [hourly_filename, daily_filename])
        if not check:

            logging.info("Download Function Started")
            #### Download Data
            logging.info("Initiating hourly data download")
            hourly_data = hourly_download(date_hourly, configuration = config)
            logging.info("Hourly data download completed successfully")

            logging.info("Initiating daily data download")
            daily_data = daily_download(date_daily, configuration = config)
            logging.info("Daily data download completed successfully")

            hourly_data.to_csv(hourly_filename, index=False, mode='w')
            daily_data.to_csv(daily_filename, index=False, mode='w')

            logging.info(f"CSV files created successfully in {new_folder_path}")

            return hourly_data, daily_data
        else:
            logging.info(f"CSV files for the mentioned date already exist. Skipping data fetching and processing.")
            hourly_data = pd.read_csv(hourly_filename)
            daily_data = pd.read_csv(daily_filename)

            return hourly_data, daily_data

    except Exception as e:
        logging.error(f"An error occurred in download_func: {str(e)}", exc_info=True)

