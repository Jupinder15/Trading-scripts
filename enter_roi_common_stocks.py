# This script will enter the ROI for all the stocks in the input file for provided time period

import pandas as pd
import datetime as dt
from calculate_roi_1 import get_total_roi
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yfinance as yf

# start_1m = dt.date.today() - dt.timedelta(days = 30)
start_2m = dt.date.today() - dt.timedelta(days = 60)
start_6m = dt.date.today() - dt.timedelta(days = 180)
end = dt.date.today()

# Read the Excel file
input_excel_file = "ROI_14-09.xlsx"
df = pd.read_excel(input_excel_file)

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options , service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
driver.implicitly_wait(5)

# Calculate ROI for each row and store in a new column
# df["ROI_1M"] = df.apply(lambda row: get_total_roi(driver, row["Stock 1"], row["Stock 2"], start_1m, end), axis=1)
df["ROI_2M"] = df.apply(lambda row: get_total_roi(driver, row["Stock 1"], row["Stock 2"], start_2m, end), axis=1)
df["ROI_6M"] = df.apply(lambda row: get_total_roi(driver, row["Stock 1"], row["Stock 2"], start_6m, end), axis=1)

# Save the updated DataFrame back to the Excel file
output_excel_file = "stocks_with_roi_14-09-2023.xlsx"
df.to_excel(output_excel_file, index=False)
