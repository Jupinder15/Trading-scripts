import numpy as np
import pandas as pd
import yfinance as yf
from statsmodels.tsa.stattools import coint

def get_cointegration_test_results(symbol1, symbol2, start, end):
    # Define the two stock symbols and the time period
    stock_symbol1 = symbol1
    stock_symbol2 = symbol2
    start_date = start
    end_date = end

    # Download historical stock data using yfinance
    stock_data1 = yf.download(stock_symbol1, start=start_date, end=end_date)["Adj Close"]
    stock_data2 = yf.download(stock_symbol2, start=start_date, end=end_date)["Adj Close"]

    # Combine the stock data into a DataFrame
    stock_prices = pd.concat([stock_data1, stock_data2], axis=1)
    stock_prices.columns = [stock_symbol1, stock_symbol2]

    # # Calculate the spread (difference) between the two stock prices
    # spread = stock_prices[stock_symbol1] - stock_prices[stock_symbol2]

    # Check for cointegration using the cointegration test
    score, p_value, _ = coint(stock_data1, stock_data2)

    # Set a significance level
    alpha = 0.05

    # Interpret the cointegration result
    print("Stocks: {} and {}".format(stock_symbol1, stock_symbol2))
    print("Time Period: {} to {}".format(start_date, end_date))
    print("Cointegration Test p-value:", p_value)
    print("Cointegration Test score:", score)

    if p_value < alpha:
        print("Result: The two stocks are likely cointegrated at a significance level of {}.".format(alpha))
        print("This suggests a long-term relationship between the stocks.")
    else:
        print("Result: The two stocks are not cointegrated at a significance level of {}.".format(alpha))

    return score, p_value

score, p_value = get_cointegration_test_results('TRMK', 'KRNY', '2023-08-09', '2023-09-08')
print(score)
print(p_value)
