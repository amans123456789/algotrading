import requests
import pandas as pd
import os
import csv


def call_put(ticker, date):

    url = "https://www.moneycontrol.com/stocks/fno/view-option-chain/{}/{}".format(ticker, date)
    print(url)

    df = pd.read_html(requests.post(url).text)[0]

    return df

# def save_data_to_csv(file_path, data):
#     # Check if the directory exists, if not, create it
#
#     # Check if the file exists, if not, create it and write the header
#     # if not os.path.exists(file_path):
#     with open(file_path, 'w', newline='') as file:
#         writer = csv.writer(file)
#         # Assuming data is a list of header columns
#         writer.writerow(data)
#
#     # Append the data to the CSV file
#     with open(file_path, 'a', newline='') as file:
#         writer = csv.writer(file)
#         # Assuming data is a list of values to be written to the CSV file
#         writer.writerow(data)
