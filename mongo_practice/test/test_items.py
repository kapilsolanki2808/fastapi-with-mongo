# from .main import app
# from fastapi.testclient import TestClient
# # import json
# client = TestClient(app)

# def test_item_get():
#     response = client.get("/items/get/items/")
#     assert response.status_code == 200
#     assert response.json == {
#                             "_id": 1,
#                             "name": "laptop",
#                             "description": "string",
#                             "price": 0
#                             }


from .main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_item_get():
    response = client.get("/items/get/items/")
    assert response.status_code == 200
    # breakpoint()
    
    # Get the response data (which is a list of items)
    items = response.json()
    # Make sure we got a list
    assert isinstance(items, list)
    
    # Check that the first item has the expected structure
    assert len(items) > 0  # Ensure the list isn't empty
    
    # Example assertion for the first item in the list
    first_item = items[0]
    assert "name" in first_item
    assert "description" in first_item
    assert "price" in first_item
    # assert "_id" in first_item  # Ensure _id exists
    # assert isinstance(first_item["_id"], str)  # Ensure _id is a string

    # Optionally, you can assert a specific item in the list if needed
    # laptop_item = next((item for item in items if item["name"] == "laptop"), None)
    # assert laptop_item is not None
    # assert laptop_item["name"] == "laptop"
    # assert laptop_item["description"] == "string"
    # assert laptop_item["price"] == 0
