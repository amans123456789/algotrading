
import pandas as pd
from postprocessing import combine_col, stock_df_creation

cfs = pd.read_csv("starting_data/annual_data/cash_flow.csv")
bs = pd.read_csv("starting_data/annual_data/balance_sheet.csv")
gp = pd.read_csv("starting_data/annual_data/general_performance.csv")
ins = pd.read_csv("starting_data/annual_data/income_statement.csv")
pnl = pd.read_csv("starting_data/annual_data/pnl.csv")

financial_fin = combine_col(bs, cfs, ins, pnl)
stock_list = financial_fin["Stock"].unique()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fin = pd.DataFrame()
    missing = []
    for i in stock_list:
        print(i)
        try:
            res = stock_df_creation(financial_fin, i, "23")
            fin = pd.concat([fin, res])
        except:
            missing.append(i)
    print(fin)

