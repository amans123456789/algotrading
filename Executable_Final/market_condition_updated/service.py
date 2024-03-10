from fastapi import FastAPI, Body, HTTPException
from datetime import date, datetime
from pandas import DataFrame, Timestamp
import json

import logging

from typing import Union
from typing_extensions import Annotated
from fastapi.responses import JSONResponse

from compilation_functions.compilation_download import download_func
from compilation_functions.compilation_indicator import indicator_func
from compilation_functions.compilation_strength_trend import strength_trend_func

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.post("/download_daily_hourly_data")
# async def stock_download_service():
async def stock_performance_service(
    end_date: Annotated[Union[date, None], Body()] = None,
    n: Annotated[Union[int, None], Body()] = 4,
    n_daily: Annotated[Union[int, None], Body()] = 240,
):
    end_date = end_date or datetime.now()
    logging.info(f"Received end_date: {end_date}")

    try:
        hourly_data, daily_data = download_func(end_date, n, n_daily)
        hourly_data_subset = hourly_data[:2]
        daily_data_subset = daily_data[:2]

    except HTTPException as e:
        return JSONResponse(
            content={"detail": str(e.detail)}, status_code=e.status_code
        )


@app.post("/indicator_function")
async def stock_indicator_service(
    end_date: Annotated[Union[date, None], Body()] = None,
    n: Annotated[Union[int, None], Body()] = 2,
    n_daily: Annotated[Union[int, None], Body()] = 240,
):
    end_date = end_date or datetime.now()
    logging.info(f"Received end_date: {end_date}")
    indicator_func(end_date, n, n_daily)


@app.post("/trend_strength_function")
async def stock_trend_strength_service(
    end_date: Annotated[Union[date, None], Body()] = None,
    n: Annotated[Union[int, None], Body()] = 4,
    n_daily: Annotated[Union[int, None], Body()] = 240,
):
    end_date = end_date or datetime.now()
    logging.info(f"Received end_date: {end_date}")
    strength_trend_func(end_date, n, n_daily)