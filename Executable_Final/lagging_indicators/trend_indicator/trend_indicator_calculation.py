import trend_indicator.trend_indicator_functions as tf
import pandas as pd

hourly_data = pd.read_csv("./time_series_data/trend_indicator_data/st_one_min.csv")
daily_data = pd.read_csv("./time_series_data/trend_indicator_data/st_daily.csv")

def trend_calculation(df):
    st = pd.DataFrame()
    # df_ma = tc.moving_average(df)
    for i in df.Stock.unique():
        num = df[df["Stock"] == i]
        num["RM_Trend"] = tf.rolling_mean_trend(num, "Open Rolling Mean 50 days", "Open Rolling Mean 200 days")
        # num["RSI_Trend"] = tf.rsi_trend(num,  upper_limit=70, lower_limit=30)
        # num["Bollinger_Trend"] = tf.bollinger_trend(num)
        num["MACD_Trend"] = tf.macd_trend(num)
        num["ATR_Trend"] = tf.atr_trend(num, multiplier=1.5)

        num["ADX_Trend"] = tf.adx_trend(num,  adx_threshold=25)
        num['Stochastic_Signal'] = tf.stochastic_trend(num, overbought_threshold=80, oversold_threshold=20)

        st = pd.concat([st, num])

    return st

hourly_trend_calc = trend_calculation(hourly_data)
daily_trend_calc = trend_calculation(daily_data)
print(hourly_trend_calc)

# hourly_trend_calc.to_csv("time_series_data/trend_data/hourly_trend_calc.csv")
# daily_trend_calc.to_csv("time_series_data/trend_data/daily_trend_calc.csv")
