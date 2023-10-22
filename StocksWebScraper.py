from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

# Change the stock symbol to the desired one; currently set to the S&P 500
stock_symbol = '^GSPC'
url = f'https://finance.yahoo.com/quote/{stock_symbol}/history?period1=-1325635200&period2=1691366400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'

driver = webdriver.Chrome()
driver.get(url)

dates = []
historical_data = []

try:
    # Currently set to scroll 3 times- adjust based on how many days worth of data are needed
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table_dates = soup.find_all(class_='Py(10px) Ta(start) Pend(10px)')
        table_data = soup.find_all(class_='Py(10px) Pstart(10px)')
        table_dates_values = [value.text.strip() for value in table_dates]
        table_data_values = [value.text.strip() for value in table_data]
        dates.extend([date for date in table_dates_values])
        dates_incrementer = 0
        for i in range(0, len(table_dates_values), 6):
            historical_data.extend([[dates[dates_incrementer]] + table_data_values[i : i + 6]])
            dates_incrementer += 1

except Exception as e:
    print("Failed to fetch the web page:", e)

driver.quit()

# Put the data into a table; however, at this point, the code can instead be modified to calculate other factors
df = pd.DataFrame(historical_data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
df = df.sort_values(by = 'Date')
print(df.to_string(index = False))