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

## Deploy

### Option 1: Render (recommended for Flask)

1. Push your code to GitHub: [github.com/srikarremani143/GreenRush](https://github.com/srikarremani143/GreenRush).
2. Go to [render.com](https://render.com) → **Sign up** / Log in → **Dashboard**.
3. Click **New +** → **Web Service**.
4. Connect your GitHub account if needed, then select the repo **srikarremani143/GreenRush**.
5. Configure:
   - **Name:** `greenrush` (or any name).
   - **Region:** Choose closest to you.
   - **Root Directory:** leave blank (repo root).
   - **Runtime:** Python 3.
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - (Render will also use your `Procfile` if present: `web: gunicorn app:app`.)
6. Under **Environment**, add a variable (optional but recommended):
   - Key: `SECRET_KEY`  
   - Value: a long random string (e.g. from `python -c "import secrets; print(secrets.token_hex(32))"`).  
   Then in `app.py` use: `app.secret_key = os.environ.get("SECRET_KEY", "fallback-dev-key")`.
7. Click **Create Web Service**. Render will build and deploy; your app will be at `https://<your-service-name>.onrender.com`.

**Note:** On the free tier, the service may spin down after inactivity; the first request after that can take 30–60 seconds.

---

### Option 2: Vercel

Vercel supports Flask with minimal config. Free tier is stateless (no persistent storage; sessions in memory are lost between requests/cold starts).

1. Push your code to GitHub (same repo as above).
2. Go to [vercel.com](https://vercel.com) → **Sign up** / Log in.
3. Click **Add New…** → **Project**.
4. Import **srikarremani143/GreenRush** from GitHub.
5. Configure:
   - **Framework Preset:** Other (or leave as detected).
   - **Root Directory:** leave as `.`
   - **Build Command:** `pip install -r requirements.txt` (or leave default).
   - **Output Directory:** leave default.
   - **Install Command:** `pip install -r requirements.txt`
6. Click **Deploy**. Vercel will build and give you a URL like `https://green-rush-xxx.vercel.app`.

**Optional:** To run the app as a single serverless function (so routing works correctly), add a `vercel.json` in the repo root:

```json
{
  "builds": [
    { "src": "app.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "app.py" }
  ]
}
```

**Vercel limits (free):** 30s timeout, no persistent storage; best for demos. For full sessions and persistence, use Render or add a database.

---

## Project structure

- `app.py` – Flask app and routes
- `*.html` – Templates (index, cart, checkout, order_confirmation, login, register) in root
- `requirements.txt`, `Procfile`, `runtime.txt` – Dependencies and deployment
