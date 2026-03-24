import mysql.connector

conn = mysql.connector.connect(
    host='caboose.proxy.rlwy.net',
    user='root',
    password='zMOsIeHUtEPgdySxShWTmjpkZPxQfIoj',
    port=32298,
    database='railway'
)
cursor = conn.cursor()

# Restore exact image_url values from database.sql - no changes, just restoring
restore = {
    'Vada Pav':           'images/vada_pav.png',
    'Poha':               'images/poha.png',
    'Veg Sandwich':       'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=500&q=80',
    'Veg Burger':         'https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=500&q=80',
    'Paneer Burger':      'https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?auto=format&fit=crop&w=500&q=80',
    'Veg Noodles':        'https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=500&q=80',
    'Veg Fried Rice':     'images/veg_fried_rice.jpg',
    'Paneer Roll':        'images/paneer_roll.jpg',
    'Masala Dosa':        'images/masala_dosa.jpg',
    'Idli Sambar':        'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=500&q=80',
    'Samosa':             'images/samosa.jpg',
    'Pav Bhaji':          'images/pav_bhaji.jpg',
    'Misal Pav':          'images/misal_pav.png',
    'Veg Pizza':          'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=500&q=80',
    'French Fries':       'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=500&q=80',
    'Cheese Sandwich':    'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=500&q=80',
    'Aloo Paratha':       'images/aloo_paratha.jpg',
    'Paneer Tikka':       'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?auto=format&fit=crop&w=500&q=80',
    'Veg Momos':          'https://images.unsplash.com/photo-1625220194771-7ebdea0b70b4?auto=format&fit=crop&w=500&q=80',
    'Chicken Burger':     'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=80',
    'Chicken Roll':       'images/chicken_roll.png',
    'Chicken Noodles':    'images/chinese_noodles.png',
    'Chicken Fried Rice': 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=500&q=80',
    'Chicken Momos':      'https://images.unsplash.com/photo-1625220194771-7ebdea0b70b4?auto=format&fit=crop&w=500&q=80',
    'Chicken Sandwich':   'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=500&q=80',
    'Chicken Biryani':    'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=500&q=80',
    'Egg Fried Rice':     'https://images.unsplash.com/photo-1623595110708-76b2afad3d76?auto=format&fit=crop&w=500&q=80',
    'Egg Noodles':        'https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=500&q=80',
    'Egg Bhurji Pav':     'https://images.unsplash.com/photo-1600192348575-b46d0a7a3712?auto=format&fit=crop&w=500&q=80',
    'Egg Omelette':       'images/egg_omelette.jpg',
    'Chicken Pizza':      'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=500&q=80',
    'Chicken Shawarma':   'https://images.unsplash.com/photo-1528736235302-52922df5c122?auto=format&fit=crop&w=500&q=80',
    'Cutting Chai':       'images/cutting_chai.png',
    'Cold Coffee':        'images/cold_cofee.jpg',
    'Mango Milkshake':    'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=500&q=80',
    'Lassi':              'images/lassi.jpg',
    'Soft Drink':         'https://images.unsplash.com/photo-1573480813647-552e9b7b5394?auto=format&fit=crop&w=500&q=80',
    'Chocolate Milkshake':'https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=500&q=80',
    'Paneer Thali':       'images/paneer_thali.png',
    'Chicken Wings':      'https://images.unsplash.com/photo-1567620832903-9fc1debc209f?auto=format&fit=crop&w=500&q=80',
    'Egg Maggi':          'https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?auto=format&fit=crop&w=500&q=80',
    'Lemon Tea':          'https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=500&q=80',
    'Buttermilk':         'images/butter_milk.jpg',
    'Oreo Shake':         'https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=500&q=80',
    'Medu Vada':          'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=500&q=80',
    'Uttapam':            'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=500&q=80',
    'Gobi Manchurian':    'https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=500&q=80',
    'Spring Rolls':       'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=500&q=80',
    'Bread Omelette':     'images/bread_omelette.jpg',
    'Gulab Jamun (2pcs)': 'images/gulab_jamun.png',
    'Vanilla Ice Cream':  'https://images.unsplash.com/photo-1570197788417-0e82375c9371?auto=format&fit=crop&w=500&q=80',
}

for name, url in restore.items():
    cursor.execute("UPDATE menu SET image_url = %s WHERE item_name = %s", (url, name))

conn.commit()
print("Done! All image URLs restored to original database.sql values.")
cursor.close()
conn.close()
