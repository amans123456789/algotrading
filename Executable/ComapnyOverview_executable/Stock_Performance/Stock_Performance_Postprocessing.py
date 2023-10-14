import pandas as pd

# bs = pd.read_csv("Stock_Performance_Document/balance_sheet.csv")
# cfs = pd.read_csv("Stock_Performance_Document/cash_flow.csv")
# gen_stock = pd.read_csv("Stock_Performance_Document/general_performance.csv")
# incs = pd.read_csv("Stock_Performance_Document/income_statement.csv")
# pl = pd.read_csv("Stock_Performance_Document/pnl.csv")


def rename_col(df):
    #     df.columns = df.iloc[0]
    if df.shape[1] > 8:
        df = df.drop(df.columns[0], axis=1)

    df.columns = ["Attribute", "First Date", "Second Date", "Third Date", "Fourth Date ", "Fifth Date", "Blank",
                  "Stock"]
    #     df = df[2:]
    return df


def operation(financial_fin, st, year):
    fin = {}
    financial_fin_st = financial_fin[financial_fin["Stock"] == st]
    financial_fin_st_T = financial_fin_st.transpose()
    #     financial_fin_st_T = financial_fin_st_T.reset_index(drop=True)

    financial_fin_st_T.columns = financial_fin_st_T.iloc[0]
    financial_fin_st_T = financial_fin_st_T[1:-3]
    financial_fin_st_T["Stock"] = st
    financial_fin_st_T_selected = financial_fin_st_T[financial_fin_st_T.iloc[:, 0].str.contains(year)]
    financial_fin_st_T_selected.reset_index(drop=True)
    #     if len(financial_fin_st_T_selected) > 0:
    financial_fin_st_T_selected["Year"] = year
    for i in ["Year", "Total Assets", "Stock", "Minority Interest", "Net CashFlow From Operating Activities",
              "Total Shareholders Funds", "Total Current Assets", "Cash And Cash Equivalents", "Current Investments",
              "Total Current Liabilities"
        , "Long Term Borrowings", "Short Term Borrowings",
              "Profit/Loss Before Exceptional, ExtraOrdinary Items And Tax", "Finance Costs", "Other Income",
              "Net CashFlow From Operating Activities", "Net Cash Used In Investing Activities", "Inventories"]:
        if i in financial_fin_st_T_selected.columns:

            fin[i] = financial_fin_st_T_selected[i].iloc[0]
        else:
            fin[i] = ""

    return fin


def stock_df_creation(financial_fin, stock, year):
    af = operation(financial_fin, stock, year)
    df = pd.DataFrame.from_dict(af, orient='index', columns=['Value'])

    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Key'}, inplace=True)
    transposed_df = df.transpose()
    transposed_df.columns = transposed_df.iloc[0]
    transposed_df = transposed_df[1:]

    return transposed_df

def cleaning_func(bs,pl,cfs,incs):
    bs_rename = rename_col(bs)
    pl_rename = rename_col(pl)
    cfs_rename = rename_col(cfs)
    incs_rename =rename_col(incs)

    financial_fin = pd.concat([bs_rename, pl_rename, cfs_rename, incs_rename])

    financial_fin = financial_fin.drop_duplicates()

    stock_list = financial_fin["Stock"].unique()

    return stock_list, financial_fin


def final_dataframe(stock_list,financial_fin ):
    fin = pd.DataFrame()
    missing = []

    for i in stock_list:
        print(i)
        try:
            res = stock_df_creation(financial_fin, i,"23")
            fin = pd.concat([fin,res])
        except:
            missing.append(i)
    return fin, missing


