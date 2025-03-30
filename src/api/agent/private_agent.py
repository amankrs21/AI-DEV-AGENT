import time
from langchain_core.messages import SystemMessage, HumanMessage

# local imports
from src.api.agent.agent_setup import mistral
from src.api.agent.agent_role import agent_role_message
from src.api.services.chat_memory import get_memory_path, save_memory

# In-memory storage for session data
session_data = {}

# Clean up old sessions after 6 hours
def clean_sessions():
    current_time = time.time()
    expired_sessions = [
        session_id for session_id, data in session_data.items()
        if current_time - data["start_time"] > 6 * 60 * 60  # 6 hours in seconds
    ]
    for session_id in expired_sessions:
        del session_data[session_id]
        print(f"Session {session_id} expired and cleared.")

# Chat with Mistral AI in streaming mode [Authenticated User]
def private_agent_chat(user_query, memory, user_id, chat_id):
    if not user_query:
        return "Oops, you didn’t type anything! Give me something to work with."

    # Clean expired sessions
    clean_sessions()

    # Get the memory file path
    file_path, chat_id = get_memory_path(user_id, chat_id)

    # Check if session already exists
    session_id = f"{user_id}_{chat_id}"
    if session_id not in session_data:
        session_data[session_id] = {
            "messages": [],  # Stores chat history
            "start_time": time.time(),
        }

    # Load previous messages from memory if available
    if not memory.messages:
        memory.add_message(SystemMessage(content=agent_role_message))

    # Prepare messages to send to the model
    messages = [
        SystemMessage(content=agent_role_message)
    ] + session_data[session_id]["messages"] + [
        HumanMessage(content=user_query)
    ]

    # Add the query to memory
    memory.add_message(HumanMessage(content=user_query))

    # Stream the response
    def generate_stream():
        full_response = ""
        try:
            for chunk in mistral.stream(messages):
                content = chunk.content
                full_response += content
                yield content
        except Exception as e:
            yield "Something went wrong while processing your request."

        # Add current query and AI response to session memory
        session_data[session_id]["messages"].extend([
            HumanMessage(content=user_query),
            HumanMessage(content=full_response)
        ])

        # Save memory to the file path
        save_memory(memory, file_path)

    return generate_stream()
