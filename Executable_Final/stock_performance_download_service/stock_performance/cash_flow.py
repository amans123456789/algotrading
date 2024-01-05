import pandas as pd
import requests
import logging
from config import config

def cash_flow(ticker, ti):
    url = 'https://www.moneycontrol.com/financials/{}/consolidated-cash-flowVI/{}'.format(ticker,ti)
    logging.info(f"Fetching data from URL: {url}")
    try:
        df = pd.read_html(requests.post(url).text)[0]
    except Exception as e:
        logging.error(f"Error fetching data for {ticker}: {str(e)}")
        logging.info(f"Fetching data again")
        df = pd.read_html(requests.post(url).text)[0]

    return df


def cash_flow_alternate(ticker, ti):

    url = 'https://www.moneycontrol.com/financials/{}/cash-flowVI/{}'.format(ticker,ti)
    logging.info(f"Fetching data from URL: {url}")
    try:
        df = pd.read_html(requests.post(url).text)[0]
    except Exception as e:
        logging.error(f"Error fetching data for {ticker} (alternate): {str(e)}")
        # Retry or handle the error as needed
        # For simplicity, we retry once
        df = pd.read_html(requests.post(url).text)[0]
    return df
def run_stock_performance(config):
    fin = []
    for i in range(len( config["tickers"])):
        try:
            if config["tickers"][i] in config["ticker_alternate"]:
                df = cash_flow_alternate(config["tickers"][i], config["ti"][i])
                df["Stock"] = config["tickers"][i]
                fin.append(df)
            else:
                df = cash_flow(config["tickers"][i], config["ti"][i])
                df["Stock"] = config["tickers"][i]
                fin.append(df)
        except Exception as e:
            logging.error(f"Error processing {config['tickers'][i]}: {str(e)}")

    cfs = pd.concat(fin)
    logging.info("Stock performance data fetched successfully")

    return cfs
# def run_stock_performance(config):
#     fin = []
#     missing_inc = []
#     for i in range(len(config["tickers"])):
#         try:
#             if config["tickers"][i] in config["ticker_alternate"]:
#
#                 df = cash_flow_alternate(config["tickers"][i], config["ti"][i])
#                 df["Stock"] = config["tickers"][i]
#                 fin.append(df)
#             else:
#                 df = cash_flow(config["tickers"][i], config["ti"][i])
#                 df["Stock"] = config["tickers"][i]
#                 fin.append(df)
#         except:
#             missing_inc.append(i)
#
#     for i in missing_inc:
#         if config["tickers"][i] in config["ticker_alternate"]:
#
#             df = cash_flow_alternate(config["tickers"][i], config["ti"][i])
#             df["Stock"] = config["tickers"][i]
#             fin.append(df)
#         else:
#             df = cash_flow(config["tickers"][i], config["ti"][i])
#             df["Stock"] = config["tickers"][i]
#             fin.append(df)
#
#     cfs = pd.concat(fin)
#     return cfs

