import os
import shutil
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, Response, request, jsonify, make_response

# Local imports
from src.api.agent.public_agent import public_agent_chat
from src.api.agent.private_agent import private_agent_chat
from src.api.services.chat_memory import load_memory, delete_memory
from src.api.services.auth_user import register_user, login_user, get_current_user
from src.api.services.chat_history import fetch_histories, get_history, update_history, delete_history


# Create a Flask Blueprint for the router
api = Blueprint('api', __name__)


# Route to register
@api.route('/register', methods=['POST'])
def register():
    data = request.json
    response, status = register_user(
        data.get('name', ''),
        data.get('email', ''),
        data.get('password', '')
    )
    return jsonify(response), status


# Route to login
@api.route('/login', methods=['POST'])
def login():

    if request.method == 'OPTIONS':
        response = make_response()
        return response, 204
    
    data = request.json
    response, status = login_user(
        data.get('email', ''),
        data.get('password', '')
    )
    if status == 200:
        resp = make_response(jsonify({'message': response['message']}))
        resp.set_cookie(
            'access_token',
            value=response['access_token'],
            httponly=True,
            secure=True,   # TODO: Set to True in production with HTTPS
            samesite="Lax", # TODO: Set to 'Lax' in production with HTTPS or 'None' for cross-site
            max_age=3600
        )
        return resp, status
    return jsonify(response), status


# Route to logout
@api.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'message': 'Logged out successfully'}))
    response.delete_cookie('access_token')
    return response, 200


# Route to validate token and get user data
@api.route('/validate', methods=['GET'])
@jwt_required(locations=['cookies'])
def validate():
    response, status = get_current_user()
    return jsonify(response), status


# Route to get list of chats (protected)
@api.route('/history', methods=['GET'])
@jwt_required(locations=['cookies'])
def fetch_chat_list():
    user_id = get_jwt_identity()
    response, status = fetch_histories(user_id)
    return jsonify(response), status


# Route to get a specific chat (protected)
@api.route('/history/<chat_id>', methods=['GET'])
@jwt_required(locations=['cookies'])
def fetch_chat(chat_id):
    user_id = get_jwt_identity()
    response, status = get_history(user_id, chat_id)
    return jsonify(response), status


# Route to delete a specific chat (protected)
@api.route('/history/<chat_id>', methods=['DELETE'])
@jwt_required(locations=['cookies'])
def delete_chat(chat_id):
    user_id = get_jwt_identity()
    if (delete_history(user_id, chat_id) and delete_memory(user_id, chat_id)):
        return '', 204
    return jsonify({'error': 'Failed to delete chat'}), 500


@api.route('/history', methods=['DELETE'])
@jwt_required(locations=['cookies'])
def clear_history():
    user_id = get_jwt_identity()
    user_folder = f"data/{user_id}"
    if os.path.exists(user_folder):
        try:
            shutil.rmtree(user_folder)
            return '', 204
        except Exception as e:
            print(f"Error deleting chat: {e}")
            return jsonify({'error': 'Failed to delete chat'}), 500
    return jsonify({'error': 'Failed to delete chat'}), 500


# Route to chat processing (protected)
@api.route('/chat', methods=['POST'])
@jwt_required(locations=['cookies'])
def chat_mistral():
    user_id = get_jwt_identity()
    data = request.json
    chat_id = data.get('chat_id', None)
    user_query = data.get('query', None)

    if not user_query and not chat_id:
        return jsonify({'error': 'No query or chat_id provided'}), 400

    memory, new_chat_id = load_memory(user_id, chat_id)
        
    stream = private_agent_chat(user_query, memory, user_id, new_chat_id)

    def event_stream():
        full_response = ''
        for chunk in stream:
            full_response += chunk
            yield chunk
            
        update_history(user_id, new_chat_id, user_query, full_response)

    response = Response(event_stream(), mimetype='text/event-stream')
    response.headers['X-Chat-ID'] = new_chat_id
    response.headers['Access-Control-Expose-Headers'] = 'X-Chat-ID'
    
    return response


# Route to chat processing (public)
@api.route('/public/chat', methods=['POST'])
def chat_mistral_public():
    data = request.json
    user_query = data.get('query', None)
    session_id = data.get('session_id', None)
    
    if not user_query:
        return jsonify({'error': 'No query provided'}), 400
    if not session_id:
        return jsonify({'error': 'No session_id provided'}), 400

    stream = public_agent_chat(user_query, session_id)

    def event_stream():
        for chunk in stream:
            yield chunk
    
    response = Response(event_stream(), mimetype='text/event-stream')
    response.headers['X-Session-ID'] = session_id
    response.headers['Access-Control-Expose-Headers'] = 'X-Session-ID'
    return response
