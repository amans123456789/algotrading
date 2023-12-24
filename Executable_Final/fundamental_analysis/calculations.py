from postprocessing import combine_col, stock_df_creation, calc, gen_stock_df
from fundamental_ratios import fundamental_analysis, merged_file_analysis
import pandas as pd


def fin_cal(year="23"):
    cfs = pd.read_csv("starting_data/annual_data/cash_flow.csv")
    bs = pd.read_csv("starting_data/annual_data/balance_sheet.csv")
    gp = pd.read_csv("starting_data/annual_data/general_performance.csv")
    ins = pd.read_csv("starting_data/annual_data/income_statement.csv")
    pnl = pd.read_csv("starting_data/annual_data/pnl.csv")


    financial_fin = combine_col(bs, cfs, ins, pnl)
    stock_list = financial_fin["Stock"].unique()
    res = calc(financial_fin, stock_list, year)

    fin = fundamental_analysis(res)
    gen = gen_stock_df(stock_list, gp)
    merged = gen.merge(fin, on = ["Stock"])

    df = merged_file_analysis(merged)

    df.to_csv("./starting_data/results/fin_analysis.csv")

#


