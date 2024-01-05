import pandas as pd
import requests
import logging
from config import config

logging.basicConfig(level=logging.INFO)

def stock_overview(sector, ticker, ti):
    url = 'https://www.moneycontrol.com/india/stockpricequote/{}/{}/{}'.format(sector[ticker], ticker, ti)
    logging.info(f"Fetching data from URL: {url}")

    all_dfs = []

    for i in range(2, 8):
        try:
            df = pd.read_html(requests.post(url).text)[i]
            all_dfs.append(df)
        except Exception as e:
            logging.error(f"Error fetching data for {ticker}: {str(e)}")
            logging.info(f"Fetching data again")
            df = pd.read_html(requests.post(url).text)[i]
            all_dfs.append(df)

    df_out = pd.concat(all_dfs)
    df_out.columns = ["Value", "Num"]

    return df_out


def run_stock_performance(config):
    fin = []
    for i in range(len( config["tickers"])):
        try:

            df = stock_overview(config["sector"], config["tickers"][i], config["ti"][i])
            df["Stock"] = config["tickers"][i]
            fin.append(df)
        except Exception as e:
            logging.error(f"Error processing {config['tickers'][i]}: {str(e)}")

    gen_stock = pd.concat(fin)
    logging.info("Stock performance data fetched successfully")

    return gen_stock


# def run_stock_performance(config):
#     fin = []
#     missing = []
#     for i in range(len(config["tickers"])):
#         try:
#             df = stock_overview(config["sector"], config["tickers"][i], config["ti"][i])
#             df["Stock"] = config["tickers"][i]
#             fin.append(df)
#         except:
#             # print("missed")
#             missing.append(config["tickers"][i])
#
#     for i in missing:
#         pos = config["tickers"].index(i)
#         df = stock_overview(config["sector"], config["tickers"][pos], config["ti"][pos])
#         df["Stock"] = config["tickers"][pos]
#         fin.append(df)
#
#     gen_stock = pd.concat(fin)
#
#     return gen_stock