
# from flask import Flask, jsonify, request, Blueprint
# import time
# import hmac
# import hashlib
# import requests
# import urllib.parse
# import json
# # import csv
# from datetime import datetime
# from config import SELL_STATUS_FILE_PATH, API_SECRET, API_KEY, BASE_URL, JSON_FILE_PATH

# pnl_report_bp = Blueprint('pnl_report', __name__)

# # Endpoint to fetch all active orders' PnL reports
# @pnl_report_bp.route('/pnl_report', methods=['GET'])
# def pnl_report():
#     order_sell_status = load_order_sell_status()
#     try:
#         active_orders = fetch_active_orders()
#         if not active_orders:
#             print("No active orders found. Exiting script...")

#         unsold_orders = [order for order in active_orders if order_sell_status.get(str(order["orderId"])) != "Sold"]

#         if not unsold_orders:
#             print("\n✅ All orders have been sold. Exiting script...")
            
#         res_data = []
        
#         for order in active_orders:
#             order_id = order["orderId"]
#             print(f"\nProcessing Order ID: {order_id}")

#             res_data.append(calculate_and_save_pnl(order_id, order_sell_status))
#             if res_data:
#                 print(json.dumps(res_data, indent=4))

#         # Stop when all orders are processed
#         if all(order_sell_status.get(str(order["orderId"])) == "Sold" for order in active_orders):
#             print("\n✅ All orders have been sold based on PnL conditions. Exiting script...")


#         return res_data
#     except Exception as err:
#         return jsonify({"message": f"{err}"})




# def fetch_active_orders():
#     """
#     Fetches all active open positions.
#     """
#     try:
#         timestamp = int(time.time() * 1000)
#         params = {
#             "timestamp": timestamp,
#             # "symbol" : "BTCUSDT",
#             "recvWindow": 5000  # Helps avoid timestamp errors
#         }
#         query_string = urllib.parse.urlencode(params)
#         signature = hmac.new(
#             API_SECRET.encode('utf-8'),
#             query_string.encode('utf-8'),
#             hashlib.sha256
#         ).hexdigest()
#         params["signature"] = signature
#         headers = {"X-MBX-APIKEY": API_KEY}
#         url = f"{BASE_URL}/fapi/v1/allOrders"
#         response = requests.get(url, params=params, headers=headers)
        
#         if response.status_code == 200:
#             orders = response.json()
#             # print("_____________", orders)
#             if not orders:
#                 print("No open orders found.")
#                 return []   
#             print("Active Orders Fetched Successfully!")
#             return orders[-10:]  # Return only the last 10 orders
#         else:
#             print(f"Error fetching active orders: {response.status_code} - {response.json()}")
#             return []

#     except Exception as e:
#         print(f"Exception occurred while fetching active orders: {e}")
#         return []



# def load_order_sell_status():
#     try:
#         with open(SELL_STATUS_FILE_PATH, 'r') as file:
#             return json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return {}


# def save_order_sell_status(order_sell_status):
#     try:
#         with open(SELL_STATUS_FILE_PATH, 'w') as file:
#             json.dump(order_sell_status, file, indent=4)
#         return "Data saved successfully!!!!"
#     except Exception as e:
#         return f"Error saving sell status: {e}"




# def fetch_order_details(order_id):
#     try:
#         timestamp = int(time.time() * 1000)
#         params = {
#             "orderId": order_id,
#             "timestamp": timestamp
#         }
#         query_string = urllib.parse.urlencode(params)
#         signature = hmac.new(
#             API_SECRET.encode('utf-8'),
#             query_string.encode('utf-8'),
#             hashlib.sha256
#         ).hexdigest()
#         params["signature"] = signature
#         headers = {
#             "X-MBX-APIKEY": API_KEY
#         }
#         url = f"{BASE_URL}/fapi/v1/userTrades"
#         response = requests.get(url, params=params, headers=headers)
#         if response.status_code == 200:
#             trades = response.json()
#             if not trades:
#                 print(f"No trades found for order ID {order_id}")
#                 # print("+++++++++++++++++++++")
#                 return None
#             # print("-----------",trades)
#             return trades
#         else:
#             print(f"Error fetching order details: {response.status_code} - {response.json()}")
#             return None
#     except Exception as e:
#         print(f"Exception occurred: {e}")
#         return None
    
    

# def fetch_current_price(symbol):
#     try:
#         url = f"{BASE_URL}/fapi/v1/ticker/price?symbol={symbol}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             return float(response.json()["price"])
#         else:
#             print(f"Error fetching current price for {symbol}: {response.status_code} - {response.json()}")
#             return None
#     except Exception as e:
#         print(f"Exception occurred: {e}")
#         return None    



# def place_sell_order(symbol, quantity):
#     try:
#         timestamp = int(time.time() * 1000)
#         params = {
#             "symbol": symbol,
#             "side": "SELL",
#             "type": "MARKET",
#             "quantity": quantity,
#             "timestamp": timestamp
#         }
#         query_string = urllib.parse.urlencode(params)
#         signature = hmac.new(
#             API_SECRET.encode('utf-8'),
#             query_string.encode('utf-8'),
#             hashlib.sha256
#         ).hexdigest()
#         params["signature"] = signature
#         headers = {
#             "X-MBX-APIKEY": API_KEY
#         }
#         url = f"{BASE_URL}/fapi/v1/openOrder"
#         response = requests.post(url, params=params, headers=headers)
#         if response.status_code == 200:
#             print(f"\U0001F680 Sell order placed successfully: {response.json()}")
#             return True
#         else:
#             print(f"Error placing sell order: {response.status_code} - {response.json()}")
#             return False
#     except Exception as e:
#         print(f"Exception occurred while placing sell order: {e}")
#         return False


# def calculate_and_save_pnl(order_id, order_sell_status):
#     """
#     Calculates and logs the PnL for an order and places a sell order if conditions are met.
#     """
#     # Check if the order is already sold
#     if order_sell_status.get(str(order_id), None) == "Sold":
#         print(f"⚠️ Order ID {order_id} has already been sold. Skipping...")
#         return None

#     trades = fetch_order_details(order_id)
#     if trades is None:
#         return None

#     symbol = trades[0]['symbol']
#     total_quantity = sum(float(trade['qty']) for trade in trades)
#     avg_buy_price = sum(float(trade['price']) * float(trade['qty']) for trade in trades) / total_quantity
#     realized_pnl = sum(float(trade['realizedPnl']) for trade in trades)

#     current_price = fetch_current_price(symbol)
#     if current_price is None:

#         return None

#     unrealized_pnl = (current_price - avg_buy_price) * total_quantity
#     pnl_percentage = ((current_price - avg_buy_price) / avg_buy_price) * 100

#     if unrealized_pnl > 0:
#         profit = unrealized_pnl
#         loss = 0
#     else:
#         profit = 0
#         loss = abs(unrealized_pnl)

#     sell_status = "Holding"

#     if pnl_percentage  >= 5:  # Adjust thresholds as needed
#         print(f"\U0001F680 Profit exceeded 30% for Order ID {order_id}! Placing sell order...")
#         if place_sell_order(symbol, total_quantity):
#             sell_status = f"Sold with Profit ({pnl_percentage:.2f}%)"
#             order_sell_status[str(order_id)] = "Sold"
#     elif pnl_percentage <= -5:  # Adjust thresholds as needed
#         print(f"⚠️ Loss exceeded -5% for Order ID {order_id}! Placing sell order...")
#         if place_sell_order(symbol, total_quantity):
#             sell_status = f"Sold with Loss ({pnl_percentage:.2f}%)"
#             order_sell_status[str(order_id)] = "Sold"

#     data = {
#         "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         "orderId": order_id,
#         "symbol": symbol,
#         "buyPrice": avg_buy_price,
#         "currentPrice": current_price,
#         "quantity": total_quantity,
#         "realizedPnL": realized_pnl,
#         "unrealizedPnL": unrealized_pnl,
#         "pnlPercentage": pnl_percentage,
#         "profit": profit,
#         "loss": loss,
#         "sellStatus": sell_status
#     }

#     print("Order PnL Report:")
#     print(json.dumps(data, indent=4))

#     # Append data to JSON file
   
     
#     try:
#         with open(JSON_FILE_PATH, 'r') as json_file:
#             json_data = json.load(json_file)
#         print(f"✅ Successfully loaded JSON file: {JSON_FILE_PATH}")
#     except (FileNotFoundError, json.JSONDecodeError):
#         print(f"⚠️ JSON file not found or empty. Creating a new one: {JSON_FILE_PATH}")
#         json_data = []

#     json_data.append(data)

#     try:
#         with open(JSON_FILE_PATH, 'w') as json_file:
#             json.dump(json_data, json_file, indent=4)
#         print(f"✅ Successfully saved data to {JSON_FILE_PATH}")
#     except Exception as e:
#         print(f"❌ Error saving to JSON: {e}")


#     # Save sell status
#     response = save_order_sell_status(order_sell_status)
#     data["response"] = response
#     return data







# from flask import Flask, jsonify, request, Blueprint
# from flask_socketio import SocketIO
# from flask_socketio import emit
# import time
# import hmac
# import hashlib
# import requests
# import urllib.parse
# import json
# from threading import Thread
# from binance import ThreadedWebsocketManager 
# from datetime import datetime
# from config import SELL_STATUS_FILE_PATH, API_SECRET, API_KEY, BASE_URL, JSON_FILE_PATH
# from binance.client import Client
# # from binance.websocket.spot.websocket_client import SpotWebsocketClient


# pnl_report_bp = Blueprint('pnl_report', __name__)


# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSocket Support

# # Store latest prices in memory
# latest_prices = {}

# def start_binance_websocket():
#     """ Start Binance WebSocket to fetch real-time prices. """
#     def handle_message(msg):
#         if msg['e'] == '24hrTicker':  # 24-hour price update
#             symbol = msg['s']
#             price = float(msg['c'])
#             latest_prices[symbol] = price
#             socketio.emit('price_update', {symbol: price})  # Send update to frontend
#             print(f"📈 {symbol} Price Updated: {price}")

#     twm = ThreadedWebsocketManager(api_key=API_KEY, api_secret=API_SECRET)
#     twm.start()
#     twm.start_symbol_ticker_socket(callback=handle_message, symbol="BTCUSDT")  # Start for BTCUSDT
#     Symbols=["BTCUSDT", "ETHUSDT"] #BNBUSDT", "ADAUSDT", "XRPUSDT", "DOGEUSDT", "DOTUSDT", "UNIUSDT", "LTCUSDT", "LINKUSDT"]
#     # symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]  # Add more symbols as needed
#     for symbol in Symbols:
#         twm.start_symbol_ticker_socket(callback=handle_message, symbol=symbol)

#     twm.join()

# # Start WebSocket in a separate thread
# ws_thread = Thread(target=start_binance_websocket)
# ws_thread.daemon = True
# ws_thread.start()



# # Endpoint to fetch all active orders' PnL reports
# @pnl_report_bp.route('/pnl_report', methods=['GET'])
# def pnl_report():
#     from app import socketio

#     order_sell_status = load_order_sell_status()
#     try:
#         active_orders = fetch_active_orders()
#         if not active_orders:
#             socketio.emit('status_update',{"massage": "No active orders found."})
#             # print("No active orders found. Exiting script...")
#             return jsonify({"message": "No active orders found."})

#         unsold_orders = [order for order in active_orders if order_sell_status.get(str(order["orderId"])) != "Sold"]

#         if not unsold_orders:
#             print("\n✅ All orders have been sold. Exiting script...")
            
#         res_data = []
        
#         for order in active_orders:
#             order_id = order["orderId"]
#             print(f"\nProcessing Order ID: {order_id}")
#             socketio.emit('status_update',{'massage': f"Processing Order ID{order_id}"})

#             res_data.append(calculate_and_save_pnl(order_id, order_sell_status))
#             if res_data:
#                 print(json.dumps(res_data, indent=4))

#         # Stop when all orders are processed
#         if all(order_sell_status.get(str(order["orderId"])) == "Sold" for order in active_orders):
#             print("\n✅ All orders have been sold based on PnL conditions. Exiting script...")


#         return res_data
#     except Exception as err:
#         return jsonify({"message": f"{err}"})

# @socketio.on('connect')
# def handle_connect():
#     print("Client connected")
#     emit('status_update', {"message": "Connected to WebSocket."})

# @socketio.on('disconnect')
# def handle_disconnect():
#     print("Client disconnected")


# def fetch_active_orders():
#     """
#     Fetches all active open positions.
#     """
#     try:
#         timestamp = int(time.time() * 1000)
#         params = {
#             "timestamp": timestamp,
#             # "symbol" : "BTCUSDT",
#             "recvWindow": 5000  # Helps avoid timestamp errors
#         }
#         query_string = urllib.parse.urlencode(params)
#         signature = hmac.new(
#             API_SECRET.encode('utf-8'),
#             query_string.encode('utf-8'),
#             hashlib.sha256
#         ).hexdigest()
#         params["signature"] = signature
#         headers = {"X-MBX-APIKEY": API_KEY}
#         url = f"{BASE_URL}/fapi/v1/allOrders"
#         response = requests.get(url, params=params, headers=headers)
        
#         if response.status_code == 200:
#             orders = response.json()
#             # print("_____________", orders)
#             if not orders:
#                 print("No open orders found.")
#                 return []   
#             print("Active Orders Fetched Successfully!")
#             return orders[-10:]  # Return only the last 10 orders
#         else:
#             print(f"Error fetching active orders: {response.status_code} - {response.json()}")
#             return []

#     except Exception as e:
#         print(f"Exception occurred while fetching active orders: {e}")
#         return []



# def load_order_sell_status():
#     try:
#         with open(SELL_STATUS_FILE_PATH, 'r') as file:
#             return json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return {}


# def save_order_sell_status(order_sell_status):
#     try:
#         with open(SELL_STATUS_FILE_PATH, 'w') as file:
#             json.dump(order_sell_status, file, indent=4)
#         return "Data saved successfully!!!!"
#     except Exception as e:
#         return f"Error saving sell status: {e}"




# def fetch_order_details(order_id):
#     try:
#         timestamp = int(time.time() * 1000)
#         params = {
#             "orderId": order_id,
#             "timestamp": timestamp
#         }
#         query_string = urllib.parse.urlencode(params)
#         signature = hmac.new(
#             API_SECRET.encode('utf-8'),
#             query_string.encode('utf-8'),
#             hashlib.sha256
#         ).hexdigest()
#         params["signature"] = signature
#         headers = {
#             "X-MBX-APIKEY": API_KEY
#         }
#         url = f"{BASE_URL}/fapi/v1/userTrades"
#         response = requests.get(url, params=params, headers=headers)
#         if response.status_code == 200:
#             trades = response.json()
#             if not trades:
#                 print(f"No trades found for order ID {order_id}")
#                 # print("+++++++++++++++++++++")
#                 return None
#             # print("-----------",trades)
#             return trades
#         else:
#             print(f"Error fetching order details: {response.status_code} - {response.json()}")
#             return None
#     except Exception as e:
#         print(f"Exception occurred: {e}")
#         return None
    
    

# def fetch_current_price(symbol):
#     try:
#         url = f"{BASE_URL}/fapi/v1/ticker/price?symbol={symbol}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             return float(response.json()["price"])
#         else:
#             print(f"Error fetching current price for {symbol}: {response.status_code} - {response.json()}")
#             return None
#     except Exception as e:
#         print(f"Exception occurred: {e}")
#         return None    



# def place_sell_order(symbol, quantity):
#     try:
#         timestamp = int(time.time() * 1000)
#         params = {
#             "symbol": symbol,
#             "side": "SELL",
#             "type": "MARKET",
#             "quantity": quantity,
#             "timestamp": timestamp
#         }
#         query_string = urllib.parse.urlencode(params)
#         signature = hmac.new(
#             API_SECRET.encode('utf-8'),
#             query_string.encode('utf-8'),
#             hashlib.sha256
#         ).hexdigest()
#         params["signature"] = signature
#         headers = {
#             "X-MBX-APIKEY": API_KEY
#         }
#         url = f"{BASE_URL}/fapi/v1/openOrder"
#         response = requests.post(url, params=params, headers=headers)
#         if response.status_code == 200:
#             print(f"\U0001F680 Sell order placed successfully: {response.json()}")
#             return True
#         else:
#             print(f"Error placing sell order: {response.status_code} - {response.json()}")
#             return False
#     except Exception as e:
#         print(f"Exception occurred while placing sell order: {e}")
#         return False


# def calculate_and_save_pnl(order_id, order_sell_status):
#     """
#     Calculates and logs the PnL for an order and places a sell order if conditions are met.
#     """
#     # Check if the order is already sold
#     if order_sell_status.get(str(order_id), None) == "Sold":
#         print(f"⚠️ Order ID {order_id} has already been sold. Skipping...")
#         return None

#     trades = fetch_order_details(order_id)
#     if trades is None:
#         return None

#     symbol = trades[0]['symbol']
#     total_quantity = sum(float(trade['qty']) for trade in trades)
#     avg_buy_price = sum(float(trade['price']) * float(trade['qty']) for trade in trades) / total_quantity
#     realized_pnl = sum(float(trade['realizedPnl']) for trade in trades)

#     current_price = fetch_current_price(symbol)
#     if current_price is None:
#         return None

#     unrealized_pnl = (current_price - avg_buy_price) * total_quantity
#     pnl_percentage = ((current_price - avg_buy_price) / avg_buy_price) * 100

#     if unrealized_pnl > 0:
#         profit = unrealized_pnl
#         loss = 0
#     else:
#         profit = 0
#         loss = abs(unrealized_pnl)

#     sell_status = "Holding"

#     if pnl_percentage  >= 5:  # Adjust thresholds as needed
#         print(f"\U0001F680 Profit exceeded 30% for Order ID {order_id}! Placing sell order...")
#         if place_sell_order(symbol, total_quantity):
#             sell_status = f"Sold with Profit ({pnl_percentage:.2f}%)"
#             order_sell_status[str(order_id)] = "Sold"
#     elif pnl_percentage <= -5:  # Adjust thresholds as needed
#         print(f"⚠️ Loss exceeded -5% for Order ID {order_id}! Placing sell order...")
#         if place_sell_order(symbol, total_quantity):
#             sell_status = f"Sold with Loss ({pnl_percentage:.2f}%)"
#             order_sell_status[str(order_id)] = "Sold"

#     data = {
#         "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         "orderId": order_id,
#         "symbol": symbol,
#         "buyPrice": avg_buy_price,
#         "currentPrice": current_price,
#         "quantity": total_quantity,
#         "realizedPnL": realized_pnl,
#         "unrealizedPnL": unrealized_pnl,
#         "pnlPercentage": pnl_percentage,
#         "profit": profit,
#         "loss": loss,
#         "sellStatus": sell_status
#     }

#     print("Order PnL Report:")
#     print(json.dumps(data, indent=4))

#     # Append data to JSON file
   
     
#     try:
#         with open(JSON_FILE_PATH, 'r') as json_file:
#             json_data = json.load(json_file)
#         print(f"✅ Successfully loaded JSON file: {JSON_FILE_PATH}")
#     except (FileNotFoundError, json.JSONDecodeError):
#         print(f"⚠️ JSON file not found or empty. Creating a new one: {JSON_FILE_PATH}")
#         json_data = []

#     json_data.append(data)

#     try:
#         with open(JSON_FILE_PATH, 'w') as json_file:
#             json.dump(json_data, json_file, indent=4)
#         print(f"✅ Successfully saved data to {JSON_FILE_PATH}")
#     except Exception as e:
#         print(f"❌ Error saving to JSON: {e}")


#     # Save sell status
#     response = save_order_sell_status(order_sell_status)
#     data["response"] = response
#     return data





















# from flask import Flask, jsonify, request, Blueprint
# from flask_socketio import SocketIO, emit
# import time
# import hmac
# import hashlib
# import requests
# import urllib.parse
# import json
# from threading import Thread
# from binance import ThreadedWebsocketManager 
# from datetime import datetime
# from config import SELL_STATUS_FILE_PATH, API_SECRET, API_KEY, BASE_URL, JSON_FILE_PATH
# from binance.client import Client
# from extensions import socketio


# # Create Blueprint for PnL report
# pnl_report_bp = Blueprint('pnl_report', __name__)

# # Store latest prices in memory
# latest_prices = {}

# def start_binance_websocket():
#     """ Start Binance WebSocket to fetch real-time prices. """
#     def handle_message(msg):
#         if msg['e'] == '24hrTicker':  # 24-hour price update
#             symbol = msg['s']
#             price = float(msg['c'])
#             latest_prices[symbol] = price
#             socketio.emit('price_update', {symbol: price})  # Send update to frontend
#             print(f"📈 {symbol} Price Updated: {price}")

#     twm = ThreadedWebsocketManager(api_key=API_KEY, api_secret=API_SECRET)
#     twm.start()
#     # twm.start_symbol_ticker_socket(callback=handle_message, symbol="BTCUSDT")  # Start for BTCUSDT
#     symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]  # Add more symbols as needed
#     for symbol in symbols:
#         twm.start_symbol_ticker_socket(callback=handle_message, symbol=symbol)
#     twm.join()

# # Start WebSocket in a separate thread
# ws_thread = Thread(target=start_binance_websocket)
# ws_thread.daemon = True
# ws_thread.start()   


# # Fetch Active Orders API
# @pnl_report_bp.route('/pnl_report', methods=['GET'])
# def pnl_report():
#     order_sell_status = load_order_sell_status()
#     try:
#         active_orders = fetch_active_orders()
#         if not active_orders:
#             socketio.emit('status_update', {"message": "No active orders found."})
#             return jsonify({"message": "No active orders found."})

#         res_data = []
        
#         for order in active_orders:
#             order_id = order["orderId"]
#             print(f"\nProcessing Order ID: {order_id}")
#             socketio.emit('status_update', {'message': f"Processing Order ID {order_id}"})
#             res_data.append(calculate_and_save_pnl(order_id, order_sell_status))
#             if res_data:
#                 print(json.dumps(res_data, indent=4))

#         # Notify clients if all orders are processed
#         if all(order_sell_status.get(str(order["orderId"])) == "Sold" for order in active_orders):
#             print("\n✅ All orders processed. Stopping monitoring.")

#         # Emit PnL updates to WebSocket clients
#         socketio.emit("pnl_update", res_data)
#         return res_data
#         # return jsonify(res_data, 200)
#     except Exception as err:
#         return jsonify({"message": f"Error: {err}"}), 500

# def fetch_active_orders():
#     """ 
#     Fetches all active open positions.
#     """
#     try:
#         timestamp = int(time.time() * 1000)
#         params = {
#             "timestamp": timestamp,
#             "recvWindow": 5000  
#         }
#         query_string = urllib.parse.urlencode(params)
#         signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
#         params["signature"] = signature
#         headers = {"X-MBX-APIKEY": API_KEY}
#         url = f"{BASE_URL}/fapi/v1/allOrders"
#         response = requests.get(url, params=params, headers=headers)
        
#         if response.status_code == 200:
#             orders = response.json()
#             if not orders:
#                 print("No open orders found.")
#                 return []   
#             print("✅ Active Orders Fetched Successfully!")
#             return orders[-10:]  # Return only the last 10 orders
#             # return orders
#         else:
#             print(f"❌ Error fetching orders: {response.status_code} - {response.json()}")
#             return []

#     except Exception as e:
#         print(f"❌ Exception fetching orders: {e}")
#         return []

# def load_order_sell_status():
#     try:
#         with open(SELL_STATUS_FILE_PATH, 'r') as file:
#             return json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return {}

# def save_order_sell_status(order_sell_status):
#     try:
#         with open(SELL_STATUS_FILE_PATH, 'w') as file:
#             json.dump(order_sell_status, file, indent=4)
#         return "✅ Sell status saved successfully!"
#     except Exception as e:
#         return f"❌ Error saving sell status: {e}"
    
    



# def fetch_order_details(order_id):
#     try:
#         timestamp = int(time.time() * 1000)
#         params = {
#             "orderId": order_id,
#             "timestamp": timestamp
#         }
#         query_string = urllib.parse.urlencode(params)
#         signature = hmac.new(
#             API_SECRET.encode('utf-8'),
#             query_string.encode('utf-8'),
#             hashlib.sha256
#         ).hexdigest()
#         params["signature"] = signature
#         headers = {
#             "X-MBX-APIKEY": API_KEY
#         }
#         url = f"{BASE_URL}/fapi/v1/userTrades"
#         response = requests.get(url, params=params, headers=headers)
#         if response.status_code == 200:
#             trades = response.json()
#             if not trades:
#                 print(f"No trades found for order ID {order_id}")
#                 # print("+++++++++++++++++++++")
#                 return None
#             # print("-----------",trades)
#             return trades
#         else:
#             print(f"Error fetching order details: {response.status_code} - {response.json()}")
#             return None
#     except Exception as e:
#         print(f"Exception occurred: {e}")
#         return None



# def fetch_current_price(symbol):
#     try:
#         url = f"{BASE_URL}/fapi/v1/ticker/price?symbol={symbol}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             return float(response.json()["price"])
#         else:
#             print(f"❌ Error fetching price for {symbol}: {response.status_code} - {response.json()}")
#             return None
#     except Exception as e:
#         print(f"❌ Exception fetching price: {e}")
#         return None    

# def place_sell_order(symbol, quantity):
#     try:
#         timestamp = int(time.time() * 1000)
#         params = {
#             "symbol": symbol,
#             "side": "SELL",
#             "type": "MARKET",
#             "quantity": quantity,
#             "timestamp": timestamp
#         }
#         query_string = urllib.parse.urlencode(params)
#         signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
#         params["signature"] = signature
#         headers = {"X-MBX-APIKEY": API_KEY}
#         url = f"{BASE_URL}/fapi/v1/order"
#         response = requests.post(url, params=params, headers=headers)
#         if response.status_code == 200:
#             print(f"✅ Sell order placed successfully: {response.json()}")
#             return True
#         else:
#             print(f"❌ Error placing sell order: {response.status_code} - {response.json()}")
#             return False
#     except Exception as e:
#         print(f"❌ Exception placing sell order: {e}")
#         return False

# def calculate_and_save_pnl(order_id, order_sell_status):
#     """
#     Calculates and logs the PnL for an order and places a sell order if conditions are met.
#     """
#     # Check if the order is already sold
#     if order_sell_status.get(str(order_id), None) == "Sold":
#         print(f"⚠️ Order ID {order_id} has already been sold. Skipping...")
#         return None

#     trades = fetch_order_details(order_id)
#     if trades is None:
#         return None

#     symbol = trades[0]['symbol']
#     total_quantity = sum(float(trade['qty']) for trade in trades)
#     avg_buy_price = sum(float(trade['price']) * float(trade['qty']) for trade in trades) / total_quantity
#     realized_pnl = sum(float(trade['realizedPnl']) for trade in trades)

#     current_price = fetch_current_price(symbol)
#     if current_price is None:
#         return None

#     unrealized_pnl = (current_price - avg_buy_price) * total_quantity
#     pnl_percentage = ((current_price - avg_buy_price) / avg_buy_price) * 100

#     if unrealized_pnl > 0:
#         profit = unrealized_pnl
#         loss = 0
#     else:
#         profit = 0
#         loss = abs(unrealized_pnl)

#     sell_status = "Holding"

#     if pnl_percentage  >= 25:  # Adjust thresholds as needed
#         print(f"\U0001F680 Profit exceeded 30% for Order ID {order_id}! Placing sell order...")
#         if place_sell_order(symbol, total_quantity):
#             sell_status = f"Sold with Profit ({pnl_percentage:.2f}%)"
#             order_sell_status[str(order_id)] = "Sold"
#     elif pnl_percentage <= -35:  # Adjust thresholds as needed
#         print(f"⚠️ Loss exceeded -5% for Order ID {order_id}! Placing sell order...")
#         if place_sell_order(symbol, total_quantity):
#             sell_status = f"Sold with Loss ({pnl_percentage:.2f}%)"
#             order_sell_status[str(order_id)] = "Sold"

#     data = {
#         "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         "orderId": order_id,
#         "symbol": symbol,
#         "buyPrice": avg_buy_price,
#         "currentPrice": current_price,
#         "quantity": total_quantity,
#         "realizedPnL": realized_pnl,
#         "unrealizedPnL": unrealized_pnl,
#         "pnlPercentage": pnl_percentage,
#         "profit": profit,
#         "loss": loss,
#         "sellStatus": sell_status
#     }

#     print("Order PnL Report:")
#     print(json.dumps(data, indent=4))


#     # Save sell status
#     response = save_order_sell_status(order_sell_status)
#     data["response"] = response

#     socketio.emit("pnl_update", data)
#     return data












# from flask import Flask, jsonify, request, Blueprint
# from flask_socketio import SocketIO, emit
# import time
# import hmac
# import hashlib
# import requests
# import urllib.parse
# import json
# from threading import Thread
# from binance import ThreadedWebsocketManager 
# from datetime import datetime
# from config import SELL_STATUS_FILE_PATH, API_SECRET, API_KEY, BASE_URL, JSON_FILE_PATH
# from binance.client import Client
# from extensions import socketio


# # Create Blueprint for PnL report
# pnl_report_bp = Blueprint('pnl_report', __name__)

# # Store latest prices in memory
# latest_prices = {}

# def start_binance_websocket():
#     """ Start Binance WebSocket to fetch real-time prices. """
#     def handle_message(msg):
#         # print("-------------",msg)
#         # if msg['data']['e'] == '24hrTicker':  # 24-hour price update
#         if 'data' in msg and msg['data']['e'] == 'markPriceUpdate':
#             symbol = msg['data']['s']
#             price = float(msg['data']['p'])
#             latest_prices[symbol] = price
#             socketio.emit('price_update', {symbol: price})  # Send update to frontend
#             print(f"📈 {symbol} Price Updated: {price}")

#     twm = ThreadedWebsocketManager(api_key=API_KEY, api_secret=API_SECRET)
#     twm.start()
#     # twm.start_symbol_ticker_socket(callback=handle_message, symbol="BTCUSDT")  # Start for BTCUSDT
#     symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]  # Add more symbols as needed
#     for symbol in symbols:
#         twm.start_symbol_mark_price_socket(callback=handle_message, symbol=symbol)  
#     twm.join()

# # Start WebSocket in a separate thread
# ws_thread = Thread(target=start_binance_websocket)
# ws_thread.daemon = True
# ws_thread.start()   

# # def start_binance_websocket():
# #     """ Start Binance WebSocket to fetch real-time prices. """
# #     print("🔄 Starting Binance WebSocket connection...")  # Debug log

# #     def handle_message(msg):
# #         # print("📩 WebSocket message received:", msg)  # Debug log
        
# #         if 'data' in msg and msg['data']['e'] == 'markPriceUpdate':  # Ensure correct structure
# #             symbol = msg['data']['s']
# #             # mark_price = float(msg['data']['p'])  # Mark Price
# #             index_price = float(msg['data']['P'])  # Index Price (Binance Futures)

# #             # Store the index price, as Binance Futures UI uses this
# #             latest_prices[symbol] = index_price
# #             socketio.emit('price_update', {symbol: index_price})  # Send update to frontend

# #             print(f"✅ {symbol} Price Updated: {index_price} (Index Price)")

# #     try:
# #         twm = ThreadedWebsocketManager(api_key=API_KEY, api_secret=API_SECRET)
# #         twm.start()
        
# #         symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]  # Add more symbols as needed
# #         for symbol in symbols:
# #             twm.start_symbol_mark_price_socket(callback=handle_message, symbol=symbol)  

# #         twm.join()
# #     except Exception as e:
# #         print(f"❌ WebSocket connection failed: {e}")

# # # # Start WebSocket in a separate thread
# # ws_thread = Thread(target=start_binance_websocket)
# # ws_thread.daemon = True
# # ws_thread.start()  



# # Fetch Active Orders API
# @pnl_report_bp.route('/pnl_report', methods=['GET'])
# def pnl_report():
#     order_sell_status = load_order_sell_status()
#     try:
#         active_orders = fetch_active_orders()
#         if not active_orders:
#             socketio.emit('status_update', {"message": "No active orders found."})
#             return jsonify({"message": "No active orders found."})

#         res_data = []
        
#         for order in active_orders:
#             order_id = order["orderId"]
#             print(f"\nProcessing Order ID: {order_id}")
#             socketio.emit('status_update', {'message': f"Processing Order ID {order_id}"})
#             res_data.append(calculate_and_save_pnl(order_id, order_sell_status))
#             if res_data:
#                 print(json.dumps(res_data, indent=4))

#         # Notify clients if all orders are processed
#         if all(order_sell_status.get(str(order["orderId"])) == "Sold" for order in active_orders):
#             print("\n✅ All orders processed. Stopping monitoring.")

#         # Emit PnL updates to WebSocket clients
#         socketio.emit("pnl_update", res_data)
#         return res_data
#         # return jsonify(res_data, 200)
#     except Exception as err:
#         print("---------------------------")
#         print(err)
#         import traceback
#         traceback.print_exc()
#         return jsonify({"message": f"Error: {err}"}), 500


# def fetch_active_orders():
#     """ 
#     Fetches all active open positions.
#     """
#     try:
#         timestamp = int(time.time() * 1000)
#         params = {
#             "timestamp": timestamp,
#             "recvWindow": 5000  
#         }
#         query_string = urllib.parse.urlencode(params)
#         signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
#         params["signature"] = signature
#         headers = {"X-MBX-APIKEY": API_KEY}
#         url = f"{BASE_URL}/fapi/v1/allOrders"
#         response = requests.get(url, params=params, headers=headers)
        
#         if response.status_code == 200:
#             orders = response.json()
#             if not orders:
#                 print("No open orders found.")
#                 return []   
#             print("✅ Active Orders Fetched Successfully!")
#             return orders[-10:]  # Return only the last 10 orders
#             # return orders
#         else:
#             print(f"❌ Error fetching order-----------------s: {response.status_code} - {response.json()}")
#             return []

#     except Exception as e:
#         print(f"❌ Exception fetching orders: {e}")
#         return []




# def load_order_sell_status():
#     try:
#         with open(SELL_STATUS_FILE_PATH, 'r') as file:
#             return json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return {}



# def save_order_sell_status(order_sell_status):
#     try:
#         with open(SELL_STATUS_FILE_PATH, 'w') as file:
#             json.dump(order_sell_status, file, indent=4)
#         return "✅ Sell status saved successfully!"
#     except Exception as e:
#         return f"❌ Error saving sell status: {e}"
    
    



# def fetch_order_details(order_id):
#     try:
#         timestamp = int(time.time() * 1000)
#         params = {
#             "orderId": order_id,
#             "timestamp": timestamp
#         }
#         query_string = urllib.parse.urlencode(params)
#         signature = hmac.new(
#             API_SECRET.encode('utf-8'),
#             query_string.encode('utf-8'),
#             hashlib.sha256
#         ).hexdigest()
#         params["signature"] = signature
#         headers = {
#             "X-MBX-APIKEY": API_KEY
#         }
#         url = f"{BASE_URL}/fapi/v1/userTrades"
#         response = requests.get(url, params=params, headers=headers)
#         if response.status_code == 200:
#             trades = response.json()
#             if not trades:
#                 print(f"No trades found for order ID {order_id}")
#                 # print("+++++++++++++++++++++")
#                 return None
#             # print("-----------",trades)
#             return trades
#         else:
#             print(f"Error fetching order details: {response.status_code} - {response.json()}")
#             return None
#     except Exception as e:
#         print(f"Exception occurred: {e}")
#         return None



# # def fetch_current_price(symbol):
# #     try:
# #         url = f"{BASE_URL}/fapi/v1/premiumIndex?symbol={symbol}"
# #         # url = f"{BASE_URL}/fapi/v1/ticker/price?symbol={symbol}"
# #         response = requests.get(url)
# #         if response.status_code == 200:
# #             return float(response.json()["markPrice"])
# #         else:
# #             print(f"❌ Error fetching price for {symbol}: {response.status_code} - {response.json()}")
# #             return None
# #     except Exception as e:
# #         print(f"❌ Exception fetching price: {e}")
# #         return None    
    
    
# def fetch_current_price(symbol):
#     """ Fetch real-time price from the WebSocket data instead of API calls. """
#     try:
#         if symbol in latest_prices:
#             return latest_prices[symbol]
#         else:
#             print(f"⚠️ No real-time price available for {symbol}, fetching via API...")
#             url = f"{BASE_URL}/fapi/v1/premiumIndex?symbol={symbol}"
#             response = requests.get(url)
#             if response.status_code == 200:
#                 return float(response.json()["markPrice"])
#             else:
#                 print(f"❌ Error fetching price for {symbol}: {response.status_code} - {response.json()}")
#                 return None
#     except Exception as e:
#         print(f"❌ Exception fetching price: {e}")
#         return None

    


# def place_sell_order(symbol, quantity):
#     try:
#         timestamp = int(time.time() * 1000)
#         params = {
#             "symbol": symbol,
#             "side": "SELL",
#             "type": "MARKET",
#             "quantity": quantity,
#             "timestamp": timestamp
#         }
#         query_string = urllib.parse.urlencode(params)
#         signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
#         params["signature"] = signature
#         headers = {"X-MBX-APIKEY": API_KEY}
#         url = f"{BASE_URL}/fapi/v1/order"
#         response = requests.post(url, params=params, headers=headers)
#         if response.status_code == 200:
#             print(f"✅ Sell order placed successfully: {response.json()}")
#             return True
#         else:
#             print(f"❌ Error placing sell order: {response.status_code} - {response.json()}")
#             return False
#     except Exception as e:
#         print(f"❌ Exception placing sell order: {e}")
#         return False


# def calculate_and_save_pnl(order_id, order_sell_status):
#     """
#     Calculates and logs the PnL for an order and places a sell order if conditions are met.
#     """
#     # Check if the order is already sold
#     if order_sell_status.get(str(order_id), None) == "Sold":
#         print(f"⚠️ Order ID {order_id} has already been sold. Skipping...")
#         return None

#     trades = fetch_order_details(order_id)
#     if trades is None:
#         return None

#     symbol = trades[0]['symbol']
#     total_quantity = sum(float(trade['qty']) for trade in trades)
#     avg_buy_price = sum(float(trade['price']) * float(trade['qty']) for trade in trades) / total_quantity
#     realized_pnl = sum(float(trade['realizedPnl']) for trade in trades)

#     current_price = fetch_current_price(symbol)
#     if current_price is None:
#         return None

#     unrealized_pnl = (current_price - avg_buy_price) * total_quantity
#     pnl_percentage = ((current_price - avg_buy_price) / avg_buy_price) * 100

#     if unrealized_pnl > 0:
#         profit = unrealized_pnl
#         loss = 0
#     else:
#         profit = 0
#         loss = abs(unrealized_pnl)

#     sell_status = "Holding"

#     if pnl_percentage  >= 50:  # Adjust thresholds as needed
#         print(f"\U0001F680 Profit exceeded 30% for Order ID {order_id}! Placing sell order...")
#         if place_sell_order(symbol, total_quantity):
#             sell_status = f"Sold with Profit ({pnl_percentage:.2f}%)"
#             order_sell_status[str(order_id)] = "Sold"
#     elif pnl_percentage <= -25:  # Adjust thresholds as needed
#         print(f"⚠️ Loss exceeded -5% for Order ID {order_id}! Placing sell order...")
#         if place_sell_order(symbol, total_quantity):
#             sell_status = f"Sold with Loss ({pnl_percentage:.2f}%)"
#             order_sell_status[str(order_id)] = "Sold"

#     data = {
#         "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         "orderId": order_id,
#         "symbol": symbol,
#         "buyPrice": avg_buy_price,
#         "currentPrice": current_price,
#         "quantity": total_quantity,
#         "realizedPnL": realized_pnl,
#         "unrealizedPnL": unrealized_pnl,
#         "pnlPercentage": pnl_percentage,
#         "profit": profit,
#         "loss": loss,
#         "sellStatus": sell_status
#     }

#     print("Order PnL Report:")
#     print(json.dumps(data, indent=4))


#     # Save sell status
#     response = save_order_sell_status(order_sell_status)
#     data["response"] = response

#     socketio.emit("pnl_update", data)
#     return data
