-- Database 101 - Example 2: Inserting Sample Data
-- Run this after creating the tables

-- Clear existing data (if any)
TRUNCATE order_items, orders, products, customers RESTART IDENTITY CASCADE;

-- Insert customers
INSERT INTO customers (first_name, last_name, email, phone, city, country) VALUES
    ('John', 'Doe', 'john.doe@email.com', '555-0101', 'New York', 'USA'),
    ('Alice', 'Smith', 'alice.smith@email.com', '555-0102', 'Los Angeles', 'USA'),
    ('Bob', 'Johnson', 'bob.j@email.com', '555-0103', 'Chicago', 'USA'),
    ('Carol', 'Williams', 'carol.w@email.com', '555-0104', 'Houston', 'USA'),
    ('David', 'Brown', 'david.b@email.com', '555-0105', 'Phoenix', 'USA'),
    ('Emma', 'Davis', 'emma.d@email.com', '555-0106', 'Philadelphia', 'USA'),
    ('Frank', 'Miller', 'frank.m@email.com', '555-0107', 'San Antonio', 'USA'),
    ('Grace', 'Wilson', 'grace.w@email.com', '555-0108', 'San Diego', 'USA');

-- Insert products
INSERT INTO products (name, description, price, stock_quantity, category, sku) VALUES
    ('Laptop Pro', 'High-performance laptop with 16GB RAM and 512GB SSD', 1299.99, 50, 'Electronics', 'ELEC-001'),
    ('Wireless Mouse', 'Ergonomic wireless mouse with silent clicks', 29.99, 200, 'Electronics', 'ELEC-002'),
    ('USB-C Hub', '7-in-1 USB-C hub with HDMI, USB-A, SD card reader', 49.99, 150, 'Electronics', 'ELEC-003'),
    ('Mechanical Keyboard', 'RGB mechanical keyboard with Cherry MX switches', 89.99, 100, 'Electronics', 'ELEC-004'),
    ('Monitor 27"', '27-inch 4K UHD monitor with HDR support', 399.99, 75, 'Electronics', 'ELEC-005'),
    ('Desk Lamp', 'LED desk lamp with adjustable brightness and color temperature', 34.99, 120, 'Home Office', 'HOME-001'),
    ('Office Chair', 'Ergonomic office chair with lumbar support', 249.99, 40, 'Home Office', 'HOME-002'),
    ('Notebook Set', 'Pack of 5 A5 lined notebooks, 100 pages each', 12.99, 300, 'Stationery', 'STAT-001'),
    ('Pen Set', 'Premium ballpoint pen set with 12 colors', 8.99, 500, 'Stationery', 'STAT-002'),
    ('Headphones', 'Noise-cancelling wireless headphones with 30h battery', 199.99, 80, 'Electronics', 'ELEC-006'),
    ('Webcam HD', '1080p HD webcam with built-in microphone', 79.99, 90, 'Electronics', 'ELEC-007'),
    ('Standing Desk', 'Electric height-adjustable standing desk', 499.99, 25, 'Home Office', 'HOME-003'),
    ('Monitor Stand', 'Adjustable monitor stand with USB ports', 44.99, 100, 'Home Office', 'HOME-004'),
    ('Desk Organizer', 'Bamboo desk organizer with multiple compartments', 24.99, 150, 'Home Office', 'HOME-005'),
    ('Wireless Charger', 'Fast wireless charger for phones', 19.99, 200, 'Electronics', 'ELEC-008');

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
    (3, 'delivered', '789 Pine Rd, Chicago, IL 60601', NULL),
    (6, 'shipped', '111 First Ave, Philadelphia, PA 19101', 'Fragile items'),
    (7, 'delivered', '222 Second St, San Antonio, TX 78201', NULL),
    (8, 'pending', '333 Third Blvd, San Diego, CA 92101', NULL),
    (4, 'delivered', '321 Elm St, Houston, TX 77001', NULL),
    (5, 'delivered', '654 Maple Dr, Phoenix, AZ 85001', NULL);

-- Insert order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    -- Order 1 (John) - Laptop setup
    (1, 1, 1, 1299.99),  -- Laptop Pro
    (1, 2, 2, 29.99),     -- 2x Wireless Mouse
    (1, 3, 1, 49.99),     -- USB-C Hub
    -- Order 2 (John) - Accessories
    (2, 4, 1, 89.99),     -- Mechanical Keyboard
    (2, 11, 1, 79.99),    -- Webcam HD
    -- Order 3 (Alice) - Monitor setup
    (3, 5, 2, 399.99),    -- 2x Monitor
    (3, 13, 2, 44.99),    -- 2x Monitor Stand
    -- Order 4 (Alice) - Audio
    (4, 10, 1, 199.99),   -- Headphones
    -- Order 5 (Bob) - Stationery
    (5, 8, 3, 12.99),     -- 3x Notebook Set
    (5, 9, 2, 8.99),      -- 2x Pen Set
    -- Order 6 (John) - Mouse replacement
    (6, 2, 1, 29.99),     -- Wireless Mouse
    -- Order 7 (Carol) - Office setup
    (7, 7, 1, 249.99),    -- Office Chair
    (7, 6, 2, 34.99),     -- 2x Desk Lamp
    (7, 14, 1, 24.99),    -- Desk Organizer
    -- Order 8 (Alice) - New laptop
    (8, 1, 1, 1299.99),   -- Laptop Pro
    (8, 15, 1, 19.99),    -- Wireless Charger
    -- Order 9 (David) - Keyboard setup
    (9, 4, 1, 89.99),     -- Mechanical Keyboard
    (9, 2, 1, 29.99),     -- Wireless Mouse
    -- Order 10 (Bob) - More stationery
    (10, 3, 2, 49.99),    -- 2x USB-C Hub
    (10, 9, 5, 8.99),     -- 5x Pen Set
    -- Order 11 (Emma) - Home office
    (11, 12, 1, 499.99),  -- Standing Desk
    (11, 7, 1, 249.99),   -- Office Chair
    -- Order 12 (Frank) - Electronics
    (12, 1, 1, 1299.99),  -- Laptop Pro
    (12, 10, 1, 199.99),  -- Headphones
    -- Order 13 (Grace) - Basic setup
    (13, 2, 1, 29.99),    -- Wireless Mouse
    (13, 4, 1, 89.99),    -- Mechanical Keyboard
    -- Order 14 (Carol) - More items
    (14, 5, 1, 399.99),   -- Monitor
    (14, 11, 1, 79.99),   -- Webcam HD
    -- Order 15 (David) - Complete setup
    (15, 1, 1, 1299.99),  -- Laptop Pro
    (15, 5, 1, 399.99),   -- Monitor
    (15, 4, 1, 89.99),    -- Mechanical Keyboard
    (15, 2, 1, 29.99);    -- Wireless Mouse

-- Update order totals
UPDATE orders o
SET total_amount = (
    SELECT COALESCE(SUM(subtotal), 0)
    FROM order_items oi
    WHERE oi.order_id = o.id
);

-- Verify data was inserted
SELECT 'Customers' as table_name, COUNT(*) as record_count FROM customers
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders
UNION ALL
SELECT 'Order Items', COUNT(*) FROM order_items;
