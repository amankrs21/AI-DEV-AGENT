# from .agent_setup import call_mistral_api
# from .agent_setup_online import call_mistral_api
from .agent_setup_deepseek import call_deepseek
import json
import time

def send_code_in_chunks(code_snapshot, chunk_size=3000):
    """
    Sends the code snapshot in multiple chunks to Mistral 7B.
    """
    json_data = json.dumps(code_snapshot, indent=2)
    
    # Split into chunks
    chunks = [json_data[i:i+chunk_size] for i in range(0, len(json_data), chunk_size)]

    print(f"Sending {len(chunks)} chunks to the model...")

    for i, chunk in enumerate(chunks):
        print(f"Sending chunk {i+1}/{len(chunks)}...")
        
        prompt = f"""
        Memorize this code snapshot chunk {i+1}/{len(chunks)}.
        ---
        {chunk}
        ---
        You will receive more chunks before I ask my actual question.
        Just store this information and do NOT generate any response yet.
        """
        call_deepseek(prompt, stream=False)
        # time.sleep(2)  # Add a small delay between chunks

    print("All chunks sent successfully!")

def request_file_selection(feature_request):
    """
    Once all chunks are sent, this function asks Mistral to identify relevant files.
    """
    prompt = f"""
    Do you remeber the code snapshot chunks that I had sent earlier?
    Can you summarize the code that I had sent earlier?
    """
    # prompt = f"""
    # You have received multiple code snapshot chunks earlier.
    # Now, based on the complete project structure and code:
    
    # ---
    # Feature Request:
    # {feature_request}
    # ---
    
    # Identify the files that should be updated to implement this feature.
    
    # Return a JSON response with:
    # {{"files_to_update": ["file1.py", "folder/file2.js", ...]}}
    # """

    response = call_deepseek(prompt, stream=False)

    try:
        print(response)
        ai_response = json.loads(response)
        return ai_response.get("files_to_update", [])
    except json.JSONDecodeError:
        print("Error: Failed to parse AI response.")
        return []
