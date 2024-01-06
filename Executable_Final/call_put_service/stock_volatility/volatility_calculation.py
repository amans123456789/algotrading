from stock_volatility.stock_data_download import daily_download
import pandas as pd
import numpy as np
import statistics
import logging

logging.basicConfig(level=logging.INFO)

# Source: https://medium.com/@polanitzer/volatility-calculation-in-python-estimate-the-annualized-volatility-of-historical-stock-prices-db937366a54d
# n_daily = 365
# daily_data = daily_download(n_daily)
# daily_data.to_csv("daily_stock_data.csv")

# daily_data = pd.read_csv("stock_volatility/daily_stock_data.csv")

def volatility(daily_data):
    daily = daily_data[["Date", "Adj Close"]]
    daily['Price relative'] = ""
    for i in range(1, len(daily.Date)):
        daily['Price relative'][i] = daily['Adj Close'][i] / daily['Adj Close'][i - 1]
    # daily['Price relative'] = (daily['Adj Close'] / daily['Adj Close'].shift(1))
    # daily['Price relative'].iloc[0] = np.nan
    daily['Daily Return'] = ""

    for i in range(1, len(daily.Date)):
        daily['Daily Return'][i] = np.log(daily['Adj Close'][i] / daily['Adj Close'][i - 1])
    # daily['Daily Return'] = np.log(daily['Adj Close'] / daily['Adj Close'].shift(1))
    # daily['Daily Return'].iloc[0] = np.nan

    DailyVolatility = statistics.stdev(daily['Daily Return'][1:])
    AnnualizedDailyVolatilityTradingDays  = DailyVolatility*np.sqrt(252)

    return DailyVolatility, AnnualizedDailyVolatilityTradingDays

def calculate_volatility_for_each_stock(dataframe, stck):
    result_dict = {}

    # Loop through each unique stock in the DataFrame
    for stock in dataframe['Stock'].unique():
        stock_data = dataframe[dataframe['Stock'] == stock].copy()
        stock_data.reset_index(drop=True, inplace=True)

        # Calculate volatility for the current stock
        daily_volatility, annualized_volatility = volatility(stock_data)

        stck.loc[stck['Stock'] == stock, 'Daily Volatility'] = daily_volatility
        stck.loc[stck['Stock'] == stock, 'Annualized Daily Volatility'] = annualized_volatility

        # Store the results in the dictionary
        result_dict[stock] = {
            'Daily Volatility': daily_volatility,
            'Annualized Daily Volatility (252 Trading Days)': annualized_volatility
        }
    logging.info("Volatility calculation results:")
    for stock, values in result_dict.items():
        logging.info(f"Stock: {stock}, Daily Volatility: {values['Daily Volatility']}, Annualized Daily Volatility: {values['Annualized Daily Volatility (252 Trading Days)']}")

    # return stck

    return result_dict

# res = volatility(daily_data)
# res.to_csv("volatility_res.csv")

# result = calculate_volatility_for_each_stock(daily_data)
# print(result)
# for stock, values in result.items():
#     print(f"Stock: {stock}")
#     print(f"Daily Volatility: {values['Daily Volatility']}")
#     print(f"Annualized Daily Volatility (252 Trading Days): {values['Annualized Daily Volatility (252 Trading Days)']}")
#     print("=" * 40)




