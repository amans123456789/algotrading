import logging
import pandas as pd
from datetime import datetime, timedelta
from Combining_Dataframes.combine import check_all_conditions
logging.basicConfig(filename="data_processing.log", level=logging.INFO)





# Read market conditions
# mark_cond_daily = pd.read_csv("Source_Data/Market_Condition/daily_market_condition_2024-01-14.csv")
# mark_cond_minute = pd.read_csv("Source_Data/Market_Condition/hourly_market_condition_2024-01-14.csv")
#
# last_mark_cond_daily = pd.read_csv("Source_Data/Market_Condition/last_day_fibonacci_market_indicator_2024-01-14.csv")
# last_mark_cond_minute = pd.read_csv("Source_Data/Market_Condition/last_hour_fibonacci_market_indicator_2024-01-14.csv")
#
# # Read Lagging conditions
# lagging_ind_cond_daily = pd.read_csv("Source_Data/Lagging_Indicators/daily_lag_indicator_2024-01-13.csv")
# lagging_ind_cond_minute = pd.read_csv("Source_Data/Lagging_Indicators/hourly_lag_indicator_2024-01-13.csv")
#
# last_lagging_ind_cond_daily = pd.read_csv("Source_Data/Lagging_Indicators/last_day_fibonacci_lag_indicator_2024-01-13.csv")
# last_lagging_ind_cond_minute = pd.read_csv("Source_Data/Lagging_Indicators/last_hour_fibonacci_lag_indicator_2024-01-13.csv")
#
# # Read Fundamental Analysis
# fund_analysis = pd.read_csv("Source_Data/Fundamental_Analysis/fundamental_analysis_2023.csv")
#
# # Call Put Analysis
# ratio_analysis = pd.read_csv("Source_Data/Call_Put/call_put_ratio_2024-01-25.csv")
#
# # Market News
# news = pd.read_csv("Source_Data/News/news-sentiment-data_2024-01-14.csv")

file_paths = {
    "mark_cond_daily": "Source_Data/Market_Condition/daily_market_condition_2024-01-14.csv",
    "mark_cond_minute": "Source_Data/Market_Condition/hourly_market_condition_2024-01-14.csv",
    "last_mark_cond_daily": "Source_Data/Market_Condition/last_day_fibonacci_market_indicator_2024-01-14.csv",
    "last_mark_cond_minute": "Source_Data/Market_Condition/last_hour_fibonacci_market_indicator_2024-01-14.csv",
    "lagging_ind_cond_daily": "Source_Data/Lagging_Indicators/daily_lag_indicator_2024-01-13.csv",
    "lagging_ind_cond_minute": "Source_Data/Lagging_Indicators/hourly_lag_indicator_2024-01-13.csv",
    "last_lagging_ind_cond_daily": "Source_Data/Lagging_Indicators/last_day_fibonacci_lag_indicator_2024-01-13.csv",
    "last_lagging_ind_cond_minute": "Source_Data/Lagging_Indicators/last_hour_fibonacci_lag_indicator_2024-01-13.csv",
    "fund_analysis": "Source_Data/Fundamental_Analysis/fundamental_analysis_2023.csv",
    "ratio_analysis": "Source_Data/Call_Put/call_put_ratio_2024-01-25.csv",
    "news": "Source_Data/News/news-sentiment-data_2024-01-14.csv",
}
check_all_conditions(file_paths)
