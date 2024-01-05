import pandas as pd
import requests
import logging
from config import config
logging.basicConfig(level=logging.INFO)

def balance_sheet(ticker, ti):

    url = 'https://www.moneycontrol.com/financials/{}/consolidated-balance-sheetVI/{}'.format(ticker, ti)
    logging.info(f"Fetching data from URL: {url}")

    try:
        df = pd.read_html(requests.post(url).text)[0]
    except Exception as e:
        logging.error(f"Error fetching data for {ticker}: {str(e)}")
        # Retry or handle the error as needed
        # For simplicity, we retry once
        df = pd.read_html(requests.post(url).text)[0]

    return df


def balance_sheet_alternate(ticker, ti):
    url = 'https://www.moneycontrol.com/financials/{}/balance-sheetVI/{}'.format(ticker, ti)

    # Log the URL
    logging.info(f"Fetching data from URL: {url}")

    try:
        df = pd.read_html(requests.post(url).text)[0]
    except Exception as e:
        logging.error(f"Error fetching data for {ticker} (alternate): {str(e)}")
        logging.info(f"Fetching data again")

        # Retry or handle the error as needed
        # For simplicity, we retry once
        df = pd.read_html(requests.post(url).text)[0]

    return df
    #
    # df = pd.read_html(requests.post(url).text)[0]
    #
    # return df

def run_stock_performance(config):
    fin = []
    for i in range(len( config["tickers"] )):
        if config["tickers"][i] in config["ticker_alternate"]:
            df = balance_sheet_alternate(config["tickers"][i], config["ti"][i])
            df["Stock"] = config["tickers"][i]
            fin.append(df)

        else:
            df = balance_sheet(config["tickers"][i], config["ti"][i])
            df["Stock"] = config["tickers"][i]
            fin.append(df)

    bs = pd.concat(fin)
    logging.info("Stock performance data fetched successfully")

    return bs