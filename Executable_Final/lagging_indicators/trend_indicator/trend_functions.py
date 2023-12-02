import pandas as pd
import yfinance as yf
import numpy as np

hourly_data = pd.read_csv("./time_series_data/trend_indicator_data/st_one_min.csv")
daily_data = pd.read_csv("./time_series_data/trend_indicator_data/st_daily.csv")

### Signals : created_feature, rolling_mean, rsi, bollinger,  macd,atr, adx, vix, stochastic_oscillator, fibonacci_levels

# def check_last_n_values(arr, n):
#     if len(arr) >= n and all(arr[-n:] ==1):
#         return 1
#     elif len(arr) >= n  and all(arr[-n:] ==-1):
#         return -1
#     return 0


### Market features - Sensex , Vix etc
def feature_creation(merge_fin):
    merge_fin["Sensex_Jump"] = merge_fin["Sensex Open"] / merge_fin["Sensex Past Open"]

    return merge_fin


### Rolling Mean Indicator
def rolling_mean_trend(df, short_term, long_term):
    # df = df.copy()
    # df = df[df["Stock"] == i]
    st = df[short_term]
    lt = df[long_term]
    df.loc[st > lt, "RM Signal"] = "Bullish"
    df.loc[lt > st, "RM Signal"] = "Bearish"

    # df["Bearish Trend Rolling Mean"] = (df[short_term] < df[long_term]).astype(int)
    # df["Bullish Trend Rolling Mean"] = (df[short_term] > df[long_term]).astype(int)

    return df["RM Signal"]






    # df["Bullish_Bollinger"] = (df["Open"] > df["UB"]).astype(int)
    # df["Bearish_Bollinger"] = (df["Open"] < df["LB"]).astype(int)

    # return df


def macd_trend(df):
    ls = []
    # df = df[df["Stock"] == stock]
    # df = df.copy()

    n = len(df)

    for i in range(1, n):
        if (
            df["macd"].iloc[i] > df["signal"].iloc[i]
            and df["macd"].iloc[i - 1] <= df["signal"].iloc[i - 1]
        ):
            ls.append("Bullish")
        elif (
            df["macd"].iloc[i] < df["signal"].iloc[i]
            and df["macd"].iloc[i - 1] >= df["signal"].iloc[i - 1]
        ):
            ls.append("Bearish")
        else:
            ls.append("Hold")
    ls = ["Hold"] + ls
    return ls


def atr_trend(df,  multiplier):
    # df = df[df["Stock"] == stock]
    # df = df.copy()

    df["ATR_Signal"] = "Hold"
    df.loc[
        df["Close"] - df["Open"] > multiplier * df["ATR"], "ATR_Signal"
    ] = "Bullish"  # Bullish signal
    df.loc[
        df["Open"] - df["Close"] > multiplier * df["ATR"], "ATR_Signal"
    ] = "Bearish"  # Bearish signal

    return df["ATR_Signal"]


def adx_trend(df, adx_threshold):
    # df = df[df["Stock"] == stock]
    # df = df.copy()

    df["ADX_Signal"] = "Hold"

    df["ADX_Signal"] = np.where(
        (df["di+"] > df["di-"])
        # & ((df["adx"] > df["adx"].shift(1))
           & (df["adx"] > adx_threshold)
        # )\
        ,
        "Bullish Trend",
        np.where(
            (df["di-"] > df["di+"])
            # & ((df["adx"] > df["adx"].shift(1))
               & (df["adx"] > adx_threshold)
            # )
            ,
            "Bearish Trend",
            "Hold",
        ),
    )
    return df["ADX_Signal"]


def stochastic_trend(df,  overbought_threshold, oversold_threshold):
    # df = df[df["Stock"] == stock]
    # df = df.copy()

    df["Stochastic_Signal"] = "Hold"
    # Bullish Signal: %K crosses above %D, and %K is below overbought threshold
    df.loc[
        (df["%K"] > df["%D"]) & (df["%K"] < overbought_threshold), "Stochastic_Signal"
    ] = "Bullish"

    # Bearish Signal: %K crosses below %D, and %K is above oversold threshold
    df.loc[
        (df["%K"] < df["%D"]) & (df["%K"] > oversold_threshold), "Stochastic_Signal"
    ] = "Bearish"

    return df["Stochastic_Signal"]
