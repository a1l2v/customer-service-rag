from supabase import create_client, Client
from typing import List, Dict, Any
import os

# Initialize Supabase client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def search_product_kb(embedding: List[float], product_id: int, threshold: float = 0.7) -> List[Dict[str, Any]]:
    """
    Perform a similarity search in the product_kb table using the provided embedding.

    Args:
        embedding (List[float]): The embedding vector to search for.
        product_id (int): The ID of the product to filter the search.
        threshold (float): The similarity threshold for filtering results.

    Returns:
        List[Dict[str, Any]]: A list of matching records from product_kb.
    """
    response = supabase.rpc("search_product_kb", {"embedding": embedding, "product_id": product_id, "threshold": threshold}).execute()
    return response.data

def search_user_kb(embedding: List[float], user_id: int, threshold: float = 0.7) -> List[Dict[str, Any]]:
    """
    Perform a similarity search in the user_kb table using the provided embedding.

    Args:
        embedding (List[float]): The embedding vector to search for.
        user_id (int): The ID of the user to filter the search.
        threshold (float): The similarity threshold for filtering results.

    Returns:
        List[Dict[str, Any]]: A list of matching records from user_kb.
    """
    response = supabase.rpc("search_user_kb", {"embedding": embedding, "user_id": user_id, "threshold": threshold}).execute()
    return response.data

def search_qa_history(query_embedding: List[float], product_id: int, threshold: float = 0.7) -> List[Dict[str, Any]]:
    """
    Perform a similarity search in the qa_history table using the provided query embedding.

    Args:
        query_embedding (List[float]): The embedding vector of the query.
        product_id (int): The ID of the product to filter the search.
        threshold (float): The similarity threshold for filtering results.

    Returns:
        List[Dict[str, Any]]: A list of matching records from qa_history.
    """
    response = supabase.rpc("search_qa_history", {"query_embedding": query_embedding, "product_id": product_id, "threshold": threshold}).execute()
    return response.data