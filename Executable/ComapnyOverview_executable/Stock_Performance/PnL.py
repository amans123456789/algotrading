import pandas as pd
import requests
import Stock_List


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

def run_stock_performance(tickers):
    fin = []
    missing_pnl = []
    for i in range(len(tickers)):
        try:
            if tickers[i] in Stock_List.ticker_alternate:
                df = pd.DataFrame()
                df = PnL_alternate(tickers[i], Stock_List.ti[i])
                df["Stock"] = tickers[i]
                fin.append(df)
            else:

                df = pd.DataFrame()
                df = PnL(tickers[i], Stock_List.ti[i])
                df["Stock"] = tickers[i]
                fin.append(df)
        except:
            missing_pnl.append(i)

    for i in missing_pnl:
        if tickers[i] in Stock_List.ticker_alternate:
            df = pd.DataFrame()
            df = PnL_alternate(tickers[i], Stock_List.ti[i])
            df["Stock"] = tickers[i]
            fin.append(df)
        else:

            df = pd.DataFrame()
            df = PnL(tickers[i], Stock_List.ti[i])
            df["Stock"] = tickers[i]
            fin.append(df)

    pl = pd.concat(fin)
    return pl