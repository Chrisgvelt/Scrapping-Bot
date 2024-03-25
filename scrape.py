import time
import pickle
import datetime
import os
import glob
import csv
import xlrd
import pandas as pd
import datetime
import requests
import json
import schedule
import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as Actions
from xlsxwriter.workbook import Workbook

def job():
    print("Hello, world!")

history = []

def updateData():
    api_url = 'https://api.airtable.com/v0/app3x8SwYo15yBTYu/tbl5siFiCvzMKsyUC'
    headers = {"Content-Type": "application/json", "Authorization": "Bearer pat0VYxeI4xFmfQef.15bd44d6c1545c096c0f0a95713c710d31d099c083286e86081cc9630236383c"}

    # Google Chrome Webdriver 
    driver_chrome = webdriver.Chrome()  
    # maximize the browser
    # driver_chrome.maximize_window()
    # set the url for scrapping
    driver_chrome.get('https://www.renthop.com/account/login?fwd=%2Faccount%2Flistings_bank')
    time.sleep(3)

    # login operation
    email = driver_chrome.find_element(By.CSS_SELECTOR, "[type = 'text']")
    email.send_keys("clients@masterkey.nyc")
    submit = driver_chrome.find_element(By.CSS_SELECTOR, "[type = 'submit']")
    submit.click()
    time.sleep(3)

    password = driver_chrome.find_element(By.CSS_SELECTOR, "[type = 'password']")
    password.send_keys("masterkey24")
    login = driver_chrome.find_element(By.ID, "login-2-button")
    login.click()
    time.sleep(3)

    count = 0

    with open('output.csv', 'w', encoding = "mbcs") as csvfile:
        # spamwriter = csv.writer(csvfile)

        for i in range(64):
            print("page", i + 1)
            driver_chrome.get('https://www.renthop.com/account/listings_bank?max_price=100000&areas=new-york-ny&status=88&usernames%5B0%5D=takumi%40renthop.com&usernames%5B1%5D=openlistingbank%40brokersnyc.com&page=' + str(i + 1) + '&sort=hopscore')
            time.sleep(2)
            
            agent_list = driver_chrome.find_element(By.ID, "search-results-list").find_elements(By.CLASS_NAME, "listing-entry")
            # .find_elements(By.CLASS_NAME, "listing-entry")
            print(len(agent_list))

            for j in range(len(agent_list)):

                # print(agent_list[j].text)

                count += 1
                # spamwriter.writerow({'Item' + str(count)})
                address = agent_list[j].find_element(By.XPATH, "./*[1]/*[2]/*[1]/*[1]")
                # spamwriter.writerow({address.text})
                
                location = agent_list[j].find_element(By.XPATH, "./*[1]/*[2]/*[1]/*[2]")
                # spamwriter.writerow({location.text})

                price = agent_list[j].find_element(By.XPATH, "./*[1]/*[2]/*[2]/*[1]")
                # spamwriter.writerow({price.text})
                
                rooms = agent_list[j].find_element(By.XPATH, "./*[1]/*[2]/*[2]/*[2]")
                # spamwriter.writerow({rooms.text})

                name = agent_list[j].find_element(By.XPATH, "./*[1]/*[2]/*[3]/*[1]")
                # spamwriter.writerow({name.text})
                
                phone= agent_list[j].find_element(By.XPATH, "./*[1]/*[2]/*[4]/*[1]")
                # spamwriter.writerow({phone.text})

                sheet = agent_list[j].find_element(By.XPATH, "./*[3]/*[1]/*[2]/*[1]")
                # spamwriter.writerow({sheet.get_attribute('href')})

                data = {
                    "fields": {
                        "Address": address.text,
                        "Location": location.text,
                        "Price": price.text,
                        "Rooms": rooms.text,
                        "Name": name.text,
                        "Phone": phone.text,
                        "Sheet": sheet.get_attribute('href')
                    }
                }
                print(data in history)

                if data in history :
                    break
    
                history.append(data)

                response = requests.post(api_url, headers=headers, json=data)
                print("data: ", response.json())

            if j < len(agent_list) - 1 :
                break




schedule.every().day.do(job)

updateData()

updateData()

while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep for 1 second to avoid high CPU usage




#     for j in range(711):
#         print(j + 1)
#         count = 20
#         for i in range(count): 
#             next_btn = driver_chrome.find_elements(By.CLASS_NAME, "pagination_pagNextButton__PT8dW")[0]
#             for k in range(j):
#                 next_btn.click()
#                 time.sleep(1)
#             driver_chrome.execute_script("window.scrollTo(0, document.body.scrollTop);")
#             time.sleep(1)

#             agent_list = driver_chrome.find_elements(By.CLASS_NAME, "memberGrid_membersTab__zHE_h")[i]
#             agent_list.find_elements(By.CSS_SELECTOR, "*")[0].click()
#             time.sleep(5)

#             email = driver_chrome.find_element(By.CLASS_NAME, "peoplePage_headerInformation__vqNIG").find_elements(By.CSS_SELECTOR, "*")[1]
#             spamwriter.writerow({email.text})
#             print(email.text)

#             driver_chrome.get('https://www.rebny.com/members/')
#             time.sleep(5)

        