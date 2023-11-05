import os
from datetime import datetime

from stock_performance import balance_sheet as bs
from stock_performance import cash_flow as cfs
from stock_performance import general_stock_performance as gsp
from stock_performance import income_statement as ics
from stock_performance import pnl as pl

from config import config


def create_csv():
    current_date = datetime.now()
    folder_name = current_date.strftime('%Y-%m')

    base_folder = 'Stock_Performance_Document'
    new_folder_path = os.path.join(base_folder, folder_name)

    os.makedirs(new_folder_path, exist_ok=True)

    res_bs = bs.run_stock_performance(config)
    res_cfs = cfs.run_stock_performance(config)
    res_gsp = gsp.run_stock_performance(config)
    res_ics = ics.run_stock_performance(config)
    res_pl = pl.run_stock_performance(config)

    bs_filename = os.path.join(new_folder_path, "balance_sheet.csv")
    cfs_filename = os.path.join(new_folder_path, "cash_flow.csv")
    gsp_filename = os.path.join(new_folder_path, "general_performance.csv")
    ics_filename = os.path.join(new_folder_path, "income_statement.csv")
    pl_filename = os.path.join(new_folder_path, "pnl.csv")


    res_bs.to_csv(bs_filename, index=False, mode='w')
    res_cfs.to_csv(cfs_filename, index=False, mode='w')
    res_gsp.to_csv(gsp_filename, index=False, mode='w')
    res_ics.to_csv(ics_filename, index=False, mode='w')
    res_pl.to_csv(pl_filename, index=False, mode='w')

