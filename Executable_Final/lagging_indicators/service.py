from fastapi import FastAPI, Body, HTTPException
from datetime import date, datetime, time, timedelta
import logging

from compilation_functions.compilation_download import download_func
from compilation_functions.compilation_indicator import indicator_func
from compilation_functions.compilation_strength_trend import strength_trend_func

logging.basicConfig(level=logging.INFO)

app = FastAPI()

from typing import Union
from typing_extensions import Annotated

from fastapi.responses import JSONResponse

# Source: https://fastapi.tiangolo.com/tutorial/extra-data-types/#__tabbed_2_3


@app.post("/download_daily_hourly_data")
# async def stock_download_service():
async def stock_performance_service(
    end_date: Annotated[Union[date, None], Body()] = None,
    n: Annotated[Union[int, None], Body()] = 5,
    n_daily: Annotated[Union[int, None], Body()] = 30,
):
    end_date = end_date or datetime.now()
    logging.info(f"Received end_date: {end_date}")

    try:
        hourly_data, daily_data = download_func(end_date, n, n_daily)
        hourly_data_subset = hourly_data[:2]
        daily_data_subset = daily_data[:2]

        return JSONResponse(
            content={
                "hourly_data": hourly_data_subset.to_dict(),
                "daily_data": daily_data_subset.to_dict(),
            },
            status_code=200,
        )

    except HTTPException as e:
        return JSONResponse(
            content={"detail": str(e.detail)}, status_code=e.status_code
        )


@app.post("/indicator_function")
async def stock_indicator_service(
    end_date: Annotated[Union[date, None], Body()] = None,
    n: Annotated[Union[int, None], Body()] = 5,
    n_daily: Annotated[Union[int, None], Body()] = 30,
):
    end_date = end_date or datetime.now()
    logging.info(f"Received end_date: {end_date}")
    indicator_func(end_date, n, n_daily)


@app.post("/trend_strength_function")
async def stock_trend_strength_service(
    end_date: Annotated[Union[date, None], Body()] = None,
    n: Annotated[Union[int, None], Body()] = 5,
    n_daily: Annotated[Union[int, None], Body()] = 30,
):
    end_date = end_date or datetime.now()
    logging.info(f"Received end_date: {end_date}")
    strength_trend_func(end_date, n, n_daily)
