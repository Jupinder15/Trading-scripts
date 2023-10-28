from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yfinance as yf
import openpyxl
import datetime as dt

def get_total_roi(driver, stock1, stock2, start_date, end_date):
    try:
        stock1_exchange = yf.Ticker(stock1).info.get('exchange')
        if stock1_exchange == 'NYQ':
            exchange1 = 'NYSE'
        elif stock1_exchange == 'ASE':
            exchange1 = 'AMEX'
        else:
            exchange1 = 'NASDAQ'

        stock2_exchange = yf.Ticker(stock2).info.get('exchange')
        if stock2_exchange == 'NYQ':
            exchange2 = 'NYSE'
        elif stock2_exchange == 'ASE':
            exchange2 = 'AMEX'
        else:
            exchange2 = 'NASDAQ'
        
        print(exchange1 + ':' + stock1)
        print(exchange2 + ':' + stock2)

        driver.get('https://www.pairtradinglab.com/index.php?command=newBacktest')

        driver.find_element(By.NAME, "b_ticker1").clear()
        driver.find_element(By.NAME, "b_ticker1").send_keys(exchange1 + ':' + stock1)
        driver.find_element(By.NAME, "b_ticker2").clear()
        driver.find_element(By.NAME, "b_ticker2").send_keys(exchange2 + ':' + stock2)

        # driver.find_element(By.NAME, "b_start").clear()
        driver.find_element(By.NAME, "b_start").send_keys(str(start_date.year) + Keys.TAB + str(start_date.month) + str(start_date.day))
        # driver.find_element(By.NAME, "b_end").clear()
        driver.find_element(By.NAME, "b_end").send_keys(str(end_date.year) + Keys.TAB + str(end_date.month) + str(end_date.day))

        # driver.find_element(By.NAME, "b_matype").clear()
        driver.find_element(By.NAME, "b_matype").click()
        driver.find_element(By.NAME, "b_matype").send_keys(Keys.UP + Keys.ENTER)

        # driver.find_element(By.NAME, "b_entrymode").clear()
        driver.find_element(By.NAME, "b_entrymode").click()
        driver.find_element(By.NAME, "b_entrymode").send_keys(Keys.DOWN + Keys.DOWN + Keys.ENTER)

        driver.find_element(By.XPATH, "//div[@class='backtestFormButtonContainer']//button[1]").click()

        # input("Press Enter to continue manually...")

        wait = WebDriverWait(driver, 25)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), 'Total ROI:')]/following-sibling::td[1]")))

        total_roi = driver.find_element(By.XPATH, "//td[contains(text(), 'Total ROI:')]/following-sibling::td[1]").text

        print(total_roi.split(' ')[0])
        return float(total_roi.split(' ')[0])
    except:
        return 0
