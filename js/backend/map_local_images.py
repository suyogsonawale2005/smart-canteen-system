import mysql.connector

try:
    conn = mysql.connector.connect(host='127.0.0.1', user='root', password='', port=3307, database='canteen_db')
    cursor = conn.cursor()

    mappings = {
        'Veg Fried Rice': 'images/veg_fried_rice.png',
        'Paneer Roll': 'images/paneer_roll.png',
        'Masala Dosa': 'images/masala_dosa.png',
        'Samosa': 'images/samosa.png',
        'Aloo Paratha': 'images/aloo_paratha.png',
        'Veg Momos': 'images/veg_momos.png',
        'Chicken Roll': 'images/chicken_roll.png',
        'Chicken Fried Rice': 'images/chicken_fried_rice.png',
        'Egg Bhurji Pav': 'images/egg_bhurji_pav.png',
        'Bread Omelette': 'images/bread_omelette.png',
        'Chicken Shawarma': 'images/chicken_shawarma.png',
        'Cold Coffee': 'images/cold_coffee.png',
        'Lassi': 'images/lassi.png',
        'Gobi Manchurian': 'images/gobi_manchurian.png',
        'Gulab Jamun (2pcs)': 'images/gulab_jamun.png',
        'Egg Omelette': 'images/egg_omelette.png',
        'Mango Milkshake': 'images/mango_milkshake.png',
        'Cutting Chai': 'images/cutting_chai.png',
        'Soft Drink': 'images/soft_drink.png',
        'Chicken Roll ' : 'images/chicken_roll.png'
    }

    for name, path in mappings.items():
        cursor.execute("UPDATE menu SET image_url = %s WHERE item_name = %s", (path, name))

    conn.commit()
    print("Database mapping updated to local images folder!")
    cursor.close()
    conn.close()
except Exception as e:
    print(e)
