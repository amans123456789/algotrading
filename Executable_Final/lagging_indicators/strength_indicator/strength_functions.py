import pandas as pd


def classify_strength(value):
    if 0 <= value < 25:
        return "Absent or Weak Trend"
    elif 25 <= value < 50:
        return "Strong Trend"
    elif 50 <= value < 75:
        return "Very Strong Trend"
    elif 75 <= value <= 100:
        return "Extremely Strong Trend"
    else:
        return "Invalid Value"  # Handle values outside the specified range


### RSI
def rsi_strength(df, upper_limit, lower_limit):
    ls = [
        "Overbought" if rsi > upper_limit else "Oversold" if rsi < lower_limit else " "
        for rsi in df.rsi
    ]
    return ls


def bollinger_strength(data):
    ls = []

    n = len(data)

    for i in range(n):
        if pd.notna(data["Open"].iloc[i]) and pd.notna(data["UB"].iloc[i]):
            if data["Open"].iloc[i] > data["UB"].iloc[i]:
                ls.append("Overbought")
            elif data["Open"].iloc[i] < data["LB"].iloc[i]:
                ls.append("Oversold")
            else:
                ls.append("")
        else:
            ls.append("")

    return ls


def adx_strength(df):
    ls = df["adx"].apply(classify_strength)
    return ls
