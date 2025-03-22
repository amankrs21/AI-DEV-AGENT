import os
import json


SECRET_PATH = "src/secrets.json"


# Load secrets.json
def load_secrets():
    if not os.path.exists(SECRET_PATH):
        with open(SECRET_PATH, "w") as file:
            json.dump(
                {
                    "MISTRAL_API_KEY": "YOUR_API_KEY"
                },
                file,
                indent=4,
            )

    with open(SECRET_PATH, "r") as file:
        secrets = json.load(file)

    return secrets
