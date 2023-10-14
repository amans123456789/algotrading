import pandas as pd
import requests
import Stock_List


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

def run_stock_performance(tickers):
    fin = []
    missing = []
    for i in range(len(tickers)):
        try:
            df = pd.DataFrame()
            df = stock_overview(Stock_List.sector, tickers[i], Stock_List.ti[i])
            df["Stock"] = tickers[i]
            fin.append(df)
        except:
            print("missed")
            missing.append(tickers[i])

    for i in missing:
        pos = tickers.index(i)
        df = pd.DataFrame()
        df = stock_overview(Stock_List.sector, tickers[pos], Stock_List.ti[pos])
        df["Stock"] = tickers[pos]
        fin.append(df)

    gen_stock = pd.concat(fin)

    return gen_stock