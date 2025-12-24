"""
Products API - Complete Flask REST API Example
This is a fully functional REST API for managing products.

Run this file to start the API server:
    python app.py

Then visit http://localhost:5000 for documentation.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from decimal import Decimal
import os

# Try to import psycopg2, fall back to mock data if not available
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    USE_DATABASE = True
except ImportError:
    USE_DATABASE = False
    print("Warning: psycopg2 not installed. Using mock data.")

app = Flask(__name__)
CORS(app)

# ============================================
# CONFIGURATION
# ============================================

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'ecommerce_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}

# ============================================
# MOCK DATA (used if database not available)
# ============================================

MOCK_PRODUCTS = [
    {"id": 1, "name": "Laptop Pro", "description": "High-performance laptop", "price": 1299.99, "stock_quantity": 50, "category": "Electronics", "sku": "ELEC-001", "is_active": True},
    {"id": 2, "name": "Wireless Mouse", "description": "Ergonomic wireless mouse", "price": 29.99, "stock_quantity": 200, "category": "Electronics", "sku": "ELEC-002", "is_active": True},
    {"id": 3, "name": "USB-C Hub", "description": "7-in-1 USB-C hub", "price": 49.99, "stock_quantity": 150, "category": "Electronics", "sku": "ELEC-003", "is_active": True},
    {"id": 4, "name": "Mechanical Keyboard", "description": "RGB mechanical keyboard", "price": 89.99, "stock_quantity": 100, "category": "Electronics", "sku": "ELEC-004", "is_active": True},
    {"id": 5, "name": "Monitor 27\"", "description": "27-inch 4K monitor", "price": 399.99, "stock_quantity": 75, "category": "Electronics", "sku": "ELEC-005", "is_active": True},
]

MOCK_ORDERS = [
    {"order_id": 1, "customer_name": "John Doe", "product_id": 1, "quantity": 1, "order_date": "2024-01-20", "status": "delivered"},
    {"order_id": 2, "customer_name": "Alice Smith", "product_id": 1, "quantity": 1, "order_date": "2024-01-18", "status": "shipped"},
    {"order_id": 3, "customer_name": "Bob Johnson", "product_id": 1, "quantity": 2, "order_date": "2024-01-15", "status": "delivered"},
]

# ============================================
# DATABASE HELPERS
# ============================================

def get_db_connection():
    """Create a database connection."""
    if not USE_DATABASE:
        return None
    return psycopg2.connect(**DB_CONFIG)

def execute_query(query, params=None, fetch_one=False):
    """Execute a query and return results."""
    if not USE_DATABASE:
        return None

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

def serialize_row(row):
    """Convert database row to JSON-serializable format."""
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
# API ENDPOINTS
# ============================================

@app.route('/')
def home():
    """API documentation endpoint."""
    return jsonify({
        "name": "Products API",
        "version": "1.0.0",
        "description": "A sample REST API for managing products",
        "database_connected": USE_DATABASE,
        "endpoints": {
            "GET /": "This documentation",
            "GET /health": "Health check",
            "GET /products": "List all products",
            "GET /products/<id>": "Get product by ID",
            "POST /products": "Create new product",
            "PUT /products/<id>": "Update product",
            "DELETE /products/<id>": "Delete product",
            "GET /products/<id>/orders": "Get last 10 orders for a product",
            "GET /categories": "List all categories"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    db_status = "connected" if USE_DATABASE else "mock_data"
    return jsonify({
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering."""
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    if USE_DATABASE:
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

        query += " ORDER BY created_at DESC LIMIT 100"
        products = execute_query(query, params)
        products = [serialize_row(p) for p in products]
    else:
        # Use mock data
        products = MOCK_PRODUCTS.copy()
        if category:
            products = [p for p in products if p['category'] == category]
        if min_price is not None:
            products = [p for p in products if p['price'] >= min_price]
        if max_price is not None:
            products = [p for p in products if p['price'] <= max_price]

    return jsonify({
        "status": "success",
        "count": len(products),
        "data": products
    })

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID."""
    if USE_DATABASE:
        query = "SELECT * FROM products WHERE id = %s"
        product = execute_query(query, (product_id,), fetch_one=True)
        product = serialize_row(product)
    else:
        product = next((p for p in MOCK_PRODUCTS if p['id'] == product_id), None)

    if product is None:
        return jsonify({
            "status": "error",
            "message": f"Product with ID {product_id} not found"
        }), 404

    return jsonify({
        "status": "success",
        "data": product
    })

@app.route('/products', methods=['POST'])
def create_product():
    """Create a new product."""
    data = request.get_json()

    # Validation
    if not data.get('name'):
        return jsonify({"status": "error", "message": "Name is required"}), 400
    if not data.get('price') or data['price'] < 0:
        return jsonify({"status": "error", "message": "Valid price is required"}), 400

    if USE_DATABASE:
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
        product = execute_query(query, params, fetch_one=True)
        product = serialize_row(product)
    else:
        # Mock create
        new_id = max(p['id'] for p in MOCK_PRODUCTS) + 1
        product = {
            "id": new_id,
            "name": data['name'],
            "description": data.get('description'),
            "price": data['price'],
            "stock_quantity": data.get('stock_quantity', 0),
            "category": data.get('category'),
            "sku": data.get('sku'),
            "is_active": True
        }
        MOCK_PRODUCTS.append(product)

    return jsonify({
        "status": "success",
        "message": "Product created successfully",
        "data": product
    }), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product."""
    data = request.get_json()

    if USE_DATABASE:
        existing = execute_query("SELECT id FROM products WHERE id = %s", (product_id,), fetch_one=True)
        if existing is None:
            return jsonify({"status": "error", "message": f"Product {product_id} not found"}), 404

        query = """
            UPDATE products
            SET name = COALESCE(%s, name),
                description = COALESCE(%s, description),
                price = COALESCE(%s, price),
                stock_quantity = COALESCE(%s, stock_quantity),
                category = COALESCE(%s, category),
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
            product_id
        )
        product = execute_query(query, params, fetch_one=True)
        product = serialize_row(product)
    else:
        product = next((p for p in MOCK_PRODUCTS if p['id'] == product_id), None)
        if product is None:
            return jsonify({"status": "error", "message": f"Product {product_id} not found"}), 404

        # Update mock product
        for key, value in data.items():
            if key in product and value is not None:
                product[key] = value

    return jsonify({
        "status": "success",
        "message": "Product updated successfully",
        "data": product
    })

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product (soft delete)."""
    if USE_DATABASE:
        existing = execute_query("SELECT id FROM products WHERE id = %s", (product_id,), fetch_one=True)
        if existing is None:
            return jsonify({"status": "error", "message": f"Product {product_id} not found"}), 404

        execute_query("UPDATE products SET is_active = FALSE WHERE id = %s", (product_id,))
    else:
        product = next((p for p in MOCK_PRODUCTS if p['id'] == product_id), None)
        if product is None:
            return jsonify({"status": "error", "message": f"Product {product_id} not found"}), 404
        product['is_active'] = False

    return jsonify({
        "status": "success",
        "message": f"Product {product_id} deleted successfully"
    })

@app.route('/products/<int:product_id>/orders', methods=['GET'])
def get_product_orders(product_id):
    """Get the last 10 orders containing this product."""
    limit = request.args.get('limit', 10, type=int)
    limit = min(limit, 50)

    if USE_DATABASE:
        # First verify product exists
        product = execute_query("SELECT * FROM products WHERE id = %s", (product_id,), fetch_one=True)
        if product is None:
            return jsonify({"status": "error", "message": f"Product {product_id} not found"}), 404

        orders_query = """
            SELECT
                p.id AS product_id,
                p.name AS product_name,
                p.price AS current_price,
                p.category AS product_category,
                o.id AS order_id,
                o.order_date,
                o.status AS order_status,
                c.first_name || ' ' || c.last_name AS customer_name,
                c.email AS customer_email,
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
        orders = [serialize_row(o) for o in orders]
        product = serialize_row(product)
    else:
        product = next((p for p in MOCK_PRODUCTS if p['id'] == product_id), None)
        if product is None:
            return jsonify({"status": "error", "message": f"Product {product_id} not found"}), 404

        orders = [o for o in MOCK_ORDERS if o['product_id'] == product_id][:limit]

    return jsonify({
        "status": "success",
        "product": {
            "id": product['id'],
            "name": product['name'],
            "current_price": product['price'],
            "category": product.get('category')
        },
        "orders_count": len(orders),
        "orders": orders
    })

@app.route('/categories', methods=['GET'])
def get_categories():
    """Get all unique categories."""
    if USE_DATABASE:
        query = """
            SELECT category, COUNT(*) as product_count
            FROM products
            WHERE is_active = TRUE AND category IS NOT NULL
            GROUP BY category
            ORDER BY product_count DESC
        """
        categories = execute_query(query)
        categories = [serialize_row(c) for c in categories]
    else:
        category_counts = {}
        for p in MOCK_PRODUCTS:
            cat = p.get('category')
            if cat:
                category_counts[cat] = category_counts.get(cat, 0) + 1
        categories = [{"category": k, "product_count": v} for k, v in category_counts.items()]

    return jsonify({
        "status": "success",
        "count": len(categories),
        "data": categories
    })

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

# ============================================
# RUN APPLICATION
# ============================================

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  Products API - Starting...")
    print("=" * 50)
    print(f"  Database: {'Connected' if USE_DATABASE else 'Using Mock Data'}")
    print(f"  Documentation: http://localhost:5000/")
    print(f"  Health Check: http://localhost:5000/health")
    print("=" * 50 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
