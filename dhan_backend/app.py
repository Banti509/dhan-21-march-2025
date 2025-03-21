


# import sys
# import os
# from flask import Flask, jsonify
# from flask_socketio import SocketIO
# from flask_cors import CORS
# from flask import Flask, jsonify
# from flask_cors import CORS
# from db import save_offline_order, get_db_connection
# from apscheduler.schedulers.background import BackgroundScheduler
# from routes.dhan_new_order import place_order_bp
# from routes.dhan_security_id_search import search_bp
# from routes.dhan_pnl import pnl_report_bp
# from routes.dhan_login import auth_bp

# # ✅ Add project root to Python path (Fix ImportError)
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# app = Flask(__name__)

# # Allow CORS for all origins
# CORS(app, resources={r"/*": {"origins": "*"}})


# # ✅ Initialize Flask App
# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for WebSocket
# socketio = SocketIO(app, async_mode='eventlet')  # Explicitly set async_mode



# from flask_cors import CORS
# CORS(app)  # This will allow cross-origin requests from all domains.

# # ✅ Load Configurations
# app.config.from_object("config")

# # ✅ Enable CORS
# CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# # ✅ Register Blueprints (APIs)
# app.register_blueprint(place_order_bp, url_prefix="/api")
# app.register_blueprint(search_bp, url_prefix="/api")
# app.register_blueprint(pnl_report_bp, url_prefix="/api")
# app.register_blueprint(auth_bp, url_prefix="/api")



# # ✅ Run Flask App
# if __name__ == "__main__":
#     # socketio = SocketIO(app, cors_allowed_origins="*")
#     app.run(host="0.0.0.0", port=5000, debug=True)
#     socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")
#     socketio = SocketIO(app, cors_allowed_origins="*")
#     print("Starting Flask app with WebSocket support...")
#     socketio.run(app, host="0.0.0.0", port=5000, debug=True)







# import sys
# import os
# from flask import Flask, jsonify
# from flask_socketio import SocketIO
# from flask_cors import CORS
# from db import save_offline_order, get_db_connection
# from apscheduler.schedulers.background import BackgroundScheduler
# from routes.dhan_new_order import place_order_bp
# from routes.dhan_security_id_search import search_bp
# from routes.dhan_pnl import pnl_report_bp
# from routes.dhan_login import auth_bp

# # ✅ Fix ImportError by adding project root to Python path
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# # ✅ Initialize Flask App (Only once)
# app = Flask(__name__)

# # ✅ Load Configurations
# app.config.from_object("config")

# # ✅ Enable CORS
# CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# # ✅ Initialize Flask-SocketIO (Only once)
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# # ✅ Register Blueprints (APIs)
# app.register_blueprint(place_order_bp, url_prefix="/api")
# app.register_blueprint(search_bp, url_prefix="/api")
# app.register_blueprint(pnl_report_bp, url_prefix="/api")
# app.register_blueprint(auth_bp, url_prefix="/api")

# # ✅ Handle WebSocket Connection
# @socketio.on("connect")
# def handle_connect():
#     print("Client connected via WebSocket.")

# @socketio.on("disconnect")
# def handle_disconnect():
#     print("Client disconnected from WebSocket.")

# # ✅ Run Flask App with WebSocket Support
# if __name__ == "__main__":
#     print("Starting Flask app with WebSocket support...")
#     socketio.run(app, host="0.0.0.0", port=5000, debug=True)







# import sys
# import os
# from flask import Flask
# from flask_cors import CORS
# from apscheduler.schedulers.background import BackgroundScheduler
# from extensions import socketio  # ✅ Import socketio from extensions.py
# from routes.dhan_new_order import place_order_bp
# from routes.dhan_security_id_search import search_bp
# from routes.dhan_pnl import pnl_report_bp  # ✅ Do NOT import stream_pnl
# from routes.dhan_login import auth_bp

# # ✅ Fix ImportError by adding project root to Python path
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# # ✅ Initialize Flask App
# app = Flask(__name__)

# # ✅ Load Configurations
# app.config.from_object("config")

# # ✅ Enable CORS
# CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# # ✅ Initialize Flask-SocketIO
# socketio.init_app(app)  # ✅ Now `socketio` is correctly attached to the app

# # ✅ Register Blueprints (APIs)
# app.register_blueprint(place_order_bp, url_prefix="/api")
# app.register_blueprint(search_bp, url_prefix="/api")
# app.register_blueprint(pnl_report_bp, url_prefix="/api")
# app.register_blueprint(auth_bp, url_prefix="/api")

# # ✅ Handle WebSocket Connection
# @socketio.on("connect")
# def handle_connect():
#     print("✅ Client connected via WebSocket.")

# @socketio.on("disconnect")
# def handle_disconnect():
#     print("❌ Client disconnected from WebSocket.")

# # ✅ Start PnL Streaming as a Background Task (Safely)
# def start_pnl_stream():
#     from routes.dhan_pnl import stream_pnl  # ✅ Import inside function to avoid circular import
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(stream_pnl, "interval", seconds=5)
#     scheduler.start()

# start_pnl_stream()

# # ✅ Run Flask App with WebSocket Support
# if __name__ == "__main__":
#     print("🚀 Starting Flask app with WebSocket support...")
#     socketio.run(app, host="0.0.0.0", port=5000, debug=True)





# import sys
# import os
# from flask import Flask
# from flask_cors import CORS
# from apscheduler.schedulers.background import BackgroundScheduler
# from extensions import socketio  # ✅ Import socketio from extensions.py
# from routes.dhan_new_order import place_order_bp
# from routes.dhan_security_id_search import search_bp
# from routes.dhan_pnl import pnl_report_bp  # ✅ Do NOT import stream_pnl directly
# from routes.dhan_login import auth_bp

# # ✅ Fix ImportError by adding project root to Python path
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# # ✅ Initialize Flask App
# app = Flask(__name__)

# # ✅ Load Configurations
# app.config.from_object("config")

# # ✅ Enable CORS
# CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# # ✅ Initialize Flask-SocketIO
# socketio.init_app(app)

# # ✅ Register Blueprints (APIs)
# app.register_blueprint(place_order_bp, url_prefix="/api")
# app.register_blueprint(search_bp, url_prefix="/api")
# app.register_blueprint(pnl_report_bp, url_prefix="/api")
# app.register_blueprint(auth_bp, url_prefix="/api")

# # ✅ Handle WebSocket Connection
# @socketio.on("connect")
# def handle_connect():
#     print("✅ Client connected via WebSocket.")

# @socketio.on("disconnect")
# def handle_disconnect():
#     print("❌ Client disconnected from WebSocket.")

# # ✅ Start PnL Streaming as a Background Task (Safely)
# def start_pnl_stream():
#     from routes.dhan_pnl import stream_pnl  # ✅ Import inside function to avoid circular import
#     try:
#         global scheduler
#         if "scheduler" not in globals():
#             scheduler = BackgroundScheduler(daemon=True)  # ✅ Set daemon mode
#             scheduler.add_job(stream_pnl, "interval", seconds=1, id="pnl_stream", replace_existing=True)
#             scheduler.start()
#             print("✅ PnL streaming job started.")
#         else:
#             print("⚠️ PnL streaming job already running.")
#     except Exception as e:
#         print(f"❌ Error starting PnL stream: {e}")

# start_pnl_stream()

# # ✅ Run Flask App with WebSocket Support
# if __name__ == "__main__":
#     print("🚀 Starting Flask app with WebSocket support...")
#     socketio.run(app, host="0.0.0.0", port=5000, debug=True)







# import sys
# import os
# from flask import Flask
# from flask_cors import CORS
# from apscheduler.schedulers.background import BackgroundScheduler
# from extensions import socketio  # ✅ Import socketio from extensions.py
# from routes.dhan_new_order import place_order_bp
# from routes.dhan_security_id_search import search_bp
# from routes.dhan_pnl import pnl_report_bp  # ✅ Do NOT import stream_pnl directly
# from routes.dhan_login import auth_bp

# # ✅ Fix ImportError by adding project root to Python path
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# # ✅ Initialize Flask App
# app = Flask(__name__)

# # ✅ Load Configurations
# app.config.from_object("config")

# # ✅ Enable CORS (Allow API requests from any frontend)
# CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# # ✅ Initialize Flask-SocketIO
# socketio.init_app(app, cors_allowed_origins="*")  # ✅ Now `socketio` is correctly attached to the app

# # ✅ Register Blueprints (APIs)
# app.register_blueprint(place_order_bp, url_prefix="/api")
# app.register_blueprint(search_bp, url_prefix="/api")
# app.register_blueprint(pnl_report_bp, url_prefix="/api")
# app.register_blueprint(auth_bp, url_prefix="/api")

# # ✅ Handle WebSocket Connection
# @socketio.on("connect")
# def handle_connect():
#     print("✅ Client connected via WebSocket.")

# @socketio.on("disconnect")
# def handle_disconnect():
#     print("❌ Client disconnected from WebSocket.")

# # ✅ Start PnL Streaming as a Background Task
# def start_pnl_stream():
#     from routes.dhan_pnl import stream_pnl  # ✅ Import inside function to avoid circular import
#     print("🔹 Starting PnL Streaming in the background...")
    
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(stream_pnl, "interval", seconds=1, max_instances=1)
#     scheduler.start()
#     print("✅ PnL Streaming Started.")

# # ✅ Ensure the background job starts only once
# if __name__ != "__main__":
#     start_pnl_stream()

# # ✅ Run Flask App with WebSocket Support
# if __name__ == "__main__":
#     print("🚀 Starting Flask app with WebSocket support...")
#     socketio.run(app, host="0.0.0.0", port=5000, debug=True)







import sys
import os
from flask import Flask
from flask_cors import CORS
from extensions import socketio
from routes.dhan_new_order import place_order_bp
from routes.dhan_security_id_search import search_bp
from routes.dhan_pnl import pnl_report_bp
from routes.dhan_login import auth_bp
from routes.dhan_sell_order import place_sell_order_bp

# Fix ImportError by adding project root to Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Initialize Flask App
app = Flask(__name__)

# Load Configurations
app.config.from_object("config")

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Initialize Flask-SocketIO
# socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS for local development
socketio.init_app(app, cors_allowed_origins="http://localhost:3000", logger=True, engineio_logger=True)

# Register Blueprints
app.register_blueprint(place_order_bp, url_prefix="/api")
app.register_blueprint(search_bp, url_prefix="/api")
app.register_blueprint(pnl_report_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(place_sell_order_bp, url_prefix="/api")

# Removed generic connect/disconnect handlers to avoid conflict with namespace-specific handlers in pnl_report.py

# Run Flask App with WebSocket Support
if __name__ == "__main__":
    print("🚀 Starting Flask app with WebSocket support...")
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)










# import sys
# import os
# from flask import Flask
# from flask_cors import CORS
# from extensions import socketio
# from routes.dhan_new_order import place_order_bp
# from routes.dhan_security_id_search import search_bp
# from routes.dhan_pnl import pnl_report_bp
# from routes.dhan_login import auth_bp
# from routes.dhan_sell_order import place_sell_order_bp

# # Fix ImportError by adding project root to Python path
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# # Initialize Flask App
# app = Flask(__name__)

# # Load Configurations
# app.config.from_object("config")

# # Enable CORS
# CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# # Initialize Flask-SocketIO
# socketio.init_app(app, cors_allowed_origins="*")

# # Register Blueprints
# app.register_blueprint(place_order_bp, url_prefix="/api")
# app.register_blueprint(search_bp, url_prefix="/api")
# app.register_blueprint(pnl_report_bp, url_prefix="/api")
# app.register_blueprint(auth_bp, url_prefix="/api")
# app.register_blueprint(place_sell_order_bp, url_prefix="/api")

# # WebSocket Event Handlers
# @socketio.on("connect")
# def handle_connect():
#     print("Client connected via WebSocket.")

# @socketio.on("disconnect")
# def handle_disconnect():
#     print("Client disconnected from WebSocket.")

# if __name__ == "__main__":
#     print("Starting Flask app with WebSocket support...")
#     socketio.run(app, host="0.0.0.0", port=5000, debug=True)