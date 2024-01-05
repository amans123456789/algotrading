import pandas as pd
import logging
import requests
from config import config

logging.basicConfig(level=logging.INFO)


def PnL(ticker, ti):

    url = 'https://www.moneycontrol.com/financials/{}/consolidated-profit-lossVI/{}'.format(ticker, ti)
    logging.info(f"Fetching data from URL: {url}")

    # df = pd.read_html(requests.post(url).text)[0]
    try:
        df = pd.read_html(requests.post(url).text)[0]
    except Exception as e:
        logging.error(f"Error fetching data for {ticker}: {str(e)}")
        # Retry or handle the error as needed
        # For simplicity, we retry once
        df = pd.read_html(requests.post(url).text)[0]

    return df


def PnL_alternate(ticker, ti):

    url = 'https://www.moneycontrol.com/financials/{}/profit-lossVI/{}'.format(ticker, ti)
    logging.info(f"Fetching data from URL: {url}")
    # df = pd.read_html(requests.post(url).text)[0]
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
                df = PnL_alternate(config["tickers"][i], config["ti"][i])
                df["Stock"] = config["tickers"][i]
                fin.append(df)

            else:
                df = PnL(config["tickers"][i], config["ti"][i])
                df["Stock"] = config["tickers"][i]
                fin.append(df)
        except Exception as e:
            logging.error(f"Error processing {config['tickers'][i]}: {str(e)}")

    pl = pd.concat(fin)
    logging.info("Stock performance data fetched successfully")

    return pl
    # fin = []
    # missing_pnl = []
    # for i in range(len(config["tickers"])):
    #     try:
    #         if config["tickers"][i] in config["ticker_alternate"]:
    #             df = PnL_alternate(config["tickers"][i], config["ti"][i])
    #             df["Stock"] = config["tickers"][i]
    #             fin.append(df)
    #         else:
    #             df = PnL(config["tickers"][i], config["ti"][i])
    #             df["Stock"] = config["tickers"][i]
    #             fin.append(df)
    #     except:
    #         missing_pnl.append(i)
    #
    # for i in missing_pnl:
    #     if config["tickers"][i] in config["ticker_alternate"]:
    #         df = PnL_alternate(config["tickers"][i], config["ti"][i])
    #         df["Stock"] = config["tickers"][i]
    #         fin.append(df)
    #     else:
    #         df = PnL(config["tickers"][i], config["ti"][i])
    #         df["Stock"] = config["tickers"][i]
    #         fin.append(df)
    #
    # pl = pd.concat(fin)
    # return pl