-- Get all users
SELECT * FROM users;

-- Get all products
SELECT * FROM products;

-- Get all orders
SELECT * FROM orders;

-- Get product count
SELECT COUNT(*) as total_products FROM products;

-- Get average product price
SELECT AVG(price) as average_price FROM products;

-- Get most expensive product
SELECT * FROM products ORDER BY price DESC LIMIT 1;

-- Get cheapest products
SELECT * FROM products ORDER BY price ASC LIMIT 5;

-- Get completed orders
SELECT * FROM orders WHERE status = 'completed' ORDER BY order_date DESC;

-- Get orders with user details
SELECT o.order_id, u.username, o.total_price, o.status, o.order_date 
FROM orders o
JOIN users u ON o.user_id = u.user_id
ORDER BY o.order_date DESC;

-- Get top 5 most ordered products
SELECT p.product_id, p.product_name, COUNT(oi.order_id) as order_count, SUM(oi.quantity) as total_quantity
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
ORDER BY order_count DESC
LIMIT 5;

-- Get user purchase history
SELECT u.user_id, u.username, COUNT(o.order_id) as total_orders, SUM(o.total_price) as total_spent
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.username
ORDER BY total_spent DESC;

-- Get low stock products
SELECT product_id, product_name, stock_quantity
FROM products
WHERE stock_quantity < 10
ORDER BY stock_quantity ASC;

-- Get products never ordered
SELECT p.*
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.order_id IS NULL;

-- Get total revenue
SELECT SUM(total_price) as total_revenue FROM orders WHERE status = 'completed';

-- Get revenue by month
SELECT MONTH(order_date) as month, YEAR(order_date) as year, SUM(total_price) as monthly_revenue
FROM orders
WHERE status = 'completed'
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY year DESC, month DESC;

-- Get cart details
SELECT c.cart_id, u.username, c.status, COUNT(ci.cart_item_id) as item_count
FROM carts c
JOIN users u ON c.user_id = u.user_id
LEFT JOIN cart_items ci ON c.cart_id = ci.cart_id
GROUP BY c.cart_id, u.username, c.status;
