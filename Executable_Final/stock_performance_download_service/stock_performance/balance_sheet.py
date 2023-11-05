import pandas as pd
import requests
from config import config

def balance_sheet(ticker, ti):

    url = 'https://www.moneycontrol.com/financials/{}/consolidated-balance-sheetVI/{}'.format(ticker, ti)
    print(url)

    df = pd.read_html(requests.post(url).text)[0]

    return df


def balance_sheet_alternate(ticker, ti):

    url = 'https://www.moneycontrol.com/financials/{}/balance-sheetVI/{}'.format(ticker, ti)
    print(url)

    df = pd.read_html(requests.post(url).text)[0]

    return df

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
    return bs