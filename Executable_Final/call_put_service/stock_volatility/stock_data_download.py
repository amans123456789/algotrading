import yfinance as yf
from config import config
from datetime import datetime, timedelta
import pandas as pd
import logging
import os

# Configure the logging module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def daily_download(directory_name, n_daily, end_date,  configuration=config):
    data_day = []


    logger.info(f"Creating call_put data for date {end_date} in directory {directory_name}")

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    csv_filename = "dailydata{}.csv".format(end_date)
    file_path = os.path.join(directory_name, csv_filename)
    if not os.path.exists(file_path):

        start_date = end_date - timedelta(days=n_daily)
        # start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=n_daily)).strftime('%Y-%m-%d')
        logger.info(f"Downloading data from {start_date} to {end_date} for tickers: {configuration['tickers_NS']}")

        for ticker in configuration["tickers_NS"]:
            logger.info(f"Downloading data for {ticker}...")
            try:
                data = yf.download(tickers=ticker, start=start_date, end=end_date, interval="1d").assign(Stock=ticker)
                data_day.append(data)
                logger.info(f"Download for {ticker} completed.")
            except Exception as e:
                logger.error(f"Error downloading data for {ticker}: {str(e)}")

        if not data_day:
            logger.warning("No data downloaded.")
        # data_day = [yf.download(tickers=i, start=start_date, end=end_date, interval="1d").assign(Stock=i) for i in
        #             configuration["tickers_NS"]]

        data_day = pd.concat(data_day)
        data_day = data_day.reset_index()

        data_day.to_csv(file_path)
        logger.info(f"daily data saved to {file_path}")
        return data_day
    else:
        logger.info(f"daily data for date {end_date} already exists. Reading data from csv.")
        return pd.read_csv(file_path)