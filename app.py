import os
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, send_from_directory, redirect, url_for

# local imports
from src.api.routes import api
from src.utils.build_ui import build_react


# Load environment variables from .env file
load_dotenv()


# Create Flask app
app = Flask(__name__, static_folder="client/dist/", static_url_path="/")


# Enable CORS for specific origins
cors_url = os.getenv("CORS_URL", "")
CORS(app, resources={r"/*": {"origins": cors_url}})


# Redirect root to /chat
@app.route("/")
def redirect_to_chat():
    return redirect(url_for("serve_react", path="chat"), code=302)

# Serve React app for /chat and other routes
@app.route("/<path:path>")
@app.route("/chat")
def serve_react(path="chat"):
    return send_from_directory(app.static_folder, "index.html")


# Register API blueprint
app.register_blueprint(api, url_prefix='/api')


# Function to run the Flask app (Production Mode)
def run_flask():
    app.register_blueprint(api, url_prefix='/api')
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


# Build React UI before running (optional, if not pre-built)
if not os.path.exists("client/dist"):
    build_react()


# Run the app
if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    app.run(host=host, port=port, debug=False, use_reloader=False)
