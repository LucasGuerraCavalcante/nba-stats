from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

chrome_options = Options()
# chrome_options.headless = True

driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)
# w_wait = WebDriverWait(driver, 10)

driver.get("https://www.nba.com/stats/teams/traditional/?sort=W_PCT&dir=-1")

page_html = driver.page_source

# w_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nba-stat-table")))

soup = BeautifulSoup(page_html, 'lxml')
table = soup.find('table')

html_table_headers = table.find('thead').findChild('tr').findChildren('th', limit=28) # Ta pegando headers com hidden

# print(html_table_headers)

data_frame_columns = []

for header in html_table_headers:
    data_frame_columns.append(header.get_text().strip())
    
# print(html_table_headers)

html_table_rows = table.find('tbody').find_all("tr")

# print(html_table_rows)

data_frame_rows = []

for tr in html_table_rows:
		row = []
  
		for td in tr.findChildren('td'):
				cell_text = td.get_text().strip()
				row.append(cell_text)
    
		data_frame_rows.append(row)
  
data_frame = pd.DataFrame(data_frame_rows, columns=data_frame_columns)

print(data_frame)

# data_frame.to_excel('nba_stats.xlsx')

driver.close()
