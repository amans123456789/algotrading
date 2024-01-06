from fastapi import FastAPI, File, UploadFile, HTTPException
from call_put_download.call_put_dwnld import call_put
from call_put_ratio.ratio import get_latest_date, group_and_sum
# from call_put_download.call_put_dwnld import save_data_to_csv
from stock_volatility.stock_data_download import daily_download
from stock_volatility.volatility_calculation import calculate_volatility_for_each_stock
from config import config
import pandas as pd
import os

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#
def call_put_data_creation(directory_name, dt, config=config):
    logger.info(f"Creating call_put data for date {dt} in directory {directory_name}")

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    csv_filename = "data{}.csv".format(dt)
    # Combine the directory and filename to get the complete path
    file_path = os.path.join(directory_name, csv_filename)
    if not os.path.exists(file_path):
        fin = []
        for i in config["ti"]:
            logger.info(f"Retrieving call_put data for stock {i} and date {dt}")
            df = call_put(i, dt)

            if df is None:
                logger.info(f"No data available for stock {i} and date {dt}. Skipping.")
                return None

            df["Stock"] = i
            fin.append(df)
        call_put_data = pd.concat(fin)
        call_put_data.to_csv(file_path)
        # save_data_to_csv(file_path, call_put_data)
        logger.info(f"Call_put data saved to {file_path}")
        return call_put_data

    else:
        logger.info(f"Call_put data for date {dt} already exists. Reading data from csv.")
        return pd.read_csv(file_path)