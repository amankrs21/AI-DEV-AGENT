import requests
import json

MISTRAL_API_URL = "http://localhost:11434/api/generate"

def call_mistral_api(prompt, stream=False):
    """
    Calls the locally hosted Mistral 7B API with a prompt.
    Supports streaming response dynamically.
    """
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"model": "mistral", "prompt": prompt, "stream": stream})

    response = requests.post(MISTRAL_API_URL, headers=headers, data=data, stream=stream)
    
    full_response = ""
    if stream:
        print("Generating response...\n")
        for line in response.iter_lines():
            if line:
                try:
                    parsed_line = json.loads(line.decode("utf-8"))
                    chunk = parsed_line.get("response", "")
                    print(chunk, end="", flush=True)  # Stream output dynamically
                    full_response += chunk
                except json.JSONDecodeError:
                    pass  # Handle any decoding errors gracefully
        print("\n")  # Newline after streaming
    else:
        full_response = response.json().get("response", "")

    print(full_response)
    return full_response


