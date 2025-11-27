import pytest
from fastapi.testclient import TestClient
from main import app, items_db, item_id_counter


@pytest.fixture(autouse=True)
def reset_database():
    """Reset the database before each test"""
    global items_db, item_id_counter
    items_db.clear()
    # Reset the counter by importing and modifying the module
    import main
    main.item_id_counter = 1
    yield
    items_db.clear()
    main.item_id_counter = 1


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def sample_item():
    """Sample item data for testing"""
    return {
        "name": "Test Laptop",
        "description": "A test laptop",
        "price": 999.99,
        "quantity": 5
    }


@pytest.fixture
def sample_item_minimal():
    """Minimal item data for testing"""
    return {
        "name": "Minimal Item",
        "price": 49.99
    }


class TestRootEndpoint:
    """Tests for the root endpoint"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data
        assert "Welcome" in data["message"]


class TestGetEndpoints:
    """Tests for GET endpoints"""
    
    def test_get_all_items_empty(self, client):
        """Test getting all items when database is empty"""
        response = client.get("/items")
        assert response.status_code == 200
        assert response.json() == {}
    
    def test_get_all_items_with_data(self, client, sample_item):
        """Test getting all items when database has data"""
        # Create an item first
        client.post("/items", json=sample_item)
        
        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert 1 in [int(k) for k in data.keys()]
    
    def test_get_item_by_id_success(self, client, sample_item):
        """Test getting a specific item by ID"""
        # Create an item first
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["id"]
        
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_item["name"]
        assert data["price"] == sample_item["price"]
    
    def test_get_item_by_id_not_found(self, client):
        """Test getting a non-existent item returns 404"""
        response = client.get("/items/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"


class TestPostEndpoint:
    """Tests for POST endpoint"""
    
    def test_create_item_success(self, client, sample_item):
        """Test creating an item successfully"""
        response = client.post("/items", json=sample_item)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["message"] == "Item created successfully"
        assert data["item"]["name"] == sample_item["name"]
        assert data["item"]["price"] == sample_item["price"]
    
    def test_create_item_minimal_fields(self, client, sample_item_minimal):
        """Test creating an item with minimal required fields"""
        response = client.post("/items", json=sample_item_minimal)
        assert response.status_code == 201
        data = response.json()
        assert data["item"]["name"] == sample_item_minimal["name"]
        assert data["item"]["price"] == sample_item_minimal["price"]
        assert data["item"]["quantity"] == 0  # Default value
        assert data["item"]["description"] is None  # Default value
    
    def test_create_multiple_items(self, client, sample_item):
        """Test creating multiple items increments IDs correctly"""
        response1 = client.post("/items", json=sample_item)
        response2 = client.post("/items", json=sample_item)
        
        assert response1.json()["id"] == 1
        assert response2.json()["id"] == 2
    
    def test_create_item_missing_required_field(self, client):
        """Test creating an item without required fields fails"""
        invalid_item = {"description": "Missing name and price"}
        response = client.post("/items", json=invalid_item)
        assert response.status_code == 422  # Validation error
    
    def test_create_item_invalid_price_type(self, client):
        """Test creating an item with invalid price type"""
        invalid_item = {
            "name": "Test",
            "price": "not_a_number"
        }
        response = client.post("/items", json=invalid_item)
        assert response.status_code == 422
    
    def test_create_item_negative_quantity(self, client):
        """Test creating an item with negative quantity"""
        item = {
            "name": "Test",
            "price": 10.0,
            "quantity": -5
        }
        response = client.post("/items", json=item)
        # This should succeed as we don't have validation for negative quantities
        assert response.status_code == 201


class TestPutEndpoint:
    """Tests for PUT endpoint"""
    
    def test_update_item_success(self, client, sample_item):
        """Test updating an item successfully"""
        # Create an item first
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["id"]
        
        # Update the item
        updated_item = {
            "name": "Updated Laptop",
            "description": "An updated laptop",
            "price": 1299.99,
            "quantity": 3
        }
        response = client.put(f"/items/{item_id}", json=updated_item)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Item updated successfully"
        assert data["item"]["name"] == updated_item["name"]
        assert data["item"]["price"] == updated_item["price"]
    
    def test_update_item_not_found(self, client, sample_item):
        """Test updating a non-existent item returns 404"""
        response = client.put("/items/999", json=sample_item)
        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"
    
    def test_update_item_missing_fields(self, client, sample_item):
        """Test updating an item with missing required fields fails"""
        # Create an item first
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["id"]
        
        # Try to update with missing fields
        invalid_update = {"name": "Only Name"}
        response = client.put(f"/items/{item_id}", json=invalid_update)
        assert response.status_code == 422


class TestPatchEndpoint:
    """Tests for PATCH endpoint"""
    
    def test_partial_update_item_success(self, client, sample_item):
        """Test partially updating an item successfully"""
        # Create an item first
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["id"]
        
        # Partially update the item (only price)
        partial_update = {"price": 899.99}
        response = client.patch(f"/items/{item_id}", json=partial_update)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Item partially updated successfully"
        assert data["item"]["price"] == 899.99
        # Other fields should remain unchanged
        assert data["item"]["name"] == sample_item["name"]
        assert data["item"]["quantity"] == sample_item["quantity"]
    
    def test_partial_update_multiple_fields(self, client, sample_item):
        """Test updating multiple fields partially"""
        # Create an item first
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["id"]
        
        # Update multiple fields
        partial_update = {
            "name": "New Name",
            "quantity": 10
        }
        response = client.patch(f"/items/{item_id}", json=partial_update)
        
        assert response.status_code == 200
        data = response.json()
        assert data["item"]["name"] == "New Name"
        assert data["item"]["quantity"] == 10
        # Price should remain unchanged
        assert data["item"]["price"] == sample_item["price"]
    
    def test_partial_update_item_not_found(self, client):
        """Test partially updating a non-existent item returns 404"""
        response = client.patch("/items/999", json={"price": 100.0})
        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"
    
    def test_partial_update_empty_body(self, client, sample_item):
        """Test partial update with empty body"""
        # Create an item first
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["id"]
        
        # Update with empty body
        response = client.patch(f"/items/{item_id}", json={})
        
        assert response.status_code == 200
        # Item should remain unchanged
        data = response.json()
        assert data["item"]["name"] == sample_item["name"]


class TestDeleteEndpoint:
    """Tests for DELETE endpoint"""
    
    def test_delete_item_success(self, client, sample_item):
        """Test deleting an item successfully"""
        # Create an item first
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["id"]
        
        # Delete the item
        response = client.delete(f"/items/{item_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Item deleted successfully"
        assert data["deleted_item"]["name"] == sample_item["name"]
        
        # Verify item is actually deleted
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 404
    
    def test_delete_item_not_found(self, client):
        """Test deleting a non-existent item returns 404"""
        response = client.delete("/items/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"
    
    def test_delete_item_twice(self, client, sample_item):
        """Test deleting the same item twice fails on second attempt"""
        # Create an item
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["id"]
        
        # Delete once - should succeed
        response1 = client.delete(f"/items/{item_id}")
        assert response1.status_code == 200
        
        # Delete again - should fail
        response2 = client.delete(f"/items/{item_id}")
        assert response2.status_code == 404


class TestIntegrationScenarios:
    """Integration tests for complete workflows"""
    
    def test_complete_crud_workflow(self, client, sample_item):
        """Test complete CRUD workflow"""
        # Create
        create_response = client.post("/items", json=sample_item)
        assert create_response.status_code == 201
        item_id = create_response.json()["id"]
        
        # Read
        read_response = client.get(f"/items/{item_id}")
        assert read_response.status_code == 200
        assert read_response.json()["name"] == sample_item["name"]
        
        # Update
        updated_item = {
            "name": "Updated Item",
            "description": "Updated description",
            "price": 1500.0,
            "quantity": 10
        }
        update_response = client.put(f"/items/{item_id}", json=updated_item)
        assert update_response.status_code == 200
        assert update_response.json()["item"]["name"] == "Updated Item"
        
        # Delete
        delete_response = client.delete(f"/items/{item_id}")
        assert delete_response.status_code == 200
        
        # Verify deletion
        final_response = client.get(f"/items/{item_id}")
        assert final_response.status_code == 404
    
    def test_multiple_items_management(self, client):
        """Test managing multiple items"""
        items = [
            {"name": "Item 1", "price": 10.0, "quantity": 5},
            {"name": "Item 2", "price": 20.0, "quantity": 3},
            {"name": "Item 3", "price": 30.0, "quantity": 7}
        ]
        
        # Create multiple items
        item_ids = []
        for item in items:
            response = client.post("/items", json=item)
            assert response.status_code == 201
            item_ids.append(response.json()["id"])
        
        # Get all items
        all_items_response = client.get("/items")
        assert len(all_items_response.json()) == 3
        
        # Delete one item
        client.delete(f"/items/{item_ids[1]}")
        
        # Verify count
        remaining_items = client.get("/items")
        assert len(remaining_items.json()) == 2
    
    def test_update_after_partial_update(self, client, sample_item):
        """Test full update after partial update"""
        # Create item
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["id"]
        
        # Partial update
        client.patch(f"/items/{item_id}", json={"price": 500.0})
        
        # Full update
        full_update = {
            "name": "Completely New",
            "description": "New description",
            "price": 2000.0,
            "quantity": 1
        }
        response = client.put(f"/items/{item_id}", json=full_update)
        
        assert response.status_code == 200
        assert response.json()["item"]["name"] == "Completely New"
        assert response.json()["item"]["price"] == 2000.0


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""
    
    def test_item_with_zero_price(self, client):
        """Test creating item with zero price"""
        item = {"name": "Free Item", "price": 0.0}
        response = client.post("/items", json=item)
        assert response.status_code == 201
    
    def test_item_with_very_large_price(self, client):
        """Test creating item with very large price"""
        item = {"name": "Expensive Item", "price": 999999999.99}
        response = client.post("/items", json=item)
        assert response.status_code == 201
    
    def test_item_with_long_name(self, client):
        """Test creating item with very long name"""
        long_name = "A" * 1000
        item = {"name": long_name, "price": 10.0}
        response = client.post("/items", json=item)
        assert response.status_code == 201
        assert response.json()["item"]["name"] == long_name
    
    def test_item_with_special_characters(self, client):
        """Test creating item with special characters in name"""
        item = {
            "name": "Item with special chars: !@#$%^&*()",
            "description": "Description with émojis 🚀 and ñ",
            "price": 99.99
        }
        response = client.post("/items", json=item)
        assert response.status_code == 201
    
    def test_concurrent_item_creation(self, client):
        """Test that item IDs are unique for concurrent creation"""
        items = [
            {"name": f"Item {i}", "price": float(i * 10)}
            for i in range(10)
        ]
        
        ids = []
        for item in items:
            response = client.post("/items", json=item)
            ids.append(response.json()["id"])
        
        # All IDs should be unique
        assert len(ids) == len(set(ids))
        # IDs should be sequential
        assert ids == list(range(1, 11))

