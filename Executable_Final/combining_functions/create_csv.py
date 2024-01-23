import pandas as pd
import os
from datetime import datetime
import logging
from Combining_Dataframes.combine import create_file_paths, read_csvs
from Combining_Dataframes.dataframe_combining_functions import df_combine
from Combining_Dataframes.news_data import (
    news_df_create,
    grading_sentiment,
    get_most_extreme_sentiment,
)
from config import config

# Set up logging
logging.basicConfig(
    filename="logfile.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
ticker_mapping = {
    config["tickers_NS"][i]: config["tickers"][i]
    for i in range(len(config["tickers_NS"]))
}
ticker_mapping_2 = {
    config["ti"][i]: config["tickers_NS"][i] for i in range(len(config["tickers_NS"]))
}


def process_and_save_data(
    date,
    fund_analysis_year,
    ratio_analysis_date,
    news_date,
    ticker_mapping,
    ticker_mapping_2,
    output_folder="Source_Data/Output",
):
    try:
        file_paths = create_file_paths(
            date, fund_analysis_year, ratio_analysis_date, news_date
        )

        res = read_csvs(file_paths)
        news = res["news"]

        result_df = news_df_create(news, config["keyword_mapping"])
        fin_news = grading_sentiment(result_df)

        fin_news["Most Extreme Sentiment"] = fin_news["Sentiment Rating"].apply(
            get_most_extreme_sentiment
        )
        fund_lag_cp_mrkt = df_combine(res, ticker_mapping, ticker_mapping_2)

        fund_lag_cp_mkt_news = pd.merge(
            fund_lag_cp_mrkt,
            fin_news,
            left_on=["Stock_x"],
            right_on=["Category"],
            how="left",
        )
        # Generate CSV file name with date
        # date_str = datetime.now().strftime("%Y%m%d")
        csv_file_path = os.path.join(
            output_folder, f"combined_df_test_feature_{date}.csv"
        )

        # Check if the file already exists
        if not os.path.exists(csv_file_path):
            # Save the combined DataFrame to CSV
            fund_lag_cp_mkt_news.to_csv(csv_file_path, index=False)
            logging.info(f"CSV file '{csv_file_path}' created successfully.")
        else:
            logging.warning(
                f"CSV file '{csv_file_path}' already exists. No new file created."
            )
    except Exception as e:
        logging.error(f"Error: {str(e)}")


