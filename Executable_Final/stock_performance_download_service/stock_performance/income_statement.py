import pandas as pd
import requests
import logging

from config import config
logging.basicConfig(level=logging.INFO)

def inc_statement(ticker, ti):
    url = 'https://www.moneycontrol.com/financials/{}/results/consolidated-yearly/{}'.format(ticker,ti)
    logging.info(f"Fetching data from URL: {url}")
    try:
        df = pd.read_html(requests.post(url).text)[0]
    except Exception as e:
        logging.error(f"Error fetching data for {ticker}: {str(e)}")
        df = pd.read_html(requests.post(url).text)[0]

    return df


def inc_statement_alternate(ticker, ti):
    url = 'https://www.moneycontrol.com/financials/{}/results/yearly/{}'.format(ticker,ti)
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


def run_stock_performance(config):
    fin = []
    for i in range(len( config["tickers"])):
        try:
            if config["tickers"][i] in config["ticker_alternate"]:
                df = inc_statement_alternate(config["tickers"][i], config["ti"][i])
                df["Stock"] = config["tickers"][i]
                fin.append(df)

            else:
                df = inc_statement(config["tickers"][i], config["ti"][i])
                df["Stock"] = config["tickers"][i]
                fin.append(df)
        except Exception as e:
            logging.error(f"Error processing {config['tickers'][i]}: {str(e)}")

    incs = pd.concat(fin)
    logging.info("Stock performance data fetched successfully")

    return incs

# def run_stock_performance(config):
#     fin = []
#     missing_inc = []
#     for i in range(len(config["tickers"])):
#         try:
#             if config["tickers"][i] in config["ticker_alternate"]:
#
#                 df = inc_statement_alternate(config["tickers"][i], config["ti"][i])
#                 df["Stock"] = config["tickers"][i]
#                 fin.append(df)
#             else:
#                 df = inc_statement(config["tickers"][i], config["ti"][i])
#                 df["Stock"] = config["tickers"][i]
#                 fin.append(df)
#         except:
#             missing_inc.append(i)
#
#     for i in missing_inc:
#         if config["tickers"][i] in config["ticker_alternate"]:
#
#             df = inc_statement_alternate( config["tickers"][i], config["ti"][i])
#             df["Stock"] = config["tickers"][i]
#             fin.append(df)
#         else:
#             df = inc_statement(config["tickers"][i], config["ti"][i])
#             df["Stock"] = config["tickers"][i]
#             fin.append(df)
#
#     incs = pd.concat(fin)
#     return incs

