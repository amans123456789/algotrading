import yfinance as yf
import logging

from config import config
from datetime import datetime, timedelta
import pickle
import pandas as pd

def hourly_download(date_hourly, configuration = config):
    try:
        start_date = date_hourly - timedelta(days=1)

        hour_data = [yf.download(tickers=i, start=start_date, end=date_hourly, interval="1m").assign(Stock=i) for i in configuration["tickers_NS"]]

        hour_data = pd.concat(hour_data)
        hour_data = hour_data.reset_index()

        return hour_data

    except Exception as e:
        logging.error(f"An error occurred in hourly_data function: {str(e)}", exc_info=True)