import os
import json
import uuid
import shutil


# Function to get the path for chat history
def get_history_path(user_id, chat_id=None):
    """Generate the file path for chat history based on user_id and chat_id."""
    base_dir = f"data/{user_id}/history"
    os.makedirs(base_dir, exist_ok=True)
    
    if chat_id is None:
        # Generate a unique chat_id if none provided
        chat_id = str(uuid.uuid4())
        return f"{base_dir}/{chat_id}.json", chat_id
    return f"{base_dir}/{chat_id}.json", chat_id



# Function to get list of chats history with names
def fetch_histories(user_id):
    history_dir = f"data/{user_id}/history"
    if not os.path.exists(history_dir):
        return [], 200

    chat_files = [f for f in os.listdir(history_dir) if f.endswith(".json")]
    chat_list = []

    for chat_file in chat_files:
        chat_id = chat_file[:-5]  # Remove .json extension
        file_path = os.path.join(history_dir, chat_file)

        try:
            with open(file_path, "r") as f:
                chat_history = json.load(f)
                # Get the first user query if it exists
                first_query = next((entry["user"] for entry in chat_history if "user" in entry), "Unnamed Chat")
                # Truncate to a short name (e.g., 30 characters)
                short_name = first_query[:30] + "..." if len(first_query) > 30 else first_query
                chat_list.append({"id": chat_id, "name": short_name})
        except (json.JSONDecodeError, FileNotFoundError):
            # Handle corrupted or missing files gracefully
            chat_list.append({"id": chat_id, "name": "Unnamed Chat"})

    return chat_list, 200



# Function to get a chat history data
def get_history(user_id, chat_id):
    file_path, chat_id = get_history_path(user_id, chat_id)

    if not os.path.exists(file_path):
        return [], 200

    with open(file_path, "r") as f:
        try:
            chat_history = json.load(f)
        except json.JSONDecodeError:
            chat_history = []

    return chat_history, 200



# Function to update chat history
def update_history(user_id, chat_id, user_query, response_message):
    file_path, chat_id = get_history_path(user_id, chat_id)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open(file_path, "r") as f:
        try:
            chat_history = json.load(f)
        except json.JSONDecodeError:
            chat_history = []

    new_chat = {"user": user_query, "bot": response_message}
    chat_history.append(new_chat)

    with open(file_path, "w") as f:
        json.dump(chat_history, f, indent=4)

    return chat_id



# Function to delete a specific chat
def delete_history(user_id, chat_id):
    file_path, chat_id = get_history_path(user_id, chat_id)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error deleting chat: {e}")
            return False
    print(f"Chat file {file_path} does not exist.")
    return False
