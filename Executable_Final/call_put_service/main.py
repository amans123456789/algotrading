from call_put_download.call_put_dwnld import call_put
from call_put_ratio.ratio import get_latest_date, group_and_sum
# from call_put_download.call_put_dwnld import save_data_to_csv
from stock_volatility.stock_data_download import daily_download
from stock_volatility.volatility_calculation import calculate_volatility_for_each_stock
from config import config
from data_creation import call_put_data_creation
import pandas as pd
import os

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#
# dt = "2024-01-25"
n_daily = 365
directory_name = "call_put_data/call_put_dwnld/"
directory_name_daily = "call_put_data/daily_dwnld/"




if __name__ == '__main__':
    ### Note: Condition of reading the file if it exists else creating it from start to be added
    dt = None
    dt = get_latest_date(directory_name) if dt is None else dt
    call_put_df = call_put_data_creation(directory_name, dt)
    stck = group_and_sum(call_put_df,dt)

    daily_data = daily_download(directory_name_daily, n_daily)
    res = calculate_volatility_for_each_stock(daily_data, stck)
    print(res)
    # daily_data.to_csv("stock_volatility/daily_stock_data.csv")
