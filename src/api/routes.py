from flask import Blueprint, request, jsonify, Response

# local imports
from src.core.ai_agent import chat_with_mistral
from src.api.services.file_handler import save_files, get_files, remove_file
from src.api.services.chat_history import update_chat_history, get_chat_history, delete_chat_history


# Create a Flask Blueprint for the router
api = Blueprint('api', __name__)


# Route to upload and process files
@api.route('/upload', methods=['POST'])
def upload_files():
    response, status = save_files()
    return jsonify(response), status


# Route to get uploaded files
@api.route('/files', methods=['GET'])
def list_files():
    response, status = get_files()
    return jsonify(response), status


# Route to remove uploaded files
@api.route('/files/<file_name>', methods=['DELETE'])
def delete_file(file_name):
    response, status = remove_file(file_name)
    return jsonify(response), status


# Route to get chat history
@api.route("/history", methods=["GET"])
def fetch_history():
    response, status = get_chat_history()
    return jsonify(response), status


# Route to delete chat history
@api.route("/history", methods=["DELETE"])
def clear_history():
    response, status = delete_chat_history()
    return jsonify(response), status


# Route to chat processing
@api.route("/chat", methods=["POST"])
def chat_mistral():
    data = request.json
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    stream = chat_with_mistral(user_query)

    def event_stream():
        full_response = ""
        for chunk in stream:
            full_response += chunk
            yield chunk
        update_chat_history(user_query, full_response)

    return Response(event_stream(), mimetype='text/event-stream')
