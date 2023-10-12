# pip install requests
# pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup as bs
import time
import schedule
import csv
import logging
import sys
import os
from requests.exceptions import ConnectionError
from pymongo import MongoClient


def save_to_mongodb(date,time,name, value):
    try:
        client = MongoClient("mongodb+srv://admin:admin@cluster0.l1slcdl.mongodb.net/")  # Replace with your MongoDB connection URI
        db = client["stock-data"] 
        collection = db["data"]  
        document = {
            "date": date,
            "time": time,
            "name": name,
            "value": value
        }
        collection.insert_one(document)
        print(f"Data saved to MongoDB")
    except Exception as e:
        logging.error("MongoDB Error:", exc_info=True)

def getStockData(url):
    try:
        r = requests.get(url)
    except ConnectionError:
        logging.error("REQUEST ERROR: ",exc_info=True)
        sys.exit()
    
    try:
        logging.info("Scraping HTML")
        soup = bs(r.content,'html.parser')
        stockName=soup.find('div',{'class':'zzDege'}).text.replace(' ','_').upper()
        curr_value = float(soup.find('div',{'class':'YMlKec fxKbKc'}).text.replace(',','').replace('₹',''))
        # time=time.strftime('%H:%M:%S')
        # date=time.strftime('%d-%m-%Y')
    except :
        logging.error("SOUP ERROR: ",exc_info=True)
        sys.exit()

    try:
        logging.info("Writing data to file")
        db_date=time.strftime('%d-%m-%Y')
        db_time=time.strftime('%H:%M:%S')
        save_to_mongodb(db_date,db_time,stockName,curr_value)
        fieldnames=['date','time','name','value'] 
        data_file=os.listdir('data/')
        if(f'{stockName}_STOCKDATA.csv' not in data_file):
            with open(f'data/{stockName}_STOCKDATA.csv',mode='w',newline='') as csvFile:
                writer=csv.DictWriter(csvFile,fieldnames=fieldnames)
                writer.writeheader()
        else:
            with open(f'data/{stockName}_STOCKDATA.csv',mode='a',newline='') as csvFile:
                writer=csv.DictWriter(csvFile,fieldnames=fieldnames)
                writer.writerow({"date":db_date,"time":db_time,"name":stockName,"value":curr_value})
                print(stockName,curr_value,db_date,db_time)
    except:
        logging.error("FILE ERROR: ",exc_info=True)
        sys.exit()


url='https://www.google.com/finance/quote/NIFTY_50:INDEXNSE'
# url='https://www.google.com/finance/quote/RELIANCE:NSE'

logging.basicConfig(level=logging.INFO,filename="log/log.log",filemode='w', format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("scheduling scraping for every 5 seconds")

schedule.every(5).seconds.do(getStockData,url)

while True:
    schedule.run_pending()