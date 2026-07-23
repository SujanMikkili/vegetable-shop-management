"""
Vegetable Shop Management System — FastAPI backend.

This is a drop-in replacement for the original Flask app.py.
Every route, method, and JSON shape is kept identical so the
existing frontend (templates/*.html) works completely unchanged.
"""

import json
from datetime import datetime, date
from decimal import Decimal

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from database import execute_query
from models import ItemCreate, StockUpdate, PriceUpdate, CartAdd, CartRemove

app = FastAPI(title="Vegetable Shop Management System")

templates = Jinja2Templates(directory="templates")

SESSION_ID = "owner_session"  # single-owner app, same as the Flask version


def _to_float(value):
    return float(value) if isinstance(value, Decimal) else value


def _to_iso(value):
    return value.isoformat() if isinstance(value, (datetime, date)) else value


# ---------------------------------------------------------------------------
# Page routes (render the untouched HTML templates)
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/manage_stock", response_class=HTMLResponse)
def manage_stock(request: Request):
    return templates.TemplateResponse(request, "manage_stock.html")


@app.get("/edit_prices", response_class=HTMLResponse)
def edit_prices(request: Request):
    return templates.TemplateResponse(request, "edit_prices.html")


@app.get("/cart_billing", response_class=HTMLResponse)
def cart_billing(request: Request):
    return templates.TemplateResponse(request, "cart_billing.html")


@app.get("/view_bills", response_class=HTMLResponse)
def view_bills(request: Request):
    return templates.TemplateResponse(request, "view_bills.html")


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------

@app.post("/add_item")
def add_item(data: ItemCreate):
    try:
        execute_query(
            "INSERT INTO items (name, unit, original_price, selling_price) VALUES (%s, %s, %s, %s)",
            (data.name, data.unit, data.original_price, data.selling_price),
        )
        item_id = execute_query("SELECT LAST_INSERT_ID() as id", fetch=True)[0]["id"]
        execute_query(
            "INSERT INTO stock (item_id, quantity) VALUES (%s, %s)",
            (item_id, data.quantity),
        )
        return {"message": "Item added to stock successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/update_stock")
def update_stock(data: StockUpdate):
    try:
        existing = execute_query(
            "SELECT quantity FROM stock WHERE item_id = %s", (data.item_id,), fetch=True
        )
        if existing:
            current_quantity = float(existing[0]["quantity"])
            new_quantity = current_quantity + data.quantity
            execute_query(
                "UPDATE stock SET quantity = %s, last_updated = NOW() WHERE item_id = %s",
                (new_quantity, data.item_id),
            )
            return {"message": f"Stock updated. New quantity: {new_quantity}"}
        else:
            execute_query(
                "INSERT INTO stock (item_id, quantity) VALUES (%s, %s)",
                (data.item_id, data.quantity),
            )
            return {"message": f"Stock added. Quantity: {data.quantity}"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.put("/edit_prices")
def edit_prices_api(data: PriceUpdate):
    try:
        execute_query(
            "UPDATE items SET original_price = %s, selling_price = %s WHERE id = %s",
            (data.original_price, data.selling_price, data.id),
        )
        return {"message": "Prices updated"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/get_items")
def get_items():
    try:
        items = execute_query("SELECT * FROM items", fetch=True)
        for item in items:
            item["original_price"] = _to_float(item["original_price"])
            item["selling_price"] = _to_float(item["selling_price"])
        return items
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/get_stock")
def get_stock():
    try:
        stock = execute_query(
            "SELECT s.id, i.id as item_id, i.name, i.unit, s.quantity "
            "FROM stock s JOIN items i ON s.item_id = i.id",
            fetch=True,
        )
        for s in stock:
            s["quantity"] = _to_float(s["quantity"])
        return stock
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/add_to_cart")
def add_to_cart(data: CartAdd):
    try:
        item_id = data.item_id
        quantity = data.quantity
        input_unit = data.unit

        item = execute_query("SELECT unit FROM items WHERE id = %s", (item_id,), fetch=True)
        if not item:
            return JSONResponse(status_code=404, content={"error": "Item not found"})
        item_unit = item[0]["unit"]

        # unit conversion, same logic as the Flask version
        if input_unit == "g" and item_unit == "kg":
            quantity /= 1000
        elif input_unit == "kg" and item_unit == "g":
            quantity *= 1000

        execute_query(
            "INSERT INTO cart (item_id, quantity, session_id) VALUES (%s, %s, %s)",
            (item_id, quantity, SESSION_ID),
        )
        return {"message": "Added to cart"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.delete("/remove_from_cart")
def remove_from_cart(data: CartRemove):
    try:
        execute_query("DELETE FROM cart WHERE id = %s", (data.cart_id,))
        return {"message": "Item removed from cart"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/get_cart")
def get_cart():
    try:
        cart = execute_query(
            "SELECT c.id, i.name, i.unit, i.selling_price, c.quantity "
            "FROM cart c JOIN items i ON c.item_id = i.id WHERE c.session_id = %s",
            (SESSION_ID,),
            fetch=True,
        )
        for c in cart:
            c["selling_price"] = _to_float(c["selling_price"])
            c["quantity"] = _to_float(c["quantity"])
        return cart
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/generate_bill")
def generate_bill():
    try:
        cart_items = execute_query(
            "SELECT c.item_id, i.name, i.unit, i.selling_price, c.quantity "
            "FROM cart c JOIN items i ON c.item_id = i.id WHERE c.session_id = %s",
            (SESSION_ID,),
            fetch=True,
        )
        if not cart_items:
            return JSONResponse(status_code=400, content={"error": "Cart is empty"})

        for item in cart_items:
            item["selling_price"] = _to_float(item["selling_price"])
            item["quantity"] = _to_float(item["quantity"])

        total = sum(item["selling_price"] * item["quantity"] for item in cart_items)
        items_sold = json.dumps(cart_items)

        execute_query(
            "INSERT INTO bills (total_amount, items_sold) VALUES (%s, %s)",
            (total, items_sold),
        )

        # deduct from stock
        for item in cart_items:
            current_stock = execute_query(
                "SELECT quantity FROM stock WHERE item_id = %s", (item["item_id"],), fetch=True
            )
            if current_stock and float(current_stock[0]["quantity"]) >= item["quantity"]:
                new_quantity = float(current_stock[0]["quantity"]) - item["quantity"]
                execute_query(
                    "UPDATE stock SET quantity = %s WHERE item_id = %s",
                    (new_quantity, item["item_id"]),
                )
            else:
                return JSONResponse(
                    status_code=400, content={"error": f"Insufficient stock for {item['name']}"}
                )

        execute_query("DELETE FROM cart WHERE session_id = %s", (SESSION_ID,))
        return {"message": f"Bill generated successfully! Total: \u20b9{total:.2f}", "total": total}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/get_bills")
def get_bills():
    try:
        bills = execute_query(
            "SELECT id, date, total_amount, items_sold FROM bills ORDER BY date DESC", fetch=True
        )
        for bill in bills:
            bill["items_sold"] = json.loads(bill["items_sold"]) if bill["items_sold"] else []
            bill["total_amount"] = _to_float(bill["total_amount"])
            bill["date"] = _to_iso(bill["date"])
        return bills
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)