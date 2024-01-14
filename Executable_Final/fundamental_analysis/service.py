from fastapi import FastAPI, Body, HTTPException
from calculations import fin_cal
import logging
from typing_extensions import Annotated
from typing import Union

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/fundamental_analysis")
async def stock_performance_service( year: Annotated[Union[str, None], Body()] = "23",):

    logging.info(f"Received end_date: {year}")

    fin_cal(year)
