import pandas as pd
import numpy as np


def rsi(DF, n=14):
    "function to calculate RSI"
    df = DF.copy()
    df["change"] = df["BSE AdjClose"] - df["BSE AdjClose"].shift(1)
    df["gain"] = np.where(df["change"] >= 0, df["change"], 0)
    df["loss"] = np.where(df["change"] < 0, -1 * df["change"], 0)
    df["avgGain"] = df["gain"].ewm(alpha=1 / n, min_periods=n).mean()
    df["avgLoss"] = df["loss"].ewm(alpha=1 / n, min_periods=n).mean()
    df["rs"] = df["avgGain"] / df["avgLoss"]
    df["rsi"] = 100 - (100 / (1 + df["rs"]))
    df = df.drop(["change", "gain", "loss", "avgGain", "avgLoss", "rs"], axis=1)
    return df


def moving_average(df):
    df["Open Rolling Mean 50 days"] = (
        df["BSE Open"].rolling(50).mean().reset_index(level=0, drop=True)
    )
    df["Open Rolling Mean 200 days"] = (
        df["BSE Open"].rolling(200).mean().reset_index(level=0, drop=True)
    )

    df["Open BSE Open Mean 10 days"] = (
        df["BSE Open"].rolling(10).mean().reset_index(level=0, drop=True)
    )
    df["Open Rolling Mean 40 days"] = (
        df["BSE Open"].rolling(40).mean().reset_index(level=0, drop=True)
    )

    return df


def boll_band(DF, n=14):
    "function to calculate Bollinger Band"
    df = DF.copy()

    df["MB"] = df["BSE AdjClose"].rolling(n).mean()
    df["UB"] = df["MB"] + 2 * df["BSE AdjClose"].rolling(n).std(ddof=0)
    df["LB"] = df["MB"] - 2 * df["BSE AdjClose"].rolling(n).std(ddof=0)

    return df


def atr(DF, n=14):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df["H-L"] = df["BSE High"] - df["BSE Low"]
    df["H-PC"] = abs(df["BSE High"] - df["BSE AdjClose"].shift(1))
    df["L-PC"] = abs(df["BSE Low"] - df["BSE AdjClose"].shift(1))
    df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1, skipna=False)
    df["ATR"] = df["TR"].ewm(com=n, min_periods=n).mean()
    df = df.drop(["H-L", "H-PC", "L-PC"], axis=1)
    return df


def macd(DF, a=12, b=26, c=9):
    """function to calculate MACD
    typical values a(fast moving average) = 12;
                   b(slow moving average) =26;
                   c(signal line ma window) =9"""
    df = DF.copy()
    df["ma_fast"] = df["BSE AdjClose"].ewm(span=a, min_periods=a).mean()
    df["ma_slow"] = df["BSE AdjClose"].ewm(span=b, min_periods=b).mean()
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signal"] = df["macd"].ewm(span=c, min_periods=c).mean()
    df = df.drop(["ma_fast", "ma_slow"], axis=1)

    return df


def adx(DF, n=20):
    "function to calculate ADX"
    df = DF.copy()
    df["upmove"] = df["BSE High"] - df["BSE High"].shift(1)
    df["downmove"] = df["BSE Low"].shift(1) - df["BSE Low"]
    df["+dm"] = np.where(
        (df["upmove"] > df["downmove"]) & (df["upmove"] > 0), df["upmove"], 0
    )
    df["-dm"] = np.where(
        (df["downmove"] > df["upmove"]) & (df["downmove"] > 0), df["downmove"], 0
    )
    df["di+"] = 100 * (df["+dm"] / df["ATR"]).ewm(alpha=1 / n, min_periods=n).mean()
    df["di-"] = 100 * (df["-dm"] / df["ATR"]).ewm(alpha=1 / n, min_periods=n).mean()
    df["adx"] = (
        100
        * abs((df["di+"] - df["di-"]) / (df["di+"] + df["di-"]))
        .ewm(alpha=1 / n, min_periods=n)
        .mean()
    )
    df = df.drop(["upmove", "downmove", "+dm", "-dm"], axis=1)
    return df


def calculate_stochastic_oscillator(df, k_period=14, d_period=3):
    # Calculate %K

    df["Lowest_Low"] = df["BSE Low"].rolling(window=k_period).min()
    df["Highest_High"] = df["BSE High"].rolling(window=k_period).max()
    df["%K"] = (
        (df["BSE Close"] - df["Lowest_Low"]) / (df["Highest_High"] - df["Lowest_Low"])
    ) * 100

    # Calculate %D
    df["%D"] = df["%K"].rolling(window=d_period).mean()

    # Drop temporary columns
    df.drop(["Lowest_Low", "Highest_High"], axis=1, inplace=True)

    return df


def calculate_fibonacci_levels(df):
    fibonacci_levels = [0.236, 0.382, 0.5, 0.618, 0.786]
    retracement_df = pd.DataFrame()
    df = df.reset_index(drop=True)

    for index, row in df.iterrows():
        # Extract the high and low prices from the row
        high_point = row["BSE High"]
        low_point = row["BSE Low"]

        price_range = high_point - low_point
        retracement_levels = [
            low_point + level * price_range for level in fibonacci_levels
        ]
        retracement_row = pd.Series(
            retracement_levels,
            index=[
                f"Fibonacci {level * 100}% Retracement Level"
                for level in fibonacci_levels
            ],
        )
        retracement_df = pd.concat([retracement_df, retracement_row], axis=1)

    retracement_df = retracement_df.T
    retracement_df = retracement_df.reset_index(drop=True)

    result_df = pd.concat([df, retracement_df], axis=1)

    return result_df
