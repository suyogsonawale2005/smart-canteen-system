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
    cursor.execute("SELECT * FROM menu WHERE stock >= 0")
    print("Success")
except Exception as e:
    print("Error:", e)
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
