import os
import json
from supabase import create_client, Client

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize Supabase client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Sample data to seed
product_kb_data = [
    {"product_id": 1001, "embedding": [0.1, 0.2, 0.3], "text": "Product 1 description."},
    {"product_id": 1002, "embedding": [0.4, 0.5, 0.6], "text": "Product 2 description."},
]

user_kb_data = [
    {"user_id": 42, "embedding": [0.7, 0.8, 0.9], "text": "User 42 preferences."},
    {"user_id": 43, "embedding": [0.1, 0.1, 0.1], "text": "User 43 preferences."},
]

qa_history_data = [
    {"product_id": 1001, "query_text": "How do I reset my password?", "query_embedding": [0.2, 0.3, 0.4], "solution_text": "Visit settings → security → reset password.", "created_at": "2023-01-01T00:00:00Z"},
]

def seed_data():
    # Insert product_kb data
    for product in product_kb_data:
        supabase.table("product_kb").insert(product).execute()

    # Insert user_kb data
    for user in user_kb_data:
        supabase.table("user_kb").insert(user).execute()

    # Insert qa_history data
    for qa in qa_history_data:
        supabase.table("qa_history").insert(qa).execute()

if __name__ == "__main__":
    seed_data()