import pandas as pd
import requests
import Stock_List

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

def run_stock_performance(tickers):
    fin = []
    missing_inc = []
    for i in range(len(tickers)):
        try:
            if tickers[i] in Stock_List.ticker_alternate:

                df = pd.DataFrame()
                df = cash_flow_alternate(tickers[i], Stock_List.ti[i])
                df["Stock"] = tickers[i]
                fin.append(df)
            else:
                df = pd.DataFrame()
                df = cash_flow(tickers[i], Stock_List.ti[i])
                df["Stock"] = tickers[i]
                fin.append(df)
        except:
            missing_inc.append(i)

    for i in missing_inc:
        if tickers[i] in Stock_List.ticker_alternate:

            df = pd.DataFrame()
            df = cash_flow_alternate(tickers[i], Stock_List.ti[i])
            df["Stock"] = tickers[i]
            fin.append(df)
        else:
            df = pd.DataFrame()
            df = cash_flow(tickers[i], Stock_List.ti[i])
            df["Stock"] = tickers[i]
            fin.append(df)

    cfs = pd.concat(fin)
    return cfs
