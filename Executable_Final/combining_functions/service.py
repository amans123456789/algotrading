import logging
from fastapi import FastAPI, Body, HTTPException
from config import config
from datetime import date, datetime, timedelta
from Test_Date_Generation.final_test_data import test_data_gen

from compilation_functions.compilation_download import download_func

logging.basicConfig( level=logging.INFO)

from typing import Union
from typing_extensions import Annotated
from create_csv import process_and_save_data


app = FastAPI()


@app.post("/test_output_feature_creation")
# async def stock_download_service():
async def stock_performance_service(
    date: Annotated[Union[str, None], Body()] = "2024-01-19",
    fund_analysis_year: Annotated[Union[str, None], Body()] = "2023",
    ratio_analysis_date: Annotated[Union[str, None], Body()] = "2024-01-25",
    news_date: Annotated[Union[str, None], Body()] = "2024-01-19",
):
    try:
        ticker_mapping = {
            config["tickers_NS"][i]: config["tickers"][i]
            for i in range(len(config["tickers_NS"]))
        }
        ticker_mapping_2 = {
            config["ti"][i]: config["tickers_NS"][i]
            for i in range(len(config["tickers_NS"]))
        }

        result = process_and_save_data(
            date,
            fund_analysis_year,
            ratio_analysis_date,
            news_date,
            ticker_mapping,
            ticker_mapping_2,
        )

        return {"message": result}
    except Exception as e:
        logging.error(f"Error in stock_performance_service: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/download_daily_hourly_data")
# async def stock_download_service():
async def stock_performance_service(
    date_daily: Annotated[Union[date, None], Body()] = None,
    date_hourly: Annotated[Union[date, None], Body()] = None,
):
    date_hourly = date_hourly or datetime.now()
    date_daily = date_daily or (datetime.now() - timedelta(days=1)).date()


    logging.info(f"Received daily download date: {date_daily}")
    logging.info(f"Received hourly download date: {date_hourly}")

    if (date_hourly - date_daily) != timedelta(days=1):
        raise HTTPException(status_code=400, detail="date_hourly must be exactly one day after date_daily")

    try:
        hourly_data, daily_data = download_func(date_daily,date_hourly)
        fin = test_data_gen(daily_data, hourly_data)

    except HTTPException as e:
        logging.error(f"An error occurred in download service: {str(e)}", exc_info=True)
