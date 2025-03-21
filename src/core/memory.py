import os
import pickle
from langchain_core.chat_history import InMemoryChatMessageHistory


MEMORY_FILE = "data/memory/chat_memory.pkl"
os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)


# Save memory to a file
def save_memory(memory):
    with open(MEMORY_FILE, "wb") as file:
        pickle.dump(memory, file)
    print("✅ Memory saved successfully!")


# Load memory from a file
def load_memory():
    try:
        with open(MEMORY_FILE, "rb") as file:
            loaded_memory = pickle.load(file)
        print("✅ Memory loaded successfully!")
        return loaded_memory
    except FileNotFoundError:
        print("⚠️ No previous memory found, starting fresh...")
        memory = InMemoryChatMessageHistory()
        return memory
