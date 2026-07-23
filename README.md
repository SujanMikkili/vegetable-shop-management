# Vegetable Shop Management System

A full-stack inventory and billing system for a vegetable shop — manage
stock, edit prices, build a cart with automatic unit conversion, generate
bills, and review bill history. Built with **FastAPI** on the backend and
a vanilla HTML/CSS/JS frontend.

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, **FastAPI**, Uvicorn |
| Validation | Pydantic |
| Database | MySQL (via `mysql-connector-python`, pooled connections) |
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Fonts | Google Fonts (Playfair Display, DM Sans) |
| BI / Analytics | Power BI (via MySQL connector) |

---

## ✨ Features

- **Inventory management** — add new items with name, unit, cost price,
  and selling price.
- **Stock tracking** — restock existing items; stock levels update live.
- **Price editing** — update original/selling price for any item.
- **Cart & billing** — add items to a cart with automatic gram ⇄
  kilogram conversion, then generate a bill.
- **Automatic stock deduction** — generating a bill deducts sold
  quantities from stock and blocks the sale if stock is insufficient.
- **Bill history** — view all past bills with itemized breakdowns.
- **Auto-generated API docs** — FastAPI's interactive Swagger UI at
  `/docs`, no extra setup required.

---

## 📁 Project Structure

```
vegetable_shop_fastapi/
│
├── main.py               # FastAPI app — all routes (pages + API)
├── database.py            # MySQL connection pool + execute_query() helper
├── models.py               # Pydantic request models
├── schema.sql                # Database schema
├── requirements.txt
│
└── templates/
    ├── index.html           # Dashboard
    ├── manage_stock.html    # Stock management
    ├── edit_prices.html     # Price editing
    ├── cart_billing.html    # Cart & billing
    └── view_bills.html      # Bill history
```

---

## 🏗️ Architecture Notes

- **Request validation** is handled entirely by Pydantic models
  (`models.py`) — every incoming JSON body is validated automatically
  before it reaches a route.
- **Database access** goes through a small MySQL connection pool
  (`mysql.connector.pooling`) in `database.py`, so concurrent requests
  under Uvicorn don't contend for a single connection.
- **Type conversion helpers** (`_to_float`, `_to_iso`) normalize
  `Decimal` and `datetime`/`date` values coming back from MySQL into
  clean JSON-serializable types.
- **Templates** are rendered server-side with Jinja2
  (`Jinja2Templates`), keeping the frontend simple and dependency-free.

---

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure the database
Edit `database.py` and set your MySQL password:
```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_PASSWORD_HERE",
    "database": "veg_shop",
}
```
> ⚠️ **Before pushing to GitHub:** don't commit a real password in
> `database.py`. For a repo-ready setup, swap it for an environment
> variable (`os.environ["DB_PASSWORD"]`) loaded from a `.env` file that's
> listed in `.gitignore`.

### 3. Create the database
```bash
mysql -u root -p < schema.sql
```

### 4. Run the app
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
(or simply `python main.py`)

### 5. Open in browser
```
http://localhost:5000
```

Interactive API docs are available at:
```
http://localhost:5000/docs
```

---

## 🧭 Page Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard |
| GET | `/manage_stock` | Manage stock page |
| GET | `/edit_prices` | Edit prices page |
| GET | `/cart_billing` | Cart & billing page |
| GET | `/view_bills` | View past bills page |

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/get_items` | Fetch all items |
| GET | `/get_stock` | Fetch current stock levels |
| GET | `/get_cart` | Fetch current cart |
| GET | `/get_bills` | Fetch all bills |
| POST | `/add_item` | Add new item to inventory |
| POST | `/update_stock` | Restock an existing item |
| POST | `/add_to_cart` | Add item to cart (auto-converts g ⇄ kg) |
| POST | `/generate_bill` | Generate bill & deduct stock |
| PUT | `/edit_prices` | Update item prices |
| DELETE | `/remove_from_cart` | Remove item from cart |

---

## 🎨 UI

Earthy green/amber palette, Playfair Display + DM Sans typography, live
stock badges, profit margin display, collapsible bill cards, and toast
notifications.

---

## 📌 Known Limitations

- **Single-session model:** the cart uses one hardcoded `SESSION_ID`
  (`"owner_session"`), so it's built for a single-owner shop, not
  multiple concurrent users/carts.
- **No authentication:** all routes are open; there's no login or
  access control layer.
- **No automated tests** yet.

These are intentional scope choices for a portfolio/learning project,
not oversights.# Vegetable Shop Management System

A full-stack inventory and billing system for a vegetable shop — manage
stock, edit prices, build a cart with automatic unit conversion, generate
bills, and review bill history. Built with **FastAPI** on the backend and
a vanilla HTML/CSS/JS frontend.

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, **FastAPI**, Uvicorn |
| Validation | Pydantic |
| Database | MySQL (via `mysql-connector-python`, pooled connections) |
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Fonts | Google Fonts (Playfair Display, DM Sans) |
| BI / Analytics | Power BI (via MySQL connector) |

---

## ✨ Features

- **Inventory management** — add new items with name, unit, cost price,
  and selling price.
- **Stock tracking** — restock existing items; stock levels update live.
- **Price editing** — update original/selling price for any item.
- **Cart & billing** — add items to a cart with automatic gram ⇄
  kilogram conversion, then generate a bill.
- **Automatic stock deduction** — generating a bill deducts sold
  quantities from stock and blocks the sale if stock is insufficient.
- **Bill history** — view all past bills with itemized breakdowns.
- **Auto-generated API docs** — FastAPI's interactive Swagger UI at
  `/docs`, no extra setup required.

---

## 📁 Project Structure

```
vegetable_shop_fastapi/
│
├── main.py               # FastAPI app — all routes (pages + API)
├── database.py            # MySQL connection pool + execute_query() helper
├── models.py               # Pydantic request models
├── schema.sql                # Database schema
├── requirements.txt
│
└── templates/
    ├── index.html           # Dashboard
    ├── manage_stock.html    # Stock management
    ├── edit_prices.html     # Price editing
    ├── cart_billing.html    # Cart & billing
    └── view_bills.html      # Bill history
```

---

## 🏗️ Architecture Notes

- **Request validation** is handled entirely by Pydantic models
  (`models.py`) — every incoming JSON body is validated automatically
  before it reaches a route.
- **Database access** goes through a small MySQL connection pool
  (`mysql.connector.pooling`) in `database.py`, so concurrent requests
  under Uvicorn don't contend for a single connection.
- **Type conversion helpers** (`_to_float`, `_to_iso`) normalize
  `Decimal` and `datetime`/`date` values coming back from MySQL into
  clean JSON-serializable types.
- **Templates** are rendered server-side with Jinja2
  (`Jinja2Templates`), keeping the frontend simple and dependency-free.

---

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure the database
Edit `database.py` and set your MySQL password:
```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_PASSWORD_HERE",
    "database": "veg_shop",
}
```
> ⚠️ **Before pushing to GitHub:** don't commit a real password in
> `database.py`. For a repo-ready setup, swap it for an environment
> variable (`os.environ["DB_PASSWORD"]`) loaded from a `.env` file that's
> listed in `.gitignore`.

### 3. Create the database
```bash
mysql -u root -p < schema.sql
```

### 4. Run the app
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
(or simply `python main.py`)

### 5. Open in browser
```
http://localhost:5000
```

Interactive API docs are available at:
```
http://localhost:5000/docs
```

---

## 🧭 Page Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard |
| GET | `/manage_stock` | Manage stock page |
| GET | `/edit_prices` | Edit prices page |
| GET | `/cart_billing` | Cart & billing page |
| GET | `/view_bills` | View past bills page |

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/get_items` | Fetch all items |
| GET | `/get_stock` | Fetch current stock levels |
| GET | `/get_cart` | Fetch current cart |
| GET | `/get_bills` | Fetch all bills |
| POST | `/add_item` | Add new item to inventory |
| POST | `/update_stock` | Restock an existing item |
| POST | `/add_to_cart` | Add item to cart (auto-converts g ⇄ kg) |
| POST | `/generate_bill` | Generate bill & deduct stock |
| PUT | `/edit_prices` | Update item prices |
| DELETE | `/remove_from_cart` | Remove item from cart |

---

## 🎨 UI

Earthy green/amber palette, Playfair Display + DM Sans typography, live
stock badges, profit margin display, collapsible bill cards, and toast
notifications.

---

## 📌 Known Limitations

- **Single-session model:** the cart uses one hardcoded `SESSION_ID`
  (`"owner_session"`), so it's built for a single-owner shop, not
  multiple concurrent users/carts.
- **No authentication:** all routes are open; there's no login or
  access control layer.
- **No automated tests** yet.

These are intentional scope choices for a portfolio/learning project,
not oversights.
