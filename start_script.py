import subprocess

process1=subprocess.Popen(["python","scraper/stock_scrapper.py"])
process2=subprocess.Popen(["python","api/api.py"])