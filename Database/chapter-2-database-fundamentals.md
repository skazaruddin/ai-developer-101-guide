# Chapter 2: Database Fundamentals with PostgreSQL

## Understanding Databases from Scratch

---

## Table of Contents

1. [What is a Database?](#what-is-a-database)
2. [Why Do We Need Databases?](#why-do-we-need-databases)
3. [Types of Databases](#types-of-databases)
4. [Introduction to PostgreSQL](#introduction-to-postgresql)
5. [Installing PostgreSQL](#installing-postgresql)
6. [SQL Basics](#sql-basics)
7. [Creating Tables](#creating-tables)
8. [CRUD Operations](#crud-operations)
9. [Constraints](#constraints)
10. [Relationships and Foreign Keys](#relationships-and-foreign-keys)
11. [JOIN Operations](#join-operations)
12. [Practice: Products and Orders System](#practice-products-and-orders-system)

---

## What is a Database?

### The Simple Explanation

Imagine you run a small library. You need to keep track of:
- All your books (title, author, ISBN)
- All your members (name, address, phone)
- Who borrowed which book and when

You could use paper notebooks, but that would be:
- Hard to search
- Easy to lose
- Difficult to update
- Impossible to share

A **database** is like a super-organized digital filing cabinet that solves all these problems!

### Real-World Analogy

Think of a database as a **spreadsheet on steroids**:

| Book ID | Title | Author | Available |
|---------|-------|--------|-----------|
| 1 | Harry Potter | J.K. Rowling | Yes |
| 2 | Lord of the Rings | J.R.R. Tolkien | No |
| 3 | 1984 | George Orwell | Yes |

But unlike a spreadsheet, a database can:
- Handle millions of records efficiently
- Allow multiple users simultaneously
- Enforce rules (e.g., "Book ID must be unique")
- Create complex relationships between data
- Recover from crashes automatically

---

## Why Do We Need Databases?

### The Problems Databases Solve

#### 1. **Data Persistence**
Your program's variables disappear when it stops running. Databases save data permanently.

```
Without Database:
  Program runs → Data in memory → Program stops → Data LOST!

With Database:
  Program runs → Save to database → Program stops → Data SAFE
  Program restarts → Load from database → Data RESTORED!
```

#### 2. **Data Organization**
Raw data is messy. Databases organize it into tables with defined structures.

#### 3. **Data Integrity**
Databases enforce rules to prevent bad data:
- "Email must be unique"
- "Age cannot be negative"
- "Every order must have a customer"

#### 4. **Data Querying**
Find exactly what you need instantly:
- "Show all customers from New York"
- "Find orders placed last week"
- "Calculate total sales by product"

#### 5. **Concurrent Access**
Multiple users can read and write simultaneously without corrupting data.

### Real-World Examples

| Application | What's in the Database |
|-------------|------------------------|
| Online Store | Products, customers, orders, payments |
| Social Media | Users, posts, comments, likes, follows |
| Banking | Accounts, transactions, customers |
| Healthcare | Patients, doctors, appointments, records |
| E-learning | Courses, students, progress, certificates |

---

## Types of Databases

### 1. Relational Databases (SQL)

Data stored in **tables** with **rows** and **columns**. Tables can be linked through **relationships**.

```
┌─────────────────────┐    ┌─────────────────────┐
│      Customers      │    │       Orders        │
├─────────────────────┤    ├─────────────────────┤
│ id   │ name         │    │ id │ customer_id    │
│ 1    │ Alice        │───→│ 1  │ 1              │
│ 2    │ Bob          │    │ 2  │ 1              │
└─────────────────────┘    │ 3  │ 2              │
                           └─────────────────────┘
```

**Examples**: PostgreSQL, MySQL, SQLite, Oracle, SQL Server

**Best for**: Structured data with clear relationships

### 2. NoSQL Databases

Data stored in flexible formats (documents, key-value pairs, graphs).

```json
{
  "customer": {
    "name": "Alice",
    "orders": [
      {"id": 1, "total": 99.99},
      {"id": 2, "total": 49.99}
    ]
  }
}
```

**Examples**: MongoDB, Redis, Cassandra, Neo4j

**Best for**: Unstructured or rapidly changing data

### Why We're Learning PostgreSQL

| Feature | PostgreSQL |
|---------|------------|
| Free & Open Source | ✓ |
| Industry Standard | ✓ |
| Feature Rich | ✓ |
| Great for Learning | ✓ |
| Scales Well | ✓ |
| AI/ML Support (pgvector) | ✓ |

---

## Introduction to PostgreSQL

### What is PostgreSQL?

PostgreSQL (often called "Postgres") is a powerful, free, open-source relational database. It's used by companies like Apple, Instagram, Spotify, and Netflix.

### Key Concepts

| Term | Meaning | Example |
|------|---------|---------|
| Database | Container for all your data | `my_store_db` |
| Table | Collection of related data | `customers`, `products` |
| Row | Single record | One customer's information |
| Column | Attribute of data | `name`, `email`, `age` |
| Primary Key | Unique identifier for each row | `id` |
| Foreign Key | Link to another table | `customer_id` in orders |

### Visual Structure

```
PostgreSQL Server
└── Database: my_store_db
    ├── Table: customers
    │   ├── id (Primary Key)
    │   ├── name
    │   ├── email
    │   └── phone
    ├── Table: products
    │   ├── id (Primary Key)
    │   ├── name
    │   ├── price
    │   └── stock
    └── Table: orders
        ├── id (Primary Key)
        ├── customer_id (Foreign Key → customers)
        ├── product_id (Foreign Key → products)
        └── order_date
```

---

## Installing PostgreSQL

### Windows Installation

1. **Download PostgreSQL**
   - Go to [postgresql.org/download/windows](https://www.postgresql.org/download/windows/)
   - Download the installer (EDB installer recommended)

2. **Run the Installer**
   - Choose installation directory (default is fine)
   - Select all components (PostgreSQL Server, pgAdmin 4, Command Line Tools)
   - Set data directory (default is fine)
   - **Set a password for the `postgres` user** - Remember this!
   - Port: 5432 (default)
   - Locale: Default locale

3. **Verify Installation**
   - Open Command Prompt
   - Type: `psql --version`
   - You should see: `psql (PostgreSQL) 16.x`

### macOS Installation

**Using Homebrew (Recommended):**

```bash
# Install PostgreSQL
brew install postgresql@16

# Start PostgreSQL service
brew services start postgresql@16

# Verify installation
psql --version
```

### Linux (Ubuntu/Debian) Installation

```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify installation
psql --version
```

### Connecting to PostgreSQL

**Using Command Line (psql):**

```bash
# Windows (after adding to PATH)
psql -U postgres

# macOS/Linux
sudo -u postgres psql

# You'll see the PostgreSQL prompt:
# postgres=#
```

**Using pgAdmin (GUI):**

1. Open pgAdmin 4 (installed with PostgreSQL on Windows)
2. Right-click "Servers" → "Create" → "Server"
3. Name: "Local PostgreSQL"
4. Connection tab:
   - Host: localhost
   - Port: 5432
   - Username: postgres
   - Password: (your password)
5. Click "Save"

### Creating Your First Database

```sql
-- In psql or pgAdmin query tool:

-- Create a new database
CREATE DATABASE tutorial_db;

-- Connect to it
\c tutorial_db

-- You're now in your new database!
```

---

## SQL Basics

### What is SQL?

**SQL** (Structured Query Language) is the language used to communicate with databases. It's pronounced "S-Q-L" or "sequel".

### SQL Statement Types

| Type | Purpose | Examples |
|------|---------|----------|
| DDL (Data Definition) | Create/modify structure | CREATE, ALTER, DROP |
| DML (Data Manipulation) | Work with data | SELECT, INSERT, UPDATE, DELETE |
| DCL (Data Control) | Permissions | GRANT, REVOKE |

### Your First SQL Commands

```sql
-- Comments start with two dashes

-- Create a simple table
CREATE TABLE greetings (
    id SERIAL PRIMARY KEY,
    message TEXT
);

-- Insert data
INSERT INTO greetings (message) VALUES ('Hello, World!');
INSERT INTO greetings (message) VALUES ('Welcome to SQL!');

-- Read data
SELECT * FROM greetings;

-- Result:
--  id |      message
-- ----+------------------
--   1 | Hello, World!
--   2 | Welcome to SQL!
```

---

## Creating Tables

### Table Syntax

```sql
CREATE TABLE table_name (
    column1 datatype constraints,
    column2 datatype constraints,
    ...
);
```

### Common Data Types

| Type | Description | Example |
|------|-------------|---------|
| `INTEGER` | Whole numbers | 1, 42, -100 |
| `SERIAL` | Auto-incrementing integer | Auto-generated IDs |
| `DECIMAL(p,s)` | Precise decimals | 19.99 |
| `VARCHAR(n)` | Variable text (max n chars) | 'Hello' |
| `TEXT` | Unlimited text | Long descriptions |
| `BOOLEAN` | True/False | TRUE, FALSE |
| `DATE` | Date only | '2024-01-15' |
| `TIMESTAMP` | Date and time | '2024-01-15 14:30:00' |

### Example: Creating a Customers Table

```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Let's break this down:
- `id SERIAL PRIMARY KEY` - Auto-incrementing unique identifier
- `VARCHAR(50) NOT NULL` - Text up to 50 chars, required
- `UNIQUE` - No duplicate values allowed
- `DEFAULT CURRENT_TIMESTAMP` - Auto-fill with current time

### Example: Creating a Products Table

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0),
    category VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## CRUD Operations

CRUD stands for **C**reate, **R**ead, **U**pdate, **D**elete - the four basic operations you can do with data.

### CREATE (INSERT)

```sql
-- Insert a single record
INSERT INTO customers (first_name, last_name, email, phone)
VALUES ('John', 'Doe', 'john@example.com', '555-1234');

-- Insert multiple records
INSERT INTO customers (first_name, last_name, email)
VALUES
    ('Alice', 'Smith', 'alice@example.com'),
    ('Bob', 'Johnson', 'bob@example.com'),
    ('Carol', 'Williams', 'carol@example.com');

-- Insert into products
INSERT INTO products (name, description, price, stock_quantity, category)
VALUES
    ('Laptop', 'High-performance laptop', 999.99, 50, 'Electronics'),
    ('Mouse', 'Wireless mouse', 29.99, 200, 'Electronics'),
    ('Notebook', 'A5 lined notebook', 4.99, 500, 'Stationery');
```

### READ (SELECT)

```sql
-- Select all columns
SELECT * FROM customers;

-- Select specific columns
SELECT first_name, last_name, email FROM customers;

-- Filter with WHERE
SELECT * FROM products WHERE category = 'Electronics';

-- Multiple conditions
SELECT * FROM products
WHERE price < 100 AND stock_quantity > 0;

-- Sorting
SELECT * FROM products ORDER BY price DESC;

-- Limiting results
SELECT * FROM products ORDER BY price DESC LIMIT 5;

-- Pattern matching with LIKE
SELECT * FROM customers WHERE email LIKE '%@gmail.com';

-- Aggregation
SELECT COUNT(*) FROM products;  -- Count all products
SELECT AVG(price) FROM products;  -- Average price
SELECT SUM(stock_quantity) FROM products;  -- Total stock
SELECT category, COUNT(*) FROM products GROUP BY category;
```

### UPDATE

```sql
-- Update a single record
UPDATE customers
SET phone = '555-9999'
WHERE email = 'john@example.com';

-- Update multiple fields
UPDATE products
SET price = 899.99, stock_quantity = 45
WHERE name = 'Laptop';

-- Update based on condition
UPDATE products
SET is_active = FALSE
WHERE stock_quantity = 0;

-- IMPORTANT: Always use WHERE to avoid updating all rows!
```

### DELETE

```sql
-- Delete specific record
DELETE FROM customers WHERE email = 'bob@example.com';

-- Delete based on condition
DELETE FROM products WHERE is_active = FALSE;

-- CAUTION: Delete all records (rarely used!)
DELETE FROM products;  -- Deletes EVERYTHING!

-- IMPORTANT: Always use WHERE to avoid deleting all rows!
```

---

## Constraints

Constraints are rules that enforce data integrity.

### Common Constraints

| Constraint | Purpose | Example |
|------------|---------|---------|
| `PRIMARY KEY` | Unique identifier for each row | `id SERIAL PRIMARY KEY` |
| `NOT NULL` | Value required | `name VARCHAR(50) NOT NULL` |
| `UNIQUE` | No duplicate values | `email VARCHAR(100) UNIQUE` |
| `CHECK` | Custom validation | `CHECK (price >= 0)` |
| `DEFAULT` | Default value if not provided | `DEFAULT TRUE` |
| `FOREIGN KEY` | Link to another table | `REFERENCES customers(id)` |

### Example with Constraints

```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(10) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    salary DECIMAL(10, 2) CHECK (salary >= 0),
    department VARCHAR(50) DEFAULT 'Unassigned',
    hire_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,

    -- Table-level constraint
    CONSTRAINT valid_email CHECK (email LIKE '%@%.%')
);
```

---

## Relationships and Foreign Keys

### What is a Relationship?

Tables can be connected through **relationships**. For example:
- One customer can have many orders (One-to-Many)
- One order can have many products (Many-to-Many)

### Foreign Keys

A **foreign key** is a column that references the primary key of another table.

```sql
-- Customers table (parent)
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Orders table (child) - references customers
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2),

    -- Foreign key constraint
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

### Why Foreign Keys Matter

```sql
-- This will FAIL if customer_id 999 doesn't exist
INSERT INTO orders (customer_id, total_amount) VALUES (999, 50.00);
-- Error: violates foreign key constraint

-- This will SUCCEED
INSERT INTO customers (name, email) VALUES ('Alice', 'alice@example.com');
-- Returns id = 1

INSERT INTO orders (customer_id, total_amount) VALUES (1, 50.00);
-- Success! Order linked to Alice
```

### Relationship Types

#### One-to-Many (Most Common)

One customer → Many orders

```
Customer (id: 1, name: Alice)
    ├── Order (id: 1, customer_id: 1)
    ├── Order (id: 2, customer_id: 1)
    └── Order (id: 3, customer_id: 1)
```

#### Many-to-Many

Many orders ↔ Many products (through a junction table)

```sql
-- Products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Order Items (junction table)
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL
);
```

---

## JOIN Operations

### What is a JOIN?

A **JOIN** combines rows from two or more tables based on a related column.

### Visual Explanation

```
Customers                    Orders
┌────┬─────────┐            ┌────┬─────────────┬────────┐
│ id │  name   │            │ id │ customer_id │ total  │
├────┼─────────┤            ├────┼─────────────┼────────┤
│ 1  │ Alice   │◄───────────│ 1  │     1       │ 99.99  │
│ 2  │ Bob     │◄───────────│ 2  │     2       │ 49.99  │
│ 3  │ Carol   │            │ 3  │     1       │ 149.99 │
└────┴─────────┘            └────┴─────────────┴────────┘

INNER JOIN Result:
┌─────────┬────────┐
│  name   │ total  │
├─────────┼────────┤
│ Alice   │ 99.99  │
│ Bob     │ 49.99  │
│ Alice   │ 149.99 │
└─────────┴────────┘
```

### Types of JOINs

#### INNER JOIN

Returns only rows with matches in both tables.

```sql
SELECT customers.name, orders.total_amount
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id;
```

#### LEFT JOIN

Returns all rows from the left table, matched rows from right (NULL if no match).

```sql
SELECT customers.name, orders.total_amount
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id;

-- Result includes Carol with NULL total (she has no orders)
```

#### RIGHT JOIN

Returns all rows from the right table, matched rows from left.

```sql
SELECT customers.name, orders.total_amount
FROM customers
RIGHT JOIN orders ON customers.id = orders.customer_id;
```

#### FULL OUTER JOIN

Returns all rows from both tables.

```sql
SELECT customers.name, orders.total_amount
FROM customers
FULL OUTER JOIN orders ON customers.id = orders.customer_id;
```

### JOIN with Multiple Tables

```sql
SELECT
    c.name AS customer_name,
    o.id AS order_id,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE c.name = 'Alice';
```

---

## Practice: Products and Orders System

Let's build a complete e-commerce database system!

### Step 1: Create the Database

```sql
-- Create database
CREATE DATABASE ecommerce_db;

-- Connect to it
\c ecommerce_db
```

### Step 2: Create Tables

```sql
-- Customers table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    country VARCHAR(50) DEFAULT 'USA',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0),
    category VARCHAR(50),
    sku VARCHAR(50) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending'
        CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(10, 2) DEFAULT 0,
    shipping_address TEXT,
    notes TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT
);

-- Order Items (junction table for Orders and Products)
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
);

-- Create indexes for better performance
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_products_category ON products(category);
```

### Step 3: Insert Sample Data

```sql
-- Insert customers
INSERT INTO customers (first_name, last_name, email, phone, city, country) VALUES
    ('John', 'Doe', 'john.doe@email.com', '555-0101', 'New York', 'USA'),
    ('Alice', 'Smith', 'alice.smith@email.com', '555-0102', 'Los Angeles', 'USA'),
    ('Bob', 'Johnson', 'bob.j@email.com', '555-0103', 'Chicago', 'USA'),
    ('Carol', 'Williams', 'carol.w@email.com', '555-0104', 'Houston', 'USA'),
    ('David', 'Brown', 'david.b@email.com', '555-0105', 'Phoenix', 'USA');

-- Insert products
INSERT INTO products (name, description, price, stock_quantity, category, sku) VALUES
    ('Laptop Pro', 'High-performance laptop with 16GB RAM', 1299.99, 50, 'Electronics', 'ELEC-001'),
    ('Wireless Mouse', 'Ergonomic wireless mouse', 29.99, 200, 'Electronics', 'ELEC-002'),
    ('USB-C Hub', '7-in-1 USB-C hub', 49.99, 150, 'Electronics', 'ELEC-003'),
    ('Mechanical Keyboard', 'RGB mechanical keyboard', 89.99, 100, 'Electronics', 'ELEC-004'),
    ('Monitor 27"', '27-inch 4K monitor', 399.99, 75, 'Electronics', 'ELEC-005'),
    ('Desk Lamp', 'LED desk lamp with adjustable brightness', 34.99, 120, 'Home Office', 'HOME-001'),
    ('Office Chair', 'Ergonomic office chair', 249.99, 40, 'Home Office', 'HOME-002'),
    ('Notebook Set', 'Pack of 5 A5 notebooks', 12.99, 300, 'Stationery', 'STAT-001'),
    ('Pen Set', 'Premium ballpoint pen set', 8.99, 500, 'Stationery', 'STAT-002'),
    ('Headphones', 'Noise-cancelling wireless headphones', 199.99, 80, 'Electronics', 'ELEC-006');

-- Insert orders
INSERT INTO orders (customer_id, status, shipping_address, notes) VALUES
    (1, 'delivered', '123 Main St, New York, NY 10001', 'Leave at door'),
    (1, 'shipped', '123 Main St, New York, NY 10001', NULL),
    (2, 'processing', '456 Oak Ave, Los Angeles, CA 90001', 'Call before delivery'),
    (2, 'delivered', '456 Oak Ave, Los Angeles, CA 90001', NULL),
    (3, 'pending', '789 Pine Rd, Chicago, IL 60601', NULL),
    (1, 'delivered', '123 Main St, New York, NY 10001', NULL),
    (4, 'shipped', '321 Elm St, Houston, TX 77001', NULL),
    (2, 'delivered', '456 Oak Ave, Los Angeles, CA 90001', 'Gift wrap'),
    (5, 'processing', '654 Maple Dr, Phoenix, AZ 85001', NULL),
    (3, 'delivered', '789 Pine Rd, Chicago, IL 60601', NULL);

-- Insert order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    -- Order 1 (John)
    (1, 1, 1, 1299.99),  -- Laptop Pro
    (1, 2, 2, 29.99),     -- 2x Wireless Mouse
    -- Order 2 (John)
    (2, 4, 1, 89.99),     -- Mechanical Keyboard
    (2, 3, 1, 49.99),     -- USB-C Hub
    -- Order 3 (Alice)
    (3, 5, 1, 399.99),    -- Monitor
    (3, 6, 1, 34.99),     -- Desk Lamp
    -- Order 4 (Alice)
    (4, 10, 1, 199.99),   -- Headphones
    -- Order 5 (Bob)
    (5, 8, 3, 12.99),     -- 3x Notebook Set
    (5, 9, 2, 8.99),      -- 2x Pen Set
    -- Order 6 (John)
    (6, 2, 1, 29.99),     -- Wireless Mouse
    -- Order 7 (Carol)
    (7, 7, 1, 249.99),    -- Office Chair
    (7, 6, 2, 34.99),     -- 2x Desk Lamp
    -- Order 8 (Alice)
    (8, 1, 1, 1299.99),   -- Laptop Pro
    -- Order 9 (David)
    (9, 4, 1, 89.99),     -- Mechanical Keyboard
    (9, 2, 1, 29.99),     -- Wireless Mouse
    -- Order 10 (Bob)
    (10, 3, 2, 49.99),    -- 2x USB-C Hub
    (10, 9, 5, 8.99);     -- 5x Pen Set

-- Update order totals
UPDATE orders o
SET total_amount = (
    SELECT COALESCE(SUM(subtotal), 0)
    FROM order_items oi
    WHERE oi.order_id = o.id
);
```

### Step 4: Practice Queries

#### Basic Queries

```sql
-- Get all products
SELECT * FROM products;

-- Get all products in Electronics category
SELECT name, price, stock_quantity
FROM products
WHERE category = 'Electronics'
ORDER BY price DESC;

-- Get products low on stock (less than 50)
SELECT name, stock_quantity
FROM products
WHERE stock_quantity < 50
ORDER BY stock_quantity;

-- Get all customers from New York
SELECT first_name, last_name, email
FROM customers
WHERE city = 'New York';
```

#### JOIN Queries

```sql
-- Get all orders with customer names
SELECT
    o.id AS order_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    o.order_date,
    o.status,
    o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
ORDER BY o.order_date DESC;

-- Get order details with products
SELECT
    o.id AS order_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price,
    oi.subtotal
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
ORDER BY o.id, p.name;
```

#### Advanced Query: Last 10 Orders for a Product

```sql
-- Get the last 10 orders containing a specific product (e.g., Laptop Pro)
SELECT
    p.id AS product_id,
    p.name AS product_name,
    p.price AS current_price,
    p.category,
    o.id AS order_id,
    o.order_date,
    o.status AS order_status,
    c.first_name || ' ' || c.last_name AS customer_name,
    oi.quantity,
    oi.unit_price AS price_at_purchase,
    oi.subtotal
FROM products p
INNER JOIN order_items oi ON p.id = oi.product_id
INNER JOIN orders o ON oi.order_id = o.id
INNER JOIN customers c ON o.customer_id = c.id
WHERE p.name = 'Laptop Pro'
ORDER BY o.order_date DESC
LIMIT 10;

-- Create a reusable function for this
CREATE OR REPLACE FUNCTION get_last_orders_for_product(
    product_name_param VARCHAR,
    limit_count INTEGER DEFAULT 10
)
RETURNS TABLE (
    product_id INTEGER,
    product_name VARCHAR,
    current_price DECIMAL,
    category VARCHAR,
    order_id INTEGER,
    order_date TIMESTAMP,
    order_status VARCHAR,
    customer_name TEXT,
    quantity INTEGER,
    price_at_purchase DECIMAL,
    subtotal DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.name,
        p.price,
        p.category,
        o.id,
        o.order_date,
        o.status,
        c.first_name || ' ' || c.last_name,
        oi.quantity,
        oi.unit_price,
        oi.subtotal
    FROM products p
    INNER JOIN order_items oi ON p.id = oi.product_id
    INNER JOIN orders o ON oi.order_id = o.id
    INNER JOIN customers c ON o.customer_id = c.id
    WHERE p.name ILIKE product_name_param
    ORDER BY o.order_date DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- Use the function
SELECT * FROM get_last_orders_for_product('Laptop Pro', 10);
SELECT * FROM get_last_orders_for_product('Wireless Mouse', 5);
```

#### Aggregation Queries

```sql
-- Total sales by product
SELECT
    p.name AS product_name,
    SUM(oi.quantity) AS total_sold,
    SUM(oi.subtotal) AS total_revenue
FROM products p
INNER JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id, p.name
ORDER BY total_revenue DESC;

-- Total sales by customer
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(DISTINCT o.id) AS order_count,
    SUM(o.total_amount) AS total_spent
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.first_name, c.last_name
ORDER BY total_spent DESC;

-- Sales by category
SELECT
    p.category,
    COUNT(DISTINCT oi.id) AS items_sold,
    SUM(oi.subtotal) AS category_revenue
FROM products p
INNER JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;

-- Orders by status
SELECT
    status,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_value
FROM orders
GROUP BY status
ORDER BY order_count DESC;
```

---

## Summary

Congratulations! You've learned:

- **What databases are** and why we need them
- **PostgreSQL installation** and setup
- **SQL basics** - the language of databases
- **Table creation** with appropriate data types
- **CRUD operations** - Create, Read, Update, Delete
- **Constraints** for data integrity
- **Relationships** and foreign keys
- **JOIN operations** to combine data from multiple tables
- **A complete e-commerce schema** with Products and Orders

### Key Takeaways

1. **Always use PRIMARY KEYs** - Every table needs a unique identifier
2. **Define relationships with FOREIGN KEYs** - Maintain data integrity
3. **Use appropriate constraints** - Prevent bad data at the database level
4. **Index frequently queried columns** - Improve performance
5. **Write clear, readable SQL** - Use aliases and proper formatting

### Next Steps

1. Practice more complex queries
2. Explore PostgreSQL's advanced features (views, triggers, stored procedures)
3. Move on to [Chapter 3: REST APIs](../REST-API/chapter-3-rest-api.md) to learn how to build APIs that interact with your database

---

[← Previous: Chapter 1 - Python](../Python/chapter-1-python-basics.md) | [Back to Main Guide](../README.md) | [Next: Chapter 3 - REST APIs →](../REST-API/chapter-3-rest-api.md)
