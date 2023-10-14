import pandas as pd
import requests
import Stock_List

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

def run_stock_performance(tickers):
    fin = []
    for i in range(len(tickers)):
        if tickers[i] in Stock_List.ticker_alternate:
            df = pd.DataFrame()
            df = balance_sheet_alternate(tickers[i], Stock_List.ti[i])
            df["Stock"] = tickers[i]
            fin.append(df)

        else:
            df = pd.DataFrame()
            df = balance_sheet(tickers[i], Stock_List.ti[i])
            df["Stock"] = tickers[i]
            fin.append(df)

    bs = pd.concat(fin)
    return bs