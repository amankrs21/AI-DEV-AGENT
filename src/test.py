import requests
import json

def call_mistral_api(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"model": "mistral", "prompt": prompt, "stream": True})

    response = requests.post(url, headers=headers, data=data, stream=True)

    print("Final Response:\n", end="", flush=True)

    for line in response.iter_lines():
        if line:
            try:
                parsed_line = json.loads(line.decode("utf-8"))
                chunk = parsed_line.get("response", "")
                print(chunk, end="", flush=True)  # Print in a streaming manner
            except json.JSONDecodeError:
                pass  # Handle any decoding errors gracefully

    print()  # Ensure the final output ends with a new line

if __name__ == "__main__":
    user_prompt = "Write a simple JAVA code to add two numbers and then compare with parent numbers."
    call_mistral_api(user_prompt)
