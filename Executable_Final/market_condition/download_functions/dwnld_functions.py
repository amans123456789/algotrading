import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import logging
logging.basicConfig(level=logging.INFO)


def market_data(symbl,frequency,start_time, end_time):
    try:
        if frequency == "daily":
            data_daily = yf.download(symbl, start=start_time, end=end_time)
            if data_daily.empty:
                logging.error("No market daily data available for the given dates.")
                return
            data_daily = data_daily.reset_index()
            # print(data_daily)
            data_daily["Date"] = data_daily["Date"].dt.date
            data_daily.columns = ["Date", "BSE Open", "BSE High", "BSE Low", "BSE Close", "BSE AdjClose", "BSE Volume"]
            return data_daily

        if frequency == "minute":
            data_minute = yf.download(symbl, start=start_time, end=end_time, interval="1m")
            if data_minute.empty:
                logging.error("No market minute data available for the given dates.")
                return
            data_minute = data_minute.reset_index()
            # print(data_minute)
            data_minute['Datetime'] = pd.to_datetime(data_minute['Datetime'], utc=True)

            data_minute['Date'] = data_minute['Datetime'].dt.date
            data_minute['Time'] = data_minute['Datetime'].dt.time
            data_minute = data_minute.drop(["Datetime"], axis = 1)
            data_minute.columns = [ "BSE Open", "BSE High", "BSE Low", "BSE Close", "BSE AdjClose", "BSE Volume", "Date", "Time"]

            return data_minute
    except Exception as e:
        logging.error(f"An error occurred in market_data: {str(e)}", exc_info=True)


def VIX(frequency,start_time, end_time):
    try:
        vix_ticker = yf.Ticker("^VIX")
        if frequency == "daily":
            vix_data = vix_ticker.history(start=start_time, end=end_time)
            if vix_data.empty:
                logging.error("No VIX daily data available for the given dates.")
                return
            vix_data = vix_data.reset_index()
            vix_data['Date'] = pd.to_datetime(vix_data['Date'], utc=True)

            vix_data['date'] = vix_data['Date'].dt.date
            vix_data['time'] = vix_data['Date'].dt.time
            vix_data = vix_data.drop(["Date"], axis=1)
            vix_data.columns = ["Vix Open", "Vix High", "Vix Low", "Vix Close", "Vix Volume", "Vix Dividends", " Vix Stock Split", "Date","Time"]
            return vix_data
        if frequency == "minute":
            vix_data = vix_ticker.history(start=start_time, end=end_time,  interval="1m")
            if vix_data.empty:
                logging.error("No VIX minute data available for the given dates.")
                return
            vix_data = vix_data.reset_index()
            vix_data['Datetime'] = pd.to_datetime(vix_data['Datetime'], utc=True)

            vix_data['date'] = vix_data['Datetime'].dt.date
            vix_data['time'] = vix_data['Datetime'].dt.time
            vix_data = vix_data.drop(["Datetime"], axis = 1)

            vix_data.columns = ["Vix Open", "Vix High", "Vix Low", "Vix Close", "Vix Volume", "Vix Dividends", " Vix Stock Split", "Date","Time"]


            return vix_data
    except Exception as e:
        logging.error(f"An error occurred in market_data: {str(e)}", exc_info=True)

