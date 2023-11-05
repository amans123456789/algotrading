import pandas as pd
import requests
from config import config


def PnL(ticker, ti):

    url = 'https://www.moneycontrol.com/financials/{}/consolidated-profit-lossVI/{}'.format(ticker, ti)
    print(url)
    df = pd.read_html(requests.post(url).text)[0]

    return df


def PnL_alternate(ticker, ti):

    url = 'https://www.moneycontrol.com/financials/{}/profit-lossVI/{}'.format(ticker, ti)
    print(url)
    df = pd.read_html(requests.post(url).text)[0]

    return df

def run_stock_performance(config):
    fin = []
    missing_pnl = []
    for i in range(len(config["tickers"])):
        try:
            if config["tickers"][i] in config["ticker_alternate"]:
                df = PnL_alternate(config["tickers"][i], config["ti"][i])
                df["Stock"] = config["tickers"][i]
                fin.append(df)
            else:
                df = PnL(config["tickers"][i], config["ti"][i])
                df["Stock"] = config["tickers"][i]
                fin.append(df)
        except:
            missing_pnl.append(i)

    for i in missing_pnl:
        if config["tickers"][i] in config["ticker_alternate"]:
            df = PnL_alternate(config["tickers"][i], config["ti"][i])
            df["Stock"] = config["tickers"][i]
            fin.append(df)
        else:
            df = PnL(config["tickers"][i], config["ti"][i])
            df["Stock"] = config["tickers"][i]
            fin.append(df)

    pl = pd.concat(fin)
    return pl