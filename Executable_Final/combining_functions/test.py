from config import config
import logging
import pandas as pd
from Combining_Dataframes.combine import create_file_paths, read_csvs
from Combining_Dataframes.dataframe_combining_functions import df_combine
from Combining_Dataframes.news_data import news_df_create, grading_sentiment, get_most_extreme_sentiment

logging.basicConfig(filename="data_processing.log", level=logging.INFO)

ticker_mapping = {config["tickers_NS"][i]: config["tickers"][i] for i in range(len(config["tickers_NS"]))}
ticker_mapping_2 = {config["ti"][i]: config["tickers_NS"][i] for i in range(len(config["tickers_NS"]))}

date = "2024-01-19"
fund_analysis_year = "2023"
ratio_analysis_date = "2024-01-25"
news_date = "2024-01-19"
file_paths = create_file_paths(date, fund_analysis_year, ratio_analysis_date, news_date)

res = (read_csvs(file_paths))
news = res["news"]

result_df = news_df_create(news, config["keyword_mapping"])
fin_news = grading_sentiment(result_df)

fin_news['Most Extreme Sentiment'] = fin_news['Sentiment Rating'].apply(get_most_extreme_sentiment)
fund_lag_cp_mrkt = df_combine(res, ticker_mapping, ticker_mapping_2)

fund_lag_cp_mkt_news = pd.merge(fund_lag_cp_mrkt, fin_news, left_on = ["Stock_x"], right_on = ["Category"], how = "left")

fund_lag_cp_mkt_news.to_csv("Source_Data/Output/combined_df_test_feature_.csv")
print(fund_lag_cp_mkt_news)