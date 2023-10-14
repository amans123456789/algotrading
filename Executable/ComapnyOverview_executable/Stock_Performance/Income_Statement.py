import pandas as pd
import requests
import Stock_List

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

def run_stock_performance(tickers):
    fin = []
    missing_inc = []
    for i in range(len(tickers)):
        try:
            if tickers[i] in Stock_List.ticker_alternate:

                df = pd.DataFrame()
                df = inc_statement_alternate(tickers[i], Stock_List.ti[i])
                df["Stock"] = tickers[i]
                fin.append(df)
            else:
                df = pd.DataFrame()
                df = inc_statement(tickers[i], Stock_List.ti[i])
                df["Stock"] = tickers[i]
                fin.append(df)
        except:
            missing_inc.append(i)

    for i in missing_inc:
        if tickers[i] in Stock_List.ticker_alternate:

            df = pd.DataFrame()
            df = inc_statement_alternate(tickers[i], Stock_List.ti[i])
            df["Stock"] = tickers[i]
            fin.append(df)
        else:
            df = pd.DataFrame()
            df = inc_statement(tickers[i], Stock_List.ti[i])
            df["Stock"] = tickers[i]
            fin.append(df)

    incs = pd.concat(fin)
    return incs