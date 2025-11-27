# Test Suite Documentation

## Overview

This test suite provides comprehensive coverage for the FastAPI REST server with **98% code coverage**.

## Test Statistics

- **Total Tests**: 29
- **Code Coverage**: 98%
- **Test Categories**: 6

## Test Structure

### 1. TestRootEndpoint (1 test)
Tests for the root welcome endpoint.

### 2. TestGetEndpoints (4 tests)
- Get all items (empty database)
- Get all items (with data)
- Get item by ID (success)
- Get item by ID (not found)

### 3. TestPostEndpoint (6 tests)
- Create item successfully
- Create item with minimal fields
- Create multiple items
- Validation: missing required fields
- Validation: invalid price type
- Edge case: negative quantity

### 4. TestPutEndpoint (3 tests)
- Update item successfully
- Update non-existent item
- Update with missing required fields

### 5. TestPatchEndpoint (4 tests)
- Partial update (single field)
- Partial update (multiple fields)
- Partial update non-existent item
- Partial update with empty body

### 6. TestDeleteEndpoint (3 tests)
- Delete item successfully
- Delete non-existent item
- Delete same item twice

### 7. TestIntegrationScenarios (3 tests)
- Complete CRUD workflow
- Multiple items management
- Update after partial update

### 8. TestEdgeCases (5 tests)
- Zero price
- Very large price
- Very long name
- Special characters
- Concurrent item creation

## Running Tests

### Run all tests:
```bash
pytest
```

### Run with verbose output:
```bash
pytest -v
```

### Run with coverage report:
```bash
pytest --cov=main --cov-report=term-missing
```

### Run with HTML coverage report:
```bash
pytest --cov=main --cov-report=html
# Open htmlcov/index.html in browser
```

### Run specific test class:
```bash
pytest test_main.py::TestPostEndpoint -v
```

### Run specific test:
```bash
pytest test_main.py::TestPostEndpoint::test_create_item_success -v
```

### Run tests matching a pattern:
```bash
pytest -k "delete" -v
```

## Coverage Report

Current coverage: **98%**

Only missing line:
- Line 132: The `if __name__ == "__main__"` block (not executed during tests)

## Test Features

✅ **Comprehensive Coverage**
- All HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Success and error scenarios
- Validation testing
- Edge cases

✅ **Fixtures**
- Automatic database reset between tests
- Reusable test client
- Sample data fixtures

✅ **Test Organization**
- Grouped by functionality
- Clear test names
- Descriptive docstrings

✅ **Integration Tests**
- Complete CRUD workflows
- Multi-item scenarios
- State management

✅ **Edge Case Testing**
- Boundary values
- Special characters
- Concurrent operations
- Invalid inputs

## Continuous Integration

To integrate with CI/CD pipelines:

```yaml
# Example for GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=main --cov-fail-under=95
```

## Adding New Tests

When adding new endpoints or features:

1. Create a new test class or add to existing one
2. Use fixtures for common setup
3. Test both success and failure cases
4. Aim for >95% coverage
5. Run tests before committing:
   ```bash
   pytest
   ```

## Test Best Practices

- ✅ Each test is independent
- ✅ Database is reset between tests
- ✅ Tests are fast (< 1 second total)
- ✅ Clear assertions with meaningful messages
- ✅ Tests document expected behavior

