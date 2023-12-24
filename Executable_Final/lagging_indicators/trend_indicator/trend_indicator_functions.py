import numpy as np


### Market features - Sensex , Vix etc
def feature_creation(merge_fin):
    merge_fin["Sensex_Jump"] = merge_fin["Sensex Open"] / merge_fin["Sensex Past Open"]

    return merge_fin


### Rolling Mean Indicator
def rolling_mean_trend(df, short_term, long_term):
    st = df[short_term]
    lt = df[long_term]
    df.loc[st > lt, "RM Signal"] = "Bullish"
    df.loc[lt > st, "RM Signal"] = "Bearish"

    return df["RM Signal"]


def macd_trend(df):
    ls = []
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


def atr_trend(df, multiplier):
    df["ATR_Signal"] = "Hold"
    df.loc[
        df["Close"] - df["Open"] > multiplier * df["ATR"], "ATR_Signal"
    ] = "Bullish"  # Bullish signal
    df.loc[
        df["Open"] - df["Close"] > multiplier * df["ATR"], "ATR_Signal"
    ] = "Bearish"  # Bearish signal

    return df["ATR_Signal"]


def adx_trend(df, adx_threshold):
    df["ADX_Signal"] = "Hold"

    df["ADX_Signal"] = np.where(
        (df["di+"] > df["di-"]) & (df["adx"] > adx_threshold),
        "Bullish Trend",
        np.where(
            (df["di-"] > df["di+"]) & (df["adx"] > adx_threshold),
            "Bearish Trend",
            "Hold",
        ),
    )
    return df["ADX_Signal"]


def stochastic_trend(df, overbought_threshold, oversold_threshold):
    df["Stochastic_Signal"] = "Hold"
    df.loc[
        (df["%K"] > df["%D"]) & (df["%K"] < overbought_threshold), "Stochastic_Signal"
    ] = "Bullish"

    df.loc[
        (df["%K"] < df["%D"]) & (df["%K"] > oversold_threshold), "Stochastic_Signal"
    ] = "Bearish"

    return df["Stochastic_Signal"]
