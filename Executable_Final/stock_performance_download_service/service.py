from fastapi import FastAPI, File, UploadFile, HTTPException
from stock_performance import stock_data_save

app = FastAPI()

@app.get("/process_stock_data")
async def stock_performance_service():
    stock_data_save.create_csv()
