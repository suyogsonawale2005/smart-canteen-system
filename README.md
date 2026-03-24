# Smart Canteen Management System

A full-stack web application that digitizes the entire food ordering process of a college canteen — from student login and menu browsing to order tracking and admin sales reporting.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python (Flask) |
| Database | MySQL |
| Payment | Razorpay Gateway |

---

## Project Structure

```
SCS/
├── index.html              # Student login page
├── signup.html             # Student registration page
├── dashboard.html          # Student menu & order dashboard
├── admin.html              # Admin login page
├── admin-dashboard.html    # Admin control panel
├── images/                 # Food item images
├── css/                    # Stylesheets
├── js/
│   ├── auth.js             # Login / Signup / Logout logic
│   ├── menu.js             # Fetches & renders menu from backend
│   ├── state.js            # Cart, orders, local state management
│   └── backend/
│       ├── app.py          # Flask REST API (main backend)
│       ├── database.sql    # MySQL schema + seed data
│       └── requirements.txt
└── script.js               # Dashboard interactions (cart, orders, payment)
```

---

## System Flow — Frontend to Backend to Database

### 1. Student Registration & Login

**Frontend → Backend → Database**

1. Student opens `index.html` and fills in their Name, Email, and Password.
2. `auth.js` sends a **POST** request to `/api/signup` on the Flask backend.
3. Flask receives the data, validates it, and executes:
   ```sql
   INSERT INTO customers (name, customer_type, phone_no, email, password)
   VALUES (...)
   ```
4. The new student record is saved in the `customers` table in MySQL.
5. For login, `auth.js` sends a **POST** to `/api/login/student`. Flask queries:
   ```sql
   SELECT * FROM customers WHERE email = ? AND password = ?
   ```
6. If found, Flask returns the student's data. The browser saves it in `localStorage` and redirects to `dashboard.html`.

---

### 2. Menu Display

**Database → Backend → Frontend**

1. When `dashboard.html` loads, `menu.js` sends a **GET** request to `/api/menu`.
2. Flask executes:
   ```sql
   SELECT * FROM menu WHERE stock >= 0
   ```
   (Items with `stock = -1` are soft-deleted and hidden from students.)
3. Flask returns a JSON list of all menu items (name, price, type, category, image).
4. `menu.js` renders each item as a food card on the screen with filters (Veg/Non-Veg, Category).

---

### 3. Cart & Order Placement

**Frontend → Backend → Database**

1. Student clicks the **`+`** button on a food card — `state.js` adds the item to the in-memory cart.
2. Student clicks **Place Order** → a payment modal appears.
3. Student selects **Cash at Counter** or **UPI**:
   - **Cash:** `script.js` directly calls `finalizeCanteenOrder()`.
   - **UPI:** `script.js` first calls `/api/razorpay/create_order` to get a Razorpay payment session. After payment success, it calls `finalizeCanteenOrder()`.
4. `finalizeCanteenOrder()` sends a **POST** to `/api/orders` with:
   ```json
   { "customer_id": 5, "items": [{ "item_id": 1, "quantity": 2, "price": 20 }] }
   ```
5. Flask calculates the total, then inserts into two tables:
   ```sql
   INSERT INTO orders (customer_id, total_amount, status) VALUES (...)
   INSERT INTO order_items (order_id, item_id, quantity, price) VALUES (...)
   ```
6. A success animation plays. The student can now track their order.

---

### 4. Student Order Tracking

**Database → Backend → Frontend (Live)**

1. In `dashboard.html`, the Student clicks **My Orders**.
2. `script.js` sends a **GET** to `/api/orders/user/<customer_id>`.
3. Flask queries the live database:
   ```sql
   SELECT o.order_id, o.status, o.total_amount, o.order_date,
          m.item_name, oi.quantity, m.price
   FROM orders o
   JOIN order_items oi ON o.order_id = oi.order_id
   JOIN menu m ON oi.item_id = m.item_id
   WHERE o.customer_id = ?
   ORDER BY o.order_date DESC
   ```
4. Orders are displayed with real-time status: **Pending → Preparing → Ready → Delivered**.
5. If an order is still **Pending** or **Preparing**, the student can **Cancel** it. Cancellation sends a **PUT** to `/api/orders/<id>/status` with `{ "status": "cancelled" }`.

---

### 5. Admin Login

**Frontend → Backend → Database**

1. Admin opens `admin.html` and enters their Email and Password.
2. `auth.js` sends a **POST** to `/api/login/admin`.
3. Flask queries:
   ```sql
   SELECT * FROM admin WHERE email = ? AND password = ?
   ```
4. If valid, the browser saves `canteen_is_admin = true` in `localStorage` and redirects to `admin-dashboard.html`.

---

### 6. Admin Order Management

**Database → Backend → Frontend**

1. `admin-dashboard.html` calls **GET** `/api/admin/orders`.
2. Flask fetches all orders joined with customer names:
   ```sql
   SELECT o.*, c.name AS customer_name
   FROM orders o
   JOIN customers c ON o.customer_id = c.customer_id
   ORDER BY o.order_date DESC
   ```
3. Admin sees a table of all orders with a **status dropdown** per order.
4. When Admin changes the status:
   - If the order is **Cancelled** by the student, the dropdown is **disabled** — Admin cannot modify it.
   - Otherwise, Admin selects a new status (Preparing / Ready / Delivered).
   - `admin-dashboard.html` sends a **PUT** to `/api/orders/<id>/status`.
   - Flask executes:
     ```sql
     UPDATE orders SET status = ? WHERE order_id = ?
     ```
5. The student's tracking view instantly reflects the new status on next refresh.

---

### 7. Admin Menu Management

**Frontend → Backend → Database**

Admin can perform full **CRUD** on the menu:

| Action | HTTP Method | API Endpoint | SQL |
|--------|-------------|--------------|-----|
| Add item | POST | `/api/menu` | `INSERT INTO menu (...)` |
| Edit item | PUT | `/api/menu/<id>` | `UPDATE menu SET ... WHERE item_id = ?` |
| Delete item | DELETE | `/api/menu/<id>` | `UPDATE menu SET stock = -1 WHERE item_id = ?` |
| Toggle stock | PUT | `/api/menu/<id>` | `UPDATE menu SET stock = ? WHERE item_id = ?` |

> **Note:** Delete is a **soft delete** — the item's `stock` is set to `-1` instead of physically removing the row. This preserves historical order records (foreign key integrity) while hiding the item from students.

---

### 8. Admin Sales Report

**Database → Backend → Frontend**

1. Admin clicks the **Sales Report** tab and selects a filter (Daily / Weekly / Monthly).
2. `admin-dashboard.html` calls **GET** `/api/admin/dashboard`.
3. Flask runs three separate SQL queries:
   - **Daily** — orders delivered **today**
   - **Weekly** — orders delivered **this current week**
   - **Monthly** — orders delivered **this current month**
   ```sql
   -- Example: Daily
   SELECT DATE(order_date) as date,
          SUM(CASE WHEN status='delivered' THEN total_amount ELSE 0 END) as revenue,
          SUM(CASE WHEN status='delivered' THEN 1 ELSE 0 END) as total_orders
   FROM orders
   WHERE DATE(order_date) = CURDATE()
   ```
4. Results are displayed as a **bar chart** and a **detailed table** with totals.
5. Only **delivered** orders count toward revenue — pending, cancelled, and preparing orders are excluded.

---

## Database Schema

```
customers       → stores student accounts
admin           → stores admin accounts
menu            → stores all food items (soft-deleted items have stock = -1)
orders          → one row per order placed by a student
order_items     → line items for each order (links order ↔ menu)
settings        → canteen operating hours (opening & closing time)
```

### Relationships

```
customers ──< orders ──< order_items >── menu
```

---

## Security Design

- **Admin signup is disabled** via the API — new admins can only be created directly in the database.
- **Admin portal** is protected: students cannot access `admin-dashboard.html` without `canteen_is_admin = true` in localStorage.
- **Cancelled orders** are locked — neither the student nor the admin can change the status once cancelled.
- **Soft delete** on menu items prevents data corruption of historical orders.

---

## Payment Flow (Razorpay)

```
Student → selects UPI
       → Frontend calls /api/razorpay/create_order
       → Backend creates a Razorpay order (gets an order_id from Razorpay)
       → Frontend opens Razorpay payment popup
       → Student completes payment
       → On success, Frontend calls /api/orders to save the order in DB
```

Cash payments skip Razorpay entirely and go directly to `/api/orders`.
