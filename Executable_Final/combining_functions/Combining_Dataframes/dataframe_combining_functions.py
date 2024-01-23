import config
import logging
import pandas as pd
from datetime import datetime, timedelta
from Combining_Dataframes.combine import  create_file_paths, read_csvs
logging.basicConfig(filename="data_processing.log", level=logging.INFO)

# ticker_mapping = {config["tickers_NS"][i]: config["tickers"][i] for i in range(len(config["tickers_NS"]))}
# ticker_mapping_2 = {config["ti"][i]: config["tickers_NS"][i] for i in range(len(config["tickers_NS"]))}

# date = "2024-01-14"
# fund_analysis_year = "2023"
# ratio_analysis_date = "2024-01-25"
# news_date = "2024-01-14"
# file_paths = create_file_paths(date, fund_analysis_year, ratio_analysis_date, news_date)

# res = (read_csvs(file_paths))

def df_combine(res,ticker_mapping, ticker_mapping_2 ):
    ### Combining market condition dataframes
    merged_mrkt = pd.merge(res["mark_cond_daily"], res["last_mark_cond_daily"][
        ["Date", "Fibonacci 23.599999999999998% Retracement Level", "Fibonacci 38.2% Retracement Level",
         "Fibonacci 50.0% Retracement Level", "Fibonacci 61.8% Retracement Level",
         "Fibonacci 78.60000000000001% Retracement Level"]], on=['Date'])
    # , how = 'outer'
    latest_date = merged_mrkt['Date'].max()
    merged_mrkt_fin = merged_mrkt[merged_mrkt['Date'] == latest_date]

    ### Combining lagging condition dataframes
    merged_lagging = pd.merge(res["lagging_ind_cond_daily"], res["last_lagging_ind_cond_daily"][
        ["Date", "Stock", "Fibonacci 23.599999999999998% Retracement Level", "Fibonacci 38.2% Retracement Level",
         "Fibonacci 50.0% Retracement Level", "Fibonacci 61.8% Retracement Level",
         "Fibonacci 78.60000000000001% Retracement Level"]], on=['Date', 'Stock'])
    latest_date = merged_lagging['Date'].max()
    merged_lagging_fin = merged_lagging[merged_lagging['Date'] == latest_date]

    ### Combining lagging condition dataframe and fundamental analysis dataframe
    merged_lagging_fin['mapped_tickers'] = merged_lagging_fin['Stock'].map(ticker_mapping)
    fund_analysis = res["fund_analysis"].drop(["Open"], axis=1)
    # Merge the two dataframes on the mapped_tickers column
    fund_lag = pd.merge(merged_lagging_fin, fund_analysis, left_on='mapped_tickers', right_on='Stock')
    # , how = "outer"

    # # Drop unnecessary columns if needed
    fund_lag = fund_lag.drop(['mapped_tickers'], axis=1)

    ### Ratio Analysis
    ratio_analysis = res["ratio_analysis"]
    ratio_analysis['mapped_tickers'] = ratio_analysis['Stock'].map(ticker_mapping_2)

    ### Merge fundamental analysis , lagging and call put dataframes
    fund_lag_cp = pd.merge(ratio_analysis[["Stock", "OI Call Put Ratio", "Volume Call Put Ratio", "mapped_tickers"]],
                           fund_lag, left_on='mapped_tickers', right_on='Stock_x')
    # , how = "outer"

    # # Drop unnecessary columns if needed
    fund_lag_cp = fund_lag_cp.drop(['mapped_tickers'], axis=1)

    merged_mrkt_fin['Date'] = pd.to_datetime(merged_mrkt_fin['Date'])
    fund_lag_cp['Date'] = pd.to_datetime(fund_lag_cp['Date'])

    merged_mrkt_fin_sel = merged_mrkt_fin[['Vix Open', 'Vix High', 'Vix Low', 'Vix Close', 'Date','BSE Open', 'BSE AdjClose', 'Open Rolling Mean 50 days', 'Open Rolling Mean 200 days',
           'Open BSE Open Mean 10 days', 'Open Rolling Mean 40 days', 'rsi', 'MB',
           'UB', 'LB', 'TR', 'ATR', 'macd', 'signal', 'di+', 'di-', 'adx', '%K',
           '%D', 'RSI_Strength', 'Bollinger_Strength', 'ADX_Strength', 'RM Signal',
           'MACD_Signal', 'ATR_Signal', 'ADX_Signal', 'Stochastic_Signal',
           'Fibonacci 23.599999999999998% Retracement Level',
           'Fibonacci 38.2% Retracement Level',
           'Fibonacci 50.0% Retracement Level',
           'Fibonacci 61.8% Retracement Level',
           'Fibonacci 78.60000000000001% Retracement Level' ]]

    merged_mrkt_fin_sel.columns = ['Vix Open', 'Vix High', 'Vix Low', 'Vix Close', 'Date', 'BSE Open',
                                   'BSE AdjClose', 'BSE Open Rolling Mean 50 days',
                                   'BSE Open Rolling Mean 200 days', 'BSE Open BSE Open Mean 10 days',
                                   'BSE Open Rolling Mean 40 days', 'BSE rsi', 'BSE MB', 'BSE UB', 'BSE LB', 'BSE TR',
                                   'BSE ATR',
                                   'BSE macd', 'BSE signal', 'BSE di+', 'BSE di-', 'BSE adx', 'BSE %K', 'BSE %D',
                                   'BSE RSI_Strength',
                                   'BSE Bollinger_Strength', 'BSE ADX_Strength', 'BSE RM Signal', 'BSE MACD_Signal',
                                   'BSE ATR_Signal', 'BSE ADX_Signal', 'BSE Stochastic_Signal',
                                   'BSE Fibonacci 23.599999999999998% Retracement Level',
                                   'BSE Fibonacci 38.2% Retracement Level',
                                   'BSE Fibonacci 50.0% Retracement Level',
                                   'BSE Fibonacci 61.8% Retracement Level',
                                   'BSE Fibonacci 78.60000000000001% Retracement Level']
    fund_lag_cp_mrkt = pd.merge(fund_lag_cp, merged_mrkt_fin_sel, on='Date')

    return fund_lag_cp_mrkt




