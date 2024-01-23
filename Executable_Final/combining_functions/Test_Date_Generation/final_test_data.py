import pandas as pd
from datetime import  timedelta
import os
import logging

def test_data_gen( df1, df2):
    df1['Date'] = pd.to_datetime(df1['Date'])

    # Convert 'Datetime' column in df2 to the same datetime type as 'Date' in df1
    df2['Date'] = pd.to_datetime(df2['Datetime'].dt.date)
    df2['Time'] = df2['Datetime'].dt.time

    df2['Date'] = df2['Date'] - timedelta(days=1)

    # Merge dataframes on 'Stock' and 'Date' columns
    merged_df = pd.merge(df1, df2, how='inner', on=['Stock', 'Date'])

    # Check if the merged dataframe is not empty
    if not merged_df.empty:
        # Calculate the ratio of 'Adj Close' in df1 to df2
        merged_df['Adj_Close_Ratio'] = merged_df['Adj Close_y'] / merged_df['Adj Close_x']
        median_df = merged_df.groupby(['Stock', 'Date']).median().reset_index()
        return median_df[['Date', 'Stock', 'Adj_Close_Ratio']]
    else:
        return None

def final_output(median_df):
    median_df.columns = ["Date", "Stock_x", "Adj_Close_Ratio"]
    expected_csv_filename = f"combined_df_test_feature_{median_df['Date'].iloc[0].strftime('%Y-%m-%d')}.csv"
    csv_path = os.path.join("Source_Data/Output", expected_csv_filename)

    if os.path.exists(csv_path):
        # Read the CSV file
        output = pd.read_csv(csv_path)
        output["Date"] = pd.to_datetime(output["Date"])

        fin = pd.merge(output, median_df, on=["Stock_x", "Date"])

        return fin
    else:
        # Log a message if the CSV file is not present
        logging.error(f"CSV file {expected_csv_filename} is not present in Source_Data/Output.")
        return None