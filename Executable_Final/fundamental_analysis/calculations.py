from postprocessing import combine_col, stock_df_creation, calc, gen_stock_df
from fundamental_ratios import fundamental_analysis, merged_file_analysis
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)

def fin_cal(year):
    logging.info("Reading stock performance files")

    cfs = pd.read_csv("starting_data/annual_data/cash_flow.csv")
    bs = pd.read_csv("starting_data/annual_data/balance_sheet.csv")
    gp = pd.read_csv("starting_data/annual_data/general_performance.csv")
    ins = pd.read_csv("starting_data/annual_data/income_statement.csv")
    pnl = pd.read_csv("starting_data/annual_data/pnl.csv")
    try:
        # folder_name = (year).strftime('%Y')
        folder_name = "20" + year

        base_folder = 'starting_data/results'
        new_folder_path = os.path.join(base_folder, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        fundamental_analysis_folder = os.path.join(new_folder_path, "fundamental_analysis_{}.csv".format(folder_name))

        check = all(os.path.exists(filename) for filename in [fundamental_analysis_folder])

        if not check:
            logging.info("Fundamental Analysis Function Started")
            logging.info("Post Processing Running")

            financial_fin = combine_col(bs, cfs, ins, pnl)
            stock_list = financial_fin["Stock"].unique()
            res = calc(financial_fin, stock_list, year)

            logging.info("Post Processing Completed")
            logging.info("Analysis Function Running")

            if res.empty:
                logging.info("The mentioned date is not present in the DataFrame. Try with a different date.")
                try:
                    os.rmdir(new_folder_path)
                    logging.info(f"Folder '{year}' deleted successfully.")
                except Exception as e:
                    logging.error(f"Error deleting folder '{year}': {str(e)}", exc_info=True)

                return
            fin = fundamental_analysis(res)
            gen = gen_stock_df(stock_list, gp)
            merged = gen.merge(fin, on = ["Stock"])

            df = merged_file_analysis(merged)
            logging.info("Analysis Completed")

            df.to_csv(fundamental_analysis_folder, index=False, mode='w')
            logging.info(f"CSV files created successfully in {new_folder_path}")

            # return df
        else:
            logging.info(f"CSV files for the mentioned date already exist. Skipping data fetching and processing.")
            df = pd.read_csv(fundamental_analysis_folder)

            # return df

    except Exception as e:
        logging.error(f"An error occurred in download_func: {str(e)}", exc_info=True)






