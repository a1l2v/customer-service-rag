import pytest
from app.services.search import perform_similarity_search

def test_perform_similarity_search():
    # Sample data for testing
    sample_embedding = [0.1, 0.2, 0.3]
    product_id = 1001

    # Call the function to test
    results = perform_similarity_search(sample_embedding, product_id)

    # Check that results are returned
    assert results is not None
    assert isinstance(results, list)

    # Further assertions can be added based on expected results
    # For example, checking the length of results or specific content
    assert len(results) > 0  # Assuming we expect at least one result

def test_perform_similarity_search_no_results():
    # Test with an embedding that should return no results
    sample_embedding = [0.0, 0.0, 0.0]
    product_id = 9999  # Assuming this product_id does not exist

    # Call the function to test
    results = perform_similarity_search(sample_embedding, product_id)

    # Check that no results are returned
    assert results == []  # Expecting an empty list for no results