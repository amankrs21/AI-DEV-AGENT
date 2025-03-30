import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI


# Load secrets
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY") 
if not api_key:
    raise ValueError("Mistral API key not found.")


# Initialize Mistral model
mistral = ChatMistralAI(
    temperature=0.6,
    max_retries=2,
    api_key=api_key,
    model="mistral-large-latest",
)
