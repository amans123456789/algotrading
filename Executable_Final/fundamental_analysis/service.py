from fastapi import FastAPI
from calculations import fin_cal

app = FastAPI()

@app.get("/fundamental_analysis")
async def stock_performance_service():
    return fin_cal()
