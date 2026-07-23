# Vegetable Shop Management System — FastAPI Edition

Same app, same UI, new backend. The Flask backend has been replaced with
**FastAPI**; every route, HTTP method, JSON request/response shape, and
the entire frontend (`templates/*.html`) are **unchanged**, so no
frontend edits were needed.

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, **FastAPI**, Uvicorn |
| Validation | Pydantic |
| Database | MySQL (via `mysql-connector-python`, pooled connections) |
| Frontend | HTML5, CSS3, JavaScript (Vanilla) — unchanged |
| Fonts | Google Fonts (Playfair Display, DM Sans) |
| BI / Analytics | Power BI (via MySQL connector) |

---

## 📁 Project Structure

```
vegetable_shop_fastapi/
│
├── main.py              # FastAPI app — all routes (pages + API)
├── database.py           # MySQL connection pool + execute_query() helper
├── models.py             # Pydantic request models
├── schema.sql             # Database schema (same as before)
├── requirements.txt
│
└── templates/
    ├── index.html          # unchanged
    ├── manage_stock.html   # unchanged
    ├── edit_prices.html    # unchanged
    ├── cart_billing.html   # unchanged
    └── view_bills.html     # unchanged
```

---

## What changed vs. the Flask version

- Flask routes → FastAPI `@app.get/post/put/delete` routes with the **exact
  same paths and HTTP methods**.
- Manual `request.json` parsing + try/except → **Pydantic models**
  (`models.py`) validate incoming JSON automatically.
- Custom `CustomEncoder` for `Decimal`/`datetime` → FastAPI handles this,
  plus small explicit `_to_float` / `_to_iso` helpers are used where the
  original code manually converted types, so JSON output is byte-for-byte
  the same shape as before.
- `render_template` (Flask/Jinja2) → `Jinja2Templates` (FastAPI/Jinja2) —
  the HTML files themselves needed zero changes.
- A single global DB connection (`g.db`) → a small **connection pool**
  (`mysql.connector.pooling`), which is a better fit for FastAPI/Uvicorn's
  concurrent request handling.
- Dev server: `flask run` → `uvicorn`.

No database schema changes were made — use the same `schema.sql`.

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
> ⚠️ **Before pushing to GitHub:** `database.py` currently stores the
> password as a plain string in the file. Don't commit a real password.
> If you want this repo-ready, swap it for an environment variable
> (`os.environ["DB_PASSWORD"]`) plus a `.env` file that's listed in
> `.gitignore`.

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

Interactive API docs (new with FastAPI, free of charge) are available at:
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

## 🔌 API Endpoints (unchanged)

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

Unchanged — same earthy green/amber palette, Playfair Display + DM Sans
typography, live stock badges, profit margin display, collapsible bill
cards, and toast notifications.

---

## 📌 Known Limitations

- **Single-session model:** the cart uses one hardcoded `SESSION_ID`
  (`"owner_session"`), so it's built for a single-owner shop, not
  multiple concurrent users/carts.
- **No authentication:** all routes are open; there's no login or
  access control layer.
- **No automated tests** yet.

These are intentional scope choices for a portfolio/learning project,
not oversights — worth calling out explicitly if this is going into an
application or interview discussion.
