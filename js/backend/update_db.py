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
    
    # Check if phone_no column exists
    cursor.execute("SHOW COLUMNS FROM admin LIKE 'phone_no'")
    result = cursor.fetchone()
    if not result:
        cursor.execute("ALTER TABLE admin ADD COLUMN phone_no VARCHAR(20) AFTER email;")
        conn.commit()
        print("Successfully added phone_no to admin table.")
    else:
        print("phone_no already exists in admin table.")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
