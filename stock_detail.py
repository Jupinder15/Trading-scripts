import numpy as np
import warnings
from pandas_datareader import data as pdr
import yfinance as yf
import datetime as dt
from yahoo_fin import stock_info as si
import pandas as pd
pd.set_option('display.max_rows', None)
warnings.filterwarnings("ignore")
yf.pdr_override()

# Weekly (approx. 5 trading days)
num_of_weeks = 8  # Adjust as needed
start = dt.date.today() - dt.timedelta(weeks=num_of_weeks)
end = dt.date.today()

ticker_info = []

try:
    stock = yf.Ticker('LNG')
    print(stock.info['exchange'])
    history = stock.history(period="3mo")  # Using 60 days period
    if history.shape[0] >= 40:
        average_volume = history['Volume'].mean()/1000000
        sector = stock.info.get('sector', 'N/A')
        ticker_info.append({'Ticker': 'BOWN', 'Average Volume (Millions)': round(average_volume, 2), 'Sector': sector})
except:
    pass

# print(ticker_info)