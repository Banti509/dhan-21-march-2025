

# from flask import Flask, jsonify, request, Blueprint
# from dhanhq import dhanhq
# import datetime
# from config import client_id, access_token
# from db import save_offline_order, get_db_connection
# from apscheduler.schedulers.background import BackgroundScheduler

# # Initialize Dhan API Client
# dhan = dhanhq(client_id, access_token)
# place_order_bp = Blueprint("place_order", __name__)

# # Function to check if the market is open
# def is_market_open():
#     """Returns True if the stock market is open."""
#     now = datetime.datetime.now()
#     return now.weekday() < 5 and 9 <= now.hour < 15  # Market open 9 AM - 3 PM

# @place_order_bp.route('/place-order', methods=['POST'])
# def place_order():
#     """Handles both online and offline order placement."""
#     try:
#         data = request.get_json()

#         # Validate required fields
#         required_fields = ["security_id", "exchange_segment", "transaction_type", "quantity", "order_type", "product_type"]
#         if data.get("order_type") in ["LIMIT", "STOP_LOSS"]:
#             required_fields.append("price")
#         if data.get("order_type") in ["STOP_LOSS", "STOP_LOSS_MARKET"]:
#             required_fields.append("trigger_price")

#         for field in required_fields:
#             if field not in data:
#                 return jsonify({"error": f"Missing required field: {field}"}), 400

#         # Extract and process input data
#         security_id = str(data["security_id"])
#         exchange_segment = data["exchange_segment"]
#         transaction_type = data["transaction_type"].upper()
#         order_type = data["order_type"].upper()
#         quantity = int(data["quantity"])
#         product_type = data["product_type"]

#         # Prices (set only when required)

#         price = float(data["price"]) if "price" in data and data["price"] is not None else None
#         trigger_price = float(data["trigger_price"]) if "trigger_price" in data and data["trigger_price"] is not None else None
#         # Validate input fields
#         valid_segments = ["NSE_EQ", "BSE_EQ", "NSE_FNO", "MCX_COM"]
#         if exchange_segment not in valid_segments:
#             return jsonify({"error": "Invalid exchange segment"}), 400

#         transaction_type = transaction_type.upper()
#         if transaction_type not in ["BUY", "SELL"]:
#             return jsonify({"error": "Invalid transaction type"}), 400

#         # Construct order payload
        
#         order_payload = {
#             "security_id": security_id,
#             "exchange_segment": exchange_segment,
#             "transaction_type": transaction_type,
#             "quantity": quantity,
#             "order_type": order_type,
#             "product_type": product_type,
#             "price": price if order_type in ["LIMIT", "STOP_LOSS"] else 0,  # Ensure price is sent properly
#             "trigger_price": trigger_price if order_type in ["STOP_LOSS", "STOP_LOSS_MARKET"] else 0  # Ensure trigger price is valid
#         }

#         # Remove trigger_price for non-SL orders

#         if order_type == "MARKET":
#             order_payload.pop("price", None)  # Remove price for MARKET orders
#             order_payload.pop("trigger_price", None)  # Remove trigger price for MARKET orders
        
#         if order_type not in ["STOP_LOSS", "STOP_LOSS_MARKET"]:
#             order_payload.pop("trigger_price", None)

#         # Ensure price is always included, but set to 0 if not required
#         if order_type not in ["LIMIT", "STOP_LOSS"]:
#             order_payload["price"] = 0  # Default to 0 for MARKET orders

#         print(f"📦 Sending Order Payload to Dhan API: {order_payload}")

#         # Send request
#         order_response = dhan.place_order(**order_payload)


#         # If market is open, place the order immediately
#         if is_market_open():
#             order_response = dhan.place_order(**order_payload)
#             print(f"🚨 Order Response from Dhan: {order_response}")

#             if order_response.get("status") == "success":
#                 # order_id = order_response["details"]["data"].get("orderId")
#                 order_id = order_response["data"].get("orderId")

#                 if not order_id:
#                     return jsonify({"error": "Order ID missing from response"}), 400

#                 # Save order in database with EXECUTED status
#                 save_offline_order(order_id, security_id, exchange_segment, transaction_type, quantity, order_type, product_type, price, trigger_price, "EXECUTED")

#                 return jsonify({
#                     "status": "success",
#                     "message": "Order placed and executed successfully",
#                     "order_id": order_id
#                 }), 200

#             return jsonify({
#                 "status": "error",
#                 "message": "Order placement failed",
#                 "details": order_response
#             }), 400
            

#         # If market is closed, save the order as PENDING
#         else:
#             test_order_id = f"TEST_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
#             save_offline_order(test_order_id, security_id, exchange_segment, transaction_type, quantity, order_type, product_type, price, trigger_price, "PENDING")

#             return jsonify({
#                 "status": "offline",
#                 "message": "Market closed. Order saved for execution when market opens.",
#                 "test_order_id": test_order_id
#             }), 200

#     except Exception as e:
#         print(f"⚠️ Error: {e}")
#         return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

# # Function to process and execute PENDING orders when market opens
# def process_offline_orders(): 
#     """Executes stored offline orders when the market opens and updates status."""
#     if is_market_open():
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM offline_order WHERE status = 'PENDING'")
#         orders = cursor.fetchall()

#         for order in orders:
#             try:
#                 # Convert Decimal values to float
#                 price = float(order["price"]) if order["price"] is not None else None
#                 trigger_price = float(order["trigger_price"]) if order["trigger_price"] is not None else None

#                 # Validate Order Type
#                 valid_order_types = ["MARKET", "LIMIT", "STOP_LOSS", "STOP_LOSS_MARKET"]
#                 if order["order_type"] not in valid_order_types:
#                     print(f"⚠️ Invalid order type: {order['order_type']}")
#                     continue  # Skip this order

#                 # Construct payload for Dhan API
#                 order_payload = {
#                     "security_id": order["security_id"],
#                     "exchange_segment": order["exchange_segment"],
#                     "transaction_type": order["transaction_type"],
#                     "quantity": order["quantity"],
#                     "order_type": order["order_type"],
#                     "product_type": order["product_type"],
#                     "price": price,
#                     "trigger_price": trigger_price
#                 }

#                 # Remove unnecessary fields
#                 if order["order_type"] == "MARKET":
#                     order_payload["price"] = None
#                 if order["order_type"] not in ["STOP_LOSS", "STOP_LOSS_MARKET"]:
#                     order_payload.pop("trigger_price", None)

#                 print(f"📦 Processing Pending Order: {order_payload}")

#                 # Place order via Dhan API
#                 order_response = dhan.place_order(**order_payload)
#                 print(f"🚀 Order Response: {order_response}")

#                 if order_response.get("status") == "success":
#                     order_id = order_response["details"]["data"].get("orderId")
                    
#                     # Update order status in the database
#                     cursor.execute("UPDATE offline_order SET status = 'EXECUTED', order_id = %s WHERE id = %s", (order_id, order["id"]))
#                     conn.commit()

#                 else:
#                     print(f"⚠️ Order execution failed: {order_response}")

#             except Exception as e:
#                 print(f"⚠️ Error processing pending order {order['id']}: {e}")

#         cursor.close()
#         conn.close()

# # Background job scheduler to process offline orders every morning
# scheduler = BackgroundScheduler()
# scheduler.add_job(process_offline_orders, 'interval', minutes=1)  # Runs every minute
# scheduler.start()

















# from flask import Flask, jsonify, request, Blueprint
# from dhanhq import dhanhq
# import datetime
# from config import client_id, access_token
# from db import save_offline_order, get_db_connection
# from apscheduler.schedulers.background import BackgroundScheduler

# # Initialize Dhan API Client
# dhan = dhanhq(client_id, access_token)
# place_order_bp = Blueprint("place_order", __name__)

# # Function to check if the market is open
# def is_market_open():
#     """Returns True if the stock market is open."""
#     now = datetime.datetime.now()
#     return now.weekday() < 5 and 9 <= now.hour < 15  # Market open 9 AM - 3 PM

# @place_order_bp.route('/place-order', methods=['POST'])
# def place_order():
#     """Handles both online and offline order placement."""
#     try:
#         data = request.get_json()

#         # Validate required fields
#         required_fields = ["security_id", "exchange_segment", "transaction_type", "quantity", "order_type", "product_type"]
#         if data.get("order_type") in ["LIMIT", "STOP_LOSS"]:
#             required_fields.append("price")
#         if data.get("order_type") in ["STOP_LOSS", "STOP_LOSS_MARKET"]:
#             required_fields.append("trigger_price")

#         for field in required_fields:
#             if field not in data:
#                 return jsonify({"error": f"Missing required field: {field}"}), 400

#         # Extract and process input data
#         security_id = str(data["security_id"])
#         exchange_segment = data["exchange_segment"]
#         transaction_type = data["transaction_type"].upper()
#         order_type = data["order_type"].upper()
#         quantity = int(data["quantity"])
#         product_type = data["product_type"]

#         # Prices (set only when required)

#         price = float(data["price"]) if "price" in data and data["price"] is not None else None
#         trigger_price = float(data["trigger_price"]) if "trigger_price" in data and data["trigger_price"] is not None else None
#         # Validate input fields
#         valid_segments = ["NSE_EQ", "BSE_EQ", "NSE_FNO", "MCX_COM"]
#         if exchange_segment not in valid_segments:
#             return jsonify({"error": "Invalid exchange segment"}), 400

#         transaction_type = transaction_type.upper()
#         if transaction_type not in ["BUY", "SELL"]:
#             return jsonify({"error": "Invalid transaction type"}), 400

#         # Construct order payload
        
#         order_payload = {
#             "security_id": security_id,
#             "exchange_segment": exchange_segment,
#             "transaction_type": transaction_type,
#             "quantity": quantity,
#             "order_type": order_type,
#             "product_type": product_type,
#             "price": price if order_type in ["LIMIT", "STOP_LOSS"] else 0,  # Ensure price is sent properly
#             "trigger_price": trigger_price if order_type in ["STOP_LOSS", "STOP_LOSS_MARKET"] else 0  # Ensure trigger price is valid
#         }

#         # Remove trigger_price for non-SL orders

#         if order_type == "MARKET":
#             order_payload.pop("price", None)  # Remove price for MARKET orders
#             order_payload.pop("trigger_price", None)  # Remove trigger price for MARKET orders
        
#         if order_type not in ["STOP_LOSS", "STOP_LOSS_MARKET"]:
#             order_payload.pop("trigger_price", None)

#         # Ensure price is always included, but set to 0 if not required
#         if order_type not in ["LIMIT", "STOP_LOSS"]:
#             order_payload["price"] = 0  # Default to 0 for MARKET orders

#         print(f"📦 Sending Order Payload to Dhan API: {order_payload}")

#         # Send request
#         order_response = dhan.place_order(**order_payload)


#         # If market is open, place the order immediately
#         if is_market_open():
#             order_response = dhan.place_order(**order_payload)
#             print(f"🚨 Order Response from Dhan: {order_response}")

#             if order_response.get("status") == "success":
#                 # order_id = order_response["details"]["data"].get("orderId")
#                 order_id = order_response["data"].get("orderId")

#                 if not order_id:
#                     return jsonify({"error": "Order ID missing from response"}), 400

#                 # Save order in database with EXECUTED status
#                 save_offline_order(order_id, security_id, exchange_segment, transaction_type, quantity, order_type, product_type, price, trigger_price, "EXECUTED")

#                 return jsonify({
#                     "status": "success",
#                     "message": "Order placed and executed successfully",
#                     "order_id": order_id
#                 }), 200

#             return jsonify({
#                 "status": "error",
#                 "message": "Order placement failed",
#                 "details": order_response
#             }), 400
            

#         # If market is closed, save the order as PENDING
#         else:
#             test_order_id = f"TEST_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
#             save_offline_order(test_order_id, security_id, exchange_segment, transaction_type, quantity, order_type, product_type, price, trigger_price, "PENDING")

#             return jsonify({
#                 "status": "offline",
#                 "message": "Market closed. Order saved for execution when market opens.",
#                 "test_order_id": test_order_id
#             }), 200

#     except Exception as e:
#         print(f"⚠️ Error: {e}")
#         return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

# # Function to process and execute PENDING orders when market opens
# def process_offline_orders(): 
#     """Executes stored offline orders when the market opens and updates status."""
#     if is_market_open():
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM offline_order WHERE status = 'PENDING'")
#         orders = cursor.fetchall()

#         for order in orders:
#             try:
#                 # Convert Decimal values to float
#                 price = float(order["price"]) if order["price"] is not None else 0.0
#                 trigger_price = float(order["trigger_price"]) if order["trigger_price"] is not None else 0.0

#                 # Validate Order Type
#                 valid_order_types = ["MARKET", "LIMIT", "STOP_LOSS", "STOP_LOSS_MARKET"]
#                 if order["order_type"] not in valid_order_types:
#                     print(f"⚠️ Invalid order type: {order['order_type']}")
#                     continue  # Skip this order

#                 # Construct payload for Dhan API
#                 order_payload = {
#                     "security_id": order["security_id"],
#                     "exchange_segment": order["exchange_segment"],
#                     "transaction_type": order["transaction_type"],
#                     "quantity": order["quantity"],
#                     "order_type": order["order_type"],
#                     "product_type": order["product_type"],
#                     "price": price,  # if order["order_type"] in ["LIMT","STOP_LOSS"] else 0,
#                     "trigger_price": trigger_price # if order["order_type"] in ["STOP_LOSS", "STOP_LOSS_MARKET"] else 0
#                 }

                
#                 if order["order_type"] == "MARKET":
#                     order_payload.pop("price", 0.0)  
#                     order_payload.pop("trigger_price", 0.0)  

#                 print(f"📦 Processing Pending Order: {order_payload}")

                
#                 order_response = dhan.place_order(
#                     security_id=order_payload["security_id"],
#                     exchange_segment=order_payload["exchange_segment"],
#                     transaction_type=order_payload["transaction_type"],
#                     quantity=order_payload["quantity"],
#                     order_type=order_payload["order_type"],
#                     product_type=order_payload["product_type"],
#                     price=order_payload.get("price", 0.0),  # ✅ Ensure price is explicitly set
#                     trigger_price=order_payload.get("trigger_price", 0.0)
#                 )

#                 print(f"🚀 Order Response: {order_response}")

#                 if order_response.get("status") == "success":
#                     order_id = order_response["data"].get("orderId")  # ✅ Fix: Get orderId directly
#                     order_status = order_response["data"].get("orderStatus", "UNKNOWN")

#                     # Update order status in the database
#                     cursor.execute("UPDATE offline_order SET status = %s, order_id = %s WHERE id = %s",
#                                 (order_status, order_id, order["id"]))
#                     conn.commit()


#                 else:
#                     print(f"⚠️ Order execution failed: {order_response}")

#             except Exception as e:
#                 print(f"⚠️ Error processing pending order {order['id']}: {e}")

#         cursor.close()
#         conn.close()

# # Background job scheduler to process offline orders every morning
# scheduler = BackgroundScheduler()
# scheduler.add_job(process_offline_orders, 'interval', minutes=1)  # Runs every minute
# scheduler.start()













from flask import Flask, jsonify, request, Blueprint
from dhanhq import dhanhq
import datetime
import json
from config import client_id, access_token
from db import save_offline_order, get_db_connection
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize Dhan API Client
dhan = dhanhq(client_id, access_token)
place_order_bp = Blueprint("place_order", __name__)

# Function to check if the market is open
def is_market_open():
    """Returns True if the stock market is open."""
    now = datetime.datetime.now()
    return now.weekday() < 5 and 9 <= now.hour < 15  # Market open 9 AM - 3 PM

@place_order_bp.route('/place-order', methods=['POST'])
def place_order():
    """Handles both online and offline order placement."""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["security_id", "exchange_segment", "transaction_type", "quantity", "order_type", "product_type"]
        if data.get("order_type") in ["LIMIT", "STOP_LOSS"]:
            required_fields.append("price")
        if data.get("order_type") in ["STOP_LOSS", "STOP_LOSS_MARKET"]:
            required_fields.append("trigger_price")

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Extract and process input data
        security_id = str(data["security_id"])
        exchange_segment = data["exchange_segment"]
        transaction_type = data["transaction_type"].upper()
        order_type = data["order_type"].upper()
        quantity = int(data["quantity"])
        product_type = data["product_type"]
        

        price = float(data["price"]) if "price" in data and data["price"] is not None else 0.0
        trigger_price = float(data["trigger_price"]) if "trigger_price" in data and data["trigger_price"] is not None else None
        # Validate input fields
        valid_segments = ["NSE_EQ", "BSE_EQ", "NSE_FNO", "MCX_COM"]
        if exchange_segment not in valid_segments:
            return jsonify({"error": "Invalid exchange segment"}), 400

        transaction_type = transaction_type.upper()
        if transaction_type not in ["BUY", "SELL"]:
            return jsonify({"error": "Invalid transaction type"}), 400

        # Construct order payload
        
        order_payload = {
            "security_id": security_id,
            "exchange_segment": exchange_segment,
            "transaction_type": transaction_type,
            "quantity": quantity,
            "order_type": order_type,
            "product_type": product_type,
            "price": price if order_type in ["LIMIT", "STOP_LOSS"] else 0,  # Ensure price is sent properly
            "trigger_price": trigger_price if order_type in ["STOP_LOSS", "STOP_LOSS_MARKET"] else 0  # Ensure trigger price is valid
        }

        # Remove trigger_price for non-SL orders

        if order_type == "MARKET":
            order_payload.pop("price", None)  # Remove price for MARKET orders
            order_payload.pop("trigger_price", None)  # Remove trigger price for MARKET orders
        
        if order_type not in ["STOP_LOSS", "STOP_LOSS_MARKET"]:
            order_payload.pop("trigger_price", None)

        # Ensure price is always included, but set to 0 if not required
        if order_type not in ["LIMIT", "STOP_LOSS"]:
            order_payload["price"] = 0  # Default to 0 for MARKET orders

        print(f"📦 Sending Order Payload to Dhan API: {order_payload}")

        # Send request
        order_response = dhan.place_order(**order_payload)


        # If market is open, place the order immediately
        if is_market_open():
            order_response = dhan.place_order(**order_payload)
            print(f"🚨 Order Response from Dhan: {order_response}")

            if order_response.get("status") == "success":
                # order_id = order_response["details"]["data"].get("orderId")
                order_id = order_response["data"].get("orderId")

                if not order_id:
                    return jsonify({"error": "Order ID missing from response"}), 400

                # Save order in database with EXECUTED status
                save_offline_order(order_id, security_id, exchange_segment, transaction_type, quantity, order_type, product_type, price, trigger_price, "EXECUTED")


                return jsonify({
                    "status": "success",
                    "message": "Order placed and executed successfully",
                    "order_id": order_id,
                    "saved_data": order_payload
                }), 200

            return jsonify({
                "status": "error",
                "message": "Order placement failed",
                "details": order_response
            }), 400
            

        # If market is closed, save the order as PENDING
        else:
            test_order_id = f"TEST_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            save_offline_order(test_order_id, security_id, exchange_segment, transaction_type, quantity, order_type, product_type, price, trigger_price, "PENDING")


            return jsonify({
                "status": "offline",
                "message": "Market closed. Order saved for execution when market opens.",
                "test_order_id": test_order_id,
                "saved_data": [order_payload]
            }), 200

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

# Function to process and execute PENDING orders when market opens
def process_offline_orders(): 
    """Executes stored offline orders when the market opens and updates status."""
    if is_market_open():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM offline_order WHERE status = 'PENDING'")
        orders = cursor.fetchall()

        for order in orders:
            try:
                # Convert Decimal values to float
                price = float(order["price"]) if order["price"] is not None else 0.0
                trigger_price = float(order["trigger_price"]) if order["trigger_price"] is not None else 0.0

                # Validate Order Type
                valid_order_types = ["MARKET", "LIMIT", "STOP_LOSS", "STOP_LOSS_MARKET"]
                if order["order_type"] not in valid_order_types:
                    print(f"⚠️ Invalid order type: {order['order_type']}")
                    continue  # Skip this order

                # Construct payload for Dhan API
                order_payload = {
                    "security_id": order["security_id"],
                    "exchange_segment": order["exchange_segment"],
                    "transaction_type": order["transaction_type"],
                    "quantity": order["quantity"],
                    "order_type": order["order_type"],
                    "product_type": order["product_type"],
                    "price": price,  # if order["order_type"] in ["LIMT","STOP_LOSS"] else 0,
                    "trigger_price": trigger_price # if order["order_type"] in ["STOP_LOSS", "STOP_LOSS_MARKET"] else 0
                }

                
                if order["order_type"] == "MARKET":
                    order_payload.pop("price", 0.0)  
                    order_payload.pop("trigger_price", 0.0)  

                print(f"📦 Processing Pending Order: {order_payload}")

                
                order_response = dhan.place_order(
                    security_id=order_payload["security_id"],
                    exchange_segment=order_payload["exchange_segment"],
                    transaction_type=order_payload["transaction_type"],
                    quantity=order_payload["quantity"],
                    order_type=order_payload["order_type"],
                    product_type=order_payload["product_type"],
                    price=order_payload.get("price", 0.0),  # ✅ Ensure price is explicitly set
                    trigger_price=order_payload.get("trigger_price", 0.0)
                )

                print(f"🚀 Order Response: {order_response}")

                if order_response.get("status") == "success":
                    order_id = order_response["data"].get("orderId")  # ✅ Fix: Get orderId directly
                    order_status = order_response["data"].get("orderStatus", "UNKNOWN")

                    # Update order status in the database
                    cursor.execute("UPDATE offline_order SET status = %s, order_id = %s WHERE id = %s",
                                (order_status, order_id, order["id"]))
                    conn.commit()


                else:
                    print(f"⚠️ Order execution failed: {order_response}")

            except Exception as e:
                print(f"⚠️ Error processing pending order {order['id']}: {e}")

        cursor.close()
        conn.close()

# Background job scheduler to process offline orders every morning
scheduler = BackgroundScheduler()
scheduler.add_job(process_offline_orders, 'interval', minutes=1)  # Runs every minute
scheduler.start()


def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is missing"}), 400

    # ✅ Search in all five columns and return a single row
    sql = """
    SELECT Exchange_segment, Security_ID, Instrument_Type, Lot_Size, Symbol_Name
    FROM trading_data 
    WHERE Exchange_segment LIKE %s 
    OR Security_ID = %s
    OR Instrument_Type LIKE %s
    OR Lot_Size = %s
    OR Symbol_Name LIKE %s
    LIMIT 1
    """

    # ✅ Searching exactly for `Security_ID` & `Lot_Size`, loosely for others
    cursor.execute(sql, (f"%{query}%", query, f"%{query}%", query, f"%{query}%"))
    result = cursor.fetchone()

    return jsonify(result) if result else jsonify({"message": "No data found"})


