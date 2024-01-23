import yfinance as yf
import logging

from config import config
from datetime import datetime, timedelta
import pandas as pd
import pickle
logging.basicConfig(level=logging.INFO)

def daily_download(date_daily, configuration = config):
    try:
        start_date = date_daily - timedelta(days=1)
        data_day = [yf.download(tickers=i, start=start_date, end=date_daily, interval="1d").assign(Stock=i) for i in
                    configuration["tickers_NS"]]

        data_day = pd.concat(data_day)
        data_day = data_day.reset_index()

        return data_day

    except Exception as e:
        logging.error(f"An error occurred in daily_download function: {str(e)}", exc_info=True)