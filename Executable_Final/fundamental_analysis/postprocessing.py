import pandas as pd
import logging


logging.basicConfig(level=logging.INFO)

def rename_col(df):
    if df.shape[1] > 8:
        df = df.drop(df.columns[0], axis=1)

    df.columns = ["Attribute", "First Date", "Second Date", "Third Date", "Fourth Date ", "Fifth Date", "Blank",
                  "Stock"]
    return df


def combine_col(bs, cfs, ins, pnl):
    bs_rename = rename_col(bs)
    pnl_rename = rename_col(pnl)
    cfs_rename = rename_col(cfs)
    incs_rename = rename_col(ins)
    financial_fin = pd.concat([bs_rename, pnl_rename, cfs_rename, incs_rename])

    financial_fin = financial_fin.drop_duplicates()
    return financial_fin


def operation(financial_fin, st, year):
    fin = {}
    financial_fin_st = financial_fin[financial_fin["Stock"] == st]
    financial_fin_st_T = financial_fin_st.transpose()
    financial_fin_st_T.columns = financial_fin_st_T.iloc[0]
    financial_fin_st_T = financial_fin_st_T[1:-3]
    financial_fin_st_T["Stock"] = st
    financial_fin_st_T_selected = financial_fin_st_T[financial_fin_st_T.iloc[:, 0].str.contains(year)]
    financial_fin_st_T_selected.reset_index(drop=True)
    financial_fin_st_T_selected["Year"] = year
    ####
    # if year not in financial_fin_st_T_selected['Year'].unique():
    #     latest_date = financial_fin_st_T_selected['Year'].max()
    #     logging.info(
    #         f"The given year ({year}) is not present in the DataFrame. Exiting and logging the latest date available: {latest_date}")
    #     return
    # else:
    #     financial_fin_st_T_selected["Year"] = year

    ####
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


def calc(df, stock_list, year):
    fin = pd.DataFrame()
    missing = []
    for i in stock_list:
        # print(i)
        try:
            res = stock_df_creation(df, i, year)
            fin = pd.concat([fin, res])
        except:
            missing.append(i)
    return fin


#### General Indicators
def gen_stock_flat(gen_stock,i):
#     for i in gen_stock["Stock"].unique():
    gen_stock_selected = gen_stock[gen_stock["Stock"] == i]
    gen_stock_selected = gen_stock_selected.drop(["Stock"], axis = 1)


    gen_stock_selected = gen_stock_selected[gen_stock_selected['Num'] != '- -']
    gen_stock_selected = gen_stock_selected.drop_duplicates()

    gen_stock_selected_transpose = gen_stock_selected.T

    gen_stock_selected_transpose.columns = gen_stock_selected_transpose.iloc[0]
    gen_stock_selected_transpose = gen_stock_selected_transpose[1:]

    gen_stock_selected_transpose["Stock"] = i
    gen_stock_selected_transpose = gen_stock_selected_transpose.reset_index(drop= True)

    gen_stock_selected_transpose = gen_stock_selected_transpose[["Stock","Dividend Yield", "Mkt Cap (Rs. Cr.)","TTM EPS See historical trend","Open"]]
#         print(gen_stock_selected_transpose.shape)

    return gen_stock_selected_transpose

#### General stock dataframe
def gen_stock_df(stock, gp):
    gen_fin = pd.DataFrame()
    for i in stock:
        tab = gen_stock_flat(gp, i)
        #     print(tab)
        #     gen_fin = gen_fin + tab
        gen_fin = pd.concat([gen_fin, tab], ignore_index=True)
    return gen_fin

