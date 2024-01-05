import yfinance as yf
import logging

from config import config
from datetime import datetime, timedelta
import pickle
import pandas as pd

def hourly_data(end_date, n, configuration = config):
    try:
        start_date = end_date - timedelta(days=n)

        hour_data = [yf.download(tickers=i, start=start_date, end=end_date, interval="1m").assign(Stock=i) for i in configuration["tickers_NS"]]

        hour_data = pd.concat(hour_data)
        hour_data = hour_data.reset_index()

        return hour_data

    except Exception as e:
        logging.error(f"An error occurred in hourly_data function: {str(e)}", exc_info=True)