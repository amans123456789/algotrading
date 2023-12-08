from fastapi import FastAPI, File, UploadFile, HTTPException
from compilation import lagging_indicator_function
from datetime import datetime, timedelta


app = FastAPI()

@app.get("/lagging_indicator")
async def stock_performance_service():
    end_date = datetime.now()
    n = 5
    n_daily = 30

    return lagging_indicator_function(end_date, n, n_daily)




