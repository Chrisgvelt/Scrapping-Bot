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

# Google Chrome Webdriver 
driver_chrome = webdriver.Chrome()  
# maximize the browser
driver_chrome.maximize_window()
# set the url for scrapping
driver_chrome.get('https://www.myrebny.com/s/login/?startURL=%2Fidp%2Flogin%3Fapp%3D0sp3s000000TNJ9%26SAMLRequest%3DnVNNj9owEP0rke%252FkA1AFFgFRUFWq7TaCtIdeKseZ7Frr2K7H2cC%252FrxPILocuB3KJNPPy3rw3k8XqWMvgFSwKrVKShDFZLRfIamnounHPag9%252FG0AXeJhC2jdS0lhFNUOBVLEakDpOD%252BvvD3QcxtRY7TTXkgS7bUr%252BzPi0LOacwyyZVJNxUcUJI8GvQdB%252F4YGIDewUOqacL8Xj6ShORsk4T6Y0ntA4CWfzT79JkF2oPwtVCvV0e47iDEL6Nc%252BzUfbjkJNg650IxVwv%252FeycQRpFbduG9clCoU4h13UkShNJ%252FSTUihmTxmgmGPdP%252FvhtToI1ItiOYaMVNjXYA9hXweHn%252FuGdkxkRvjP2bBFnUhaMv5BzvrR3ba%252BCve2HDbpkOahYYNI7Yg4KzWypKwXtSdsXbyfErlVpy6EbYRFdSQ77ffQau22mpeCne%252Fb7RduauY%252FRSZj0FVGOqh5KG4UGuKgElD5IKXW78R4cpMTZBkg0THY5Oij7E%252FRBOzjedYIbXRtmBXb7hiPjbgj%252FmngjfbZ7qO5ZxU0Yp7yj9uXMv1pty%252B6CgXtjuWU%252BC23dZTP%252Fm2d57n0Qx1v3%252Bjdd%252FgM%253D')
time.sleep(3)

# login operation
email = driver_chrome.find_element(By.CSS_SELECTOR, "[type = 'text']")
email.send_keys("Ileone@corcoran.com")
password = driver_chrome.find_element(By.CSS_SELECTOR, "[type = 'password']")
password.send_keys("Ignazio310")
login = driver_chrome.find_element(By.CSS_SELECTOR, "[type = 'button']")
login.click()   
time.sleep(3)
driver_chrome.get('https://www.rebny.com/members/')
time.sleep(5)
# agent_list = driver_chrome.find_elements(By.CLASS_NAME, "memberGrid_membersTab__zHE_h")
# print(agent_list)

emails = []

for j in range(711):
    count = 20
    for i in range(count):
        next_btn = driver_chrome.find_elements(By.CLASS_NAME, "pagination_pagNextButton__PT8dW")[0]
        for k in range(j):
            next_btn.click()
            time.sleep(1)
        driver_chrome.execute_script("window.scrollTo(0, document.body.scrollTop);")
        time.sleep(1)

        agent_list = driver_chrome.find_elements(By.CLASS_NAME, "memberGrid_membersTab__zHE_h")[i]
        agent_list.find_elements(By.CSS_SELECTOR, "*")[0].click()
        time.sleep(5)

        email = driver_chrome.find_element(By.CLASS_NAME, "peoplePage_headerInformation__vqNIG").find_elements(By.CSS_SELECTOR, "*")[1]
        emails.append(email.text)
        print(email.text)

        driver_chrome.get('https://www.rebny.com/members/')
        time.sleep(5)


with open('emails.csv', 'w', encoding = "mbcs") as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow({'Emails'})
    for i in range(len(emails)):
        spamwriter.writerow({emails[i]})
        