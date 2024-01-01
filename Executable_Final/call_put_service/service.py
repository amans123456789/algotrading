from fastapi import FastAPI, File, UploadFile, HTTPException
from call_put_download.call_put_dwnld import call_put
from call_put_ratio.ratio import get_latest_date, group_and_sum
# from call_put_download.call_put_dwnld import save_data_to_csv
from stock_volatility.stock_data_download import daily_download
from stock_volatility.volatility_calculation import calculate_volatility_for_each_stock
from data_creation import call_put_data_creation

from config import config
import pandas as pd
import os

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/call_put_data_download")
async def call_put_download():
    dt = None
    directory_name = "call_put_data/call_put_dwnld/"
    dt = get_latest_date(directory_name) if dt is None else dt

    call_put_data_creation(directory_name, dt)



@app.get("/call_put_ratio")
async def ratio_calculation():
    dt = None
    directory_name = "call_put_data/call_put_dwnld/"
    dt = get_latest_date(directory_name) if dt is None else dt
    call_put_df = call_put_data_creation(directory_name, dt)

    group_and_sum(call_put_df,dt)

@app.get("/daily_data_download")
async def daily_stock_data():
    n_daily = 365
    directory_name_daily = "call_put_data/daily_dwnld/"
    daily_download(directory_name_daily, n_daily)


@app.get("/volatility_calculation")
async def daily_stock_data():
    dt = None
    directory_name_daily = "call_put_data/daily_dwnld/"
    directory_name = "call_put_data/call_put_dwnld/"
    n_daily = 365

    dt = get_latest_date(directory_name) if dt is None else dt
    call_put_df = call_put_data_creation(directory_name, dt)
    stck = group_and_sum(call_put_df,dt)

    daily_data = daily_download(directory_name_daily, n_daily)
    calculate_volatility_for_each_stock(daily_data, stck)