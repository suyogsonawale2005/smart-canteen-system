import mysql.connector

try:
    db_config = {'host': '127.0.0.1', 'user': 'root', 'password': '', 'port': 3307, 'database': 'canteen_db'}
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Create settings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        setting_key VARCHAR(50) PRIMARY KEY,
        setting_value VARCHAR(255)
    )
    """)
    
    # Insert defaults
    cursor.execute("INSERT IGNORE INTO settings (setting_key, setting_value) VALUES ('opening_time', '09:00')")
    cursor.execute("INSERT IGNORE INTO settings (setting_key, setting_value) VALUES ('closing_time', '18:00')")
    
    conn.commit()
    print("Settings table created and initialized.")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
