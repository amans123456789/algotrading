from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from call_put_download.call_put_dwnld import call_put
from call_put_ratio.ratio import get_latest_date, group_and_sum

# from call_put_download.call_put_dwnld import save_data_to_csv
from stock_volatility.stock_data_download import daily_download
from stock_volatility.volatility_calculation import calculate_volatility_for_each_stock
from data_creation import call_put_data_creation
from datetime import date, datetime, time, timedelta

from typing_extensions import Annotated
from typing import Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()


@app.post("/call_put_data_download")
async def call_put_download(dt: Annotated[Union[date, None], Body()] = None):
    directory_name = "call_put_data/call_put_dwnld/"
    dt = get_latest_date(directory_name) if dt is None else dt

    call_put_data_creation(directory_name, dt)


@app.post("/call_put_ratio")
async def ratio_calculation(dt: Annotated[Union[date, None], Body()] = None):
    # dt = None
    directory_name = "call_put_data/call_put_dwnld/"
    dt = get_latest_date(directory_name) if dt is None else dt
    call_put_df = call_put_data_creation(directory_name, dt)
    if call_put_df is None:
        logger.info(f"No data available for the given date {dt}. Exiting.")
        return
    group_and_sum(call_put_df, dt)


@app.post("/daily_data_download")
async def daily_stock_data(
        end_date: Annotated[Union[date, None], Body()] = None,
        n_daily: Annotated[Union[int, None], Body()] = 10
):
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')

    directory_name_daily = "call_put_data/daily_dwnld/"
    daily_download(directory_name_daily, n_daily, end_date)


@app.post("/volatility_calculation")
async def daily_stock_data(
        end_date: Annotated[Union[date, None], Body()] = None,
        n_daily: Annotated[Union[int, None], Body()] = 365,
        dt: Annotated[Union[date, None], Body()] = None
):
    directory_name_daily = "call_put_data/daily_dwnld/"
    directory_name = "call_put_data/call_put_dwnld/"

    dt = get_latest_date(directory_name) if dt is None else dt
    call_put_df = call_put_data_creation(directory_name, dt)

    if call_put_df is None:
        logger.info(f"No data available for the given date {dt}. Exiting.")
        return

    stck = group_and_sum(call_put_df, dt)
    #
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')

    daily_data = daily_download(directory_name_daily, n_daily, end_date)
    return calculate_volatility_for_each_stock(daily_data, stck)
