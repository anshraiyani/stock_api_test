from pymongo import MongoClient
import time

def save_to_mongodb(stock_name, curr_value):
    # try:
        client = MongoClient("mongodb+srv://admin:admin@cluster0.l1slcdl.mongodb.net/")  # Replace with your MongoDB connection URI
        db = client["stock-data"]  # Replace with your database name
        collection = db["data"]  # Replace with your collection name
        document = {
            "date": time.strftime('%d-%m-%Y'),
            "time": time.strftime('%H:%M:%S'),
            "name": stock_name,
            "value": curr_value
        }
        collection.insert_one(document)
        print(f"Data saved to MongoDB")
    # except Exception as e:
        # logging.error("MongoDB Error:", exc_info=True)

# After processing the data, call the function to save it to MongoDB
save_to_mongodb("Adani", 19.6)
