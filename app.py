from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, template_folder=".")
app.secret_key = "green-rush-secret-key-change-in-production"

# Plant data (id, name, price, image filename) - your images in static/images/
plants = [
    {"id": 1, "name": "Rose", "price": 50, "image": "Rose.jpg"},
    {"id": 2, "name": "Orchid", "price": 150, "image": "Moth-orchid.jpg.webp"},
    {"id": 3, "name": "Lily", "price": 150, "image": "lily.jpg"},
    {"id": 4, "name": "Tulip", "price": 120, "image": "Tulip.webp"},
    {"id": 5, "name": "Tulsi", "price": 60, "image": "Tulsi.webp"},
    {"id": 6, "name": "Aloe Vera", "price": 90, "image": "Aloevra.jpg"},
]

# In-memory user store (for demo only; use a database in production)
users = {}

# In-memory orders (for demo)
orders = {}
_next_order_id = 1


def _get_cart_from_session():
    """Get selected_plants and total_price from session cart."""
    cart_ids = session.get("cart_ids") or []
    selected_plants = [p for p in plants if str(p["id"]) in cart_ids]
    total_price = sum(p["price"] for p in selected_plants)
    return selected_plants, total_price


@app.route("/")
def home():
    return render_template("index.html", plants=plants)


@app.route("/cart", methods=["POST"])
def cart():
    selected_ids = request.form.getlist("plant")
    selected_plants = [p for p in plants if str(p["id"]) in selected_ids]
    total_price = sum(p["price"] for p in selected_plants)
    # Save cart to session so checkout can use it
    session["cart_ids"] = selected_ids
    session["cart_total"] = total_price
    return render_template(
        "cart.html",
        selected_plants=selected_plants,
        total_price=total_price,
    )


@app.route("/checkout", methods=["GET"])
def checkout():
    selected_plants, total_price = _get_cart_from_session()
    if not selected_plants:
        return redirect(url_for("home"))
    # Pre-fill delivery info if user is logged in
    user_data = {}
    if session.get("user") and session["user"] in users:
        u = users[session["user"]]
        user_data = {
            "fullname": u.get("fullname", ""),
            "email": u.get("email", ""),
            "phone": u.get("phone", ""),
            "address": u.get("address", ""),
        }
    error = session.pop("checkout_error", None)
    return render_template(
        "checkout.html",
        selected_plants=selected_plants,
        total_price=total_price,
        user_data=user_data,
        error=error,
    )


@app.route("/place-order", methods=["POST"])
def place_order():
    selected_plants, total_price = _get_cart_from_session()
    if not selected_plants:
        return redirect(url_for("home"))
    fullname = request.form.get("fullname", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    if not all([fullname, email, phone, address]):
        session["checkout_error"] = "Please fill all delivery fields."
        return redirect(url_for("checkout"))
    global _next_order_id
    order_id = f"GR{_next_order_id:05d}"
    _next_order_id += 1
    orders[order_id] = {
        "id": order_id,
        "items": selected_plants,
        "total": total_price,
        "fullname": fullname,
        "email": email,
        "phone": phone,
        "address": address,
        "user": session.get("user"),
    }
    # Clear cart
    session.pop("cart_ids", None)
    session.pop("cart_total", None)
    return redirect(url_for("order_confirmation", order_id=order_id))


@app.route("/order-confirmation/<order_id>")
def order_confirmation(order_id):
    if order_id not in orders:
        return redirect(url_for("home"))
    return render_template("order_confirmation.html", order=orders[order_id])


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username in users and users[username]["password"] == password:
            session["user"] = username
            return redirect(url_for("home"))
        return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username in users:
            return render_template("register.html", error="Username already exists.")
        users[username] = {
            "fullname": fullname,
            "email": email,
            "phone": phone,
            "address": address,
            "password": password,
        }
        session["user"] = username
        return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/reg")
def reg():
    return redirect(url_for("register"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
