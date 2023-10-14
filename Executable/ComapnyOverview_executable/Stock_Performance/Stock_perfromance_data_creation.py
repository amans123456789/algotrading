import Stock_List
import Stock_Performance.Balance_Sheet as bs
import Stock_Performance.CashFlow as cfs
import Stock_Performance.General_Stock_Performance as gsp
import Stock_Performance.Income_Statement as ics
import Stock_Performance.PnL as pl


res_bs = bs.run_stock_performance(Stock_List.tickers)
res_cfs = cfs.run_stock_performance(Stock_List.tickers)
res_gsp = gsp.run_stock_performance(Stock_List.tickers)
res_ics = ics.run_stock_performance(Stock_List.tickers)
res_pl = pl.run_stock_performance(Stock_List.tickers)


res_bs.to_csv("Stock_Performance_Document/balance_sheet.csv")
res_cfs.to_csv("Stock_Performance_Document/cash_flow.csv")
res_gsp.to_csv("Stock_Performance_Document/general_performance.csv")
res_ics.to_csv("Stock_Performance_Document/income_statement.csv")
res_pl.to_csv("Stock_Performance_Document/pnl.csv")