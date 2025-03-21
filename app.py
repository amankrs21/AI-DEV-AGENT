import sys
import logging
import threading
import webbrowser
from flask_cors import CORS
from flask import Flask, send_from_directory

# local imports
from src.api.routes import api
from src.utils.build_ui import build_react


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Create Flask app
app = Flask(__name__, static_folder="client/dist/", static_url_path="/")


# Enable CORS for specific origins
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


# Main route to serve the React app
@app.route("/")
def serve_react():
    return send_from_directory(app.static_folder, "index.html")


# Function to open the browser
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


# Function to run the Flask app (Production Mode)
def run_flask():
    app.register_blueprint(api)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


# Main entry point
if __name__ == "__main__":
    
    # Check if --prod flag is provided (Production mode)
    is_prod = len(sys.argv) > 1 and sys.argv[1] == "--prod"
    
    if is_prod:
        # Production mode: Build the React UI and run the Flask server in a separate thread
        build_react()

        flask_thread = threading.Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()

        threading.Timer(1.5, open_browser).start()

        flask_thread.join()
        
    else:
        # Default mode: Just run the Flask server in the main thread
        app.register_blueprint(api)
        app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=True)
