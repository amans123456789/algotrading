import yfinance as yf
from config import config
from datetime import datetime, timedelta
import pandas as pd
import pickle

##### This is to be taken as user input #####
end_date = datetime.now()
n_daily = 30

file_path = "time_series_data/daily_data.pkl"
def daily_download(end_date, n_daily, configuration = config):
    start_date = end_date - timedelta(days=n_daily)
    data_day = [yf.download(tickers=i, start=start_date, end=end_date, interval="1d").assign(Stock=i) for i in
                configuration["tickers_NS"]]

    data_day = pd.concat(data_day)
    data_day = data_day.reset_index()

    return data_day

daily_data = daily_download(end_date, n_daily, configuration = config)



daily_data.to_csv("time_series_data/daily_data.csv")
# with open(file_path, "wb") as file:
#     pickle.dump(daily_data, file)
# print(daily_download(end_date, 30, configuration = config))