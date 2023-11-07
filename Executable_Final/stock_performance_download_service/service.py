from fastapi import FastAPI, File, UploadFile, HTTPException
from stock_performance import stock_data_save

app = FastAPI()

# @app.get("/process_stock_data/")
@app.get("/process_stock_data")
async def stock_performance_service():
    return stock_data_save.create_csv()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)