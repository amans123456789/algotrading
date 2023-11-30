import yfinance as yf
from config import config
from datetime import datetime, timedelta
import pickle
import pandas as pd

##### This is to be taken as user input #####
end_date = datetime.now()
n = 5

file_path = "time_series_data/hour_data.pkl"
def hourly_data(end_date, n, configuration = config):
    start_date = end_date - timedelta(days=n)
    hour_data = [yf.download(tickers=i, start=start_date, end=end_date, interval="1m").assign(Stock=i) for i in configuration["tickers_NS"]]

    hour_data = pd.concat(hour_data)
    hour_data = hour_data.reset_index()

    return hour_data

hour_data = hourly_data(end_date, n, configuration = config)


hour_data.to_csv("time_series_data/hour_data.csv")
# with open(file_path, "wb") as file:
#     pickle.dump(hour_data, file)
# print(hourly_data(end_date, n, configuration = config))