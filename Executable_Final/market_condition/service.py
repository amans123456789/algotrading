from config import config
from fastapi import FastAPI, Body
from download_functions.download import daily_data, minute_data
from datetime import date, datetime
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()
from typing import Union
from typing_extensions import Annotated

@app.post("/download_market_data")
async def stock_download_service(
        start_date: Annotated[Union[date, None], Body()] = None,
        end_date: Annotated[Union[date, None], Body()] = None
):
    logging.info(f"Received end_date: {end_date}")
    logging.info(f"Received end_date: {start_date}")

    (minute_data(config["tickers_NS"], start_date, end_date))
    (daily_data(config["tickers_NS"], start_date, end_date))


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Health check passed."}


