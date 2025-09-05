from openai import OpenAI
import os

def get_openai_client():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    return openai

def generate_embedding(text):
    client = get_openai_client()
    response = client.Embedding.create(
        model="text-embedding-3-small",
        input=text
    )
    return response['data'][0]['embedding']