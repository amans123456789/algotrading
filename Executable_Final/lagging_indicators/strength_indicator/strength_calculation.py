import pandas as pd
import strength_indicator.strength_functions as sf


def strength_calculation(df, upper_limit, lower_limit):
    st = pd.DataFrame()
    for i in df.Stock.unique():
        num = df[df["Stock"] == i]
        num["RSI_Strength"] = sf.rsi_strength(num, upper_limit, lower_limit)
        num["Bollinger_Strength"] = sf.bollinger_strength(num)
        num["ADX_Strength"] = sf.adx_strength(num)

        st = pd.concat([st, num])

    return st
