import os
import json
import logging
from flask import Blueprint, request, jsonify

# local imports
from .chat.mistral import chat_with_mistral
from .handler.file_handler import save_files, get_files, remove_file
# from .code_scan import project_initial_report, scan_directory, scan_dependencies, scan_security, save_code_snapshot


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Create a Flask Blueprint for the router
router = Blueprint("router", __name__)


# Route to upload and process files
@router.route("/upload-files", methods=["POST"])
def upload_files():
    return save_files()


# Route to get uploaded files
@router.route("/uploaded-files", methods=["GET"])
def fetch_files():
    return get_files()


# Route to remove uploaded files
@router.route("/remove-file/<file>", methods=["DELETE"])
def delete_file(file):
    return remove_file(file)


# Route to chat processing (to be integrated later)
@router.route("/chat-process", methods=["POST"])
def chat_process():
    data = request.json
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # AI Model integration will happen here
    response_message = f"Received query: {user_query}. AI response will be processed."

    return jsonify({"response": response_message})


@router.route("/chat-mistral", methods=["POST"])
def chat_mistral():
    data = request.json
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # AI Model integration will happen here
    response_message = chat_with_mistral(user_query)
    print(response_message)

    return jsonify({"response": response_message})
