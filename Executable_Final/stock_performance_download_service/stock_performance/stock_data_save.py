import os
from datetime import datetime
import logging

from stock_performance import balance_sheet as bs
from stock_performance import cash_flow as cfs
from stock_performance import general_stock_performance as gsp
from stock_performance import income_statement as ics
from stock_performance import pnl as pl

from config import config

logging.basicConfig(level=logging.INFO)

def csv_files_exist(folder_path, current_date):
    bs_filename = os.path.join(folder_path, f"balance_sheet.csv")
    cfs_filename = os.path.join(folder_path, f"cash_flow.csv")
    gsp_filename = os.path.join(folder_path, f"general_performance.csv")
    ics_filename = os.path.join(folder_path, f"income_statement.csv")
    pl_filename = os.path.join(folder_path, f"pnl.csv")

    return all(os.path.exists(filename) for filename in [bs_filename, cfs_filename, gsp_filename, ics_filename, pl_filename])

def create_csv():
    try:
        current_date = datetime.now()
        folder_name = current_date.strftime('%Y-%m')

        base_folder = 'Stock_Performance_Document'
        new_folder_path = os.path.join(base_folder, folder_name)

        os.makedirs(new_folder_path, exist_ok=True)
        if not csv_files_exist(new_folder_path, current_date):
            logging.info(f"Fetching and processing stock balance sheet data")
            res_bs = bs.run_stock_performance(config)
            logging.info(f"Fetching and processing stock cash flow data")
            res_cfs = cfs.run_stock_performance(config)
            logging.info(f"Fetching and processing stock general data")
            res_gsp = gsp.run_stock_performance(config)
            logging.info(f"Fetching and processing stock income statement data")
            res_ics = ics.run_stock_performance(config)
            logging.info(f"Fetching and processing stock pnl data")
            res_pl = pl.run_stock_performance(config)

            bs_filename = os.path.join(new_folder_path, "balance_sheet.csv")
            cfs_filename = os.path.join(new_folder_path, "cash_flow.csv")
            gsp_filename = os.path.join(new_folder_path, "general_performance.csv")
            ics_filename = os.path.join(new_folder_path, "income_statement.csv")
            pl_filename = os.path.join(new_folder_path, "pnl.csv")

            logging.info(f"Saving data to CSV files")

            res_bs.to_csv(bs_filename, index=False, mode='w')
            res_cfs.to_csv(cfs_filename, index=False, mode='w')
            res_gsp.to_csv(gsp_filename, index=False, mode='w')
            res_ics.to_csv(ics_filename, index=False, mode='w')
            res_pl.to_csv(pl_filename, index=False, mode='w')

            logging.info(f"CSV files created successfully in {new_folder_path}")
        else:
            logging.info(f"CSV files for today's date already exist. Skipping data fetching and processing.")

    except Exception as e:
        logging.error(f"Error creating CSV files: {str(e)}")





