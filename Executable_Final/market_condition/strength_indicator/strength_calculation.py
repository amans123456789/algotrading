import pandas as pd
import strength_indicator.strength_functions as sf


def strength_calculation(df, upper_limit, lower_limit):
    st = pd.DataFrame()
    df["RSI_Strength"] = sf.rsi_strength(df, upper_limit, lower_limit)
    df["Bollinger_Strength"] = sf.bollinger_strength(df)
    df["ADX_Strength"] = sf.adx_strength(df)

    st = pd.concat([st, df])

    return st
