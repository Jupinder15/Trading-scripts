

import numpy as np
import warnings
import yfinance as yf
import pandas as pd

pd.set_option('display.max_rows', None)
warnings.filterwarnings("ignore")
yf.pdr_override()

# Read the list of stock symbols from the CSV file
df = pd.read_csv('stocks.csv')
symbol_list = df['Symbol'].tolist()

# Define a function to fetch short ratio and short float for a stock
def get_short_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        short_ratio = stock.info.get('shortRatio', 'N/A')
        short_float = stock.info.get('shortPercentOfFloat', None)

        if short_float:
            short_float = float(short_float) * 100
        else:
            short_float = 'N/A'

        return short_ratio, short_float
    except:
        return 'N/A', 'N/A'

# Create lists to store data
filtered_data = []

# Iterate through the list of stock symbols
for ticker in symbol_list:
    print(ticker)
    short_ratio, short_float = get_short_data(ticker)

    if short_ratio != 'N/A' and short_float != 'N/A':
        short_ratio = float(short_ratio)
        short_float = float(short_float)
        if short_ratio > 10 and short_float > 20:
            filtered_data.append([ticker, short_ratio, short_float])

# Create a DataFrame from the filtered data
result_df = pd.DataFrame(filtered_data, columns=['Ticker', 'Short Ratio', 'Short Float'])

# Save the data to a CSV file
result_df.to_csv('filtered_short_data.csv', index=False)

print("Data saved to 'filtered_short_data.csv'")
