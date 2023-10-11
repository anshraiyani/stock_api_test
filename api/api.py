from flask import Flask, jsonify, request
import json
import csv
import os

app = Flask(__name__)

@app.route('/stocks/<string:symbol>', methods=['GET'])
def get_stock(symbol):
    temp_names=os.listdir("data/")
    stock_names=[temp_names[i].lower().split('.')[0].split('_stockdata')[0] for i in range(len(temp_names))]
    if symbol in stock_names:
        stock_data=[]
        with open(f'data/{symbol.upper()}_STOCKDATA.csv','r') as f:
            reader=csv.DictReader(f)
            for row in reader:
                stock_data.append({'date':row['date'],'time':row['time'],'name':row['name'],'value':row['value']})
        return jsonify(stock_data)
    else:
        return "Stock not found", 404

if __name__ == '__main__':
    app.run(debug=True)