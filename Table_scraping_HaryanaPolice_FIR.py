from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup as BSoup
import time
import pandas as pd
import csv
url = "https://haryanapoliceonline.gov.in/ViewFIR/FIRStatusSearch.aspx?From=LFhlihlx%2fW49VSlBvdGc4w%3d%3d%2f"
driver = webdriver.Chrome(executable_path='C:/webdrivers/chromedriver.exe')
year = 2016
district = 13223
police_station = 13223015
driver.get(url)

#choosing the year from dropdown

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//select[@name='ctl00$ContentPlaceHolder1$ddFIRYear']/option[@value='"+str(year)+"']"))
)
element.click()

#choosing the District by value from dropdown

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//select[@name='ctl00$ContentPlaceHolder1$ddlDistrict']/option[@value='"+str(district)+"']"))
)
element.click()

#choosing the Police Station by value from dropdown

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//select[@name='ctl00$ContentPlaceHolder1$ddlPoliceStation']/option[@value='"+str(police_station)+"']"))
)
element.click()

#clicking the search button

driver.find_element_by_id('ContentPlaceHolder1_btnStatusSearch').click()
time.sleep(5)

page = driver.page_source
soup = BSoup(page, 'html.parser')
data = []
#To get all rows inside the body without headrow
table = soup.find('table', class_="datatable").tbody
rows = table.find_all('tr')

#To get headrow of a table

headrow = soup.find('table', class_="datatable").thead
headr = headrow.find_all('tr')
for row in headr:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])
driver.quit()

# converting into pandas dataframe

dftable = pd.DataFrame(data[1:], columns=data[0])
print(dftable)
dftable.to_csv (r'C:\Users\uttam\Desktop\python\export_dataframe.csv', index = False, header=True)