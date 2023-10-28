
import numpy as np
import warnings
from pandas_datareader import data as pdr
import yfinance as yf
import datetime as dt
from yahoo_fin import stock_info as si
import pandas as pd
from calculate_roi import get_total_roi
pd.set_option('display.max_rows', None)
warnings.filterwarnings("ignore")
yf.pdr_override()

# num_of_years = 1
# start = dt.date.today() - dt.timedelta(days = int(365.25*num_of_years))
# end = dt.date.today()

# Monthly
num_of_days = 30
start = dt.date.today() - dt.timedelta(days = int(num_of_days))
end = dt.date.today()

ticker_1 = ['KRNY']
ticker_2 = ['TRMK']

# Combine the two lists of tickers
all_tickers = ticker_1 + ticker_2

dataset = pdr.get_data_yahoo(all_tickers, start, end)['Adj Close']
stocks_returns = np.log(dataset/dataset.shift(1))

# print('\nCorrelation Matrix')
# corr_matrix = stocks_returns.corr()
# print (corr_matrix)

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

print(top_abs_correlations)
print(start)
print(end)

# # Filter correlations >= 0.6
# filtered_correlations = top_abs_correlations[top_abs_correlations >= 0.6]

# print('Total Roi is ', get_total_roi('FULT', 'OCFC', start, end))