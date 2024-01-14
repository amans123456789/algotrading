from config import config
from fastapi import FastAPI, Body
from download_functions.download import daily_data, minute_data
from datetime import date, datetime, timedelta
import logging
from fastapi.responses import JSONResponse

from compilation_functions.compilation_indicator import indicator_func
from compilation_functions.compilation_strength_trend import strength_trend_func

logging.basicConfig(level=logging.INFO)

app = FastAPI()
from typing import Union
from typing_extensions import Annotated


@app.post("/download_market_data")
async def stock_download_service(
        n: Annotated[Union[int, None], Body()] = 2,
        n_daily: Annotated[Union[int, None], Body()] = 240,
        end_date: Annotated[Union[date, None], Body()] = None
):
    start_date_n = end_date - timedelta(days=n)
    start_date_n_daily = end_date - timedelta(days=n_daily)

    logging.info(f"Received end_date: {end_date}")
    logging.info(f"Received start_date for minute data: {start_date_n}")
    logging.info(f"Received start_date for daily data: {start_date_n_daily}")

    # if start_date is not None and end_date is not None and start_date > end_date:
    #     error_mssg = "Start date cannot be greater than end date."
    #     logging.error(error_mssg)
    #     # return {"error": "Start date cannot be greater than end date."}
    #     return JSONResponse(status_code=400, content={"error": error_mssg})

    fin_min = (minute_data(config["tickers_NS"], start_date_n, end_date))
    fin_daily = (daily_data(config["tickers_NS"], start_date_n_daily, end_date))

    if fin_min is None:
        error_mssg = "Download failed for minute data. Exiting the loop."
        logging.error(error_mssg)
        # return {"error": "Download failed for minute data."}
        return JSONResponse(status_code=400, content={"error": error_mssg})

    # Check if the download failed for daily_data
    if fin_daily is None:
        error_mssg = "Download failed for daily data. Exiting the loop."
        logging.error(error_mssg)
        return JSONResponse(status_code=400, content={"error": error_mssg})

    success_message = "Data download completed successfully."
    logging.info(success_message)
    return {"message": success_message}

@app.post("/indicator_function")
async def stock_indicator_service(
    end_date: Annotated[Union[date, None], Body()] = None,
    n: Annotated[Union[int, None], Body()] = 2,
    n_daily: Annotated[Union[int, None], Body()] = 240,
):
    end_date = end_date or datetime.now()
    logging.info(f"Received end_date: {end_date}")
    indicator_func(end_date, n, n_daily)
    # indicator_func(end_date)


@app.post("/trend_strength_function")
async def stock_trend_strength_service(
    end_date: Annotated[Union[date, None], Body()] = None,
    n: Annotated[Union[int, None], Body()] = 2,
    n_daily: Annotated[Union[int, None], Body()] = 240,
):
    end_date = end_date or datetime.now()
    logging.info(f"Received end_date: {end_date}")
    strength_trend_func(end_date, n, n_daily)


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Health check passed."}


