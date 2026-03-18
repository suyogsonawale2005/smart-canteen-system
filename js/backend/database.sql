CREATE DATABASE IF NOT EXISTS canteen_db;
USE canteen_db;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    customer_type VARCHAR(50) NOT NULL,
    phone_no VARCHAR(20),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_no VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    address TEXT
);

CREATE TABLE IF NOT EXISTS menu (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    type VARCHAR(50),
    category VARCHAR(50),
    image_url VARCHAR(255),
    stock INT DEFAULT 50
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    total_amount DECIMAL(10, 2) NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    prep_time INT DEFAULT 10,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_id INT,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES menu(item_id)
);

CREATE TABLE IF NOT EXISTS settings (
    setting_key VARCHAR(50) PRIMARY KEY,
    setting_value VARCHAR(255)
);

-- Insert a default admin for testing
INSERT IGNORE INTO admin (admin_id, name, email, phone_no, password, address) VALUES (1, 'Admin', 'admin@canteen.com', '1234567890', 'admin123', 'Canteen Office');

-- Insert default settings
INSERT IGNORE INTO settings (setting_key, setting_value) VALUES ('opening_time', '09:00'), ('closing_time', '18:00');

-- Insert all menu items with default stock
INSERT IGNORE INTO menu (item_id, item_name, price, type, category, image_url, stock) VALUES 
(1, 'Vada Pav', 20, 'Veg', 'Snacks', 'images/vada_pav.png', 50),
(2, 'Poha', 30, 'Veg', 'Breakfast', 'images/poha.png', 50),
(3, 'Veg Sandwich', 40, 'Veg', 'Snacks', 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=500&q=80', 50),
(4, 'Veg Burger', 60, 'Veg', 'Burgers', 'https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=500&q=80', 50),
(5, 'Paneer Burger', 80, 'Veg', 'Burgers', 'https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?auto=format&fit=crop&w=500&q=80', 50),
(6, 'Veg Noodles', 70, 'Veg', 'Chinese', 'https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=500&q=80', 50),
(7, 'Veg Fried Rice', 70, 'Veg', 'Chinese', 'https://images.unsplash.com/photo-1623595110708-76b2afad3d76?auto=format&fit=crop&w=500&q=80', 50),
(8, 'Paneer Roll', 60, 'Veg', 'Rolls', 'https://images.unsplash.com/photo-1626776876729-bab4b273343a?auto=format&fit=crop&w=500&q=80', 50),
(9, 'Masala Dosa', 50, 'Veg', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=500&q=80', 50),
(10, 'Idli Sambar', 40, 'Veg', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=500&q=80', 50),
(11, 'Samosa', 15, 'Veg', 'Snacks', 'https://images.unsplash.com/photo-1601050638917-3f048d793fc0?auto=format&fit=crop&w=500&q=80', 50),
(12, 'Pav Bhaji', 80, 'Veg', 'Snacks', 'https://images.unsplash.com/photo-1626132646529-500637532a3d?auto=format&fit=crop&w=500&q=80', 50),
(13, 'Misal Pav', 70, 'Veg', 'Snacks', 'images/misal_pav.png', 50),
(14, 'Veg Pizza', 120, 'Veg', 'Pizza', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=500&q=80', 50),
(15, 'French Fries', 50, 'Veg', 'Snacks', 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=500&q=80', 50),
(16, 'Cheese Sandwich', 50, 'Veg', 'Snacks', 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=500&q=80', 50),
(17, 'Aloo Paratha', 40, 'Veg', 'Breakfast', 'https://images.unsplash.com/photo-1601050638917-3f048d793fc0?auto=format&fit=crop&w=500&q=80', 50),
(18, 'Paneer Tikka', 100, 'Veg', 'Starters', 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?auto=format&fit=crop&w=500&q=80', 50),
(19, 'Veg Momos', 60, 'Veg', 'Starters', 'https://images.unsplash.com/photo-1625220194771-7ebdea0b70b4?auto=format&fit=crop&w=500&q=80', 50),
(20, 'Chicken Burger', 90, 'Non-Veg', 'Burgers', 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=80', 50),
(21, 'Chicken Roll', 80, 'Non-Veg', 'Rolls', 'https://images.unsplash.com/photo-1626776876729-bab4b273343a?auto=format&fit=crop&w=500&q=80', 50),
(22, 'Chicken Noodles', 90, 'Non-Veg', 'Chinese', 'images/chinese_noodles.png', 50),
(23, 'Chicken Fried Rice', 90, 'Non-Veg', 'Chinese', 'https://images.unsplash.com/photo-1623595110708-76b2afad3d76?auto=format&fit=crop&w=500&q=80', 50),
(24, 'Chicken Momos', 80, 'Non-Veg', 'Starters', 'https://images.unsplash.com/photo-1625220194771-7ebdea0b70b4?auto=format&fit=crop&w=500&q=80', 50),
(25, 'Chicken Sandwich', 70, 'Non-Veg', 'Snacks', 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=500&q=80', 50),
(26, 'Chicken Biryani', 150, 'Non-Veg', 'Meals', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=500&q=80', 50),
(27, 'Egg Fried Rice', 80, 'Non-Veg', 'Chinese', 'https://images.unsplash.com/photo-1623595110708-76b2afad3d76?auto=format&fit=crop&w=500&q=80', 50),
(28, 'Egg Noodles', 80, 'Non-Veg', 'Chinese', 'https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=500&q=80', 50),
(29, 'Egg Bhurji Pav', 60, 'Non-Veg', 'Snacks', 'https://images.unsplash.com/photo-1626132646529-500637532a3d?auto=format&fit=crop&w=500&q=80', 50),
(30, 'Egg Omelette', 40, 'Non-Veg', 'Breakfast', 'https://images.unsplash.com/photo-1518491755924-f58620296718?auto=format&fit=crop&w=500&q=80', 50),
(31, 'Chicken Pizza', 150, 'Non-Veg', 'Pizza', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=500&q=80', 50),
(32, 'Chicken Shawarma', 90, 'Non-Veg', 'Rolls', 'https://images.unsplash.com/photo-1616641810313-95827367bc87?auto=format&fit=crop&w=500&q=80', 50),
(33, 'Cutting Chai', 15, 'Veg', 'Beverages', 'images/cutting_chai.png', 50),
(34, 'Cold Coffee', 60, 'Veg', 'Beverages', 'https://images.unsplash.com/photo-1517701604599-bb2952803ead?auto=format&fit=crop&w=500&q=80', 50),
(35, 'Mango Milkshake', 70, 'Veg', 'Beverages', 'https://images.unsplash.com/photo-1546173159-315724a9389a?auto=format&fit=crop&w=500&q=80', 50),
(36, 'Lassi', 50, 'Veg', 'Beverages', 'https://images.unsplash.com/photo-1563227812-0ea4c22e6cc8?auto=format&fit=crop&w=500&q=80', 50),
(37, 'Soft Drink', 40, 'Veg', 'Beverages', 'https://images.unsplash.com/photo-1581006852262-e4307cf6283a?auto=format&fit=crop&w=500&q=80', 50),
(38, 'Chocolate Milkshake', 80, 'Veg', 'Beverages', 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=500&q=80', 50),
(39, 'Paneer Thali', 120, 'Veg', 'Meals', 'images/paneer_thali.png', 50),
(40, 'Chicken Wings', 120, 'Non-Veg', 'Starters', 'https://images.unsplash.com/photo-1567620832903-9fc1debc209f?auto=format&fit=crop&w=500&q=80', 50),
(41, 'Egg Maggi', 50, 'Non-Veg', 'Snacks', 'https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?auto=format&fit=crop&w=500&q=80', 50),
(42, 'Lemon Tea', 25, 'Veg', 'Beverages', 'https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=500&q=80', 50),
(43, 'Buttermilk', 30, 'Veg', 'Beverages', 'https://images.unsplash.com/photo-1626132646529-500637532a3d?auto=format&fit=crop&w=500&q=80', 50),
(44, 'Oreo Shake', 90, 'Veg', 'Beverages', 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=500&q=80', 50),
(45, 'Medu Vada', 45, 'Veg', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=500&q=80', 50),
(46, 'Uttapam', 55, 'Veg', 'South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=500&q=80', 50),
(47, 'Gobi Manchurian', 80, 'Veg', 'Chinese', 'https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=500&q=80', 50),
(48, 'Spring Rolls', 60, 'Veg', 'Snacks', 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=500&q=80', 50),
(49, 'Bread Omelette', 50, 'Non-Veg', 'Breakfast', 'https://images.unsplash.com/photo-1518491755924-f58620296718?auto=format&fit=crop&w=500&q=80', 50),
(50, 'Gulab Jamun (2pcs)', 40, 'Veg', 'Desserts', 'https://images.unsplash.com/photo-1589113110260-fe63a6f9589d?auto=format&fit=crop&w=500&q=80', 50),
(51, 'Vanilla Ice Cream', 40, 'Veg', 'Desserts', 'https://images.unsplash.com/photo-1570197788417-0e82375c9371?auto=format&fit=crop&w=500&q=80', 50);
