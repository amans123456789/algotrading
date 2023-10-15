import pandas as pd
import numpy as np
from Stock_Performance import Stock_Performance_Postprocessing as sp


bs = pd.read_csv("./Stock_Performance_Document/balance_sheet.csv")
cfs = pd.read_csv("./Stock_Performance_Document/cash_flow.csv")
gen_stock = pd.read_csv("./Stock_Performance_Document/general_performance.csv")
incs = pd.read_csv("./Stock_Performance_Document/income_statement.csv")
pl = pd.read_csv("./Stock_Performance_Document/pnl.csv")


def gen_stock_flat(gen_stock,i):
#     for i in gen_stock["Stock"].unique():
#     gen_stock_selected = gen_stock[gen_stock["Stock"] == i]
#     gen_stock_selected = gen_stock_selected.drop(["Stock","Unnamed: 0"], axis = 1)
#     gen_stock_selected_transpose = gen_stock_selected.T
#
#     gen_stock_selected_transpose.columns = gen_stock_selected_transpose.iloc[0]
#     gen_stock_selected_transpose = gen_stock_selected_transpose[1:]
#
#     gen_stock_selected_transpose["Stock"] = i
#     gen_stock_selected_transpose = gen_stock_selected_transpose.reset_index(drop= True)
#
#     gen_stock_selected_transpose = gen_stock_selected_transpose[["Stock","Dividend Yield", "Mkt Cap (Rs. Cr.)","TTM EPS See historical trend","Open"]]
#         print(gen_stock_selected_transpose.shape)
    gen_stock_selected_transpose = pd.DataFrame()
    gen_stock_selected = gen_stock[gen_stock["Stock"] == i]
    # ["Stock","Dividend Yield", "Mkt Cap (Rs. Cr.)","TTM EPS See historical trend","Open"]
    gen_stock_selected_transpose["Dividend Yield"] = gen_stock_selected[gen_stock_selected["Value"] == "Dividend Yield"]["Num"].values
    gen_stock_selected_transpose["Mkt Cap (Rs. Cr.)"] = gen_stock_selected[gen_stock_selected["Value"] == "Mkt Cap (Rs. Cr.)"]["Num"].values
    gen_stock_selected_transpose["TTM EPS See historical trend"] = gen_stock_selected[gen_stock_selected["Value"] == "TTM EPS See historical trend"][
        "Num"].values
    gen_stock_selected_transpose["Open"] = gen_stock_selected[gen_stock_selected["Value"] == "Open"]["Num"].values[0]
    gen_stock_selected_transpose["Stock"] = i

    return gen_stock_selected_transpose

def minority_interet_other_income_extraction(s):
    try:
        if isinstance(s, str):
            return s
        else:
            return s[0]
    except:
        return np.nan


def metric_creation(bs,cfs, incs,pl):
    stock_list, financial_fin = sp.cleaning_func(bs, pl, cfs, incs)
    fin, missing = sp.final_dataframe(stock_list, financial_fin)

    fin = fin.reset_index(drop=True)

    fin["Total Current Assets"] = pd.to_numeric(fin["Total Current Assets"].values, errors='coerce')
    fin["Cash And Cash Equivalents"] = pd.to_numeric(fin["Cash And Cash Equivalents"].values, errors='coerce')
    fin["Current Investments"] = pd.to_numeric(fin["Current Investments"].values, errors='coerce')

    fin["Total Current Liabilities"] = pd.to_numeric(fin["Total Current Liabilities"].values, errors='coerce')

    fin["Short Term Borrowings"] = pd.to_numeric(fin["Short Term Borrowings"].values, errors='coerce')

    fin["Total Shareholders Funds"] = pd.to_numeric(fin["Total Shareholders Funds"].values, errors='coerce')

    fin["Profit/Loss Before Exceptional, ExtraOrdinary Items And Tax"] = pd.to_numeric(
        fin["Profit/Loss Before Exceptional, ExtraOrdinary Items And Tax"].values, errors='coerce')
    fin["Finance Costs"] = pd.to_numeric(fin["Finance Costs"].values, errors='coerce')

    fin["Total Shareholders Funds"] = pd.to_numeric(fin["Total Shareholders Funds"].values, errors='coerce')
    fin["Short Term Borrowings"] = pd.to_numeric(fin["Short Term Borrowings"].values, errors='coerce')

    fin["Long Term Borrowings"] = pd.to_numeric(fin["Long Term Borrowings"].values, errors='coerce')
    fin["Cash And Cash Equivalents"] = pd.to_numeric(fin["Cash And Cash Equivalents"].values, errors='coerce')

    fin["Current Assets"] = fin["Total Current Assets"] - fin["Cash And Cash Equivalents"] - fin["Current Investments"]
    fin["Current Liabilities"] = fin["Total Current Liabilities"] - fin["Short Term Borrowings"]
    fin["Working Capital"] = fin["Current Assets"] - fin["Current Liabilities"]

    # fin = fin.dropna()

    fin['Minority Interest Balance Sheet'] = fin['Minority Interest'].apply(minority_interet_other_income_extraction)
    fin["Other Income PnL"] = fin['Other Income'].apply(minority_interet_other_income_extraction)

    # fin = fin[fin['Minority Interest'].str.strip() != '']
    #
    # fin = fin.reset_index(drop=True)

    # fin['Minority Interest Balance Sheet'] = ""
    # for i in range(fin.shape[0]):
    #     fin['Minority Interest Balance Sheet'][i] = fin['Minority Interest'][i][0]
    #
    # fin['Other Income PnL'] = -1
    # for i in range(fin.shape[0]):
    #     try:
    #         fin['Other Income PnL'][i] = fin['Other Income'][i].values[0]
    #     except:
    #         fin['Other Income PnL'][i] = fin['Other Income'][i]
    ####################################################################################################################
    # fin['Minority Interest Balance Sheet'] = -1
    # fin['Other Income PnL'] = -1

    ####################################################################################################################


    fin["EBIT"] = fin["Profit/Loss Before Exceptional, ExtraOrdinary Items And Tax"].astype("float") + \
                       fin["Finance Costs"].astype("float") - fin["Other Income PnL"].astype("float")

    fin["ROC"] = fin["EBIT"].astype("float") / (
                fin["Total Shareholders Funds"].astype("float") + fin["Short Term Borrowings"].astype(
            "float") + fin["Long Term Borrowings"].astype("float") - fin["Cash And Cash Equivalents"].astype(
            "float"))

    return fin

def gen_stock_metric(gen_stock, bs, cfs, incs, pl):

    gen_stock[gen_stock["Value"] == "TTM EPS See historical trend"]
    fin = metric_creation(bs, cfs, incs, pl)
    gen_fin = pd.DataFrame()

    for i in gen_stock.Stock.unique():
        tab = gen_stock_flat(gen_stock, i)
        gen_fin = pd.concat([gen_fin, tab], ignore_index=True)

    merged = gen_fin.merge(fin, on=["Stock"])

    merged["Current_Ratio"] = merged["Current Assets"] / merged["Current Liabilities"]
    merged["Inventories"] = pd.to_numeric(merged["Inventories"])
    merged["Quick_Ratio"] = (merged["Current Assets"] - merged["Inventories"]) / merged["Current Liabilities"]
    merged["BookToMkt"] = merged["Total Shareholders Funds"].astype("float") / merged["Mkt Cap (Rs. Cr.)"].astype(
        "float")
    merged["Net Debt"] = fin["Long Term Borrowings"].astype("float") - fin["Cash And Cash Equivalents"].astype("float")
    merged["TEV"] = merged["Mkt Cap (Rs. Cr.)"].astype("float") + merged["Net Debt"].astype("float") +\
                    pd.to_numeric(merged["Minority Interest Balance Sheet"], errors='coerce')

    merged["EarningYield"] = merged["EBIT"].astype('float') / merged["TEV"].astype('float')


    return merged




