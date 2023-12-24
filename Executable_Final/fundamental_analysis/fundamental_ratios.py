import pandas as pd

def fundamental_analysis(fin):
    fin["Total Current Assets"] = pd.to_numeric(fin["Total Current Assets"].values, errors='coerce')
    fin["Cash And Cash Equivalents"] = pd.to_numeric(fin["Cash And Cash Equivalents"].values, errors='coerce')
    fin["Current Investments"] = pd.to_numeric(fin["Current Investments"].values, errors='coerce')
    fin["Total Current Liabilities"] = pd.to_numeric(fin["Total Current Liabilities"].values, errors='coerce')
    fin["Short Term Borrowings"] = pd.to_numeric(fin["Short Term Borrowings"].values, errors='coerce')
    fin["Total Shareholders Funds"] = pd.to_numeric(fin["Total Shareholders Funds"].values, errors='coerce')

    fin["Profit/Loss Before Exceptional, ExtraOrdinary Items And Tax"] = pd.to_numeric(fin["Profit/Loss Before Exceptional, ExtraOrdinary Items And Tax"].values, errors='coerce')
    fin["Finance Costs"] = pd.to_numeric(fin["Finance Costs"].values, errors='coerce')

    fin["Total Shareholders Funds"] = pd.to_numeric(fin["Total Shareholders Funds"].values, errors='coerce')
    fin["Short Term Borrowings"] = pd.to_numeric(fin["Short Term Borrowings"].values, errors='coerce')
    fin["Long Term Borrowings"] = pd.to_numeric(fin["Long Term Borrowings"].values, errors='coerce')
    fin["Cash And Cash Equivalents"] = pd.to_numeric(fin["Cash And Cash Equivalents"].values, errors='coerce')

    fin["Current Assets"] = fin["Total Current Assets"] - fin["Cash And Cash Equivalents"] - fin["Current Investments"]
    fin["Current Liabilities"] = fin["Total Current Liabilities"] - fin["Short Term Borrowings"]
    fin["Working Capital"] = fin["Current Assets"] - fin["Current Liabilities"]


    # fin = fin.dropna()
    # fin_copy = fin_copy[fin_copy['Minority Interest'].str.strip() != '']

    fin['Minority Interest Balance Sheet'] = ""
    for i in range(fin.shape[0]):
        try:
            fin['Minority Interest Balance Sheet'][i] = fin['Minority Interest'][i][0]
        except:
            fin['Minority Interest Balance Sheet'][i] = fin['Minority Interest Balance Sheet'][i]

    fin['Other Income PnL'] = ""
    for i in range(fin.shape[0]):
        try:
            fin['Other Income PnL'][i] = fin['Other Income'][i].values[0]
        except:
            fin['Other Income PnL'][i] = fin['Other Income'][i]


    fin["EBIT"] = fin["Profit/Loss Before Exceptional, ExtraOrdinary Items And Tax"].astype("float") + \
                       fin["Finance Costs"].astype("float") - fin["Other Income PnL"].astype("float")

    fin["ROC"] = fin["EBIT"].astype("float") / (
                fin["Total Shareholders Funds"].astype("float") + fin["Short Term Borrowings"].astype(
            "float") + fin["Long Term Borrowings"].astype("float") - fin["Cash And Cash Equivalents"].astype(
            "float"))

    return fin

def earning_yield_func(merged):
    blank_flag = merged["Minority Interest Balance Sheet"].apply(lambda x: x == "")
    merged["Minority Interest Balance Sheet"] = merged["Minority Interest Balance Sheet"].replace('', 0)
    ls = merged["Mkt Cap (Rs. Cr.)"].astype("float") + merged["Net Debt"].astype("float") + merged["Minority Interest Balance Sheet"].astype("float")
    return ls , blank_flag


def merged_file_analysis(merged):
    merged["BookToMkt"] = merged["Total Shareholders Funds"].astype("float") / merged["Mkt Cap (Rs. Cr.)"].astype(
        "float")
    merged["Net Debt"] = merged["Long Term Borrowings"].astype("float") - merged["Cash And Cash Equivalents"].astype("float")
    merged["TEV"], merged["blank_flag"] = earning_yield_func(merged)


    merged["EarningYield"] =  merged["EBIT"].astype('float')/merged["TEV"].astype('float')

    merged["Current_Ratio"] = merged["Current Assets"] / merged["Current Liabilities"]
    merged["Inventories"] = pd.to_numeric(merged["Inventories"])
    merged["Quick_Ratio"] = (merged["Current Assets"] - merged["Inventories"]) / merged["Current Liabilities"]

    merged["Rank EarningYield"]  = merged["EarningYield"].rank(ascending=False,na_option='bottom')
    merged["Rank ROC"]  = merged["ROC"].rank(ascending=False,na_option='bottom')

    merged["CombRank"] = merged["Rank EarningYield"] + merged["Rank ROC"]
    merged["MagicFormulaRank"] = merged["CombRank"].rank(method='first')

    return merged


