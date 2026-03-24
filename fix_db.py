import mysql.connector

try:
    conn = mysql.connector.connect(
        host='caboose.proxy.rlwy.net', 
        user='root', 
        password='zMOsIeHUtEPgdySxShWTmjpkZPxQfIoj', 
        port=32298, 
        database='railway'
    )
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE menu ADD COLUMN stock INT DEFAULT 50;")
    conn.commit()
    print("Fixed! Stock column officially added to Railway!")
except Exception as e:
    print("Error:", e)
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
