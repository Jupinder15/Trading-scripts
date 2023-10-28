# This script takes all the stocks from stocks file and enter correlations and p value

import numpy as np
import warnings
from pandas_datareader import data as pdr
import yfinance as yf
import datetime as dt
from statsmodels.tsa.stattools import coint
from yahoo_fin import stock_info as si  
import pandas as pd
pd.set_option('display.max_rows', None)
warnings.filterwarnings("ignore")
yf.pdr_override()

# Get the list of all symbols from https://www.nasdaq.com/market-activity/stocks/screener
df = pd.read_csv('stocks.csv')
symbol_list = df['Symbol'].tolist()

# Monthly
num_of_days = 60
start = dt.date.today() - dt.timedelta(days=num_of_days)
end = dt.date.today()

# Combine the two lists of tickers
all_tickers = symbol_list

# Get the average daily volumes and industry for the tickers using yfinance
ticker_info = []

for ticker in all_tickers:
    try:
        print(ticker)
        stock = yf.Ticker(ticker)
        history = stock.history(period="3mo")
        if history.shape[0] >= 40:
            average_volume = history['Volume'].mean()
            sector = stock.info.get('sector', 'N/A')
            ticker_info.append({'Ticker': ticker, 'Average Volume': average_volume, 'Sector': sector})
    except:
        pass

# Create a DataFrame from the ticker_info list
ticker_info_df = pd.DataFrame(ticker_info)

# Filter tickers with average daily volume > 100000
filtered_tickers = ticker_info_df[ticker_info_df['Average Volume'] > 100000]['Ticker'].tolist()

dataset = pdr.get_data_yahoo(filtered_tickers, start, end)['Adj Close']
stocks_returns = np.log(dataset/dataset.shift(1))

def get_redundant_pairs(df):
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_abs_correlations(df):
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr

top_abs_correlations = get_top_abs_correlations(stocks_returns)

# Filter correlations >= 0.6
filtered_correlations = top_abs_correlations[top_abs_correlations >= 0.8]

# Save the filtered correlations to an Excel file
filtered_correlations_df = pd.DataFrame(filtered_correlations, columns=['Correlation'])

# Add columns for Stock 1 and Stock 2
filtered_correlations_df['Stock 1'] = filtered_correlations_df.index.get_level_values(0)
filtered_correlations_df['Stock 2'] = filtered_correlations_df.index.get_level_values(1)

# Reorder columns
filtered_correlations_df = filtered_correlations_df[['Stock 1', 'Stock 2', 'Correlation']]

# Merge with ticker_info_df to add average daily volume and industry
merged_df = filtered_correlations_df.merge(ticker_info_df, left_on='Stock 1', right_on='Ticker', how='left')
merged_df = merged_df.merge(ticker_info_df, left_on='Stock 2', right_on='Ticker', how='left', suffixes=('_Stock1', '_Stock2'))

def get_cointegration_test_results(row):
    symbol1 = row['Stock 1']
    symbol2 = row['Stock 2']
    # Define the time period
    start_date = start
    end_date = end

    try:
        # Download historical stock data using yfinance
        stock_data1 = yf.download(symbol1, start=start_date, end=end_date)["Adj Close"]
        stock_data2 = yf.download(symbol2, start=start_date, end=end_date)["Adj Close"]

        if stock_data1.empty or stock_data2.empty:
            return np.nan  # Return NaN for cases with missing data

        # Check for cointegration using the cointegration test
        _, p_value, _ = coint(stock_data1, stock_data2)

        return p_value
    except:
        return np.nan

merged_df['p_value'] = merged_df.apply(get_cointegration_test_results, axis=1)

# Reorder columns for output
output_df = merged_df[[
    'Stock 1', 'Average Volume_Stock1', 'Sector_Stock1',
    'Stock 2', 'Average Volume_Stock2', 'Sector_Stock2',
    'Correlation', 'p_value'
]]

# Save the updated DataFrame to an Excel file
output_excel_file = 'top_pairs_' + str(num_of_days) + '_days_' + str(start) + '_to_' + str(end) + '.xlsx'
output_df.to_excel(output_excel_file, index=False)

print("Processing completed. Results saved to:", output_excel_file)

print(start)
print(end)