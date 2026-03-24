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

    mappings = {
        'Aloo Paratha': 'images/aloo_paratha.jpg',
        'Bread Omelette': 'images/bread_omelette.jpg',
        'Buttermilk': 'images/butter_milk.jpg',
        'Chicken Noodles': 'images/chinese_noodles.jpg',
        'Cold Coffee': 'images/cold_cofee.jpg',
        'Cutting Chai': 'images/cutting_chai.png',
        'Egg Omelette': 'images/egg_omelette.jpg',
        'Lassi': 'images/lassi.jpg',
        'Masala Dosa': 'images/masala_dosa.jpg',
        'Misal Pav': 'images/misal_pav.png',
        'Paneer Roll': 'images/paneer_roll.jpg',
        'Paneer Thali': 'images/paneer_thali.png',
        'Pav Bhaji': 'images/pav_bhaji.jpg',
        'Poha': 'images/poha.png',
        'Samosa': 'images/samosa.jpg',
        'Vada Pav': 'images/vada_pav.png',
        'Veg Fried Rice': 'images/veg_fried_rice.jpg',
        'Gulab Jamun(2pcs)' :'images/gulab_jamun.png',
        'Poha ' : 'images/poha.png',
        'Chocolate Milk ' : 'images/chocolate_milk.png',
        'Chicken Roll ' : 'images/chicken_roll.png'
    }

    for name, path in mappings.items():
        cursor.execute("UPDATE menu SET image_url = %s WHERE item_name = %s", (path, name))

    conn.commit()
    print("Database mapping perfectly updated to your exact .jpg images list!")
    cursor.close()
    conn.close()
except Exception as e:
    print("Database Error:", e)
