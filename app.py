import threading
import webbrowser
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS  # Import CORS extension

# local imports
from src.router import router
from src.build_ui import build_react


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
    """Opens the browser once after a slight delay."""
    webbrowser.open("http://127.0.0.1:5000")


# Function to run the Flask app
def run_flask():
    """Runs Flask without debug mode."""
    app.register_blueprint(router)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


# Main entry point
if __name__ == "__main__":
    # Check if --prod flag is provided
    is_prod = len(sys.argv) > 1 and sys.argv[1] == "--prod"

    if is_prod:
        # Production mode: Build UI, run Flask, and open browser
        build_react()  # Build the React UI first

        # Start the Flask app in a new thread
        flask_thread = threading.Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()

        # Open the browser once
        threading.Timer(1.5, open_browser).start()

        # Keep the main thread alive
        flask_thread.join()
    else:
        # Default mode: Just run the Flask server in the main thread
        app.register_blueprint(router)
        app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=True)
