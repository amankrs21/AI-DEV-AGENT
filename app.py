import os
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask import Flask, send_from_directory, redirect, url_for, jsonify

# Local imports
from src.api.routes import api
from src.utils.build_ui import build_react


# Load environment variables
load_dotenv()


# Create Flask app
app = Flask(__name__, static_folder="client/dist/", static_url_path="/")


# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False   # Disable CSRF protection for now

JWTManager(app)


# Enable CORS
cors_url = os.getenv("CORS_URL", "*")
# CORS(app, resources={r"/*": {"origins": "*"}}, access_control_allow_origin=cors_url)
CORS(app, supports_credentials=True, origins=cors_url)


# Redirect root to /chat
@app.route("/")
def redirect_to_chat():
    return redirect(url_for("serve_react", path="chat"), code=302)


# Serve React app
@app.route("/<path:path>")
@app.route("/chat")
def serve_react(path="chat"):
    return send_from_directory(app.static_folder, "index.html")


# Register API blueprint
app.register_blueprint(api, url_prefix='/api')


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500


# Run the app
if __name__ == "__main__":
    if not os.path.exists("client/dist"):
        build_react()
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    app.run(host=host, port=port, debug=False, use_reloader=False)
