from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import uvicorn

app = FastAPI(title="REST API Server", version="1.0.0")

# In-memory storage for demonstration
items_db: Dict[int, dict] = {}
item_id_counter = 1


# Pydantic models for request/response validation
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


# GET - Retrieve all items
@app.get("/items", response_model=Dict[int, dict])
async def get_all_items():
    """Get all items from the database"""
    return items_db


# GET - Retrieve a specific item by ID
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """Get a specific item by ID"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


# POST - Create a new item
@app.post("/items", status_code=201)
async def create_item(item: Item):
    """Create a new item"""
    global item_id_counter
    
    item_data = item.model_dump()
    items_db[item_id_counter] = item_data
    
    response = {
        "id": item_id_counter,
        "message": "Item created successfully",
        "item": item_data
    }
    
    item_id_counter += 1
    return response


# PUT - Update an existing item (full update)
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """Update an existing item completely"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    items_db[item_id] = item.model_dump()
    
    return {
        "id": item_id,
        "message": "Item updated successfully",
        "item": items_db[item_id]
    }


# PATCH - Partially update an item (optional)
@app.patch("/items/{item_id}")
async def partial_update_item(item_id: int, item: ItemUpdate):
    """Partially update an existing item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    stored_item = items_db[item_id]
    update_data = item.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        stored_item[field] = value
    
    return {
        "id": item_id,
        "message": "Item partially updated successfully",
        "item": stored_item
    }


# DELETE - Remove an item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item by ID"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted_item = items_db.pop(item_id)
    
    return {
        "message": "Item deleted successfully",
        "deleted_item": deleted_item
    }


# Root endpoint
@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to the FastAPI REST Server",
        "endpoints": {
            "GET /items": "Get all items",
            "GET /items/{id}": "Get item by ID",
            "POST /items": "Create new item",
            "PUT /items/{id}": "Update item completely",
            "PATCH /items/{id}": "Update item partially",
            "DELETE /items/{id}": "Delete item"
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

