import mysql.connector

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'port': 3307,
    'database': 'canteen_db'
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Check if status column exists
    cursor.execute("SHOW COLUMNS FROM orders LIKE 'status'")
    result = cursor.fetchone()
    if not result:
        cursor.execute("ALTER TABLE orders ADD COLUMN status VARCHAR(50) DEFAULT 'pending';")
        conn.commit()
        print("Successfully added status to orders table.")
    else:
        print("status already exists in orders table.")
        
    # Check if prep_time column exists
    cursor.execute("SHOW COLUMNS FROM orders LIKE 'prep_time'")
    result2 = cursor.fetchone()
    if not result2:
        cursor.execute("ALTER TABLE orders ADD COLUMN prep_time INT DEFAULT 10;")
        conn.commit()
        print("Successfully added prep_time to orders table.")
    else:
        print("prep_time already exists in orders table.")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
