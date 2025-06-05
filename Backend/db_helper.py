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

# import os
# from dotenv import load_dotenv
# from pymongo import MongoClient
#
# from pymongo.errors import ConnectionFailure
#
# load_dotenv()
#
# MONGO_URI = os.getenv("MONGO_URI")
#
# def get_db():
#     try:
#         client = MongoClient(MONGO_URI)
#         # Try to connect to server
#         client.admin.command('ping')
#         print("MongoDB connected successfully!")
#         db = client.get_database()  # gets the default db from URI
#         return db
#     except ConnectionFailure as e:
#         print(f"Could not connect to MongoDB: {e}")
#         return None
#
# # Example function to insert an order item
# def insert_order_item(food_item, quantity, order_id):
#     db = get_db()
#     if db is None:
#         return -1
#
#     try:
#         order_items_collection = db.order_items  # Collection name
#         order_item_doc = {
#             "food_item": food_item,
#             "quantity": quantity,
#             "order_id": order_id
#         }
#         result = order_items_collection.insert_one(order_item_doc)
#         print(f"Inserted order item with id: {result.inserted_id}")
#         return 1
#     except Exception as e:
#         print(f"Error inserting order item: {e}")
#         return -1
#
# # Example function to get total order price (assuming you store prices)
# def get_total_order_price(order_id):
#     db = get_db()
#     if db is None:
#         return None
#
#     try:
#         order_items_collection = db.order_items
#         # Let's say each document has a "price" field
#         pipeline = [
#             {"$match": {"order_id": order_id}},
#             {"$group": {"_id": "$order_id", "total_price": {"$sum": {"$multiply": ["$quantity", "$price"]}}}}
#         ]
#         result = list(order_items_collection.aggregate(pipeline))
#         if result:
#             return result[0]["total_price"]
#         return 0
#     except Exception as e:
#         print(f"Error calculating total price: {e}")
#         return None
#
# # Example usage
# if __name__ == "__main__":
#     insert_order_item("Pizza", 2, 123)
#     total_price = get_total_order_price(123)
#     print("Total order price:", total_price)

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from datetime import datetime

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


def get_db():
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command('ping')
        db = client.get_database()  # default DB from URI
        return db
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        return None


def generate_order_id():
    # Use MongoDB ObjectId as order ID (string)
    return str(ObjectId())


def insert_order(order_dict: dict, user_info: dict = None):
    """
    Save order metadata + items to DB
    order_dict: {food_item: quantity, ...}
    user_info: optional dict with user details like {"name":..., "email":...}
    Returns order_id string or None on failure
    """
    db = get_db()
    if db is None:
        return None

    try:
        order_id = generate_order_id()
        orders_col = db.orders
        order_items_col = db.order_items

        # Insert order metadata
        order_doc = {
            "_id": ObjectId(order_id),
            "user_info": user_info or {},
            "status": "in progress",
            "created_at": datetime.utcnow()
        }
        orders_col.insert_one(order_doc)

        # Insert items
        items_docs = []
        for food_item, quantity in order_dict.items():
            items_docs.append({
                "order_id": ObjectId(order_id),
                "food_item": food_item,
                "quantity": quantity,
                # You can add price here if known, or fetch from another collection
            })

        if items_docs:
            order_items_col.insert_many(items_docs)

        return order_id
    except Exception as e:
        print(f"Error inserting order: {e}")
        return None


def get_total_order_price(order_id: str):
    """
    Aggregate total price for the order by summing quantity * price
    Assumes `price` field exists in order_items documents.
    Returns total price as float or 0 if none, or None on error.
    """
    db = get_db()
    if db is None:
        return None

    try:
        order_items_col = db.order_items
        pipeline = [
            {"$match": {"order_id": ObjectId(order_id)}},
            {"$group": {
                "_id": "$order_id",
                "total_price": {"$sum": {"$multiply": ["$quantity", "$price"]}}
            }}
        ]
        result = list(order_items_col.aggregate(pipeline))
        if result:
            return result[0].get("total_price", 0)
        return 0
    except Exception as e:
        print(f"Error calculating total price: {e}")
        return None


def get_order_status(order_id: str):
    """
    Returns order status string or None if not found
    """
    db = get_db()
    if db is None:
        return None

    try:
        orders_col = db.orders
        order = orders_col.find_one({"_id": ObjectId(order_id)})
        if order:
            return order.get("status", None)
        return None
    except Exception as e:
        print(f"Error fetching order status: {e}")
        return None


def update_order_status(order_id: str, status: str):
    """
    Updates order status to the given value
    """
    db = get_db()
    if db is None:
        return False

    try:
        orders_col = db.orders
        result = orders_col.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": status}})
        return result.modified_count > 0
    except Exception as e:
        print(f"Error updating order status: {e}")
        return False

