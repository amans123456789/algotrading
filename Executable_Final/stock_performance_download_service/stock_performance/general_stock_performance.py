import pandas as pd
import requests
from config import config


def stock_overview(sector, ticker, ti):

    url = 'https://www.moneycontrol.com/india/stockpricequote/{}/{}/{}'.format(sector[ticker], ticker, ti)
    print(url)

    all_dfs = []

    for i in range(2, 8):
        df = pd.read_html(requests.post(url).text)[i]
        all_dfs.append(df)

    df_out = pd.concat(all_dfs)
    df_out.columns = ["Value", "Num"]

    return df_out

def run_stock_performance(config):
    fin = []
    missing = []
    for i in range(len(config["tickers"])):
        try:
            df = stock_overview(config["sector"], config["tickers"][i], config["ti"][i])
            df["Stock"] = config["tickers"][i]
            fin.append(df)
        except:
            # print("missed")
            missing.append(config["tickers"][i])

    for i in missing:
        pos = config["tickers"].index(i)
        df = stock_overview(config["sector"], config["tickers"][pos], config["ti"][pos])
        df["Stock"] = config["tickers"][pos]
        fin.append(df)

    gen_stock = pd.concat(fin)

    return gen_stock