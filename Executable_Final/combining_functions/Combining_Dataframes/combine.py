import logging
import pandas as pd
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(filename="data_processing.log", level=logging.INFO)

def check_data_consistency(file_path, expected_date, max_days_difference=0):
    # Extracting date from the file name
    try:
        file_date_str = file_path.split("_")[-1].split(".")[0]
        file_date = datetime.strptime(file_date_str, "%Y-%m-%d").date()
    except ValueError:
        logging.error(f"Error extracting date from the file name in {file_path}")
        raise ValueError(f"Error extracting date from the file name in {file_path}")

    # Logging the check for Condition 1
    logging.info(
        f"Checking Condition 1 for {file_path}: Date should be within the last {max_days_difference} days from today."
    )

    # Checking if the date is within the expected range
    if abs((expected_date - file_date).days) > max_days_difference:
        logging.error(
            f"Date in {file_path} is not within the last {max_days_difference} days from today."
        )
        raise ValueError(
            f"Date in {file_path} is not within the last {max_days_difference} days from today."
        )

    # Logging the check for Condition 2
    logging.info(
        f"Checking Condition 2 for {file_path}: CSV name format should be as expected."
    )

    # Checking if the file name format is as expected
    if not file_path.endswith(f"{file_date_str}.csv"):
        logging.error(f"Invalid file name format for {file_path}")
        raise ValueError(f"Invalid file name format for {file_path}")

    return file_date


def check_fundamental_analysis(file_path, expected_date, max_days_difference=0):
    # Extracting year from the file name
    try:
        file_year_str = file_path.split("_")[-1].split(".")[0]
        file_year = int(file_year_str)
    except ValueError:
        logging.error(f"Error extracting year from the file name in {file_path}")
        raise ValueError(f"Error extracting year from the file name in {file_path}")

    # Logging the check for Condition 1
    logging.info(
        f"Checking Condition 1 for {file_path}: Date should be within the last {max_days_difference} days from today."
    )

    # Check if the year is within the expected range
    if abs(expected_date.year - file_year) > 1:
        logging.error(
            f"Year in {file_path} is not within the expected range of {expected_date.year - 1} to {expected_date.year}."
        )
        raise ValueError(
            f"Year in {file_path} is not within the expected range of {expected_date.year - 1} to {expected_date.year}."
        )

    # Logging the check for Condition 2
    logging.info(
        f"Checking Condition 2 for {file_path}: CSV name format should be as expected."
    )

    # Checking if the file name format is as expected
    if not file_path.endswith(f"{file_year_str}.csv"):
        logging.error(f"Invalid file name format for {file_path}")
        raise ValueError(f"Invalid file name format for {file_path}")

    return file_year


def check_all_conditions(file_paths):
    try:
        # Current date
        today = datetime.now().date()

        # Read Market Condition data
        mark_cond_daily_date = check_data_consistency(
            file_paths["mark_cond_daily"], today, max_days_difference=2
        )
        mark_cond_minute_date = check_data_consistency(
            file_paths["mark_cond_minute"], today, max_days_difference=2
        )

        # Condition 3: Date of all market data and lagging data should be the same.
        # Logging the check for Condition 3
        logging.info(
            "Checking Condition 3: Dates of daily and hourly market conditions should match."
        )
        if mark_cond_daily_date != mark_cond_minute_date:
            logging.error("Dates of daily and hourly market conditions do not match.")
            raise ValueError("Dates of daily and hourly market conditions do not match.")

        # Read Lagging conditions data
        lagging_ind_cond_daily_date = check_data_consistency(
            file_paths["lagging_ind_cond_daily"], today, max_days_difference=2
        )
        lagging_ind_cond_minute_date = check_data_consistency(
            file_paths["lagging_ind_cond_minute"], today, max_days_difference=2
        )

        # Logging the check for Condition 3 (continued)
        logging.info(
            "Checking Condition 3 (continued): Dates of daily and hourly lagging indicators should match."
        )
        if lagging_ind_cond_daily_date != lagging_ind_cond_minute_date:
            logging.error("Dates of daily and hourly lagging indicators do not match.")
            raise ValueError("Dates of daily and hourly lagging indicators do not match.")

        # Read Fundamental Analysis data
        fund_analysis_year = check_fundamental_analysis(
            file_paths["fund_analysis"], mark_cond_daily_date
        )

        # Condition 4: Fundamental analysis year should be the same as or just the year before the year of market condition and lagging condition.
        # Logging the check for Condition 4
        logging.info(
            "Checking Condition 4: Year of fundamental analysis should match with market condition and lagging condition years."
        )
        if fund_analysis_year not in [
            mark_cond_daily_date.year,
            mark_cond_daily_date.year - 1,
        ]:
            logging.error(
                "Year of fundamental analysis does not match with market condition and lagging condition years."
            )
            raise ValueError(
                "Year of fundamental analysis does not match with market condition and lagging condition years."
            )

        # Read Call Put Analysis data
        ratio_analysis_date = check_data_consistency(
            file_paths["ratio_analysis"], mark_cond_daily_date, max_days_difference=30
        )
        logging.info(
            "Checking Condition 6: Call Put Analysis CSV should be within 30 days of market condition and lagging condition CSV."
        )
        if abs((mark_cond_daily_date - ratio_analysis_date).days) > 30:
            logging.error(
                "Call Put Analysis CSV is more than 30 days in the future compared to market condition or lagging condition CSVs."
            )
            raise ValueError(
                "Call Put Analysis CSV is more than 30 days in the future compared to market condition or lagging condition CSVs."
            )
        # Read Market News data
        news_date = check_data_consistency(
            file_paths["news"], mark_cond_daily_date, max_days_difference=5
        )

        # Condition 5: Market news CSV should be within plus and minus 5 days of market condition and lagging condition CSV.
        # Logging the check for Condition 5
        logging.info(
            "Checking Condition 5: Market news CSV should be within plus and minus 5 days of market condition and lagging condition CSV."
        )
        if abs((mark_cond_daily_date - news_date).days) > 5:
            logging.error(
                "Market news CSV is not within plus and minus 5 days of market condition and lagging condition CSV."
            )
            raise ValueError(
                "Market news CSV is not within plus and minus 5 days of market condition and lagging condition CSV."
            )

        # Read Last Day Fibonacci Market Indicator data
        last_mark_cond_daily_date = check_data_consistency(
            file_paths["last_mark_cond_daily"], today, max_days_difference=2
        )
        last_mark_cond_minute_date = check_data_consistency(
            file_paths["last_mark_cond_minute"], today, max_days_difference=2
        )

        # Logging the check for Condition 3 (continued) for Last Day Fibonacci Market Indicator
        logging.info(
            "Checking Condition 3 (continued): Dates of last day daily and hourly market indicators should match."
        )
        if last_mark_cond_daily_date != last_mark_cond_minute_date:
            logging.error("Dates of last day daily and hourly market indicators do not match.")
            raise ValueError("Dates of last day daily and hourly market indicators do not match.")

        # Read Last Day Fibonacci Lagging Indicator data
        last_lagging_ind_cond_daily_date = check_data_consistency(
            file_paths["last_lagging_ind_cond_daily"], today, max_days_difference=2
        )
        last_lagging_ind_cond_minute_date = check_data_consistency(
            file_paths["last_lagging_ind_cond_minute"], today, max_days_difference=2
        )

        # Logging the check for Condition 3 (continued) for Last Day Fibonacci Lagging Indicator
        logging.info(
            "Checking Condition 3 (continued): Dates of last day daily and hourly lagging indicators should match."
        )
        if last_lagging_ind_cond_daily_date != last_lagging_ind_cond_minute_date:
            logging.error("Dates of last day daily and hourly lagging indicators do not match.")
            raise ValueError("Dates of last day daily and hourly lagging indicators do not match.")







        # If all conditions are met, continue with data processing
        logging.info("All conditions are met. Continue with data processing.")
        return True
    except ValueError as ve:
        # Catching ValueError exceptions and logging the corresponding error message
        logging.error(str(ve))
        print(f"Error: {ve}")
        return False
    except Exception as e:
        # Catching any unexpected exceptions and logging a generic error message
        logging.error(f"An unexpected error occurred: {str(e)}")
        return False





#
# def check_all_conditions(file_paths):
#     try:
#         # Condition 1: Market condition and lagging condition data read should be within the last 2 days from today.
#         # Condition 2: Check if the CSV name format is the same as mentioned above.
#         def check_data_consistency(file_path, expected_date, max_days_difference=0):
#             # Extracting date from the file name
#             try:
#                 file_date_str = file_path.split("_")[-1].split(".")[0]
#                 file_date = datetime.strptime(file_date_str, "%Y-%m-%d").date()
#             except ValueError:
#                 logging.error(f"Error extracting date from the file name in {file_path}")
#                 raise ValueError(f"Error extracting date from the file name in {file_path}")
#
#             # Logging the check for Condition 1
#             logging.info(
#                 f"Checking Condition 1 for {file_path}: Date should be within the last {max_days_difference} days from today."
#             )
#
#             # Checking if the date is within the expected range
#             if abs((expected_date - file_date).days) > max_days_difference:
#                 logging.error(
#                     f"Date in {file_path} is not within the last {max_days_difference} days from today."
#                 )
#                 raise ValueError(
#                     f"Date in {file_path} is not within the last {max_days_difference} days from today."
#                 )
#
#             # Logging the check for Condition 2
#             logging.info(
#                 f"Checking Condition 2 for {file_path}: CSV name format should be as expected."
#             )
#
#             # Checking if the file name format is as expected
#             if not file_path.endswith(f"{file_date_str}.csv"):
#                 logging.error(f"Invalid file name format for {file_path}")
#                 raise ValueError(f"Invalid file name format for {file_path}")
#
#             return file_date
#
#         # Current date
#         today = datetime.now().date()
#
#         # Read Market Condition data
#         mark_cond_daily_date = check_data_consistency(
#             file_paths["mark_cond_daily"], today, max_days_difference=2
#         )
#         mark_cond_minute_date = check_data_consistency(
#             file_paths["mark_cond_minute"], today, max_days_difference=2
#         )
#
#         # Condition 3: Date of all market data and lagging data should be the same.
#         # Logging the check for Condition 3
#         logging.info(
#             "Checking Condition 3: Dates of daily and hourly market conditions should match."
#         )
#         if mark_cond_daily_date != mark_cond_minute_date:
#             logging.error("Dates of daily and hourly market conditions do not match.")
#             raise ValueError("Dates of daily and hourly market conditions do not match.")
#
#         # Read Lagging conditions data
#         lagging_ind_cond_daily_date = check_data_consistency(
#             file_paths["lagging_ind_cond_daily"], today, max_days_difference=2
#         )
#         lagging_ind_cond_minute_date = check_data_consistency(
#             file_paths["lagging_ind_cond_minute"], today, max_days_difference=2
#         )
#
#         # Logging the check for Condition 3 (continued)
#         logging.info(
#             "Checking Condition 3 (continued): Dates of daily and hourly lagging indicators should match."
#         )
#         if lagging_ind_cond_daily_date != lagging_ind_cond_minute_date:
#             logging.error("Dates of daily and hourly lagging indicators do not match.")
#             raise ValueError("Dates of daily and hourly lagging indicators do not match.")
#
#         # Read Fundamental Analysis data
#         fund_analysis_date = check_data_consistency(
#             file_paths["fund_analysis"], mark_cond_daily_date
#         )
#
#         # Condition 4: Fundamental analysis year should be the same as or just the year before the year of market condition and lagging condition.
#         # Logging the check for Condition 4
#         logging.info(
#             "Checking Condition 4: Year of fundamental analysis should match with market condition and lagging condition years."
#         )
#         if fund_analysis_date.year not in [
#             mark_cond_daily_date.year,
#             mark_cond_daily_date.year - 1,
#         ]:
#             logging.error(
#                 "Year of fundamental analysis does not match with market condition and lagging condition years."
#             )
#             raise ValueError(
#                 "Year of fundamental analysis does not match with market condition and lagging condition years."
#             )
#
#         # Read Call Put Analysis data
#         ratio_analysis_date = check_data_consistency(
#             file_paths["ratio_analysis"], mark_cond_daily_date, max_days_difference=30
#         )
#
#         # Read Market News data
#         news_date = check_data_consistency(
#             file_paths["news"], mark_cond_daily_date, max_days_difference=5
#         )
#
#         # Condition 5: Market news CSV should be within plus and minus 5 days of market condition and lagging condition CSV.
#         # Logging the check for Condition 5
#         logging.info(
#             "Checking Condition 5: Market news CSV should be within plus and minus 5 days of market condition and lagging condition CSV."
#         )
#         if abs((mark_cond_daily_date - news_date).days) > 5:
#             logging.error(
#                 "Market news CSV is not within plus and minus 5 days of market condition and lagging condition CSV."
#             )
#             raise ValueError(
#                 "Market news CSV is not within plus and minus 5 days of market condition and lagging condition CSV."
#             )
#
#         # If all conditions are met, continue with data processing
#         logging.info("All conditions are met. Continue with data processing.")
#
#     except ValueError as ve:
#         # Catching ValueError exceptions and logging the corresponding error message
#         logging.error(str(ve))
#         print(f"Error: {ve}")
#     except Exception as e:
#         # Catching any unexpected exceptions and logging a generic error message
#         logging.error(f"An unexpected error occurred: {str(e)}")
#         # print(f"An unexpected error occurred: {str(e)}")


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
print(check_all_conditions(file_paths) )