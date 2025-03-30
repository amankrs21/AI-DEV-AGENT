import os
import uuid
import pickle
from langchain_core.chat_history import InMemoryChatMessageHistory


# Function to get the path for chat memory
def get_memory_path(user_id, chat_id=None):
    base_dir = f"data/{user_id}/memory"
    os.makedirs(base_dir, exist_ok=True)
    
    if chat_id is None:
        # Generate a unique chat_id if none provided
        chat_id = str(uuid.uuid4())
        return f"{base_dir}/{chat_id}.pkl", chat_id
    return f"{base_dir}/{chat_id}.pkl", chat_id


# Function to save chat memory
def save_memory(memory, file_path):
    """Save memory to a file."""
    with open(file_path, "wb") as file:
        pickle.dump(memory, file)


# Function to load chat memory
def load_memory(user_id, chat_id):
    """Load memory from a file for a specific user and chat_id."""
    file_path, chat_id = get_memory_path(user_id, chat_id)
    try:
        with open(file_path, "rb") as file:
            loaded_memory = pickle.load(file)
        return loaded_memory, chat_id
    except FileNotFoundError:
        # If file doesn't exist, create a new memory
        memory = InMemoryChatMessageHistory()
        save_memory(memory, file_path)
        return memory, chat_id
    
    
# Function to delete chat memory
def delete_memory(user_id, chat_id):
    file_path, chat_id = get_memory_path(user_id, chat_id)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error deleting memory: {e}")
            return False
    print(f"Memory file {file_path} does not exist.")
    return False
