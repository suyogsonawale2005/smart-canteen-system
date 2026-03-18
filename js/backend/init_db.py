import mysql.connector
import os

# Configuration (Matches your local XAMPP/MySQL Setup)
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'port': 3307  # Your specific MySQL port
}

def setup_database():
    try:
        # 1. Connect and Create Database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS canteen_db")
        cursor.execute("USE canteen_db")
        print("✔ Database 'canteen_db' is ready.")

        # 2. Execute SQL File for Schema
        sql_file_path = os.path.join(os.path.dirname(__file__), 'database.sql')
        if os.path.exists(sql_file_path):
            with open(sql_file_path, 'r') as f:
                sql_script = f.read()
            
            for statement in sql_script.split(';'):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except mysql.connector.Error as e:
                        # Ignore errors for inserts that might already exist
                        if e.errno != 1061 and e.errno != 1060: # index or column exists
                            pass
            conn.commit()
            print("✔ Schema and seed data applied from database.sql.")
        
        # 3. Dynamic Column Updates (Idempotent)
        # Ensure 'stock' in menu
        cursor.execute("SHOW COLUMNS FROM menu LIKE 'stock'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE menu ADD COLUMN stock INT DEFAULT 50")
            print("✔ Added 'stock' column to menu.")

        # Ensure 'status' and 'prep_time' in orders
        cursor.execute("SHOW COLUMNS FROM orders LIKE 'status'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE orders ADD COLUMN status VARCHAR(50) DEFAULT 'pending'")
            print("✔ Added 'status' column to orders.")

        cursor.execute("SHOW COLUMNS FROM orders LIKE 'prep_time'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE orders ADD COLUMN prep_time INT DEFAULT 10")
            print("✔ Added 'prep_time' column to orders.")

        # Ensure 'phone_no' in admin
        cursor.execute("SHOW COLUMNS FROM admin LIKE 'phone_no'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE admin ADD COLUMN phone_no VARCHAR(20) AFTER email")
            print("✔ Added 'phone_no' column to admin.")

        # 4. Image Fallback Standardization
        cursor.execute("""
            UPDATE menu 
            SET image_url = CASE 
                WHEN category LIKE '%Beverage%' THEN 'https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=500&q=80'
                WHEN category LIKE '%Snack%' THEN 'https://images.unsplash.com/photo-1626074353765-517a681e40be?auto=format&fit=crop&w=500&q=80'
                WHEN category LIKE '%Breakfast%' THEN 'https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?auto=format&fit=crop&w=500&q=80'
                WHEN category LIKE '%Meal%' THEN 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=500&q=80'
                WHEN category LIKE '%Burger%' OR category LIKE '%Pizza%' THEN 'https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=500&q=80'
                ELSE 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=500&q=80'
            END
            WHERE image_url IS NULL OR image_url = '' OR image_url = 'null' OR image_url LIKE '%loremflickr%';
        """)
        
        conn.commit()
        print("✔ Database maintenance and updates complete.")

    except Exception as e:
        print(f"✖ Error occurred: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
