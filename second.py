import time
import pickle
import datetime
import os
import glob
import csv
import xlrd
import pandas as pd
import datetime

from xlsxwriter.workbook import Workbook

today = datetime.datetime.today()

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
with open('output.csv', 'w', encoding = "mbcs") as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow({'Investor Name', 'Announced Date'})
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
                            print(name+" "+in_data[k][2])
                            spamwriter.writerow({name, in_data[k][2]})

