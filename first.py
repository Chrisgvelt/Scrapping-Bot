import time
import pickle
import datetime
import os
import glob
import csv
import xlrd
import pandas as pd
import datetime

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as Actions
from xlsxwriter.workbook import Workbook

today = datetime.datetime.today()

# function to calc the end of the date loop and end of month
def is_end(year, month, day):
    if(year == 2020 and month == 2 and day == 30):
        return True
    if(year == 2019 and month == 2 and day == 29):
        return True
    if(month == 4 and day == 31):
        return True
    if(month == 6 and day == 31):
        return True
    if(month == 9 and day == 31):
        return True
    if(month == 11 and day == 31):
        return True
    if(year == today.year and month > today.month):
        return True
    if(year == today.year and month == today.month and day > today.day):
        return True

# Google Chrome Webdriver 
driver_chrome = webdriver.Chrome()  
# maximize the browser
driver_chrome.maximize_window()
# set the url for scrapping
driver_chrome.get('https://www.crunchbase.com/login?redirect_to=%2Flists%2Frecent-funding-rounds%2Ff535c118-e157-443a-bb64-46bff7dfbe40%2Ffunding_rounds')

# wait while the website is loading
try: 
    element = wait(driver_chrome, 1).until(
        EC.presence_of_element_located((By.ID, "you can't find id"))
    )        
finally:
    # recaptcha operation
    # recaptcha = driver_chrome.find_elements_by_css_selector("body>section>.content-wrapper>div>div>iframe")[0]
    # print(recaptcha)
    # ActionChains(driver_chrome).move_to_element(recaptcha).perform()
    # ActionChains(driver_chrome).click_and_hold(recaptcha).perform()
    # try:
    #     element = wait(driver_chrome, 40).until(
    #         EC.presence_of_element_located((By.ID, "mat-input-1"))
    #     )
    # finally:        
        # login operation
        email = driver_chrome.find_elements_by_css_selector("[type = 'email']")[0]
        email.send_keys("diana@voyajoy.com")
        password = driver_chrome.find_elements_by_css_selector("[type = 'password']")[0]
        password.send_keys("6181crunchbase")
        login = driver_chrome.find_elements_by_css_selector("[type = 'submit']")[0]
        login.click()

        # wait while the website is loading
        try: 
            element = wait(driver_chrome, 10).until(
                EC.presence_of_element_located((By.ID, "you can't find id"))
            )        
        finally:
            # column operation
            column = driver_chrome.find_elements_by_css_selector("[key='columns']")[0]
            column.click()            
            funding_type = driver_chrome.find_elements_by_css_selector(".panelWrapper.activePanel1>div")[1].find_elements_by_css_selector("mat-nav-list>checkbox")[1].find_elements_by_css_selector("mat-checkbox>label")[0]
            money_raised = driver_chrome.find_elements_by_css_selector(".panelWrapper.activePanel1>div")[1].find_elements_by_css_selector("mat-nav-list>checkbox")[3].find_elements_by_css_selector("mat-checkbox>label")[0]
            funding_type.click()
            money_raised.click()
            funded_organization = driver_chrome.find_elements_by_css_selector(".panelWrapper.activePanel1>div")[0].find_elements_by_css_selector("mat-nav-list>mat-list-item")[1]
            funded_organization.click()
            organization_name = driver_chrome.find_elements_by_css_selector(".panelWrapper.activePanel1>div")[1].find_elements_by_css_selector("mat-nav-list>checkbox")[0].find_elements_by_css_selector("mat-checkbox>label")[0]
            organization_name.click()            
            investors = driver_chrome.find_elements_by_css_selector(".panelWrapper.activePanel1>div")[0].find_elements_by_css_selector("mat-nav-list>mat-list-item")[2]
            investors.click()
            number_investors = driver_chrome.find_elements_by_css_selector(".panelWrapper.activePanel1>div")[1].find_elements_by_css_selector("mat-nav-list>checkbox")[2].find_elements_by_css_selector("mat-checkbox>label")[0]
            number_investors.click()
            investor_names = driver_chrome.find_elements_by_css_selector(".panelWrapper.activePanel1>div")[1].find_elements_by_css_selector("mat-nav-list>checkbox")[1].find_elements_by_css_selector("mat-checkbox>label")[0]
            investor_names.click()
            apply = driver_chrome.find_elements_by_css_selector("mat-dialog-actions>div>button")[0]
            apply.click()

            # date loop            
            for year in range(2019,2021):
                for month in range(1,13):
                    for day in range(1,32):
                        if(is_end(year, month, day) == True):
                            break                    
                        cur_date = str(year)+"/"+str(month)+"/"+str(day)
                        print(cur_date)
                        # date filter operation
                        filter_type = driver_chrome.find_elements_by_css_selector(".component--operators>mat-form-field>div>div")[0]
                        filter_type.click()
                        equals = driver_chrome.find_elements_by_css_selector(".mat-select-panel>.mat-option")[2]
                        equals.click()
                        date = driver_chrome.find_elements_by_css_selector(".component--text-input>mat-form-field>div>div>div>input")[0]
                        date.clear()
                        date.send_keys(cur_date)
                        
                        # export to csv individually operation
                        export_csv = driver_chrome.find_elements_by_css_selector("export-csv-button>button")[0]
                        export_csv.click()
                        time.sleep(2)
                        continue_limit = driver_chrome.find_elements_by_css_selector("mat-dialog-actions>div>button")
                        if(len(continue_limit)>0):
                            continue_limit[1].click()

workbook = Workbook('output.xlsx')
worksheet = workbook.add_worksheet()

# Individual csv file into google spreadsheet                            
home = os.path.expanduser("~")
basic_path = os.path.join(home, "Downloads")

addr_array = []
for i in range(0,101):
    if(i == 0):
        input_file_addr = "recent-funding-rounds-"+str(today.month)+"-"+str(today.day)+"-"+str(today.year)+".csv"
    else:
        input_file_addr = "recent-funding-rounds-"+str(today.month)+"-"+str(today.day)+"-"+str(today.year)+"("+str(i)+").csv"
    input_file_addr = os.path.join(basic_path, input_file_addr)
    addr_array.append(input_file_addr)

count = 0
for file in os.listdir(basic_path):
    if file.endswith(".csv"):
        count += 1
        if(count < 101): 
            continue
        input_file_addr = os.path.join(basic_path, file)
        addr_array.append(input_file_addr)

valid_columns = [2]
num_row = 1
for i in range(0, len(addr_array)-1):
    print(addr_array[i]+"------------------------------------------")
    for csvfile in glob.glob(addr_array[i]):  
        with open(csvfile, 'rt', encoding="mbcs") as f:
            in_data = [row for row in csv.reader(f)]
            df = pd.read_csv(addr_array[i], encoding = "ISO-8859-1", index_col = 1)
            collen = len(df)
            for k in range(2,collen+1):
                namedatas = in_data[k][3]
                if(namedatas != ''):
                    names = namedatas.split(', ')
                    for name in names:
                        value = name
                        worksheet.write(num_row,1,name)
                        num_col=2
                        for j in valid_columns:
                            worksheet.write(num_row,num_col,in_data[k][j])
                            num_col += 1
                        num_row += 1

