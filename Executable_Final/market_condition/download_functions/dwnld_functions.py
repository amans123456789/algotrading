import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta


def market_data(symbl,frequency,start_time, end_time):
    if frequency == "daily":
        data_daily = yf.download(symbl, start=start_time, end=end_time)
        data_daily = data_daily.reset_index()
        data_daily["Date"] = data_daily["Date"].dt.date
        data_daily.columns = ["Date", "BSE Open", "BSE High", "BSE Low", "BSE Close", "BSE AdjClose", "BSE Volume"]
        return data_daily

    if frequency == "minute":
        data_minute = yf.download(symbl, start=start_time, end=end_time, interval="1m")
        data_minute = data_minute.reset_index()
        data_minute['Datetime'] = pd.to_datetime(data_minute['Datetime'], utc=True)

        data_minute['Date'] = data_minute['Datetime'].dt.date
        data_minute['Time'] = data_minute['Datetime'].dt.time
        data_minute = data_minute.drop(["Datetime"], axis = 1)
        data_minute.columns = [ "BSE Open", "BSE High", "BSE Low", "BSE Close", "BSE AdjClose", "BSE Volume", "Date", "Time"]

        return data_minute


def VIX(frequency,start_time, end_time):
    vix_ticker = yf.Ticker("^VIX")
    if frequency == "daily":
        vix_data = vix_ticker.history(start=start_time, end=end_time)
        vix_data = vix_data.reset_index()
        vix_data['Date'] = pd.to_datetime(vix_data['Date'], utc=True)

        vix_data['date'] = vix_data['Date'].dt.date
        vix_data['time'] = vix_data['Date'].dt.time
        vix_data = vix_data.drop(["Date"], axis=1)
        vix_data.columns = ["Vix Open", "Vix High", "Vix Low", "Vix Close", "Vix Volume", "Vix Dividends", " Vix Stock Split", "Date","Time"]
        return vix_data
    if frequency == "minute":
        vix_data = vix_ticker.history(start=start_time, end=end_time,  interval="1m")
        vix_data = vix_data.reset_index()
        vix_data['Datetime'] = pd.to_datetime(vix_data['Datetime'], utc=True)

        vix_data['date'] = vix_data['Datetime'].dt.date
        vix_data['time'] = vix_data['Datetime'].dt.time
        vix_data = vix_data.drop(["Datetime"], axis = 1)

        vix_data.columns = ["Vix Open", "Vix High", "Vix Low", "Vix Close", "Vix Volume", "Vix Dividends", " Vix Stock Split", "Date","Time"]


        return vix_data

