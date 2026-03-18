import mysql.connector

try:
    db_config = {'host': '127.0.0.1', 'user': 'root', 'password': '', 'port': 3307, 'database': 'canteen_db'}
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Update blank or null images
    query = """
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
    """
    cursor.execute(query)
    conn.commit()
    print("Updated empty/null images in DB.")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
