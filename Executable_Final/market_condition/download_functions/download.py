from download_functions.dwnld_functions import market_data, VIX
import pandas as pd
# from config import config

def daily_data(mkt_symb,start_time, end_time):

    res = market_data(mkt_symb,"daily",start_time, end_time)
    vx = VIX("daily",start_time, end_time)
    fin = pd.merge(vx, res, on='Date')
    return fin, res, vx

def minute_data(mkt_symb,start_time, end_time):

    res = market_data(mkt_symb,"minute",start_time, end_time)
    vx = VIX("minute",start_time, end_time)
    fin = pd.merge(vx, res, on=['Date','Time'])
    return fin, res, vx

