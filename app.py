from flask import Flask,request,jsonify
import json
import pymysql

app=Flask(__name__)

def db_connection():
    conn=None
    try:
        conn=pymysql.connect(host= 'sql12.freesqldatabase.com',
                            database= 'sql12656564',
                            user= 'sql12656564',
                            password= 'dH6g8QdaVS',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    except pymysql.error as e:
        print(e)
    return conn

@app.route('/stocks', methods=["GET","POST","DELETE"])
def getData():
    conn=db_connection()
    cursor=conn.cursor()
    if(request.method=="GET"):
        cursor.execute("SELECT * FROM stock")
        stocks=[
            dict(id=row['id'],date=row['date'],name=row['name'],open=row['open'],high=row['high'],low=row['low'],close=row['close'])
            for row in cursor.fetchall()
        ]
        if stocks is not None:
            return jsonify(stocks)
    if(request.method=="POST"):
        date=request.form.get("date")
        name=request.form.get("name")
        open_price=request.form.get("open")
        high=request.form.get("high")
        low=request.form.get("low")
        close=request.form.get("close")
        
        sql=""" INSERT INTO stock (date,name,open,high,low,close) VALUES (%s, %s, %s, %s, %s, %s) """
        cursor.execute(sql,(date,name,open_price,high,low,close))
        conn.commit()
        return f"stock with id: {cursor.lastrowid} created successfully"
    if(request.method=="DELETE"):
        stock_id=request.form.get("id")
        sql="""DELETE FROM stock WHERE id=%s"""
        cursor.execute(sql,(stock_id,))
        conn.commit()
        return f"stock with id: {stock_id} deleted successfully"


@app.route('/<string:name>', methods=["GET"])
def stock(name):
    conn=db_connection()
    cursor=conn.cursor()
    if(request.method=="GET"):
        cursor.execute("SELECT * FROM stock WHERE name=%s",(name,))
        stocks=[
            dict(id=row['id'],date=row['date'],name=row['name'],open=row['open'],high=row['high'],low=row['low'],close=row['close'])
            for row in cursor.fetchall()
        ]
        if stocks is not None:
            return jsonify(stocks)

if __name__=="__main__":
    app.run()