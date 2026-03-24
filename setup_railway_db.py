import mysql.connector

conn = mysql.connector.connect(
    host='caboose.proxy.rlwy.net',
    user='root',
    password='zMOsIeHUtEPgdySxShWTmjpkZPxQfIoj',
    port=32298,
    database='railway'
)
cursor = conn.cursor()

statements = [
    # 1. customers
    """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        customer_type VARCHAR(50) NOT NULL DEFAULT 'Student',
        phone_no VARCHAR(20),
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """,

    # 2. admin
    """
    CREATE TABLE IF NOT EXISTS admin (
        admin_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone_no VARCHAR(20),
        password VARCHAR(255) NOT NULL,
        address TEXT
    )
    """,

    # 3. orders
    """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        total_amount DECIMAL(10,2) NOT NULL,
        order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(50) DEFAULT 'pending',
        prep_time INT DEFAULT 10,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    """,

    # 4. order_items
    """
    CREATE TABLE IF NOT EXISTS order_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        item_id INT,
        quantity INT NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (item_id) REFERENCES menu(item_id)
    )
    """,

    # 5. settings
    """
    CREATE TABLE IF NOT EXISTS settings (
        setting_key VARCHAR(50) PRIMARY KEY,
        setting_value VARCHAR(255)
    )
    """,

    # 6. default admin user
    """
    INSERT IGNORE INTO admin (admin_id, name, email, phone_no, password, address)
    VALUES (1, 'Admin', 'admin@canteen.com', '1234567890', 'admin123', 'Canteen Office')
    """,

    # 7. default settings
    """
    INSERT IGNORE INTO settings (setting_key, setting_value)
    VALUES ('opening_time', '09:00'), ('closing_time', '18:00')
    """,

    # 8. ensure stock column exists on menu (safe if already added)
    # (skip duplicate — already added via fix_db.py earlier)
]

for sql in statements:
    try:
        cursor.execute(sql.strip())
        conn.commit()
    except Exception as e:
        print(f"⚠  Skipped: {e}")

print("✅ Railway database fully set up!")
cursor.close()
conn.close()
