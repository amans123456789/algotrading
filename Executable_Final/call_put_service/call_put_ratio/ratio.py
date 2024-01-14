import pandas as pd
import os
import re
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_latest_date(directory):
    logger.info(f"Searching for the latest date in directory: {directory}")

    # Get all files in the directory
    files = os.listdir(directory)

    # Filter files based on the naming pattern
    csv_files = [file for file in files if re.match(r'^data\d{4}-\d{2}-\d{2}\.csv$', file)]

    if not csv_files:
        logger.info("No matching CSV files found.")
        return None

    # Extract dates from filenames and find the latest one
    latest_date = max([datetime.datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', file).group(), '%Y-%m-%d') for file in csv_files])
    latest_date_str = latest_date.strftime('%Y-%m-%d')
    logger.info(f"Latest date found: {latest_date_str}")

    return latest_date_str


def group_and_sum(df, dt):
    logger.info("Grouping and summing the DataFrame.")

    columns_to_sum = ['OI', 'OI.1', 'Volume', 'Volume.1']
    df[columns_to_sum] = df[columns_to_sum].replace('-', 0, regex=True)

    # Convert columns to numeric
    df[columns_to_sum] = df[columns_to_sum].apply(pd.to_numeric, errors='coerce')

    # Group by 'Stock' and sum the specified columns
    grouped_df = df.groupby('Stock')[columns_to_sum].sum().reset_index()

    grouped_df['OI Call Put Ratio'] = grouped_df['OI'] / grouped_df['OI.1']
    grouped_df['Volume Call Put Ratio'] = grouped_df['Volume'] / grouped_df['Volume.1']

    ratio_folder = os.path.join("call_put_data", "call_put_ratio")
    if not os.path.exists(ratio_folder):
        os.makedirs(ratio_folder)

    # Form the filename for the ratio CSV
    ratio_filename = f"call_put_ratio_{dt}.csv"
    ratio_filepath = os.path.join(ratio_folder, ratio_filename)

    # Save the grouped DataFrame to a CSV file if it doesn't exist
    if not os.path.exists(ratio_filepath):
        grouped_df.to_csv(ratio_filepath, index=False)
        logger.info(f"Grouped data saved to {ratio_filepath}")

    logger.info("Grouping and summing completed.")
    return grouped_df