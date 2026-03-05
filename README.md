# Green Rush – 10-Minute Plant Delivery

A Flask web app for ordering plants with cart, checkout, and order confirmation.

## Features

- Browse plants (Rose, Orchid, Lily, Tulip, Tulsi, Aloe Vera) with prices in ₹
- Add to cart → View cart → Proceed to Checkout
- Delivery form (pre-filled if logged in)
- Place order → Order confirmation with order ID
- Register / Login (session-based; in-memory store for demo)

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**

## Deploy (e.g. Render)

- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app`
- Set root to this directory and add a Web Service; Render will use the `Procfile`.

## Project structure

- `app.py` – Flask app and routes
- `*.html` – Templates (index, cart, checkout, order_confirmation, login, register) in root
- `requirements.txt`, `Procfile`, `runtime.txt` – Dependencies and deployment
