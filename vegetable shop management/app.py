from flask import Flask, request, jsonify, render_template, g
import mysql.connector
import json
from datetime import datetime, date
from decimal import Decimal

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Sujan@1228",
    "database": "veg_shop"
}

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**DB_CONFIG)
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

class CustomEncoder(json.JSONEncoder):
    """Fix: Handle Decimal and datetime serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

app.json_encoder = CustomEncoder

def execute_query(query, params=None, fetch=False):
    """Fix: Removed infinite recursion on DB error."""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
        else:
            db.commit()
            result = None
        cursor.close()
        return result
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        raise Exception(f"Database error: {err}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manage_stock')
def manage_stock():
    return render_template('manage_stock.html')

@app.route('/edit_prices')
def edit_prices():
    return render_template('edit_prices.html')

@app.route('/cart_billing')
def cart_billing():
    return render_template('cart_billing.html')

@app.route('/view_bills')
def view_bills():
    return render_template('view_bills.html')

@app.route('/add_item', methods=['POST'])
def add_item():
    try:
        data = request.json
        execute_query(
            "INSERT INTO items (name, unit, original_price, selling_price) VALUES (%s, %s, %s, %s)",
            (data['name'], data['unit'], float(data['original_price']), float(data['selling_price']))
        )
        item_id = execute_query("SELECT LAST_INSERT_ID() as id", fetch=True)[0]['id']
        execute_query("INSERT INTO stock (item_id, quantity) VALUES (%s, %s)", (item_id, float(data['quantity'])))
        return jsonify({"message": "Item added to stock successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_stock', methods=['POST'])
def update_stock():
    try:
        data = request.json
        item_id = data['item_id']
        add_quantity = float(data['quantity'])
        existing = execute_query("SELECT quantity FROM stock WHERE item_id = %s", (item_id,), fetch=True)
        if existing:
            current_quantity = float(existing[0]['quantity'])
            new_quantity = current_quantity + add_quantity
            execute_query("UPDATE stock SET quantity = %s, last_updated = NOW() WHERE item_id = %s",
                          (new_quantity, item_id))
            return jsonify({"message": f"Stock updated. New quantity: {new_quantity}"})
        else:
            execute_query("INSERT INTO stock (item_id, quantity) VALUES (%s, %s)", (item_id, add_quantity))
            return jsonify({"message": f"Stock added. Quantity: {add_quantity}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/edit_prices', methods=['PUT'])
def edit_prices_api():
    try:
        data = request.json
        execute_query("UPDATE items SET original_price = %s, selling_price = %s WHERE id = %s",
                      (float(data['original_price']), float(data['selling_price']), data['id']))
        return jsonify({"message": "Prices updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_items', methods=['GET'])
def get_items():
    try:
        items = execute_query("SELECT * FROM items", fetch=True)
        # Fix: convert Decimal to float
        for item in items:
            item['original_price'] = float(item['original_price'])
            item['selling_price'] = float(item['selling_price'])
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_stock', methods=['GET'])
def get_stock():
    try:
        stock = execute_query(
            "SELECT s.id, i.id as item_id, i.name, i.unit, s.quantity FROM stock s JOIN items i ON s.item_id = i.id",
            fetch=True
        )
        for s in stock:
            s['quantity'] = float(s['quantity'])
        return jsonify(stock)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.json
        session_id = 'owner_session'
        item_id = data['item_id']
        quantity = float(data['quantity'])
        input_unit = data['unit']

        item = execute_query("SELECT unit FROM items WHERE id = %s", (item_id,), fetch=True)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        item_unit = item[0]['unit']

        # Fix: unit conversion
        if input_unit == 'g' and item_unit == 'kg':
            quantity /= 1000
        elif input_unit == 'kg' and item_unit == 'g':
            quantity *= 1000

        execute_query("INSERT INTO cart (item_id, quantity, session_id) VALUES (%s, %s, %s)",
                      (item_id, quantity, session_id))
        return jsonify({"message": "Added to cart"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/remove_from_cart', methods=['DELETE'])
def remove_from_cart():
    """Fix: Added missing remove from cart endpoint."""
    try:
        data = request.json
        cart_id = data['cart_id']
        execute_query("DELETE FROM cart WHERE id = %s", (cart_id,))
        return jsonify({"message": "Item removed from cart"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_cart', methods=['GET'])
def get_cart():
    try:
        session_id = 'owner_session'
        cart = execute_query(
            "SELECT c.id, i.name, i.unit, i.selling_price, c.quantity FROM cart c JOIN items i ON c.item_id = i.id WHERE c.session_id = %s",
            (session_id,), fetch=True
        )
        for c in cart:
            c['selling_price'] = float(c['selling_price'])
            c['quantity'] = float(c['quantity'])
        return jsonify(cart)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    try:
        session_id = 'owner_session'
        cart_items = execute_query(
            "SELECT c.item_id, i.name, i.unit, i.selling_price, c.quantity FROM cart c JOIN items i ON c.item_id = i.id WHERE c.session_id = %s",
            (session_id,), fetch=True
        )
        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400

        # Fix: Convert Decimal to float for JSON serialization; include unit in items_sold
        for item in cart_items:
            item['selling_price'] = float(item['selling_price'])
            item['quantity'] = float(item['quantity'])

        total = sum(item['selling_price'] * item['quantity'] for item in cart_items)
        items_sold = json.dumps(cart_items)

        execute_query("INSERT INTO bills (total_amount, items_sold) VALUES (%s, %s)", (total, items_sold))

        # Deduct from stock
        for item in cart_items:
            current_stock = execute_query("SELECT quantity FROM stock WHERE item_id = %s", (item['item_id'],), fetch=True)
            if current_stock and float(current_stock[0]['quantity']) >= item['quantity']:
                new_quantity = float(current_stock[0]['quantity']) - item['quantity']
                execute_query("UPDATE stock SET quantity = %s WHERE item_id = %s", (new_quantity, item['item_id']))
            else:
                return jsonify({"error": f"Insufficient stock for {item['name']}"}), 400

        execute_query("DELETE FROM cart WHERE session_id = %s", (session_id,))
        return jsonify({"message": f"Bill generated successfully! Total: ₹{total:.2f}", "total": total})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_bills', methods=['GET'])
def get_bills():
    try:
        bills = execute_query("SELECT id, date, total_amount, items_sold FROM bills ORDER BY date DESC", fetch=True)
        for bill in bills:
            bill['items_sold'] = json.loads(bill['items_sold']) if bill['items_sold'] else []
            bill['total_amount'] = float(bill['total_amount'])
            # Fix: Convert datetime to string for JSON serialization
            if isinstance(bill['date'], (datetime, date)):
                bill['date'] = bill['date'].isoformat()
        return jsonify(bills)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
