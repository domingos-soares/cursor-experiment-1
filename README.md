# FastAPI REST Server

A simple REST API server built with FastAPI that demonstrates all standard HTTP methods (GET, POST, PUT, PATCH, DELETE).

## Features

- **GET** - Retrieve all items or a specific item by ID
- **POST** - Create new items
- **PUT** - Update an entire item
- **PATCH** - Partially update an item
- **DELETE** - Remove an item

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the server with:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Get all items
```bash
curl http://localhost:8000/items
```

### Get a specific item
```bash
curl http://localhost:8000/items/1
```

### Create a new item
```bash
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "A powerful laptop",
    "price": 999.99,
    "quantity": 5
  }'
```

### Update an item (full update)
```bash
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Laptop",
    "description": "An even better laptop",
    "price": 1299.99,
    "quantity": 3
  }'
```

### Partially update an item
```bash
curl -X PATCH http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 899.99
  }'
```

### Delete an item
```bash
curl -X DELETE http://localhost:8000/items/1
```

## Data Model

Items have the following structure:
- `name` (string, required): Item name
- `description` (string, optional): Item description
- `price` (float, required): Item price
- `quantity` (integer, optional, default: 0): Item quantity

## Testing

This project includes a comprehensive test suite with **98% code coverage**.

### Run tests:
```bash
# Activate virtual environment first
source venv/bin/activate

# Run all tests
pytest

# Run with coverage report
pytest --cov=main --cov-report=term-missing

# Run with HTML coverage report
pytest --cov=main --cov-report=html
# Then open htmlcov/index.html in your browser
```

### Test Coverage:
- ✅ 29 comprehensive tests
- ✅ 98% code coverage
- ✅ All HTTP methods tested
- ✅ Success and error scenarios
- ✅ Edge cases and validation
- ✅ Integration workflows

See [TEST_README.md](TEST_README.md) for detailed testing documentation.

## Notes

- This implementation uses in-memory storage, so data will be lost when the server restarts
- For production use, consider integrating a database (PostgreSQL, MongoDB, etc.)
- The server includes automatic data validation using Pydantic models
- Comprehensive test suite ensures reliability and maintainability
cursos experiment
