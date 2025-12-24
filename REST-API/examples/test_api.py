"""
API Testing Script
This script demonstrates how to interact with the Products API using Python.

Before running:
1. Make sure the API is running: python app.py
2. Install requests: pip install requests
"""

import requests
import json

# API Base URL
BASE_URL = "http://localhost:5000"

def print_response(title, response):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    print()

def main():
    print("Testing Products API")
    print("Make sure the API is running at", BASE_URL)

    # 1. Health Check
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_response("Health Check", response)
    except requests.exceptions.ConnectionError:
        print(f"\nError: Could not connect to {BASE_URL}")
        print("Make sure the API is running: python app.py")
        return

    # 2. Get API Documentation
    response = requests.get(f"{BASE_URL}/")
    print_response("API Documentation", response)

    # 3. List All Products
    response = requests.get(f"{BASE_URL}/products")
    print_response("All Products", response)

    # 4. Get Products by Category
    response = requests.get(f"{BASE_URL}/products", params={"category": "Electronics"})
    print_response("Electronics Products", response)

    # 5. Get Products by Price Range
    response = requests.get(f"{BASE_URL}/products", params={"min_price": 50, "max_price": 200})
    print_response("Products $50-$200", response)

    # 6. Get Single Product
    response = requests.get(f"{BASE_URL}/products/1")
    print_response("Product ID: 1", response)

    # 7. Create New Product
    new_product = {
        "name": "Test Product",
        "description": "This is a test product created via API",
        "price": 99.99,
        "stock_quantity": 25,
        "category": "Test"
    }
    response = requests.post(f"{BASE_URL}/products", json=new_product)
    print_response("Create New Product", response)

    # Get the new product ID if created
    if response.status_code == 201:
        new_product_id = response.json()['data']['id']

        # 8. Update Product
        update_data = {"price": 79.99, "stock_quantity": 50}
        response = requests.put(f"{BASE_URL}/products/{new_product_id}", json=update_data)
        print_response(f"Update Product {new_product_id}", response)

        # 9. Delete Product
        response = requests.delete(f"{BASE_URL}/products/{new_product_id}")
        print_response(f"Delete Product {new_product_id}", response)

    # 10. Get Orders for Product (with JOIN)
    response = requests.get(f"{BASE_URL}/products/1/orders")
    print_response("Last 10 Orders for Product 1", response)

    # 11. Get Categories
    response = requests.get(f"{BASE_URL}/categories")
    print_response("All Categories", response)

    # 12. Test 404 Error
    response = requests.get(f"{BASE_URL}/products/99999")
    print_response("Product Not Found (404)", response)

    print("\nAPI Testing Complete!")

if __name__ == "__main__":
    main()
