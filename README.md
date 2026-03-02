# Vegetable Shop Management System

A full-stack web application built to digitize and streamline day-to-day operations of a local vegetable shop — replacing manual record-keeping with a clean, modern interface.

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| Database | MySQL |
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Fonts | Google Fonts (Playfair Display, DM Sans) |
| BI / Analytics | Power BI (via MySQL connector) |

---

##  Features

- ** Inventory Management** — Add new items, track stock levels with live status indicators (Good / Low / Critical)
- ** Dynamic Pricing** — Update cost and selling prices with real-time profit margin calculator
- ** Cart & Billing** — Add items to cart, remove items, auto-calculate totals and generate bills
- ** Bill History** — Browse complete billing history with expandable item-level breakdowns
- ** Power BI Ready** — MySQL backend connects directly to Power BI for revenue, stock, and margin dashboards
- ** Toast Notifications** — Real-time success and error feedback on every action

---

##  Project Structure

```
shop_management_new/
│
├── app.py                  # Flask backend — all API routes
├── sales.csv               # Sample data (optional)
│
└── templates/
    ├── index.html          # Dashboard with live stats
    ├── manage_stock.html   # Add items & restock inventory
    ├── edit_prices.html    # Edit cost & selling prices
    ├── cart_billing.html   # Cart management & bill generation
    └── view_bills.html     # Bill history viewer
```

---

##  Database Schema

Run the following SQL to set up the database:

```sql
CREATE DATABASE veg_shop;
USE veg_shop;

CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    unit VARCHAR(10) NOT NULL,
    original_price DECIMAL(10,2) NOT NULL,
    selling_price DECIMAL(10,2) NOT NULL
);

CREATE TABLE stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    quantity DECIMAL(10,3) NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id)
);

CREATE TABLE cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    quantity DECIMAL(10,3) NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items(id)
);

CREATE TABLE bills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    items_sold TEXT NOT NULL
);
```

---

##  Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/vegetable-shop-management.git
cd vegetable-shop-management/shop_management_new
```

### 2. Install dependencies
```bash
pip install flask mysql-connector-python
```

### 3. Configure the database
Update `app.py` with your MySQL credentials:
```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_PASSWORD_HERE",
    "database": "veg_shop"
}
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://localhost:5000
```

---

##  API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard |
| GET | `/get_items` | Fetch all items |
| GET | `/get_stock` | Fetch current stock levels |
| GET | `/get_cart` | Fetch current cart |
| GET | `/get_bills` | Fetch all bills |
| POST | `/add_item` | Add new item to inventory |
| POST | `/update_stock` | Restock an existing item |
| POST | `/add_to_cart` | Add item to cart |
| POST | `/generate_bill` | Generate bill & deduct stock |
| PUT | `/edit_prices` | Update item prices |
| DELETE | `/remove_from_cart` | Remove item from cart |

---

##  Power BI Integration

Connect Power BI directly to the MySQL database:

1. Open Power BI Desktop → **Get Data** → **MySQL database**
2. Server: `localhost` | Database: `veg_shop`
3. Enter your MySQL credentials
4. Select tables: `items`, `stock`, `bills`
5. Build dashboards for revenue trends, stock levels, and profit margins

---

## 🐛 Bugs Fixed

- Resolved infinite recursion in database error handler
- Fixed JSON serialization failures for MySQL `Decimal` and `datetime` types
- Corrected missing `unit` field in stored bill data causing broken bill history
- Added missing `DELETE /remove_from_cart` API endpoint
- Fixed unstyled and broken form inputs across all pages

---

## 🎨 UI Highlights

- Earthy green and amber color palette with cream background
- Playfair Display + DM Sans typography pairing
- Live stock status badges (Good / Low / Critical)
- Real-time profit margin display in price editor
- Collapsible bill cards with item-level detail
- Toast notifications for all user actions
- Responsive layout for mobile and desktop

---
