from flask import Flask, jsonify, request, Blueprint
from dhanhq import dhanhq
import datetime
import json
from config import client_id, access_token
from db import save_offline_order, get_db_connection


# Initialize DhanHQ API client
dhan = dhanhq(access_token, client_id)


HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "access-token": access_token,
    "client-id": client_id,
}

def is_market_open():
    """Returns True if the stock market is open."""
    now = datetime.datetime.now()
    return now.weekday() < 5 and 9 <= now.hour < 15  # Market open 9 AM - 3 PM

place_sell_order_bp = Blueprint("place_sell_order", __name__)

@place_sell_order_bp.route("/place_sell_order", methods=["POST"])
def place_sell_order():
    """Handles selling an existing buy order."""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["security_id", "exchange_segment", "quantity", "order_type", "product_type"]
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
        order_type = data["order_type"].upper()
        quantity = int(data["quantity"])
        product_type = data["product_type"]

        # Automatically set transaction type to "SELL"
        transaction_type = "SELL"

        price = float(data["price"]) if "price" in data and data["price"] is not None else 0.0
        trigger_price = float(data["trigger_price"]) if "trigger_price" in data and data["trigger_price"] is not None else None

        # Construct sell order payload
        order_payload = {
            "security_id": security_id,
            "exchange_segment": exchange_segment,
            "transaction_type": transaction_type,
            "quantity": quantity,
            "order_type": order_type,
            "product_type": product_type,
            "price": price if order_type in ["LIMIT", "STOP_LOSS"] else 0,  
            "trigger_price": trigger_price if order_type in ["STOP_LOSS", "STOP_LOSS_MARKET"] else 0  
        }

        # Remove unnecessary fields for market orders
        if order_type == "MARKET":
            order_payload.pop("price", None)  
            order_payload.pop("trigger_price", None)

        if order_type not in ["STOP_LOSS", "STOP_LOSS_MARKET"]:
            order_payload.pop("trigger_price", None)

        # Ensure price is set properly
        if order_type not in ["LIMIT", "STOP_LOSS"]:
            order_payload["price"] = 0  

        print(f"📦 Sending Sell Order Payload to Dhan API: {order_payload}")

        # If market is open, execute the sell order immediately
        if is_market_open():
            order_response = dhan.place_order(**order_payload)
            print(f"🚨 Sell Order Response from Dhan: {order_response}")

            if order_response.get("status") == "success":
                order_id = order_response["data"].get("orderId")

                if not order_id:
                    return jsonify({"error": "Order ID missing from response"}), 400

                # Save order in database with EXECUTED status
                save_offline_order(order_id, security_id, exchange_segment, transaction_type, quantity, order_type, product_type, price, trigger_price, "EXECUTED")

                return jsonify({
                    "status": "success",
                    "message": "Sell order placed and executed successfully",
                    "order_id": order_id,
                    "saved_data": order_payload
                }), 200

            return jsonify({
                "status": "error",
                "message": "Sell order placement failed",
                "details": order_response
            }), 400

        # If market is closed, save the order for later execution
        else:
            test_order_id = f"TEST_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            save_offline_order(test_order_id, security_id, exchange_segment, transaction_type, quantity, order_type, product_type, price, trigger_price, "PENDING")

            return jsonify({
                "status": "offline",
                "message": "Market closed. Sell order saved for execution when market opens.",
                "test_order_id": test_order_id,
                "saved_data": [order_payload]
            }), 200

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


def process_offline_orders():
    """Executes stored offline orders when the market opens and updates status."""
    if is_market_open():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM offline_order WHERE status = 'PENDING'")
        orders = cursor.fetchall()

        for order in orders:
            try:
                price = float(order["price"]) if order["price"] is not None else 0.0
                trigger_price = float(order["trigger_price"]) if order["trigger_price"] is not None else 0.0

                # Construct payload for Dhan API
                order_payload = {
                    "security_id": order["security_id"],
                    "exchange_segment": order["exchange_segment"],
                    "transaction_type": order["transaction_type"],
                    "quantity": order["quantity"],
                    "order_type": order["order_type"],
                    "product_type": order["product_type"],
                    "price": price,
                    "trigger_price": trigger_price
                }

                if order["order_type"] == "MARKET":
                    order_payload.pop("price", 0.0)
                    order_payload.pop("trigger_price", 0.0)

                print(f"📦 Processing Pending Order: {order_payload}")

                # Execute pending order
                order_response = dhan.place_order(**order_payload)

                print(f"🚀 Order Response: {order_response}")

                if order_response.get("status") == "success":
                    order_id = order_response["data"].get("orderId")
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
