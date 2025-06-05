#
# from fastapi import FastAPI
# from fastapi import Request
# from fastapi.responses import JSONResponse
#
# # from Backend import generic_helper, db_helper
# import generic_helper, db_helper
#
# app = FastAPI()
#
#
# inprogress_orders = {}
#
# @app.post("/")
# async def handle_request(request: Request):
#     # Retrieve the JSON data from the request
#     payload = await request.json()
#
#     # Extract the necessary information from the payload
#     # based on the structure of the WebhookRequest from Dialogflow
#     intent = payload['queryResult']['intent']['displayName']
#     parameters = payload['queryResult']['parameters']
#     output_contexts = payload['queryResult']['outputContexts']
#
#     session_id = generic_helper.extract_session_id(output_contexts[0]['name'])
#
#     intent_handler_dict = {
#         'order.add - context: ongoing-order': add_to_order,
#         'order.remove - context: ongoing-order': remove_from_order,
#         'order.complete - context: ongoing-order': complete_order,
#         'track.order - context: ongoing-tracking': track_order
#     }
#
#     return intent_handler_dict[intent](parameters,session_id)
#
#
# def remove_from_order(parameters: dict, session_id: str):
#     if session_id not in inprogress_orders:
#         return JSONResponse(content={
#             "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
#         })
#
#     food_items = parameters["food-item"]
#     current_order = inprogress_orders[session_id]
#
#     removed_items = []
#     no_such_items = []
#
#     for item in food_items:
#         if item not in current_order:
#             no_such_items.append(item)
#         else:
#             removed_items.append(item)
#             del current_order[item]
#
#     if len(removed_items) > 0:
#         fulfillment_text = f'Removed {",".join(removed_items)} from your order!'
#
#     if len(no_such_items) > 0:
#         fulfillment_text = f' Your current order does not have {",".join(no_such_items)}'
#
#     if len(current_order.keys()) == 0:
#         fulfillment_text += " Your order is empty!"
#     else:
#         order_str = generic_helper.get_str_from_food_dict(current_order)
#         fulfillment_text += f" Here is what is left in your order: {order_str}"
#
#     return JSONResponse(content={
#         "fulfillmentText": fulfillment_text
#     })
# def complete_order(parameters: dict, session_id: str):
#     if session_id not in inprogress_orders:
#         fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
#     else:
#         order = inprogress_orders[session_id]
#         order_id = save_to_db(order)
#         if order_id == -1:
#             fulfillment_text = "Sorry, I couldn't process your order due to a backend error. " \
#                                "Please place a new order again"
#         else:
#             order_total = db_helper.get_total_order_price(order_id)
#
#             fulfillment_text = f"Awesome. We have placed your order. " \
#                            f"Here is your order id # {order_id}. " \
#                            f"Your order total is {order_total} which you can pay at the time of delivery!"
#
#         del inprogress_orders[session_id]
#
#     return JSONResponse(content={
#         "fulfillmentText": fulfillment_text
#     })
# def save_to_db(order: dict):
#     next_order_id = db_helper.get_next_order_id()
#
#     # Insert individual items along with quantity in orders table
#     for food_item, quantity in order.items():
#         rcode = db_helper.insert_order_item(
#             food_item,
#             quantity,
#             next_order_id
#         )
#
#         if rcode == -1:
#             return -1
#
#     # Now insert order tracking status
#     db_helper.insert_order_tracking(next_order_id, "in progress")
#
#     return next_order_id
#
#
# def add_to_order(parameters: dict,session_id : str):
#     food_items = parameters['food-item']
#     quantities = parameters['number']
#
#     if len(food_items) != len(quantities):
#         fulfillment_text = "Sorry I didn't understand.Can you please specify food items and quantities clearly?"
#     else:
#         new_food_dict =  dict(zip(food_items, quantities))
#
#         if  session_id in inprogress_orders:
#             current_food_dict = inprogress_orders[session_id]
#             current_food_dict.update(new_food_dict)
#             inprogress_orders[session_id] = current_food_dict
#         else:
#             inprogress_orders[session_id] = new_food_dict
#
#         order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
#         fulfillment_text = f"So far you have: {order_str}.Do you need anything else?"
#
#     return JSONResponse(content={
#         "fulfillmentText": fulfillment_text
#     })
#
# def track_order(parameters: dict,session_id: str):
#     order_id = int(parameters['order_id'])
#     order_status = db_helper.get_order_status(order_id)
#
#     if order_status:
#         fulfillment_text = f"The order status for order id: {order_id} is:{order_status}"
#     else:
#         fulfillment_text = f"No order found with order id: {order_id}"
#
#     return JSONResponse(content={
#             "fulfillmentText": fulfillment_text
#         })

## for mongo db
# from fastapi import FastAPI, Request
# from fastapi.openapi.models import Response
# from fastapi.responses import JSONResponse, FileResponse
#
# import generic_helper, db_helper
# from fastapi.middleware.cors import CORSMiddleware
#
#
# app = FastAPI()
#
# origins = [
#     "*",  # Or specify domains you want to allow
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[" https://mohit-chatbot-53209.web.app ", "https://your-firebase-domain.firebaseapp.com"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
#
#
#
# inprogress_orders = {}
#
# # Add GET "/" route to avoid 405 error on GET requests to root
# @app.get("/")
# async def root():
#     return {"message": "Hello! This endpoint only supports POST requests for dialogflow webhook."}
#
# # Optionally serve favicon.ico to avoid 404 in browser requests
# @app.get("/favicon.ico")
# async def favicon():
#     # Put your favicon.ico file in the "static" folder in your project root
#     # and serve it here. Or return 404 if you don't have one.
#     # return FileResponse("static/favicon.ico") sataic folder not create so i use
#     return Response(status_code=204)
#
# @app.post("/")
# async def handle_request(request: Request):
#     payload = await request.json()
#     intent = payload['queryResult']['intent']['displayName']
#     parameters = payload['queryResult']['parameters']
#     output_contexts = payload['queryResult']['outputContexts']
#
#     session_id = generic_helper.extract_session_id(output_contexts[0]['name'])
#
#     intent_handler_dict = {
#         'order.add - context: ongoing-order': add_to_order,
#         'order.remove - context: ongoing-order': remove_from_order,
#         'order.complete - context: ongoing-order': complete_order,
#         'track.order - context: ongoing-tracking': track_order
#     }
#
#     if intent not in intent_handler_dict:
#         return JSONResponse(content={"fulfillmentText": f"Sorry, I don't understand the intent '{intent}'."})
#
#     return intent_handler_dict[intent](parameters, session_id)
#
#
# def remove_from_order(parameters: dict, session_id: str):
#     if session_id not in inprogress_orders:
#         return JSONResponse(content={
#             "fulfillmentText": "I'm having trouble finding your order. Sorry! Can you place a new order please?"
#         })
#
#     food_items = parameters["food-item"]
#     current_order = inprogress_orders[session_id]
#
#     removed_items = []
#     no_such_items = []
#
#     for item in food_items:
#         if item not in current_order:
#             no_such_items.append(item)
#         else:
#             removed_items.append(item)
#             del current_order[item]
#
#     fulfillment_text = ""
#     if len(removed_items) > 0:
#         fulfillment_text += f'Removed {", ".join(removed_items)} from your order! '
#
#     if len(no_such_items) > 0:
#         fulfillment_text += f'Your current order does not have {", ".join(no_such_items)}. '
#
#     if len(current_order.keys()) == 0:
#         fulfillment_text += "Your order is empty!"
#     else:
#         order_str = generic_helper.get_str_from_food_dict(current_order)
#         fulfillment_text += f"Here is what is left in your order: {order_str}"
#
#     return JSONResponse(content={
#         "fulfillmentText": fulfillment_text
#     })
#
#
# def complete_order(parameters: dict, session_id: str):
#     if session_id not in inprogress_orders:
#         fulfillment_text = "I'm having trouble finding your order. Sorry! Can you place a new order please?"
#     else:
#         order = inprogress_orders[session_id]
#         order_id = save_to_db(order)
#         if order_id == -1:
#             fulfillment_text = "Sorry, I couldn't process your order due to a backend error. Please place a new order again"
#         else:
#             order_total = db_helper.get_total_order_price(order_id)
#             fulfillment_text = (
#                 f"Awesome. We have placed your order. Here is your order id # {order_id}. "
#                 f"Your order total is {order_total} which you can pay at the time of delivery!"
#             )
#         del inprogress_orders[session_id]
#
#     return JSONResponse(content={
#         "fulfillmentText": fulfillment_text
#     })
#
#
# def save_to_db(order: dict):
#     next_order_id = db_helper.get_next_order_id()
#
#     # Insert individual items along with quantity in orders table
#     for food_item, quantity in order.items():
#         rcode = db_helper.insert_order_item(
#             food_item,
#             quantity,
#             next_order_id
#         )
#         if rcode == -1:
#             return -1
#
#     # Now insert order tracking status
#     db_helper.insert_order_tracking(next_order_id, "in progress")
#
#     return next_order_id
#
#
# def add_to_order(parameters: dict, session_id: str):
#     food_items = parameters['food-item']
#     quantities = parameters['number']
#
#     if len(food_items) != len(quantities):
#         fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
#     else:
#         new_food_dict = dict(zip(food_items, quantities))
#
#         if session_id in inprogress_orders:
#             current_food_dict = inprogress_orders[session_id]
#             current_food_dict.update(new_food_dict)
#             inprogress_orders[session_id] = current_food_dict
#         else:
#             inprogress_orders[session_id] = new_food_dict
#
#         order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
#         fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"
#
#     return JSONResponse(content={
#         "fulfillmentText": fulfillment_text
#     })
#
#
# def track_order(parameters: dict, session_id: str):
#     order_id = int(parameters['order_id'])
#     order_status = db_helper.get_order_status(order_id)
#
#     if order_status:
#         fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
#     else:
#         fulfillment_text = f"No order found with order id: {order_id}"
#
#     return JSONResponse(content={
#         "fulfillmentText": fulfillment_text
#     })

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware

import generic_helper
import db_helper

app = FastAPI()

# Adjust origins as needed; "*" for all or your domains
origins = [
    "*",
    # "https://your-allowed-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


inprogress_orders = {}


@app.get("/")
async def root():
    return {"message": "Hello! This endpoint only supports POST requests for dialogflow webhook."}


@app.get("/favicon.ico")
async def favicon():
    # No favicon available; return 204 No Content
    return Response(status_code=204)


@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult'].get('outputContexts', [])

    if not output_contexts:
        return JSONResponse(content={"fulfillmentText": "Session context missing. Please try again."})

    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])

    intent_handler_dict = {
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_from_order,
        'order.complete - context: ongoing-order': complete_order,
        'track.order - context: ongoing-tracking': track_order,
    }

    if intent not in intent_handler_dict:
        return JSONResponse(content={"fulfillmentText": f"Sorry, I don't understand the intent '{intent}'."})

    return intent_handler_dict[intent](parameters, session_id)


def add_to_order(parameters: dict, session_id: str):
    food_items = parameters.get('food-item', [])
    quantities = parameters.get('number', [])

    if not food_items or not quantities or len(food_items) != len(quantities):
        return JSONResponse(content={
            "fulfillmentText": "Sorry, I didn't understand. Please specify food items and quantities clearly."
        })

    new_food_dict = dict(zip(food_items, quantities))

    if session_id in inprogress_orders:
        current_food_dict = inprogress_orders[session_id]
        # Update quantities: sum if item already exists
        for item, qty in new_food_dict.items():
            current_food_dict[item] = current_food_dict.get(item, 0) + qty
        inprogress_orders[session_id] = current_food_dict
    else:
        inprogress_orders[session_id] = new_food_dict

    order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
    fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having trouble finding your order. Sorry! Can you place a new order please?"
        })

    food_items = parameters.get("food-item", [])
    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    fulfillment_text = ""
    if removed_items:
        fulfillment_text += f'Removed {", ".join(removed_items)} from your order! '

    if no_such_items:
        fulfillment_text += f'Your current order does not have {", ".join(no_such_items)}. '

    if not current_order:
        fulfillment_text += "Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"Here is what is left in your order: {order_str}"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having trouble finding your order. Sorry! Can you place a new order please?"
        return JSONResponse(content={"fulfillmentText": fulfillment_text})

    order = inprogress_orders[session_id]

    # Extract user info if available from parameters (optional)
    user_info = {}
    for key in ['name', 'email', 'phone-number']:
        if key in parameters:
            user_info[key] = parameters[key]

    order_id = db_helper.insert_order(order, user_info)

    if order_id is None:
        fulfillment_text = "Sorry, I couldn't process your order due to a backend error. Please place a new order again."
    else:
        order_total = db_helper.get_total_order_price(order_id)
        order_total_str = f"{order_total}" if order_total is not None else "unknown"
        fulfillment_text = (
            f"Awesome. We have placed your order. Here is your order id # {order_id}. "
            f"Your order total is {order_total_str} which you can pay at the time of delivery!"
        )

    # Clear session order
    del inprogress_orders[session_id]

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


def track_order(parameters: dict, session_id: str):
    order_id = parameters.get('order_id')

    if not order_id:
        return JSONResponse(content={"fulfillmentText": "Please provide an order ID to track."})

    order_status = db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}."
    else:
        fulfillment_text = f"No order found with order id: {order_id}."

    return JSONResponse(content={"fulfillmentText": fulfillment_text})

