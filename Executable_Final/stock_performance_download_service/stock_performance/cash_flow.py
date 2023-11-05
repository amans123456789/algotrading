import pandas as pd
import requests
from config import config

def cash_flow(ticker, ti):

    url = 'https://www.moneycontrol.com/financials/{}/consolidated-cash-flowVI/{}'.format(ticker,ti)
    print(url)
    df = pd.read_html(requests.post(url).text)[0]

    return df

def cash_flow_alternate(ticker, ti):

    url = 'https://www.moneycontrol.com/financials/{}/cash-flowVI/{}'.format(ticker,ti)
    print(url)
    df = pd.read_html(requests.post(url).text)[0]

    return df

def run_stock_performance(config):
    fin = []
    missing_inc = []
    for i in range(len(config["tickers"])):
        try:
            if config["tickers"][i] in config["ticker_alternate"]:

                df = cash_flow_alternate(config["tickers"][i], config["ti"][i])
                df["Stock"] = config["tickers"][i]
                fin.append(df)
            else:
                df = cash_flow(config["tickers"][i], config["ti"][i])
                df["Stock"] = config["tickers"][i]
                fin.append(df)
        except:
            missing_inc.append(i)

    for i in missing_inc:
        if config["tickers"][i] in config["ticker_alternate"]:

            df = cash_flow_alternate(config["tickers"][i], config["ti"][i])
            df["Stock"] = config["tickers"][i]
            fin.append(df)
        else:
            df = cash_flow(config["tickers"][i], config["ti"][i])
            df["Stock"] = config["tickers"][i]
            fin.append(df)

    cfs = pd.concat(fin)
    return cfs

