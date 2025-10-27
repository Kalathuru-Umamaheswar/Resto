from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# -----------------------
# Flask App Configuration
# -----------------------
import logging
logging.basicConfig(level=logging.DEBUG)

# Serve frontend files (index.html, css/, js/) from the frontend folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")
print(f"Frontend directory path: {FRONTEND_DIR}")

app = Flask(__name__)
app.static_folder = FRONTEND_DIR
app.static_url_path = ''
app.debug = True
CORS(app)  # Allow requests from frontend

# Database path (SQLite used for simplicity)
DB_PATH = os.path.join(BASE_DIR, "../database/food_delivery.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------
# Database Models
# -----------------------
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cuisine = db.Column(db.String(100))
    rating = db.Column(db.Float)
    image = db.Column(db.String(200))
    menu = db.relationship('MenuItem', backref='restaurant', lazy=True)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200))  # URL to the food image
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

# -----------------------
# API Routes
# -----------------------

# Get all restaurants
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    print("Fetching restaurants from database...")
    restaurants = Restaurant.query.all()
    print(f"Found {len(restaurants)} restaurants")
    data = []
    for r in restaurants:
        restaurant_data = {
            "id": r.id,
            "name": r.name,
            "cuisine": r.cuisine,
            "rating": r.rating,
            "image": r.image
        }
        data.append(restaurant_data)
        print(f"Added restaurant: {restaurant_data['name']}")
    return jsonify(data)

# Get menu items of a restaurant
@app.route("/restaurants/<int:restaurant_id>/menu", methods=["GET"])
def get_menu(restaurant_id):
    items = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
    data = []
    for i in items:
        data.append({
            "id": i.id,
            "name": i.name,
            "description": i.description,
            "price": i.price
        })
    return jsonify(data)


# -----------------------
# Simple in-memory cart implementation
# Format: CARTS = { user_id: { item_id: quantity, ... }, ... }
# This keeps things simple for a demo. For production, persist carts in DB.
CARTS = {}


@app.route('/cart/add', methods=['POST'])
def cart_add():
    data = request.json or {}
    user_id = str(data.get('user_id', '1'))
    item_id = data.get('item_id')
    qty = int(data.get('quantity', 1))
    if item_id is None:
        return jsonify({"error": "item_id required"}), 400
    CARTS.setdefault(user_id, {})
    CARTS[user_id][str(item_id)] = CARTS[user_id].get(str(item_id), 0) + qty
    return jsonify({"message": "Added to cart"})


@app.route('/cart/<user_id>', methods=['GET'])
def cart_get(user_id):
    user_cart = CARTS.get(str(user_id), {})
    items = []
    for item_id, qty in user_cart.items():
        menu_item = MenuItem.query.get(int(item_id))
        if menu_item:
            items.append({
                "id": menu_item.id,
                "name": menu_item.name,
                "price": menu_item.price,
                "quantity": qty
            })
    return jsonify(items)


@app.route('/cart/remove', methods=['POST'])
def cart_remove():
    data = request.json or {}
    user_id = str(data.get('user_id', '1'))
    item_id = data.get('item_id')
    if not item_id:
        return jsonify({"error": "item_id required"}), 400
    user_cart = CARTS.get(user_id, {})
    user_cart.pop(str(item_id), None)
    CARTS[user_id] = user_cart
    return jsonify({"message": "Removed"})

# Place order (simple example)
@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.json or {}
    # Accept either explicit cart or use in-memory cart by user_id
    total = 0
    if 'cart' in data:
        for item in data['cart']:
            menu_item = MenuItem.query.get(item['id'])
            if menu_item:
                total += menu_item.price * item.get('quantity', 1)
    else:
        user_id = str(data.get('user_id', '1'))
        user_cart = CARTS.get(user_id, {})
        for item_id, qty in user_cart.items():
            menu_item = MenuItem.query.get(int(item_id))
            if menu_item:
                total += menu_item.price * qty
        # clear cart after checkout
        CARTS[user_id] = {}
    return jsonify({"message": "Order placed successfully!", "total": total})

# Serve frontend
@app.route('/')
def home():
    try:
        print("Attempting to serve index.html...")
        return app.send_static_file('index.html')
    except Exception as e:
        print(f"Error serving index.html: {e}")
        return str(e), 500

@app.route('/<path:path>')
def serve_static(path):
    try:
        print(f"Attempting to serve static file: {path}")
        return app.send_static_file(path)
    except Exception as e:
        print(f"Error serving {path}: {e}")
        return str(e), 404

# -----------------------
# Run App
# -----------------------
if __name__ == "__main__":
    print("Starting Flask application...")
    
    # Create DB tables if they don't exist
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Verify if we have restaurants in the database
        restaurants = Restaurant.query.all()
        print(f"Found {len(restaurants)} restaurants in database")
        
        if len(restaurants) == 0:
            print("No restaurants found. Please run init_db.py to populate the database.")
    
    # Run the Flask app
    print(f"Starting Flask server... Frontend will be served from: {FRONTEND_DIR}")
    app.run(debug=True, host='127.0.0.1', port=5000)
