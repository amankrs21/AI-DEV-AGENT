import os
import json
import shutil


CHAT_HISTORY_FILE = "data/chat/history.json"
os.makedirs(os.path.dirname(CHAT_HISTORY_FILE), exist_ok=True)


# funtion to update chat history
def update_chat_history(user_query, response_message):
    os.makedirs(os.path.dirname(CHAT_HISTORY_FILE), exist_ok=True)
    if not os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump([], f)

    with open(CHAT_HISTORY_FILE, "r") as f:
        try:
            chat_history = json.load(f)
        except json.JSONDecodeError:
            chat_history = []

    new_chat = {"user": user_query, "bot": response_message}
    chat_history.append(new_chat)

    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(chat_history, f, indent=4)


# function to get chat history
def get_chat_history():
    if not os.path.exists(CHAT_HISTORY_FILE):
        return [], 200

    with open(CHAT_HISTORY_FILE, "r") as f:
        try:
            chat_history = json.load(f)
        except json.JSONDecodeError:
            chat_history = []

    return chat_history, 200


# function to delete chat history
def delete_chat_history():
    data_directory = "data"
    try:
        if not os.path.exists(data_directory):
            return {"error": "No 'data' folder found to clear!"}, 404

        for item in os.listdir(data_directory):
            item_path = os.path.join(data_directory, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                
        return {}, 204
    
    except Exception as e:
        return {"error": f"Failed to clear 'data' folder contents: {str(e)}"}, 500
    