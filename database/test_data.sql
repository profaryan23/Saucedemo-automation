CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    role VARCHAR(50) DEFAULT 'customer',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100),
    description TEXT,
    stock_quantity INT DEFAULT 0,
    reorder_level INT DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS carts (
    cart_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS cart_items (
    cart_item_id INT PRIMARY KEY AUTO_INCREMENT,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    FOREIGN KEY (cart_id) REFERENCES carts(cart_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO users (username, password, email, role, status) VALUES
('standard_user', 'secret_sauce_hash', 'standard@saucedemo.com', 'customer', 'active'),
('locked_out_user', 'secret_sauce_hash', 'locked@saucedemo.com', 'customer', 'locked'),
('problem_user', 'secret_sauce_hash', 'problem@saucedemo.com', 'customer', 'active'),
('performance_glitch_user', 'secret_sauce_hash', 'performance@saucedemo.com', 'customer', 'active'),
('admin_user', 'admin_hash', 'admin@saucedemo.com', 'admin', 'active');

INSERT INTO products (product_name, price, category, description, stock_quantity, reorder_level) VALUES
('Sauce Labs Backpack', 29.99, 'Backpacks', 'Carry your everyday essentials with this sleek backpack', 50, 10),
('Sauce Labs Bike Light', 9.99, 'Bike Lights', 'A sturdy and reliable bike light for your commute', 100, 20),
('Sauce Labs Bolt T-Shirt', 15.99, 'T-Shirts', 'High-quality and comfortable t-shirt with awesome graphics', 75, 15),
('Sauce Labs Fleece Jacket', 49.99, 'Jackets', 'Perfect for outdoor activities and staying warm', 30, 10),
('Sauce Labs Onesie', 7.99, 'Clothing', 'Cozy and fun onesie pajamas', 60, 15),
('Test.allTheThings() T-Shirt (Red)', 15.99, 'T-Shirts', 'Testing themed t-shirt in red color', 45, 10),
('Sauce Labs Lab Coat', 24.99, 'Lab Gear', 'Official Sauce Labs lab coat', 25, 8);

INSERT INTO orders (user_id, total_price, status) VALUES
(1, 39.98, 'completed'),
(1, 75.97, 'completed'),
(2, 29.99, 'pending'),
(3, 59.98, 'completed'),
(4, 15.99, 'processing');

INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1, 1, 1),
(1, 2, 1),
(2, 3, 2),
(2, 4, 1),
(3, 1, 1),
(4, 5, 2),
(4, 6, 1),
(5, 3, 1);

INSERT INTO carts (user_id, status) VALUES
(1, 'active'),
(3, 'active'),
(4, 'abandoned');

INSERT INTO cart_items (cart_id, product_id, quantity) VALUES
(1, 1, 1),
(1, 3, 2),
(2, 2, 1),
(3, 4, 1),
(3, 6, 2);
