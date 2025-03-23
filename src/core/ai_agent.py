import os
import json
import time
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage

# Import memory functions from utils
from .memory import load_memory, save_memory


# Load secrets
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY") 
print(f"API Key: {api_key}")
if not api_key:
    raise ValueError("Mistral API key not found.")


# Load existing memory or create a new one
memory = load_memory()


# Initialize Mistral model
llm = ChatMistralAI(
    temperature=0.3,  # Lowered slightly for less wild creativity, more focus
    max_retries=2,
    api_key=api_key,
    model="mistral-large-latest",
)


# System message with moderated humor and simpler language
agent_role_message = """
Hello, coder! I’m your AI Developer Agent Anya, here to help with your code and add a little fun along the way. I’m great at understanding, fixing, and improving code you send me.

What I Can Do:
- Figure out how your code works, step by step.
- Find hidden issues or suggest better ways to write it.
- Help you add new features or make your code sharper.
- Point out security or speed problems with clear advice.

My Rules:
- If you ask about non-coding stuff (like philosophy or novels), I’ll say: "Hey, I’m here for code, not big life questions! Let’s focus on your project."
- For simple greetings like "Hi" or "Hey," I’ll keep it short and friendly.
- For code questions, I’ll stick to what you’re working on unless you tell me otherwise.
- I’ll keep things light and fun, but always focused on your code and sometimes I can use emojis.

Extra Skills:
- I read code fast and suggest smart fixes.
- I add good coding habits to keep things clean and safe.
- I explain things simply so you get it right away.

Let’s team up and make your code better—fun but focused! What do you want to work on?
"""
# Add system message if memory is empty
if not memory.messages:
    memory.add_message(SystemMessage(content=agent_role_message))



# Send code in chunks to the model
def send_code_in_chunks(code_snapshot):
    json_data = json.dumps(code_snapshot, indent=2)
    total_length = len(json_data)
    
    CHUNK_THRESHOLD = 25000  # Threshold set to 20,000 characters

    if total_length <= CHUNK_THRESHOLD:
        print(f"Code size: {total_length} characters. Sending it all at once!")
        prompt = f"""
        Here’s a code snapshot for you to remember:
        ---
        {json_data}
        ---
        Ready for your questions!
        """
        memory.add_message(HumanMessage(content=prompt))
        llm.invoke(memory.messages)
    else:
        chunks = [json_data[i:i + CHUNK_THRESHOLD] for i in range(0, total_length, CHUNK_THRESHOLD)]
        print(f"Code size: {total_length} characters. Splitting into {len(chunks)} parts!")

        for i, chunk in enumerate(chunks):
            print(f"Sending part {i + 1} of {len(chunks)} ({len(chunk)} characters)...")
            prompt = f"""
            Here’s code snapshot part {i + 1} of {len(chunks)} ({len(chunk)} characters):
            ---
            {chunk}
            ---
            {'More parts coming!' if i < len(chunks) - 1 else 'All done—ask away!'}
            """
            memory.add_message(HumanMessage(content=prompt))
            llm.invoke(memory.messages)
            if i < len(chunks) - 1:  # Delay between chunks
                time.sleep(2)

        print("All code parts sent successfully!")

        acknowledgment_prompt = """
        I’ve got all your code parts loaded up. Ready to help—what’s your next step?
        """
        memory.add_message(HumanMessage(content=acknowledgment_prompt))
        llm.invoke(memory.messages)

    # Save memory after processing code chunks
    save_memory(memory)



# Remove a file from uploaded files
def remove_file_from_memory(file_name):
    removal_prompt = f"""
    The file '{file_name}' has been removed. Do not consider this file in any responses unless it’s uploaded again.
    """
    memory.add_message(HumanMessage(content=removal_prompt))
    save_memory(memory)
    llm.invoke(memory.messages)



# Chat with Mistral AI in streaming mode
def chat_with_mistral(user_query):
    if not user_query:
        return "Oops, you didn’t type anything! Give me something to work with."

    # Check if the query is a casual greeting
    casual_greetings = {"hi", "hello", "how are you", "hey"}
    is_casual = user_query.lower().strip() in casual_greetings

    # Prepare the messages to send to the model
    if is_casual:
        messages = [
            SystemMessage(content=agent_role_message),
            HumanMessage(content=user_query)
        ]
    else:
        code_messages = [msg for msg in memory.messages if "Here’s a code snapshot" in msg.content]
        if code_messages:
            messages = (
                [SystemMessage(content=agent_role_message)] +
                code_messages +
                [HumanMessage(content=f"Here’s your question: {user_query}")]
            )
        else:
            messages = [
                SystemMessage(content=agent_role_message),
                HumanMessage(content=f"No code loaded yet, but I’ll help with this: {user_query}")
            ]

    # Add the query to memory
    memory.add_message(HumanMessage(content=user_query))

    # Stream the response
    def generate_stream():
        full_response = ""
        for chunk in llm.stream(messages):
            content = chunk.content
            full_response += content
            yield content

        # Save the full response to memory after streaming
        memory.add_message(HumanMessage(content=full_response))
        save_memory(memory)

    return generate_stream()
