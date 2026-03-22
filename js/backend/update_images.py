import mysql.connector

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'port': 3307,
    'database': 'canteen_db'
}

image_updates = {
    'Veg Fried Rice': 'https://images.unsplash.com/photo-1512058564366-18510be2db19?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Paneer Roll': 'https://plus.unsplash.com/premium_photo-1664478311546-3f1fbacacb6f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Masala Dosa': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Samosa': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Aloo Paratha': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Veg Momos': 'https://images.unsplash.com/photo-1625220194771-7ebdea0b70b4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Chicken Roll': 'https://images.unsplash.com/photo-1626776876729-bab4b273343a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Chicken Fried Rice': 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Egg Bhurji Pav': 'https://images.unsplash.com/photo-1600192348575-b46d0a7a3712?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Bread Omelette': 'https://images.unsplash.com/photo-1525351484163-e145d0e9a65c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Chicken Shawarma': 'https://images.unsplash.com/photo-1528736235302-52922df5c122?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Cold Coffee': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Lassi': 'https://images.unsplash.com/photo-1546522368-21d7fdbe06d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Gobi Manchurian': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    'Gulab Jamun (2pcs)': 'https://images.unsplash.com/photo-1589113110260-fe63a6f9589d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
}

def update_images():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        for name, url in image_updates.items():
            cursor.execute("UPDATE menu SET image_url = %s WHERE item_name = %s", (url, name))
            
        conn.commit()
        print("Updated menu images successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    update_images()
