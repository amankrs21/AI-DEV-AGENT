import json
import time
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage

# Import memory functions from utils
from src.utils.config_loader import load_secrets
from .memory import load_memory, save_memory


# Load secrets
secrets = load_secrets()
api_key = secrets.get("mistral_api_key")
if not api_key:
    raise ValueError("Mistral API key not found in secrets.json! Please check your secrets file.")


# Load existing memory or create a new one
memory = load_memory()
import json
import time
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage

# Import memory functions from utils
from src.utils.config_loader import load_secrets
from .memory import load_memory, save_memory


# Load secrets
secrets = load_secrets()
api_key = secrets.get("mistral_api_key")
if not api_key:
    raise ValueError("❌ Mistral API key not found in secrets.json! Time to panic... just kidding, check your secrets file! 😜")


# ✅ Load existing memory or create a new one
memory = load_memory()


# Initialize Mistral model
llm = ChatMistralAI(
    temperature=0.4,  # Slightly higher for more creative, fun responses
    max_retries=2,
    api_key=api_key,
    model="mistral-large-latest",
)


# ✅ System message to define agent role with humor
agent_role_message = """
Greetings, human coder! I’m your AI Developer Agent, here to sprinkle some magic (and a dash of humor) on your code! 🎉 I specialize in analyzing, understanding, and jazzing up code snippets you throw my way.

✅ My Superpowers Include:
- Decoding your code structure like a detective with a magnifying glass 🕵️‍♂️.
- Spotting sneaky dependencies and suggesting upgrades (because who doesn’t love a glow-up?).
- Adding pizzazz to your features or building new ones—think of me as your code’s personal stylist! 💅
- Dropping truth bombs on security, optimization, and performance (no pressure, but I’ve got your back!).

🚫 The Fine Print (aka Rules I Can’t Break):
- If you ask me to write a novel, solve world hunger, or chat about the meaning of life, I’ll politely say: "Whoa there, I’m a coding ninja, not a philosopher! Let’s get back to some sweet, sweet code. 😎"
- For casual chit-chat like "Hi" or "How’s it going?", I’ll keep it fun and light—no boring robot vibes here!
- For coding tasks, I’ll focus on your current mission unless you say, “Hey, mix it up with that other thing I asked!”

🔍 Extra Cool Tricks:
- I can read code faster than you can say “bug-free” and tweak it like a pro.
- I’ll sprinkle best practices like confetti to keep your code sparkling ✨.
- Security holes? I’ll sniff ‘em out and patch ‘em up with a wink and a grin.

So, buckle up and let’s make coding an adventure—serious when it counts, hilarious when it doesn’t! What’s on your mind, code warrior? 🚀
"""
# Add system message if memory is empty
if not memory.messages:
    memory.add_message(SystemMessage(content=agent_role_message))


# ✅ Send code in chunks to the model
def send_code_in_chunks(code_snapshot):
    json_data = json.dumps(code_snapshot, indent=2)
    total_length = len(json_data)
    
    CHUNK_THRESHOLD = 20000  # Threshold set to 10,000 characters

    if total_length <= CHUNK_THRESHOLD:
        # Send as one piece
        print(f"🍪 Code snack detected ({total_length} chars)! Sending it in one glorious gulp!")
        prompt = f"""
        Memorize this code snapshot—it’s a perfect bite! 😋
        ---
        {json_data}
        ---
        Ready for your questions, code chef!
        """
        memory.add_message(HumanMessage(content=prompt))
        llm.invoke(memory.messages)
    else:
        # Split into chunks of up to 10,000 chars each
        chunks = [json_data[i:i + CHUNK_THRESHOLD] for i in range(0, total_length, CHUNK_THRESHOLD)]
        print(f"🍽️ Code feast detected ({total_length} chars)! Splitting into {len(chunks)} delicious bites!")

        for i, chunk in enumerate(chunks):
            print(f"Sending chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)... get ready! 🎢")
            prompt = f"""
            Memorize this code snapshot chunk {i+1}/{len(chunks)}. It’s a {'' if len(chunk) == CHUNK_THRESHOLD else 'tasty '}nibble of {len(chunk)} chars! 😋
            ---
            {chunk}
            ---
            {'More chunks coming—stay tuned!' if i < len(chunks) - 1 else 'That’s the last bite—ready for action!'}
            """
            memory.add_message(HumanMessage(content=prompt))
            llm.invoke(memory.messages)
            if i < len(chunks) - 1:  # Only delay between chunks
                time.sleep(2)

        print("✅ All chunks sent successfully! Code buffet devoured! 🧠")

        # Acknowledge memory after all chunks
        acknowledgment_prompt = """
        Whoa, I’ve chowed down on all your code chunks like a pro! 🍪 Now I’m stuffed and ready—hit me with your queries!
        """
        memory.add_message(HumanMessage(content=acknowledgment_prompt))
        llm.invoke(memory.messages)

    # ✅ Save memory after processing code chunks
    save_memory(memory)
     


# ✅ Chat with Mistral AI in streaming mode
def chat_with_mistral(user_query):
    if not user_query:
        return "⚠️ Whoops, you forgot to say something! Did your keyboard take a coffee break? ☕"

    # Check if the query seems to be a casual greeting
    casual_greetings = {"hi", "hello", "how are you", "hey"}
    is_casual = user_query.lower().strip() in casual_greetings

    # Prepare the messages to send to the model
    if is_casual:
        messages = [
            SystemMessage(content=agent_role_message),
            HumanMessage(content=user_query)
        ]
    else:
        code_messages = [msg for msg in memory.messages if "Memorize this code snapshot" in msg.content]
        if code_messages:
            messages = (
                [SystemMessage(content=agent_role_message)] +
                code_messages +
                [HumanMessage(content=f"Alright, code maestro, here’s your next challenge: {user_query} 🎤")]
            )
        else:
            messages = [
                SystemMessage(content=agent_role_message),
                HumanMessage(content=f"No code yet? No problem! Let’s tackle this anyway: {user_query} 🚀")
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
