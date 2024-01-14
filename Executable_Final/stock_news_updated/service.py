from fastapi import FastAPI, File, UploadFile, HTTPException
from analysis.sentiment_postrocessing import postproc

from download_news.news_data import news_download, news_df
from analysis.ner_execution import ner_exec, sentiment_exec
from config import config
import pandas as pd
import os
from datetime import datetime
import logging

app = FastAPI()

folder_name = "news_data"
csv_prefix = "news-dwnld-data"

ner_folder = "ner_data"
ner_csv_prefix = "news-ner-data"

sentiment_folder = "sentiment_data"
sentiment_csv_prefix = "news-sentiment-data"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_latest_csv(folder_name, csv_prefix):

    files = [file for file in os.listdir(folder_name) if file.startswith(csv_prefix) and file.endswith(".csv")]
    if files:
        # Extract dates from the filenames and find the latest date
        latest_date = max([file.split("_")[1].split(".")[0] for file in files])

        # Form the filename with the latest date
        latest_csv_filename = f"{csv_prefix}_{latest_date}.csv"
        latest_csv_path = os.path.join(folder_name, latest_csv_filename)


        # Read the CSV file with the latest date
        if os.path.exists(latest_csv_path):
            latest_data = pd.read_csv(latest_csv_path)
            logger.info(f"Read data from {latest_csv_filename}")
            return latest_data
        else:
            logger.error(f"CSV file not found: {latest_csv_filename}")
            return None
    else:
        logger.error("No CSV files found in the specified folder.")
        return None


def news_download_analysis(df, func,folder_name, csv_prefix):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    today_date = datetime.today().strftime("%Y-%m-%d")
    csv_filename = f"{csv_prefix}_{today_date}.csv"

    csv_path = os.path.join(folder_name, csv_filename)
    if not os.path.exists(csv_path):
        if func == "download":
            news_data, missing = news_df(config)
            news_data.to_csv(csv_path, index=False)
            logger.info(f"CSV file created: {csv_path}")
        if func == "ner":
            ner_data = ner_exec(df)
            ner_data.to_csv(csv_path, index=False)
            logger.info(f"CSV file created: {csv_path}")
        if func == "sent":
            sent_data = sentiment_exec(df)
            # postprocess_sent_data = postproc(sent_data)
            # postprocess_sent_data.to_csv(csv_path, index=False)
            sent_data.to_csv(csv_path, index=False)
            logger.info(f"CSV file created: {csv_path}")
    else:
        logger.warning(f"CSV file already exists: {csv_path}")



@app.get("/stock_news")
async def stock_news_service():
    df = pd.DataFrame()
    news_download_analysis(df, "download", folder_name, csv_prefix)

    df = read_latest_csv(folder_name, csv_prefix)
    # print(df)

    news_download_analysis(df, "ner", ner_folder, ner_csv_prefix)

    df_ner = read_latest_csv(ner_folder, ner_csv_prefix)
    news_download_analysis(df_ner, "sent", sentiment_folder, sentiment_csv_prefix)





