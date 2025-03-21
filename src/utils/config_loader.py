import os
import json


# Load secrets.json
def load_secrets(file_path="src/secrets.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found!")

    with open(file_path, "r") as file:
        secrets = json.load(file)

    return secrets
