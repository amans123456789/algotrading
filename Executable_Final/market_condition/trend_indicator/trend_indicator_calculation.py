import trend_indicator.trend_indicator_functions as tf
import pandas as pd


def trend_calculation(df):
    st = pd.DataFrame()
    tf.rolling_mean_trend(
        df, "Open Rolling Mean 50 days", "Open Rolling Mean 200 days"
    )
    df["MACD_Signal"] = tf.macd_trend(df)
    tf.atr_trend(df, multiplier=1.5)
    tf.adx_trend(df, adx_threshold=25)
    tf.stochastic_trend(df, overbought_threshold=80, oversold_threshold=20)
    # num["RM_Trend"] = tf.rolling_mean_trend(num, "Open Rolling Mean 50 days", "Open Rolling Mean 200 days")
    # num["MACD_Trend"] = tf.macd_trend(num)
    # num["ATR_Trend"] = tf.atr_trend(num, multiplier=1.5)

    # num["ADX_Trend"] = tf.adx_trend(num,  adx_threshold=25)
    # num['Stochastic_Signal'] = tf.stochastic_trend(num, overbought_threshold=80, oversold_threshold=20)

    st = pd.concat([st, df])

    return st
