# Smart Canteen Management System

A modern web application that completely digitalizes the food ordering process of a college canteen. Students can browse the menu, place orders, and track their food in real time — while the Admin can manage orders, update the menu, and view sales reports from a dedicated dashboard.

---

## Tech Stack

| Layer | Technology Used |
|-------|----------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python (Flask Framework) |
| Database | MySQL |
| Payment | Razorpay Payment Gateway |

---

## How the Project Works — Full Flow

---

### 1. Student Registration

When a new student visits the website, they are taken to the **Sign Up** page. They fill in their name, email, phone number, and password. This information is securely sent to the backend server, which saves it into the **Customers** table in the database. Once registered, the student can log in.

---

### 2. Student Login

On the **Login** page, the student enters their email and password. The backend checks the database to verify if these credentials match an existing account. If they do, the student is granted access and redirected to their personal **Dashboard**.

---

### 3. Browsing the Menu

Once logged in, the student lands on the **Dashboard** which displays the full canteen menu. The menu is fetched live from the database every time the page loads — so any item added, edited, or removed by the Admin is instantly reflected for students.

Students can filter items by:
- **Category** (Breakfast, Snacks, Chinese, Beverages, etc.)
- **Type** (Veg or Non-Veg)
- **Search** by name

---

### 4. Adding Items to Cart & Placing Order

The student clicks the **+** button on any food item to add it to their cart. The cart shows a running total. When ready, the student clicks **Place Order**, which opens a **Secure Checkout** screen where they choose a payment method:

- **Cash at Counter** — Order is placed directly. Student pays physically when collecting the food.
- **UPI** — Razorpay's payment gateway opens. The student completes the UPI payment online. Only after successful payment is the order officially placed.

Once the order is placed, it is saved in the database with a status of **Pending**, and the student sees an animated success screen with their Order ID.

---

### 5. Student Order Tracking

In the **My Orders** section of the dashboard, the student can see all their previous and current orders. The order status is fetched live from the database each time, so it always reflects the latest update from the Admin. The statuses are:

- **Pending** — Order received, waiting for the canteen to start preparing
- **Preparing** — Canteen is actively cooking the food
- **Ready** — Food is ready for pickup at the counter
- **Delivered** — Food has been handed to the student
- **Cancelled** — Order was cancelled

If an order is still **Pending** or **Preparing**, the student has the option to **Cancel** it. Once cancelled, the status is permanently locked — neither the student nor the Admin can change it.

---

### 6. Admin Login

The Admin logs in through a separate **Admin Login** page using their registered email and password. The backend verifies these against the **Admin** table in the database. On success, the Admin is redirected to the **Admin Dashboard**.

> Admin accounts cannot be created from the website — they can only be added directly in the database by the system owner. This prevents unauthorized people from gaining admin access.

---

### 7. Admin — Managing Orders

The Admin Dashboard shows a live table of **all orders** placed by all students, including the student's name, items ordered, total price, and current status. The Admin can change the status of any order using a dropdown menu (Pending → Preparing → Ready → Delivered).

The moment the Admin updates a status, the change is saved in the database and the student's tracking view reflects the new status.

**Important rule:** If a student has **cancelled** an order, the Admin's dropdown is permanently disabled for that order — the Admin cannot modify a cancelled order in any way.

---

### 8. Admin — Menu Management

The Admin can fully manage the canteen menu from the dashboard:

- **Add** a new food item with name, price, type (Veg/Non-Veg), category, and image
- **Edit** an existing item to update its details
- **Delete** an item to remove it from the student menu
- **Toggle availability** — Mark an item as Out of Stock or bring it back

When an item is deleted, it is not permanently erased from the database. Instead, it is hidden from students while keeping past order records safe and intact. This ensures that old orders which included that item are never corrupted.

---

### 9. Admin — Sales Report

The Admin can view a **Sales Report** with three time filters:

- **Daily** — Shows all delivered orders placed today, with the total revenue earned today
- **Weekly** — Shows all delivered orders from the current week (Monday to today), broken down day by day
- **Monthly** — Shows all delivered orders from the current month, broken down day by day

The report displays a **bar chart** for visual understanding and a **detailed table** with order counts and revenue. Only **Delivered** orders are counted toward revenue — pending, preparing, and cancelled orders are excluded.

---

### 10. Canteen Operating Hours

The Admin can set the canteen's **Opening** and **Closing** time from the dashboard. If a student tries to place an order outside these hours, they are informed that the canteen is currently closed and orders are blocked automatically.

---

## Database Overview

The database has 6 main tables:

| Table | What it stores |
|-------|---------------|
| **customers** | All registered student accounts |
| **admin** | Admin login credentials |
| **menu** | All food items available in the canteen |
| **orders** | Every order placed by students |
| **order_items** | The individual food items within each order |
| **settings** | Canteen operating hours |

### How the tables connect

- Each **student** can place multiple **orders**
- Each **order** contains one or more **order_items**
- Each **order_item** links back to a specific item in the **menu**

---

## Security Highlights

- Admin signup is completely disabled from the website — only database-level creation is allowed
- Students cannot access the Admin Dashboard — they are automatically redirected to the login page
- Cancelled orders are permanently locked from modification by anyone
- Menu deletions are safe — historical orders are never lost or broken

---

## Payment Flow Summary

When a student pays via UPI, the system creates a secure payment session through Razorpay. The student scans the QR or enters their UPI ID and completes the transaction. Only after Razorpay confirms the payment does the system officially record the order. Cash payments skip this step entirely and are confirmed immediately at checkout.
