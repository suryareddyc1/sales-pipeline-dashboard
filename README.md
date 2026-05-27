# Sales Pipeline Revenue Dashboard

Full-stack starter project:

- **Backend:** Python, FastAPI, Pandas, SQLite SQL queries
- **Frontend:** React JS, Vite, Plotly dashboard
- **Pipeline:** CSV upload/load sample CSV → clean data with Pandas → store in SQLite → query metrics → display charts

## 1. Start backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open this to confirm backend is running:

```text
http://localhost:8000
```

You should see:

```json
{"status":"ok","message":"Sales Pipeline API is running"}
```

## 2. Start frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

Click **Load Sample Data** to populate the dashboard.

## CSV columns expected

Your CSV should include these columns:

```text
order_id, order_date, customer, region, product, category, quantity, unit_price, discount
```

## Blank screen fix included

This version avoids the common blank screen issue by:

- Pinning React to stable React 18
- Pinning Vite/plugin versions
- Replacing the heavier `react-plotly.js` wrapper with direct `plotly.js-basic-dist-min`
- Showing empty chart placeholders when no data is loaded
- Allowing CORS from frontend dev server

## Useful backend endpoints

```text
POST /pipeline/load-sample
POST /pipeline/upload-csv
GET  /dashboard/summary
GET  /dashboard/revenue-by-month
GET  /dashboard/revenue-by-region
GET  /dashboard/top-products
GET  /dashboard/category-share
GET  /sales
```
