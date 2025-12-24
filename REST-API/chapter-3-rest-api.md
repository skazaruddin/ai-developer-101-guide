# Chapter 3: REST APIs

## Building the Bridge Between Frontend and Backend

---

## Table of Contents

1. [What is an API?](#what-is-an-api)
2. [Why Do We Need APIs?](#why-do-we-need-apis)
3. [What is REST?](#what-is-rest)
4. [How REST APIs Work](#how-rest-apis-work)
5. [HTTP Methods](#http-methods)
6. [JSON: The Language of APIs](#json-the-language-of-apis)
7. [API Architecture](#api-architecture)
8. [Setting Up Your First API](#setting-up-your-first-api)
9. [Building the Products API](#building-the-products-api)
10. [Testing Your API](#testing-your-api)
11. [Best Practices](#best-practices)

---

## What is an API?

### The Simple Explanation

Imagine you're at a restaurant:
- You (the customer) don't go into the kitchen
- You tell the **waiter** what you want
- The waiter tells the kitchen
- The kitchen prepares your food
- The waiter brings it back to you

An **API (Application Programming Interface)** is like that waiter. It's the messenger that:
- Takes your request
- Tells the system what you want
- Returns the response back to you

### Technical Definition

An API is a set of rules and protocols that allows different software applications to communicate with each other.

```
┌─────────────┐       API       ┌─────────────┐
│   Client    │ ◄─────────────► │   Server    │
│ (Frontend)  │    Request/     │  (Backend)  │
│             │    Response     │  + Database │
└─────────────┘                 └─────────────┘
```

### Real-World Examples

| When You... | The API... |
|-------------|------------|
| Check weather on your phone | Fetches data from a weather service |
| Log in with Google | Authenticates through Google's API |
| Share to Twitter | Posts via Twitter's API |
| Order food on DoorDash | Communicates with restaurant systems |
| Pay with credit card | Processes through payment APIs |

---

## Why Do We Need APIs?

### The Problem Without APIs

Imagine every app had to build everything from scratch:
- Weather app? Build your own satellites and sensors
- Maps app? Survey every road yourself
- Payment app? Create your own banking system

**That's impossible!**

### How APIs Solve This

APIs let applications share data and functionality:

```
Your App
    │
    ├── Google Maps API ──► Get directions
    ├── Stripe API ────────► Process payments
    ├── Twilio API ────────► Send SMS
    ├── OpenAI API ────────► AI capabilities
    └── Your Database ─────► Your data
```

### Benefits of APIs

1. **Modularity**: Break complex systems into manageable parts
2. **Reusability**: Use existing services instead of building from scratch
3. **Scalability**: Different teams can work on different parts
4. **Security**: Control what data and actions are exposed
5. **Flexibility**: Frontend and backend can evolve independently

---

## What is REST?

### REST = Representational State Transfer

REST is an **architectural style** for designing networked applications. A REST API (or RESTful API) follows these principles.

### Key Principles

#### 1. **Client-Server Separation**
The client (frontend) and server (backend) are independent.

```
Mobile App  ─┐
Web App     ─┼─► REST API ─► Database
Desktop App ─┘
```

#### 2. **Stateless**
Each request contains all information needed. The server doesn't remember previous requests.

```
Request 1: "Get user 123" → Server processes → Response
Request 2: "Get user 123" → Server processes → Response
(Server doesn't remember Request 1 when handling Request 2)
```

#### 3. **Uniform Interface**
Consistent way to interact with resources using standard HTTP methods.

```
GET    /products      → List all products
GET    /products/1    → Get product with ID 1
POST   /products      → Create new product
PUT    /products/1    → Update product 1
DELETE /products/1    → Delete product 1
```

#### 4. **Resource-Based**
Everything is a "resource" identified by URLs (URIs).

```
/users          → Collection of users
/users/42       → Specific user (ID: 42)
/users/42/orders → Orders for user 42
```

### Why REST Became Popular

| Feature | Benefit |
|---------|---------|
| Uses HTTP | Works with existing web infrastructure |
| Stateless | Easy to scale horizontally |
| Standard methods | Developers already understand GET, POST, etc. |
| JSON format | Lightweight and human-readable |
| Language agnostic | Any language can consume REST APIs |

---

## How REST APIs Work

### The Request-Response Cycle

```
1. Client sends HTTP Request
   ┌──────────────────────────────────────┐
   │ GET /api/products/1                  │
   │ Host: api.mystore.com                │
   │ Authorization: Bearer token123       │
   └──────────────────────────────────────┘
                    │
                    ▼
2. Server processes the request
   - Validates authentication
   - Queries database
   - Formats response

                    │
                    ▼
3. Server sends HTTP Response
   ┌──────────────────────────────────────┐
   │ HTTP/1.1 200 OK                      │
   │ Content-Type: application/json       │
   │                                      │
   │ {                                    │
   │   "id": 1,                           │
   │   "name": "Laptop Pro",              │
   │   "price": 1299.99                   │
   │ }                                    │
   └──────────────────────────────────────┘
```

### Anatomy of an HTTP Request

```
┌─────────────────────────────────────────────────────┐
│  METHOD   URL                    HTTP Version       │
│  GET      /api/products?limit=10  HTTP/1.1          │
├─────────────────────────────────────────────────────┤
│  Headers:                                           │
│  Host: api.mystore.com                              │
│  Content-Type: application/json                     │
│  Authorization: Bearer eyJhbGci...                  │
├─────────────────────────────────────────────────────┤
│  Body (for POST/PUT/PATCH):                         │
│  {                                                  │
│    "name": "New Product",                           │
│    "price": 99.99                                   │
│  }                                                  │
└─────────────────────────────────────────────────────┘
```

### Anatomy of an HTTP Response

```
┌─────────────────────────────────────────────────────┐
│  Status Line:                                       │
│  HTTP/1.1 200 OK                                    │
├─────────────────────────────────────────────────────┤
│  Headers:                                           │
│  Content-Type: application/json                     │
│  Content-Length: 256                                │
│  Date: Mon, 15 Jan 2024 10:30:00 GMT               │
├─────────────────────────────────────────────────────┤
│  Body:                                              │
│  {                                                  │
│    "id": 1,                                         │
│    "name": "Laptop Pro",                            │
│    "price": 1299.99,                                │
│    "stock": 50                                      │
│  }                                                  │
└─────────────────────────────────────────────────────┘
```

---

## HTTP Methods

### CRUD Operations Mapped to HTTP Methods

| HTTP Method | CRUD | Action | Example |
|-------------|------|--------|---------|
| `GET` | Read | Retrieve data | Get product details |
| `POST` | Create | Create new resource | Add new product |
| `PUT` | Update | Replace entire resource | Update all product fields |
| `PATCH` | Update | Partial update | Update just the price |
| `DELETE` | Delete | Remove resource | Delete a product |

### Common HTTP Status Codes

#### Success (2xx)

| Code | Meaning | When to Use |
|------|---------|-------------|
| `200 OK` | Request successful | GET, PUT, PATCH success |
| `201 Created` | Resource created | POST success |
| `204 No Content` | Success, no body | DELETE success |

#### Client Errors (4xx)

| Code | Meaning | When to Use |
|------|---------|-------------|
| `400 Bad Request` | Invalid request | Missing/invalid data |
| `401 Unauthorized` | Not authenticated | Missing/invalid token |
| `403 Forbidden` | Not authorized | Insufficient permissions |
| `404 Not Found` | Resource doesn't exist | Invalid ID |
| `422 Unprocessable` | Validation failed | Business rule violation |

#### Server Errors (5xx)

| Code | Meaning | When to Use |
|------|---------|-------------|
| `500 Internal Error` | Server crashed | Unexpected error |
| `502 Bad Gateway` | Upstream error | Backend service down |
| `503 Service Unavailable` | Server overloaded | Maintenance/overload |

---

## JSON: The Language of APIs

### What is JSON?

**JSON (JavaScript Object Notation)** is a lightweight data format that's easy for humans to read and write, and easy for machines to parse.

### JSON Syntax

```json
{
    "string": "Hello, World!",
    "number": 42,
    "decimal": 3.14,
    "boolean": true,
    "null_value": null,
    "array": [1, 2, 3, "four"],
    "object": {
        "nested": "value",
        "another": 123
    }
}
```

### Real-World API Response

```json
{
    "status": "success",
    "data": {
        "product": {
            "id": 1,
            "name": "Laptop Pro",
            "description": "High-performance laptop",
            "price": 1299.99,
            "currency": "USD",
            "stock": 50,
            "category": "Electronics",
            "images": [
                "https://example.com/laptop1.jpg",
                "https://example.com/laptop2.jpg"
            ],
            "specifications": {
                "ram": "16GB",
                "storage": "512GB SSD",
                "processor": "Intel i7"
            },
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-20T14:45:00Z"
        }
    },
    "meta": {
        "request_id": "abc123",
        "timestamp": "2024-01-22T09:00:00Z"
    }
}
```

### Why JSON is Popular

| Feature | Benefit |
|---------|---------|
| Human-readable | Easy to debug and understand |
| Lightweight | Small payload size |
| Language-agnostic | Works with any programming language |
| Native to JavaScript | Perfect for web applications |
| Hierarchical | Represents complex data structures |

---

## API Architecture

### How UI Applications Communicate with Backend

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Mobile  │  │   Web    │  │ Desktop  │  │   IoT    │        │
│  │   App    │  │   App    │  │   App    │  │  Device  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │             │               │
└───────┼─────────────┼─────────────┼─────────────┼───────────────┘
        │             │             │             │
        └─────────────┼─────────────┼─────────────┘
                      │             │
                      ▼             ▼
        ┌─────────────────────────────────────────┐
        │              REST API                    │
        │         (HTTPS Requests)                 │
        └─────────────────┬───────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                         BACKEND                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Server                             │  │
│  │  (Python/Flask, Node.js/Express, Java/Spring, etc.)      │  │
│  │                                                           │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │  │
│  │  │   Routes    │  │   Business  │  │    Data     │       │  │
│  │  │  /products  │──│    Logic    │──│   Access    │       │  │
│  │  │  /orders    │  │             │  │   Layer     │       │  │
│  │  └─────────────┘  └─────────────┘  └──────┬──────┘       │  │
│  └───────────────────────────────────────────┼──────────────┘  │
│                                              │                  │
│                                              ▼                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     DATABASE                              │  │
│  │                   (PostgreSQL)                            │  │
│  │                                                           │  │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────────────────┐   │  │
│  │   │ Products │  │ Customers│  │      Orders           │   │  │
│  │   └──────────┘  └──────────┘  └──────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### The Flow: User Buys a Product

```
1. User clicks "Buy" on mobile app
       │
       ▼
2. App sends request:
   POST /api/orders
   {
     "product_id": 1,
     "quantity": 2
   }
       │
       ▼
3. API Server receives request
   - Validates the data
   - Checks product availability
   - Calculates total
       │
       ▼
4. API queries Database
   - SELECT from products
   - INSERT into orders
   - UPDATE stock
       │
       ▼
5. API sends response:
   {
     "order_id": 456,
     "status": "confirmed",
     "total": 2599.98
   }
       │
       ▼
6. App shows "Order Confirmed!"
```

---

## Setting Up Your First API

### Installing Dependencies

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Flask (our web framework)
pip install flask flask-cors

# Install database connector
pip install psycopg2-binary

# Install other useful packages
pip install python-dotenv
```

### Project Structure

```
products-api/
├── app.py              # Main application
├── config.py           # Configuration
├── models/
│   ├── __init__.py
│   └── product.py      # Product model
├── routes/
│   ├── __init__.py
│   └── products.py     # Product routes
├── database.py         # Database connection
├── requirements.txt    # Dependencies
└── .env               # Environment variables
```

### Basic Flask App

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Products API!",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

Run it:
```bash
python app.py
# Visit http://localhost:5000
```

---

## Building the Products API

### Complete API Implementation

Let's build a full Products API with CRUD operations and an endpoint for the last 10 orders.

#### Configuration (config.py)

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'ecommerce_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
```

#### Database Connection (database.py)

```python
# database.py
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

config = Config()

def get_db_connection():
    """Create a database connection."""
    conn = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )
    return conn

def execute_query(query, params=None, fetch_one=False):
    """Execute a query and return results."""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                if fetch_one:
                    return cursor.fetchone()
                return cursor.fetchall()
            else:
                conn.commit()
                if cursor.description:
                    return cursor.fetchone()
                return None
    finally:
        conn.close()
```

#### Main Application (app.py)

```python
# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import execute_query
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Helper function to convert Decimal to float for JSON serialization
def serialize_row(row):
    if row is None:
        return None
    result = dict(row)
    for key, value in result.items():
        if isinstance(value, Decimal):
            result[key] = float(value)
        elif isinstance(value, datetime):
            result[key] = value.isoformat()
    return result

# ============================================
# HEALTH & INFO ENDPOINTS
# ============================================

@app.route('/')
def home():
    """API documentation endpoint."""
    return jsonify({
        "name": "Products API",
        "version": "1.0.0",
        "endpoints": {
            "GET /products": "List all products",
            "GET /products/<id>": "Get product by ID",
            "POST /products": "Create new product",
            "PUT /products/<id>": "Update product",
            "DELETE /products/<id>": "Delete product",
            "GET /products/<id>/orders": "Get last 10 orders for a product"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

# ============================================
# PRODUCTS ENDPOINTS (CRUD)
# ============================================

@app.route('/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering."""
    # Query parameters
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    in_stock = request.args.get('in_stock', type=bool)
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)

    # Build query dynamically
    query = "SELECT * FROM products WHERE is_active = TRUE"
    params = []

    if category:
        query += " AND category = %s"
        params.append(category)
    if min_price is not None:
        query += " AND price >= %s"
        params.append(min_price)
    if max_price is not None:
        query += " AND price <= %s"
        params.append(max_price)
    if in_stock:
        query += " AND stock_quantity > 0"

    query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    products = execute_query(query, params)

    return jsonify({
        "status": "success",
        "count": len(products),
        "data": [serialize_row(p) for p in products]
    })

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID."""
    query = "SELECT * FROM products WHERE id = %s"
    product = execute_query(query, (product_id,), fetch_one=True)

    if product is None:
        return jsonify({
            "status": "error",
            "message": f"Product with ID {product_id} not found"
        }), 404

    return jsonify({
        "status": "success",
        "data": serialize_row(product)
    })

@app.route('/products', methods=['POST'])
def create_product():
    """Create a new product."""
    data = request.get_json()

    # Validation
    required_fields = ['name', 'price']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "status": "error",
                "message": f"Missing required field: {field}"
            }), 400

    if data['price'] < 0:
        return jsonify({
            "status": "error",
            "message": "Price cannot be negative"
        }), 400

    query = """
        INSERT INTO products (name, description, price, stock_quantity, category, sku)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *
    """
    params = (
        data['name'],
        data.get('description'),
        data['price'],
        data.get('stock_quantity', 0),
        data.get('category'),
        data.get('sku')
    )

    try:
        product = execute_query(query, params, fetch_one=True)
        return jsonify({
            "status": "success",
            "message": "Product created successfully",
            "data": serialize_row(product)
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product."""
    data = request.get_json()

    # Check if product exists
    existing = execute_query("SELECT id FROM products WHERE id = %s", (product_id,), fetch_one=True)
    if existing is None:
        return jsonify({
            "status": "error",
            "message": f"Product with ID {product_id} not found"
        }), 404

    query = """
        UPDATE products
        SET name = COALESCE(%s, name),
            description = COALESCE(%s, description),
            price = COALESCE(%s, price),
            stock_quantity = COALESCE(%s, stock_quantity),
            category = COALESCE(%s, category),
            sku = COALESCE(%s, sku),
            is_active = COALESCE(%s, is_active),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *
    """
    params = (
        data.get('name'),
        data.get('description'),
        data.get('price'),
        data.get('stock_quantity'),
        data.get('category'),
        data.get('sku'),
        data.get('is_active'),
        product_id
    )

    product = execute_query(query, params, fetch_one=True)

    return jsonify({
        "status": "success",
        "message": "Product updated successfully",
        "data": serialize_row(product)
    })

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Soft delete a product (set is_active to false)."""
    # Check if product exists
    existing = execute_query("SELECT id FROM products WHERE id = %s", (product_id,), fetch_one=True)
    if existing is None:
        return jsonify({
            "status": "error",
            "message": f"Product with ID {product_id} not found"
        }), 404

    query = "UPDATE products SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
    execute_query(query, (product_id,))

    return jsonify({
        "status": "success",
        "message": f"Product {product_id} deleted successfully"
    }), 200

# ============================================
# SPECIAL ENDPOINT: Last 10 Orders for Product
# ============================================

@app.route('/products/<int:product_id>/orders', methods=['GET'])
def get_product_orders(product_id):
    """
    Get the last 10 orders containing this product.
    Includes product details and customer information.
    Uses JOINs across products, order_items, orders, and customers tables.
    """
    # First, verify the product exists
    product_query = "SELECT * FROM products WHERE id = %s"
    product = execute_query(product_query, (product_id,), fetch_one=True)

    if product is None:
        return jsonify({
            "status": "error",
            "message": f"Product with ID {product_id} not found"
        }), 404

    # Get limit from query params (default 10)
    limit = request.args.get('limit', 10, type=int)
    if limit > 50:
        limit = 50  # Cap at 50 for performance

    # Query for orders with JOINs
    orders_query = """
        SELECT
            p.id AS product_id,
            p.name AS product_name,
            p.price AS current_price,
            p.category AS product_category,
            p.stock_quantity AS current_stock,
            o.id AS order_id,
            o.order_date,
            o.status AS order_status,
            o.total_amount AS order_total,
            c.id AS customer_id,
            c.first_name || ' ' || c.last_name AS customer_name,
            c.email AS customer_email,
            c.city AS customer_city,
            oi.quantity,
            oi.unit_price AS price_at_purchase,
            oi.subtotal AS line_total
        FROM products p
        INNER JOIN order_items oi ON p.id = oi.product_id
        INNER JOIN orders o ON oi.order_id = o.id
        INNER JOIN customers c ON o.customer_id = c.id
        WHERE p.id = %s
        ORDER BY o.order_date DESC
        LIMIT %s
    """

    orders = execute_query(orders_query, (product_id, limit))

    # Format the response
    return jsonify({
        "status": "success",
        "product": {
            "id": product['id'],
            "name": product['name'],
            "current_price": float(product['price']),
            "category": product['category'],
            "stock_quantity": product['stock_quantity']
        },
        "orders_count": len(orders),
        "orders": [serialize_row(order) for order in orders]
    })

# ============================================
# CATEGORIES ENDPOINT
# ============================================

@app.route('/categories', methods=['GET'])
def get_categories():
    """Get all unique categories with product counts."""
    query = """
        SELECT
            category,
            COUNT(*) AS product_count,
            AVG(price)::DECIMAL(10,2) AS avg_price,
            SUM(stock_quantity) AS total_stock
        FROM products
        WHERE is_active = TRUE AND category IS NOT NULL
        GROUP BY category
        ORDER BY product_count DESC
    """
    categories = execute_query(query)

    return jsonify({
        "status": "success",
        "count": len(categories),
        "data": [serialize_row(c) for c in categories]
    })

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Resource not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

# ============================================
# RUN THE APPLICATION
# ============================================

if __name__ == '__main__':
    print("Starting Products API...")
    print("Documentation: http://localhost:5000/")
    print("Health check: http://localhost:5000/health")
    app.run(debug=True, host='0.0.0.0', port=5000)
```

#### Requirements File

```
# requirements.txt
flask==3.0.0
flask-cors==4.0.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

#### Environment Variables

```
# .env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_password_here
```

---

## Testing Your API

### Using cURL (Command Line)

```bash
# Get all products
curl http://localhost:5000/products

# Get a specific product
curl http://localhost:5000/products/1

# Get products filtered by category
curl "http://localhost:5000/products?category=Electronics"

# Create a new product
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "New Product", "price": 99.99, "category": "Electronics"}'

# Update a product
curl -X PUT http://localhost:5000/products/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 1199.99}'

# Delete a product
curl -X DELETE http://localhost:5000/products/1

# Get last 10 orders for a product
curl http://localhost:5000/products/1/orders

# Get categories
curl http://localhost:5000/categories
```

### Using Python Requests

```python
# test_api.py
import requests

BASE_URL = "http://localhost:5000"

# Get all products
response = requests.get(f"{BASE_URL}/products")
print("All Products:", response.json())

# Get a specific product
response = requests.get(f"{BASE_URL}/products/1")
print("Product 1:", response.json())

# Create a new product
new_product = {
    "name": "Test Product",
    "description": "A test product",
    "price": 49.99,
    "stock_quantity": 100,
    "category": "Test"
}
response = requests.post(f"{BASE_URL}/products", json=new_product)
print("Created:", response.json())

# Get last 10 orders for product 1
response = requests.get(f"{BASE_URL}/products/1/orders")
print("Orders for Product 1:", response.json())
```

### Using Postman or Thunder Client

1. Download [Postman](https://www.postman.com/) or install Thunder Client extension in VS Code
2. Create a new request
3. Set the method (GET, POST, etc.)
4. Enter the URL
5. For POST/PUT, go to Body tab, select "raw" and "JSON"
6. Click Send

---

## Best Practices

### 1. Use Meaningful HTTP Status Codes

```python
# Good
return jsonify({"data": product}), 200  # OK
return jsonify({"data": product}), 201  # Created
return jsonify({"error": "Not found"}), 404  # Not Found

# Bad - Don't always return 200
return jsonify({"error": "Not found"}), 200  # ❌
```

### 2. Consistent Response Format

```python
# Success response
{
    "status": "success",
    "data": {...},
    "meta": {
        "total": 100,
        "page": 1,
        "per_page": 10
    }
}

# Error response
{
    "status": "error",
    "message": "Product not found",
    "code": "PRODUCT_NOT_FOUND"
}
```

### 3. Validate Input Data

```python
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()

    # Validate required fields
    if not data.get('name'):
        return jsonify({"error": "Name is required"}), 400

    if not isinstance(data.get('price'), (int, float)) or data['price'] < 0:
        return jsonify({"error": "Valid price is required"}), 400
```

### 4. Use Pagination for Large Datasets

```python
@app.route('/products')
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)  # Cap at 100

    offset = (page - 1) * per_page

    query = "SELECT * FROM products LIMIT %s OFFSET %s"
    products = execute_query(query, (per_page, offset))

    return jsonify({
        "data": products,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": get_total_count()
        }
    })
```

### 5. Handle Errors Gracefully

```python
@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error
    app.logger.error(f"Unhandled exception: {str(e)}")

    # Return generic error to client
    return jsonify({
        "status": "error",
        "message": "An unexpected error occurred"
    }), 500
```

---

## Summary

Congratulations! You've learned:

- **What APIs are** and why they're essential
- **REST principles** and how they work
- **HTTP methods** and status codes
- **JSON** as the data format for APIs
- **How to build a complete REST API** with Flask
- **CRUD operations** for products
- **JOIN queries** for complex data (orders with product details)
- **Best practices** for API design

### What We Built

- A Products API with full CRUD operations
- An endpoint to get the last 10 orders for any product
- Proper error handling and validation
- Consistent response formats

### Next Steps

1. Add authentication (JWT tokens)
2. Implement rate limiting
3. Add request logging
4. Deploy to a cloud provider
5. Move on to [Chapter 4: Language Models](../AI-Models/chapter-4-language-models.md)

---

[← Previous: Chapter 2 - Database](../Database/chapter-2-database-fundamentals.md) | [Back to Main Guide](../README.md) | [Next: Chapter 4 - Language Models →](../AI-Models/chapter-4-language-models.md)
