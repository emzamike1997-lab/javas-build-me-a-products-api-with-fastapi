Here's an example of how you can write comprehensive tests for the products API using FastAPI and the Pytest framework.

### === test_products_api.py ===

```python
# test_products_api.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_products():
    """Test reading all products"""
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Product 1", "price": 10.99},
        {"id": 2, "name": "Product 2", "price": 9.99},
    ]

def test_read_product():
    """Test reading a single product"""
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Product 1", "price": 10.99}

def test_create_product():
    """Test creating a new product"""
    data = {"name": "New Product", "price": 12.99}
    response = client.post("/products", json=data)
    assert response.status_code == 201
    assert response.json() == {"id": 3, "name": "New Product", "price": 12.99}

def test_update_product():
    """Test updating an existing product"""
    data = {"name": "Updated Product", "price": 11.99}
    response = client.put("/products/1", json=data)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Updated Product", "price": 11.99}

def test_delete_product():
    """Test deleting a product"""
    response = client.delete("/products/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Product deleted successfully"}

def test_read_product_not_found():
    """Test reading a non-existent product"""
    response = client.get("/products/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_create_product_invalid_data():
    """Test creating a new product with invalid data"""
    data = {"name": "New Product"}
    response = client.post("/products", json=data)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "price"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
```

### === test_products_api_integration.py ===

```python
# test_products_api_integration.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration():
    """Test the entire API workflow"""
    # Create a new product
    data = {"name": "New Product", "price": 12.99}
    response = client.post("/products", json=data)
    assert response.status_code == 201
    product_id = response.json()["id"]

    # Read the newly created product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"id": product_id, "name": "New Product", "price": 12.99}

    # Update the product
    data = {"name": "Updated Product", "price": 11.99}
    response = client.put(f"/products/{product_id}", json=data)
    assert response.status_code == 200
    assert response.json() == {"id": product_id, "name": "Updated Product", "price": 11.99}

    # Delete the product
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Product deleted successfully"}

    # Try to read the deleted product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
```

### === test_products_api_unit.py ===

```python
# test_products_api_unit.py

import pytest
from main import products

def test_get_all_products():
    """Test getting all products"""
    products_list = products.get_all_products()
    assert len(products_list) == 2
    assert products_list[0].id == 1
    assert products_list[0].name == "Product 1"
    assert products_list[0].price == 10.99

def test_get_product_by_id():
    """Test getting a product by ID"""
    product = products.get_product_by_id(1)
    assert product.id == 1
    assert product.name == "Product 1"
    assert product.price == 10.99

def test_create_product():
    """Test creating a new product"""
    product = products.create_product(name="New Product", price=12.99)
    assert product.id == 3
    assert product.name == "New Product"
    assert product.price == 12.99

def test_update_product():
    """Test updating an existing product"""
    product = products.update_product(1, name="Updated Product", price=11.99)
    assert product.id == 1
    assert product.name == "Updated Product"
    assert product.price == 11.99

def test_delete_product():
    """Test deleting a product"""
    products.delete_product(1)
    assert products.get_product_by_id(1) is None
```

Note that the `products` module is assumed to be a separate module that contains the business logic for managing products. The unit tests in `test_products_api_unit.py` test the individual functions in the `products` module, while the integration tests in `test_products_api_integration.py` test the entire API workflow. The API tests in `test_products_api.py` test the API endpoints directly.