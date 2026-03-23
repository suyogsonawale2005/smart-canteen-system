import os
from flask import Flask, request, jsonify, g
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes so frontend can connect

# Database configuration dynamically pulled from Render Environment or fallback to Local
db_config = {
    'host': os.getenv('MYSQLHOST', os.getenv('DB_HOST', 'localhost')),
    'user': os.getenv('MYSQLUSER', os.getenv('DB_USER', 'root')),
    'password': os.getenv('MYSQLPASSWORD', os.getenv('DB_PASS', '')),
    'database': os.getenv('MYSQLDATABASE', os.getenv('DB_NAME', 'canteen_db')),
    'port': int(os.getenv('MYSQLPORT', os.getenv('DB_PORT', 3307)))
}

@app.route('/')
def home():
    return jsonify({
        "status": "Smart Canteen API is Running Perfectly!",
        "message": "Render is online. Please setup DB_HOST environment variables to activate full database connection."
    }), 200

# Global error string to bubble up to API
last_db_error = ""

def get_db_connection():
    global last_db_error
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        last_db_error = str(err)
        print(f"Error connecting to MySQL Database: {err}")
        return None

# ==========================================
# 1. Student Signup API
# ==========================================
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    customer_type = data.get('customer_type', 'Student') # Defaulting to Student
    phone_no = data.get('phone_no')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"error": "Missing required fields (name, email or password)"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": f"Database connection failed: {last_db_error}"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO customers (name, customer_type, phone_no, email, password) VALUES (%s, %s, %s, %s, %s)", 
            (name, customer_type, phone_no, email, password)
        )
        conn.commit()
        return jsonify({"message": "Signup successful", "customer_id": cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        if err.errno == 1062: # Duplicate entry error code for MySQL
            return jsonify({"error": "Email already exists"}), 409
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# ==========================================
# 2. Student Login API
# ==========================================
@app.route('/api/login/student', methods=['POST'])
def student_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"error": "Missing email or password"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": f"Database connection failed: {last_db_error}"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT customer_id, name, customer_type, email, phone_no FROM customers WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "Login successful", "user": user}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# ==========================================
# 3. Admin Login & Signup API
# ==========================================
@app.route('/api/signup/admin', methods=['POST'])
def admin_signup():
    # SECURITY LOCKDOWN: Prevent students from hitting the API to create unauthorized admin accounts
    return jsonify({"error": "Admin signup is strictly disabled for security. Please create admin accounts manually inside MySQL Workbench using your Railway DB credentials."}), 403

@app.route('/api/login/admin', methods=['POST'])
def admin_login():
    data = request.json
    admin_id_or_email = data.get('email') # Assuming frontend might pass email in 'email' field
    password = data.get('password')

    if not all([admin_id_or_email, password]):
        return jsonify({"error": "Missing credentials"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": f"Database connection failed: {last_db_error}"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT admin_id, name, email, phone_no, address FROM admin WHERE (email = %s OR admin_id = %s) AND password = %s", (admin_id_or_email, admin_id_or_email, password))
        admin = cursor.fetchone()
        if admin:
            return jsonify({"message": "Admin login successful", "admin": admin}), 200
        else:
            return jsonify({"error": "Invalid admin credentials"}), 401
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# ==========================================
# 4. Menu API
# ==========================================
@app.route('/api/menu', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_menu():
    if request.method == 'GET':
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": f"Database connection failed: {last_db_error}"}), 500

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM menu WHERE stock >= 0")
            menu_items = cursor.fetchall()
            for item in menu_items:
                item['price'] = float(item['price'])
            return jsonify({"menu": menu_items}), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()

    elif request.method == 'POST':
        data = request.json
        name = data.get('item_name') or data.get('name')
        price = data.get('price')
        type = data.get('type')
        category = data.get('category')
        image_url = data.get('image_url') or data.get('img')

        if not all([name, price]):
            return jsonify({"error": "Missing required fields (name, price)"}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({"error": f"Database connection failed: {last_db_error}"}), 500

        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO menu (item_name, price, type, category, image_url) VALUES (%s, %s, %s, %s, %s)",
                (name, price, type, category, image_url)
            )
            conn.commit()
            return jsonify({"message": "Menu item added successfully", "item_id": cursor.lastrowid}), 201
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()

@app.route('/api/menu/<int:item_id>', methods=['PUT', 'DELETE'])
def manage_menu_item(item_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": f"Database connection failed: {last_db_error}"}), 500
    
    cursor = conn.cursor()
    if request.method == 'PUT':
        data = request.json
        name = data.get('item_name') or data.get('name')
        price = data.get('price')
        type = data.get('type')
        category = data.get('category')
        image_url = data.get('image_url') or data.get('img')
        
        try:
            cursor.execute(
                "UPDATE menu SET item_name=%s, price=%s, type=%s, category=%s, image_url=%s WHERE item_id=%s",
                (name, price, type, category, image_url, item_id)
            )
            conn.commit()
            return jsonify({"message": "Menu item updated successfully"}), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()
            
    elif request.method == 'DELETE':
        try:
            # Soft delete instead of physical delete to preserve foreign key constraints for historical receipts
            cursor.execute("UPDATE menu SET stock = -1 WHERE item_id=%s", (item_id,))
            conn.commit()
            return jsonify({"message": "Menu item deleted successfully"}), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()

import razorpay

# Initialize the Razorpay client with TEST Keys (Safe for Localhost)
razorpay_client = razorpay.Client(auth=("rzp_test_SUDIa8UBhPN8rS", "vp3M75Yrxxah9xZNdfGpScG5"))

# ==========================================
# 5. Order API & Payment Gateway
# ==========================================
@app.route('/api/razorpay/create_order', methods=['POST'])
def create_razorpay_order():
    try:
        data = request.json
        amount_in_rupees = data.get('amount')
        
        # Razorpay processes money in 'paisa' (smallest denomination)
        # So multiply your Rupee total by 100
        amount_in_paisa = int(amount_in_rupees * 100)
        
        order_data = {
            "amount": amount_in_paisa,
            "currency": "INR",
            "payment_capture": 1 # Auto capture payment
        }
        
        # This talks to Razorpay's servers
        payment_order = razorpay_client.order.create(data=order_data)
        
        return jsonify({
            "status": "success",
            "razorpay_order_id": payment_order['id'],
            "amount": payment_order['amount'],
            "currency": payment_order['currency']
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/orders', methods=['POST'])
def place_order():
    data = request.json
    customer_id = data.get('customer_id')
    items = data.get('items') # Expected format: [{"item_id": 1, "quantity": 2, "price": 40.0}]
    
    if not items or not customer_id:
        return jsonify({"error": "Missing customer_id or items"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": f"Database connection failed: {last_db_error}"}), 500

    cursor = conn.cursor()
    try:
        prep_time = data.get('prep_time', 10)
        status = data.get('status', 'pending')
        # Calculate total amount
        total_amount = sum(float(item['quantity']) * float(item['price']) for item in items)
        
        # Insert into orders table
        cursor.execute("INSERT INTO orders (customer_id, total_amount, status, prep_time) VALUES (%s, %s, %s, %s)", 
                       (customer_id, total_amount, status, prep_time))
        order_id = cursor.lastrowid
        
        # Insert into order_items table
        for item in items:
            cursor.execute("INSERT INTO order_items (order_id, item_id, quantity, price) VALUES (%s, %s, %s, %s)",
                           (order_id, item['item_id'], item['quantity'], item['price']))
        
        conn.commit()
        return jsonify({"message": "Order placed successfully", "order_id": order_id, "total_amount": total_amount, "prep_time": prep_time, "status": status}), 201
    except mysql.connector.Error as err:
        conn.rollback() # Rollback in case of an error to prevent partial entries
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.json
    new_status = data.get('status')
    if not new_status:
        return jsonify({"error": "Missing status"}), 400
        
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": f"Database connection failed: {last_db_error}"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE orders SET status=%s WHERE order_id=%s", (new_status, order_id))
        conn.commit()
        return jsonify({"message": "Order status updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/orders/user/<int:customer_id>', methods=['GET'])
def get_user_orders(customer_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": f"Database connection failed: {last_db_error}"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT order_id, order_date, total_amount, status, prep_time
            FROM orders
            WHERE customer_id = %s
            ORDER BY order_date DESC
        """, (customer_id,))
        orders = cursor.fetchall()
        
        for order in orders:
            order['total_amount'] = float(order['total_amount'])
            # Append Z to let the frontend know this time is from Railway's UTC clock
            order['order_date'] = str(order['order_date']).replace(' ', 'T') + "Z"
            
            cursor.execute("""
                SELECT oi.quantity, m.item_name as name, m.price
                FROM order_items oi
                JOIN menu m ON oi.item_id = m.item_id
                WHERE oi.order_id = %s
            """, (order['order_id'],))
            items = cursor.fetchall()
            for item in items:
                item['price'] = float(item['price'])
            order['items'] = items
            
        return jsonify({"orders": orders}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/orders', methods=['GET'])
def get_admin_orders():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": f"Database connection failed: {last_db_error}"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        # Fetch all orders with customer details
        cursor.execute("""
            SELECT o.order_id, o.order_date, o.total_amount, o.status, o.prep_time,
                   c.name as customer_name, c.customer_type
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            ORDER BY o.order_date DESC
        """)
        orders = cursor.fetchall()
        
        # Fetch items for each order
        for order in orders:
            order['total_amount'] = float(order['total_amount'])
            order['order_date'] = str(order['order_date'])
            cursor.execute("""
                SELECT oi.quantity, m.item_name, m.price
                FROM order_items oi
                JOIN menu m ON oi.item_id = m.item_id
                WHERE oi.order_id = %s
            """, (order['order_id'],))
            items = cursor.fetchall()
            for item in items:
                item['price'] = float(item['price'])
            order['items'] = items
            
        return jsonify({"orders": orders}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# ==========================================
# 6. Admin Dashboard APIs (Sales Data)
# ==========================================
@app.route('/api/admin/dashboard', methods=['GET'])
def get_dashboard_data():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": f"Database connection failed: {last_db_error}"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        # 1. Overall totals and Today's totals
        cursor.execute("""
            SELECT 
                COUNT(*) AS total_orders, 
                IFNULL(SUM(CASE WHEN status = 'delivered' THEN total_amount ELSE 0 END), 0) AS total_revenue 
            FROM orders
        """)
        overall = cursor.fetchone()
        overall['total_revenue'] = float(overall['total_revenue'])
        
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS total_orders, 
                IFNULL(SUM(CASE WHEN status = 'delivered' THEN total_amount ELSE 0 END), 0) AS total_revenue 
            FROM orders
            WHERE DATE(order_date) = CURDATE()
        """)
        today = cursor.fetchone()
        today['total_revenue'] = float(today['total_revenue'])

        # 2. Daily Sales (last 7 days grouped by date)
        cursor.execute("""
            SELECT 
                DATE(order_date) as date, 
                IFNULL(SUM(CASE WHEN status = 'delivered' THEN total_amount ELSE 0 END), 0) as daily_revenue,
                SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) as total_orders
            FROM orders 
            GROUP BY DATE(order_date) 
            ORDER BY date DESC 
            LIMIT 7
        """)
        daily_sales = cursor.fetchall()
        for d in daily_sales:
            d['daily_revenue'] = float(d['daily_revenue'])
            d['date'] = str(d['date']) # Format date for JSON

        # 3. Weekly Sales (last 4 weeks)
        cursor.execute("""
            SELECT 
                YEARWEEK(order_date) as week, 
                IFNULL(SUM(CASE WHEN status = 'delivered' THEN total_amount ELSE 0 END), 0) as weekly_revenue,
                COUNT(order_id) as total_orders
            FROM orders 
            GROUP BY YEARWEEK(order_date) 
            ORDER BY week DESC 
            LIMIT 4
        """)
        weekly_sales = cursor.fetchall()
        for w in weekly_sales:
            w['weekly_revenue'] = float(w['weekly_revenue'])

        # 4. Monthly Sales (last 12 months)
        cursor.execute("""
            SELECT 
                DATE_FORMAT(order_date, '%Y-%m') as month, 
                IFNULL(SUM(CASE WHEN status = 'delivered' THEN total_amount ELSE 0 END), 0) as monthly_revenue,
                COUNT(order_id) as total_orders
            FROM orders 
            GROUP BY DATE_FORMAT(order_date, '%Y-%m') 
            ORDER BY month DESC 
            LIMIT 12
        """)
        monthly_sales = cursor.fetchall()
        for m in monthly_sales:
            m['monthly_revenue'] = float(m['monthly_revenue'])
            
        return jsonify({
            "overall": overall,
            "today": today,
            "daily_sales": daily_sales,
            "weekly_sales": weekly_sales,
            "monthly_sales": monthly_sales
        }), 200
        
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# ==========================================
# 7. Settings APIs
# ==========================================
@app.route('/api/settings', methods=['GET', 'PUT'])
def manage_settings():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed", "details": last_db_error}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute("SELECT setting_key, setting_value FROM settings")
            rows = cursor.fetchall()
            settings = {row['setting_key']: row['setting_value'] for row in rows}
            return jsonify({"settings": settings}), 200

        elif request.method == 'PUT':
            data = request.json
            if not data or 'settings' not in data:
                return jsonify({"error": "Missing settings payload"}), 400
            
            for k, v in data['settings'].items():
                cursor.execute("""
                    INSERT INTO settings (setting_key, setting_value) VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE setting_value = %s
                """, (k, v, v))
            conn.commit()
            return jsonify({"message": "Settings updated successfully"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
   