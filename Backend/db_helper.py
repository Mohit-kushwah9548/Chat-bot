# # import mysql.connector
# import pymysql
# import os
# from dotenv import load_dotenv
#
# load_dotenv()  # Load .env for local development
#
# # Environment variables (set in .env or Render dashboard)
# DB_HOST = os.environ.get("DB_HOST")        # e.g. "aws.connect.psdb.io"
# DB_USER = os.environ.get("DB_USER")        # e.g. "your_user"
# DB_PORT = int(os.getenv("DB_PORT", 3306))
# DB_PASSWORD = os.environ.get("DB_PASSWORD")# e.g. "your_password"
# DB_NAME = os.environ.get("DB_NAME")
#
# # cnx = pymysql.connect(
# #     host="localhost",
# #     user="root",
# #     password='9917050240',
# #     database='pandeyji_eatery'
# # )
# cnx = pymysql.connect(
#     host=DB_HOST,
#     user=DB_USER,
#     port=DB_PORT,
#     password=DB_PASSWORD,
#     database=DB_NAME,
#     ssl={"ssl": {}}  # Required for some hosted DBs like PlanetScale
# )
# print("Database connected !")
# # cnx = mysql.connector.connect(
# #     host='localhost',
# #     user='root',
# #     password='9917050240',
# #     port='3306',
# #     database='pandeyji_eatery'
# #
# # )
#
# # Function to call the MySQL stored procedure and insert an order item
# def insert_order_item(food_item, quantity, order_id):
#     try:
#         cursor = cnx.cursor()
#
#         # Calling the stored procedure
#         cursor.callproc('insert_order_item', (food_item, quantity, order_id))
#
#         # Committing the changes
#         cnx.commit()
#
#         # Closing the cursor
#         cursor.close()
#
#         print("Order item inserted successfully!")
#
#         return 1
#
#     # except mysql.connector.Error as err:
#     #     print(f"Error inserting order item: {err}")
#
#         # Rollback changes if necessary
#         cnx.rollback()
#
#         return -1
#
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         # Rollback changes if necessary
#         cnx.rollback()
#
#         return -1
#
# def get_total_order_price(order_id):
#     cursor = cnx.cursor()
#
#     # Executing the SQL query to get the total order price
#     query = f"SELECT get_total_order_price({order_id})"
#     cursor.execute(query)
#
#     # Fetching the result
#     result = cursor.fetchone()[0]
#
#     # Closing the cursor
#     cursor.close()
#
#     return result
#
# # Function to insert a record into the order_tracking table
# def insert_order_tracking(order_id, status):
#     cursor = cnx.cursor()
#
#     # Inserting the record into the order_tracking table
#     insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
#     cursor.execute(insert_query, (order_id, status))
#
#     # Committing the changes
#     cnx.commit()
#
#     # Closing the cursor
#     cursor.close()
#
# # Function to get the next available order_id
# def get_next_order_id():
#     cursor = cnx.cursor()
#
#     # Executing the SQL query to get the next available order_id
#     query = "SELECT MAX(order_id) FROM orders"
#     cursor.execute(query)
#
#     # Fetching the result
#     result = cursor.fetchone()[0]
#
#     # Closing the cursor
#     cursor.close()
#
#     # Returning the next available order_id
#     if result is None:
#         return 1
#     else:
#         return result + 1
#
# # Function to fetch the order status from the order_tracking table
# def get_order_status(order_id):
#     cursor = cnx.cursor()
#
#     # Executing the SQL query to fetch the order status
#     query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
#     cursor.execute(query)
#
#     # Fetching the result
#     result = cursor.fetchone()
#
#     # Closing the cursor
#     cursor.close()
#
#     # Returning the order status
#     if result:
#         return result[0]
#     else:
#         return None

import os
from dotenv import load_dotenv
from pymongo import MongoClient

from pymongo.errors import ConnectionFailure

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

def get_db():
    try:
        client = MongoClient(MONGO_URI)
        # Try to connect to server
        client.admin.command('ping')
        print("MongoDB connected successfully!")
        db = client.get_database()  # gets the default db from URI
        return db
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        return None

# Example function to insert an order item
def insert_order_item(food_item, quantity, order_id):
    db = get_db()
    if db is None:
        return -1

    try:
        order_items_collection = db.order_items  # Collection name
        order_item_doc = {
            "food_item": food_item,
            "quantity": quantity,
            "order_id": order_id
        }
        result = order_items_collection.insert_one(order_item_doc)
        print(f"Inserted order item with id: {result.inserted_id}")
        return 1
    except Exception as e:
        print(f"Error inserting order item: {e}")
        return -1

# Example function to get total order price (assuming you store prices)
def get_total_order_price(order_id):
    db = get_db()
    if db is None:
        return None

    try:
        order_items_collection = db.order_items
        # Let's say each document has a "price" field
        pipeline = [
            {"$match": {"order_id": order_id}},
            {"$group": {"_id": "$order_id", "total_price": {"$sum": {"$multiply": ["$quantity", "$price"]}}}}
        ]
        result = list(order_items_collection.aggregate(pipeline))
        if result:
            return result[0]["total_price"]
        return 0
    except Exception as e:
        print(f"Error calculating total price: {e}")
        return None

# Example usage
if __name__ == "__main__":
    insert_order_item("Pizza", 2, 123)
    total_price = get_total_order_price(123)
    print("Total order price:", total_price)
