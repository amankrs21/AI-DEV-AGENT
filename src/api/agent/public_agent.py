import time
from langchain_core.messages import HumanMessage, SystemMessage

from src.api.agent.agent_setup import mistral
from src.api.agent.agent_role import agent_role_message


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


# Public agent to limit response & manage session
def public_agent_chat(user_query, session_id):
    if not user_query:
        return "Oops, you didn’t type anything! Give me something to work with."

    # Clean expired sessions
    clean_sessions()

    # Check if session already exists
    if session_id not in session_data:
        session_data[session_id] = {
            "messages": [],  # Stores last 5 messages
            "count": 0,
            "start_time": time.time(),
        }

    # Session limit check
    if session_data[session_id]["count"] >= 5:
        return "You’ve hit the limit of 5 messages for this session. Please wait 6 hours before chatting again."

    # Prepare messages to send
    messages = [
        SystemMessage(content=agent_role_message)
    ] + session_data[session_id]["messages"] + [
        HumanMessage(content=user_query)
    ]

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

        # Add current query and AI response to memory
        session_data[session_id]["messages"].extend([
            HumanMessage(content=user_query),
            HumanMessage(content=full_response)
        ])

        # Keep only the last 5 messages
        if len(session_data[session_id]["messages"]) > 5:
            session_data[session_id]["messages"] = session_data[session_id]["messages"][-5:]

        # Increase message count
        session_data[session_id]["count"] += 1

        # Auto clear memory after 6 hours or limit hit
        if session_data[session_id]["count"] >= 5:
            session_data[session_id]["start_time"] = time.time()

    return generate_stream()
