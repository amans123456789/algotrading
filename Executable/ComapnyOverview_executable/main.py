import pandas as pd
from Stock_Performance import Stock_Performance_Metrics as sm

bs = pd.read_csv("Stock_Performance_Document/Stock_performance/balance_sheet.csv")
cfs = pd.read_csv("Stock_Performance_Document/Stock_performance/cash_flow.csv")
gen_stock = pd.read_csv("Stock_Performance_Document/Stock_performance/general_performance.csv")
incs = pd.read_csv("Stock_Performance_Document/Stock_performance/income_statement.csv")
pl = pd.read_csv("Stock_Performance_Document/Stock_performance/pnl.csv")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # stock_list, financial_fin = sp.cleaning_func(bs, pl, cfs, incs)
    # fin, missing = sp.final_dataframe(stock_list,financial_fin)
    # merged = sm.gen_stock_metric(gen_stock, bs, cfs, incs, pl)
    merged = sm.gen_stock_metric(gen_stock, bs, cfs, incs, pl)


    print("ho gya")
    merged.to_csv("Stock_Performance_Document/merged.csv")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
