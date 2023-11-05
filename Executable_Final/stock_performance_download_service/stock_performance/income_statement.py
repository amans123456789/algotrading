import pandas as pd
import requests
from config import config

def inc_statement(ticker, ti):

    url = 'https://www.moneycontrol.com/financials/{}/results/consolidated-yearly/{}'.format(ticker,ti)
    print(url)
    df = pd.read_html(requests.post(url).text)[0]

    return df

def inc_statement_alternate(ticker, ti):

    url = 'https://www.moneycontrol.com/financials/{}/results/yearly/{}'.format(ticker,ti)
    print(url)
    df = pd.read_html(requests.post(url).text)[0]

    return df

def run_stock_performance(config):
    fin = []
    missing_inc = []
    for i in range(len(config["tickers"])):
        try:
            if config["tickers"][i] in config["ticker_alternate"]:

                df = pd.DataFrame()
                df = inc_statement_alternate(config["tickers"][i], config["ti"][i])
                df["Stock"] = config["tickers"][i]
                fin.append(df)
            else:
                df = pd.DataFrame()
                df = inc_statement(config["tickers"][i], config["ti"][i])
                df["Stock"] = config["tickers"][i]
                fin.append(df)
        except:
            missing_inc.append(i)

    for i in missing_inc:
        if config["tickers"][i] in config["ticker_alternate"]:

            df = inc_statement_alternate( config["tickers"][i], config["ti"][i])
            df["Stock"] = config["tickers"][i]
            fin.append(df)
        else:
            df = inc_statement(config["tickers"][i], config["ti"][i])
            df["Stock"] = config["tickers"][i]
            fin.append(df)

    incs = pd.concat(fin)
    return incs