

#########################################################################################################################
# from flask import Blueprint, jsonify
# from flask_socketio import emit
# from config import client_id, access_token
# from db import get_db_connection
# from extensions import socketio
# import requests
# import time
# import mysql.connector
# from apscheduler.schedulers.background import BackgroundScheduler

# # ✅ Blueprint for PnL Report API
# pnl_report_bp = Blueprint("pnl_report", __name__)

# # ✅ Dhan API Configuration
# DHAN_LTP_URL = "https://api.dhan.co/v2/marketfeed/ltp"
# HEADERS = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "access-token": access_token,
#     "client-id": client_id,
# }

# # ✅ Caching and Rate Limit Handling
# live_price_cache = {}
# last_updated_time = 0
# CACHE_REFRESH_INTERVAL = 30  # Refresh every 30 seconds

# def fetch_with_backoff(url, payload, headers, max_retries=5):
#     delay = 1
#     for attempt in range(max_retries):
#         try:
#             response = requests.post(url, json=payload, headers=headers)
#             response.raise_for_status()
#             return response.json()
#         except requests.exceptions.RequestException as e:
#             if "429" in str(e):
#                 print(f"⚠️ Rate limited. Retrying in {delay} seconds...")
#                 time.sleep(delay)
#                 delay *= 2
#             else:
#                 print(f"❌ API Request Failed: {e}")
#                 return None
#     return None

# # ✅ Fetch Executed Orders from Database
# def get_orders_from_db():
#     connection = None
#     orders = []
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT order_id, security_id, transaction_type, quantity, price FROM offline_order WHERE status = 'EXECUTED'")
#         orders = cursor.fetchall()

#         for order in orders:
#             if float(order["price"]) == 0.00:
#                 security_id = order["security_id"]
#                 order["price"] = live_price_cache.get(security_id, 0.0)
#     except mysql.connector.Error as e:
#         print(f"Database error: {e}")
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#     finally:
#         if connection:
#             connection.close()
#     return orders

# # ✅ Fetch Live Prices with Caching
# def get_live_prices(security_ids):
#     global last_updated_time, live_price_cache
#     if time.time() - last_updated_time < CACHE_REFRESH_INTERVAL:
#         print("🟢 Using cached prices...")
#         return {sid: live_price_cache.get(sid, 0.0) for sid in security_ids}
    
#     if not security_ids:
#         return {}
    
#     url = DHAN_LTP_URL
#     payload = {"NSE_EQ": [int(sid) for sid in security_ids]}
#     data = fetch_with_backoff(url, payload, HEADERS)
#     if not data:
#         return {}
    
#     live_prices = {}
#     if "data" in data and "NSE_EQ" in data["data"]:
#         for sid in security_ids:
#             if str(sid) in data["data"]["NSE_EQ"]:
#                 live_prices[sid] = float(data["data"]["NSE_EQ"][str(sid)]["last_price"])
    
#     live_price_cache = live_prices
#     last_updated_time = time.time()
#     return live_prices

# # ✅ Stream PnL via WebSockets
# def stream_pnl():
#     print("✅ PnL stream started.", flush=True)
#     while True:
#         orders = get_orders_from_db()
#         if not orders:
#             print("⚠️ No executed orders found.", flush=True)
#             time.sleep(5)
#             continue

#         security_ids = list(set(order["security_id"] for order in orders))
#         live_prices = get_live_prices(security_ids)
#         if not live_prices:
#             print("⚠️ Live price data is empty.", flush=True)
#             time.sleep(5)
#             continue

#         pnl_report = []
#         total_pnl = 0.0
#         for order in orders:
#             try:
#                 security_id = order["security_id"]
#                 entry_price = float(order["price"])
#                 quantity = int(order["quantity"])
#                 transaction_type = order["transaction_type"]
#                 live_price = live_prices.get(security_id, 0.0)

#                 pnl = (live_price - entry_price) * quantity
#                 if transaction_type == "SELL":
#                     pnl = (entry_price - live_price) * quantity

#                 total_pnl += pnl
#                 pnl_report.append({
#                     "order_id": order["order_id"],
#                     "security_id": security_id,
#                     "entry_price": entry_price,
#                     "current_price": live_price,
#                     "quantity": quantity,
#                     "transaction_type": transaction_type,
#                     "pnl": round(pnl, 2),
#                     "pnl_percentage": round((pnl / (entry_price * quantity)) * 100, 2) if entry_price * quantity else 0,
#                 })
#             except Exception as e:
#                 print(f"❌ Error processing order {order}: {e}", flush=True)

#         socketio.emit("pnl_update", {"status": "success", "pnl_report": pnl_report, "total_pnl": round(total_pnl, 2)})
#         print("✅ Sent live PnL data to frontend.", flush=True)
#         time.sleep(5)

# # ✅ API Endpoint to Fetch PnL Report
# @pnl_report_bp.route("/pnl-report", methods=["GET"])
# def pnl_report():
#     orders = get_orders_from_db()
#     security_ids = [order["security_id"] for order in orders] if orders else []
#     live_prices = get_live_prices(security_ids)
#     return jsonify({"status": "success", "orders": orders, "live_prices": live_prices})

# # ✅ Schedule PnL Streaming as a Background Task
# scheduler = BackgroundScheduler()
# scheduler.add_job(stream_pnl, "interval", seconds=5)
# scheduler.start()


#########################################################################################################################
 

# ========================================================================================================================


# from flask import Blueprint, jsonify
# from flask_socketio import emit
# from config import client_id, access_token
# from db import get_db_connection
# from extensions import socketio
# import requests
# import time
# import mysql.connector
# from apscheduler.schedulers.background import BackgroundScheduler

# # ✅ Blueprint for PnL Report API
# pnl_report_bp = Blueprint("pnl_report", __name__)

# # ✅ Dhan API Configuration
# # DHAN_LTP_URL = "https://api.dhan.co/v2/marketfeed/ltp"
# DHAN_BASE_URL = "https://api.dhan.co/v2/marketfeed/ltp"


# HEADERS = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "access-token": access_token,
#     "client-id": client_id,
# }

# # ✅ Caching and Rate Limit Handling
# live_price_cache = {}
# last_updated_time = 0
# CACHE_REFRESH_INTERVAL = 30  # Refresh every 30 seconds

# def fetch_with_backoff(url, payload, headers, max_retries=5):
#     delay = 1
#     for attempt in range(max_retries):
#         try:
#             response = requests.post(url, json=payload, headers=headers)
#             response.raise_for_status()
#             return response.json()
#         except requests.exceptions.RequestException as e:
#             if "429" in str(e):
#                 print(f"⚠️ Rate limited. Retrying in {delay} seconds...")
#                 time.sleep(delay)
#                 delay *= 2
#             else:
#                 print(f"❌ API Request Failed: {e}")
#                 return None
#     return None

# # ✅ Fetch Executed Orders from Database
# def get_orders_from_db():
#     connection = None
#     orders = []
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT order_id, security_id, transaction_type, quantity, price FROM offline_order WHERE status = 'EXECUTED'")
#         orders = cursor.fetchall()

#         for order in orders:
#             if float(order["price"]) == 0.00:
#                 security_id = order["security_id"]
#                 order["price"] = live_price_cache.get(security_id, 0.0)
#     except mysql.connector.Error as e:
#         print(f"Database error: {e}")
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#     finally:
#         if connection:
#             connection.close()
#     return orders

# # ✅ Fetch Live Prices with Caching
# def get_live_prices(security_ids):
#     global last_updated_time, live_price_cache
#     if time.time() - last_updated_time < CACHE_REFRESH_INTERVAL:
#         # print("🟢 Using cached prices...",live_price_cache)
#         return {sid: live_price_cache.get(sid, 0.0) for sid in security_ids}
    
#     if not security_ids:
#         return {}
    
#     url = DHAN_BASE_URL
#     payload = {"NSE_EQ": [int(sid) for sid in security_ids]}
#     data = fetch_with_backoff(url, payload, HEADERS)
#     if not data:
#         return {}
    
#     live_prices = {}
#     if "data" in data and "NSE_EQ" in data["data"]:
#         for sid in security_ids:
#             if str(sid) in data["data"]["NSE_EQ"]:
#                 live_prices[sid] = float(data["data"]["NSE_EQ"][str(sid)]["last_price"])
    
#     live_price_cache = live_prices
#     print("🟢 live_price_cache----------------",live_price_cache)
#     last_updated_time = time.time()
#     return live_prices

# # ✅ Stream PnL via WebSockets
# def stream_pnl():
#     print("✅ PnL stream started.", flush=True)
#     while True:
#         orders = get_orders_from_db()
#         if not orders:
#             print("⚠️ No executed orders found.", flush=True)
#             time.sleep(5)
#             continue

#         security_ids = list(set(order["security_id"] for order in orders))
#         live_prices = get_live_prices(security_ids)
#         print("🟢 live_prices-------++++++++---------",live_prices)
#         if not live_prices:
#             print("⚠️ Live price data is empty.", flush=True)
#             time.sleep(5)
#             continue

#         pnl_report = []
#         total_pnl = 0.0
#         for order in orders:
#             try:
#                 security_id = order["security_id"]
#                 entry_price = float(order["price"])
#                 quantity = int(order["quantity"])
#                 transaction_type = order["transaction_type"]
#                 live_price = live_prices.get(security_id, 0.0)

#                 pnl = (live_price - entry_price) * quantity
#                 if transaction_type == "SELL":
#                     pnl = (entry_price - live_price) * quantity

#                 total_pnl += pnl
#                 pnl_report.append({
#                     "order_id": order["order_id"],
#                     "security_id": security_id,
#                     "entry_price": entry_price,
#                     "current_price": live_price,
#                     "quantity": quantity,
#                     "transaction_type": transaction_type,
#                     "pnl": round(pnl, 2),
#                     "pnl_percentage": round((pnl / (entry_price * quantity)) * 100, 2) if entry_price * quantity else 0,
#                 })
#             except Exception as e:
#                 print(f"❌ Error processing order {order}: {e}", flush=True)

#         socketio.emit("pnl_update", {"status": "success", "pnl_report": pnl_report, "total_pnl": round(total_pnl, 2)})
#         print("✅ Sent live PnL data to frontend.", flush=True)
#         time.sleep(5)

# # ✅ API Endpoint to Fetch PnL Report
# @pnl_report_bp.route("/pnl-report", methods=["GET"])
# def pnl_report():
#     orders = get_orders_from_db()
#     security_ids = [order["security_id"] for order in orders] if orders else []
#     live_prices = get_live_prices(security_ids)
#     return jsonify({"status": "success", "orders": orders, "live_prices": live_prices})

# # ✅ Schedule PnL Streaming as a Background Task
# scheduler = BackgroundScheduler()
# scheduler.add_job(stream_pnl, "interval", seconds=5)
# scheduler.start()

# ========================================================================================================================














# from flask import Blueprint, jsonify
# from flask_socketio import emit
# from config import client_id, access_token
# from db import get_db_connection
# from extensions import socketio
# import websocket
# import json
# import struct
# import threading
# import logging
# import mysql.connector

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# pnl_report_bp = Blueprint("pnl_report", __name__)
# live_price_cache = {}

# ws_url = f"wss://api-feed.dhan.co?version=2&token={access_token}&clientId={client_id}&authType=2"

# def get_orders_from_db():
#     connection = None
#     orders = []
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT order_id, security_id, transaction_type, quantity, price FROM offline_order WHERE status = 'EXECUTED'")
#         orders = cursor.fetchall()
#         for order in orders:
#             if float(order["price"]) == 0.00:
#                 order["price"] = live_price_cache.get(order["security_id"], 0.0)
#     except mysql.connector.Error as e:
#         logger.error(f"Database error: {e}")
#     finally:
#         if connection:
#             connection.close()
#     return orders

# def on_open(ws):
#     logger.info("WebSocket opened")
#     update_subscriptions(ws)
    

# def on_message(ws, message):
#     global live_price_cache
#     logger.info(f"Raw message length: {len(message)} bytes")

#     if isinstance(message, bytes) and len(message) >= 12:
#         try:
#             # Extract bytes
#             sec_id_bytes = message[4:8]
#             ltp_bytes = message[8:12]

#             # Log extracted byte values
#             logger.info(f"Raw bytes (4-7): {sec_id_bytes.hex()}, (8-11): {ltp_bytes.hex()}")

#             # Try Big-Endian first
#             security_id_be = struct.unpack('>I', sec_id_bytes)[0]
#             last_price_be = struct.unpack('>f', ltp_bytes)[0]

#             # Try Little-Endian as a backup
#             security_id_le = struct.unpack('<I', sec_id_bytes)[0]
#             last_price_le = struct.unpack('<f', ltp_bytes)[0]

#             # Choose valid security_id and price
#             security_id = str(security_id_be) if security_id_be < 100000 else str(security_id_le)
#             last_price = last_price_be if 0 < last_price_be < 1000000 else last_price_le

#             # Round price to 2 decimal places
#             last_price = round(last_price, 2)

#             logger.info(f"Parsed - Security ID: {security_id}, LTP: {last_price}")

#             # Store in cache only if valid
#             if 0 < last_price < 1000000:
#                 live_price_cache[security_id] = last_price
                
#                 # Log formatted cache
#                 formatted_prices = {key: round(value, 2) for key, value in live_price_cache.items()}
#                 logger.info(f"Updated live_price_cache: {formatted_prices}")

#                 # Stream updated PnL
#                 stream_pnl()
#             else:
#                 logger.warning(f"Invalid price detected: {last_price}")

#         except Exception as e:
#             logger.error(f"Parsing error: {e}")


# def on_error(ws, error):
#     logger.error(f"WebSocket error: {error}")

# def on_close(ws, code, reason):
#     logger.info(f"WebSocket closed: {code}, {reason}")

# def update_subscriptions(ws):
#     orders = get_orders_from_db()
#     if not orders:
#         logger.info("No executed orders to subscribe to")
#         return
#     security_ids = list(set(order["security_id"] for order in orders))
#     subscription = {
#         "RequestCode": 15,
#         "InstrumentCount": len(security_ids),
#         "InstrumentList": [{"ExchangeSegment": "NSE_EQ", "SecurityId": sid} for sid in security_ids]
#     }
#     subscription_json = json.dumps(subscription)
#     ws.send(subscription_json)
#     logger.info(f"Subscription sent: {subscription_json}")
#     logger.info(f"Subscribed to: {security_ids}")

# def stream_pnl():
#     orders = get_orders_from_db()
#     if not orders:
#         socketio.emit("pnl_update", {"status": "error", "message": "No executed orders found"})
#         logger.info("No orders to stream")
#         return

#     pnl_report = []
#     total_pnl = 0.0
#     for order in orders:
#         security_id = order["security_id"]
#         entry_price = float(order["price"])
#         quantity = int(order["quantity"])
#         transaction_type = order["transaction_type"]
#         live_price = live_price_cache.get(security_id, entry_price)  # Use entry_price as fallback
#         pnl = (live_price - entry_price) * quantity if transaction_type == "BUY" else (entry_price - live_price) * quantity
#         pnl_percentage = round((pnl / (entry_price * quantity)) * 100, 2) if entry_price * quantity else 0
#         total_pnl += pnl
#         pnl_report.append({
#             "order_id": order["order_id"],
#             "security_id": security_id,
#             "entry_price": entry_price,
#             "current_price": live_price,
#             "quantity": quantity,
#             "transaction_type": transaction_type,
#             "pnl": round(pnl, 2),
#             "pnl_percentage": pnl_percentage,
#         })

#     socketio.emit("pnl_update", {
#         "status": "success",
#         "pnl_report": pnl_report,
#         "total_pnl": round(total_pnl, 2)
#     })
#     logger.info(f"Emitted pnl_update: {len(pnl_report)} orders, total_pnl: {total_pnl}")

# @pnl_report_bp.route("/pnl-report", methods=["GET"])
# def pnl_report():
#     orders = get_orders_from_db()
#     security_ids = [order["security_id"] for order in orders] if orders else []
#     live_prices = {sid: live_price_cache.get(sid, 0.0) for sid in security_ids}
#     logger.info(f"Returning PnL report: orders={len(orders)}, live_prices={live_prices}")
#     return jsonify({"status": "success", "orders": orders, "live_prices": live_prices})

# def start_websocket():
#     logger.info("Starting WebSocket...")
#     ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
#     ws.run_forever(ping_interval=10)

# websocket_thread = threading.Thread(target=start_websocket, daemon=True)
# websocket_thread.start()









from flask import Blueprint, jsonify
from flask_socketio import emit
from config import client_id, access_token
from db import get_db_connection
from extensions import socketio
import websocket
import json
import struct
import threading
import logging
import mysql.connector

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

pnl_report_bp = Blueprint("pnl_report", __name__)
live_price_cache = {}

# WebSocket URL for Dhan API
ws_url = f"wss://api-feed.dhan.co?version=2&token={access_token}&clientId={client_id}&authType=2"

def get_orders_from_db():
    connection = None
    orders = []
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT order_id, security_id, transaction_type, quantity, price FROM offline_order WHERE status = 'EXECUTED'")
        orders = cursor.fetchall()
        for order in orders:
            if float(order["price"]) == 0.00:
                order["price"] = live_price_cache.get(order["security_id"], 0.0)
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()
    return orders

def on_open(ws):
    logger.info("WebSocket opened")
    update_subscriptions(ws)

def on_message(ws, message):
    global live_price_cache
    logger.info(f"Raw message length: {len(message)} bytes")

    if isinstance(message, bytes) and len(message) >= 12:
        try:
            # Extract bytes
            sec_id_bytes = message[4:8]
            ltp_bytes = message[8:12]

            # Log extracted byte values
            logger.info(f"Raw bytes (4-7): {sec_id_bytes.hex()}, (8-11): {ltp_bytes.hex()}")

            # Try Big-Endian first
            security_id_be = struct.unpack('>I', sec_id_bytes)[0]
            last_price_be = struct.unpack('>f', ltp_bytes)[0]

            # Try Little-Endian as a backup
            security_id_le = struct.unpack('<I', sec_id_bytes)[0]
            last_price_le = struct.unpack('<f', ltp_bytes)[0]

            # Choose valid security_id and price
            security_id = str(security_id_be) if security_id_be < 100000 else str(security_id_le)
            last_price = last_price_be if 0 < last_price_be < 1000000 else last_price_le

            # Round price to 2 decimal places
            last_price = round(last_price, 2)

            logger.info(f"Parsed - Security ID: {security_id}, LTP: {last_price}")

            # Store in cache and emit update if valid
            if 0 < last_price < 1000000:
                live_price_cache[security_id] = last_price
                formatted_prices = {key: round(value, 2) for key, value in live_price_cache.items()}
                logger.info(f"Updated live_price_cache: {formatted_prices}")
                stream_pnl()
            else:
                logger.warning(f"Invalid price detected: {last_price}")

        except Exception as e:
            logger.error(f"Parsing error: {e}")

def on_error(ws, error):
    logger.error(f"WebSocket error: {error}")

def on_close(ws, code, reason):
    logger.info(f"WebSocket closed: {code}, {reason}")

def update_subscriptions(ws):
    orders = get_orders_from_db()
    if not orders:
        logger.info("No executed orders to subscribe to")
        return
    security_ids = list(set(order["security_id"] for order in orders))
    subscription = {
        "RequestCode": 15,
        "InstrumentCount": len(security_ids),
        "InstrumentList": [{"ExchangeSegment": "NSE_EQ", "SecurityId": sid} for sid in security_ids]
    }
    subscription_json = json.dumps(subscription)
    ws.send(subscription_json)
    logger.info(f"Subscription sent: {subscription_json}")
    logger.info(f"Subscribed to: {security_ids}")





def stream_pnl():
    orders = get_orders_from_db()
    if not orders:
        socketio.emit("price_update", {"status": "error", "message": "No executed orders found"})
        logger.info("No orders to stream")
        return
    
   

    price_data = {}
    for order in orders:
        security_id = order["security_id"]
        last_price = live_price_cache.get(security_id, float(order["price"]))  # Use last_price or cached value
        price_data[security_id] = last_price

    emitted_data = {"status": "success", "prices": price_data}
    socketio.emit("price_update", emitted_data)
    logger.info(f"Emitted price_update: {emitted_data}")


    # pnl_report = []
    # total_pnl = 0
    # price_data = {}
    # for order in orders:
    #     security_id = order["security_id"]
    #     price_data[security_id] = live_price
    #     entry_price = float(order["price"])
    #     quantity = int(order["quantity"])
    #     transaction_type = order["transaction_type"]
    #     live_price = live_price_cache.get(security_id, float(order["price"]))  # Fallback to entry price
    #     price_data[security_id] = live_price
    #     pnl = (live_price - entry_price) * qunntity if transaction_type == "BUY" else (entry_price - live_price) * quantity
    #     pnl_percentage = round((pnl / (entry_price * quntity)) * 100, 2) if entry_price * quntity else 0

    #     total_pnl += pnl
        


    #     pnl_report.append({
    #         "order_id" : order["order_id"],
    #         "security_id": security_id,
    #         "entry_price": entry_price,
    #         "current_price": live_price,
    #         "quantity": quantity,
    #         "transaction_type": transaction_type,
    #         "pnl": round(pnl, 2),
    #         "pnl_percentage": pnl_percentage
    #     })

    #     if pnl_percentage >= 2 or pnl_percentage <= -5:
    #         logger.info(f"Triggering sell order for Order ID: {order['order_id']}, Security ID: {security_id}, PnL %: {pnl_percentage}")
    #         place_sell_order(order)
            


    # socketio.emit("price_update", {
    #     "status": "success",
    #     "prices": price_data
    # })
    # logger.info(f"Emitted price_update for {len(price_data)} securities")


def place_sell_order(order):
    try:
        payload = {
            "order_id": order["order_id"],
            "security_id": order["security_id"],
            "quantity": order["quantity"],
            "transaction_type": "SELL",
            "price": live_price_cache.get(order["security_id"], order["price"]),
            "product_type": "INTRADAY",
            "order_type": "MARKET"
        }

        response = requests.post("http://localhost:5000/place_sell_order", json=payload)

        if response.status_code == 200:
            logger.info(f"Triggered sell order for {order['order_id']}")
        else:
            logger.error(f"Failed to trigger sell order for {order['order_id']}: {response.json()}") 

    except Exception as e:
        logger.error(f"Error triggering sell order for {order['order_id']}: {e}")      




@pnl_report_bp.route("/pnl-report", methods=["GET"])
def pnl_report():
    orders = get_orders_from_db()
    security_ids = [order["security_id"] for order in orders] if orders else []
    live_prices = {sid: live_price_cache.get(sid, 0.0) for sid in security_ids}
    logger.info(f"Returning PnL report: orders={len(orders)}, live_prices={live_prices}")
    return jsonify({"status": "success", "orders": orders, "live_prices": live_prices})

def start_websocket():
    logger.info("Starting WebSocket...")
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever(ping_interval=10, ping_timeout=5)

# Start WebSocket in a separate thread
websocket_thread = threading.Thread(target=start_websocket, daemon=True)
websocket_thread.start()

# Test emission on client connect (for debugging)
@socketio.on("connect")
def handle_connect():
    logger.info("Client connected to SocketIO")
    # emit("pnl_update", {"status": "success", "message": "Connected to server", "pnl_report": [], "total_pnl": 0})
    emit("price_update", {"status": "success", "message": "Connected to server", "prices": {}})







