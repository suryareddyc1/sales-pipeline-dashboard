from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .database import fetch_all, fetch_one, init_db, replace_sales_records
from .pipeline import clean_sales_dataframe, load_csv_file, load_csv_path, to_records
from .schemas import PipelineResult

app = FastAPI(title="Sales Pipeline Dashboard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def health_check() -> dict:
    return {"status": "ok", "message": "Sales Pipeline API is running"}


@app.post("/pipeline/upload-csv", response_model=PipelineResult)
def upload_csv(file: UploadFile = File(...)) -> PipelineResult:
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file")

    try:
        raw_df = load_csv_file(file.file)
        clean_df = clean_sales_dataframe(raw_df)
        rows_loaded = replace_sales_records(to_records(clean_df))
        return PipelineResult(message="CSV cleaned and loaded successfully", rows_loaded=rows_loaded)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {exc}") from exc


@app.post("/pipeline/load-sample", response_model=PipelineResult)
def load_sample() -> PipelineResult:
    try:
        sample_path = Path(__file__).resolve().parent / "sample_sales.csv"
        raw_df = load_csv_path(sample_path)
        clean_df = clean_sales_dataframe(raw_df)
        rows_loaded = replace_sales_records(to_records(clean_df))
        return PipelineResult(message="Sample data loaded successfully", rows_loaded=rows_loaded)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Sample load failed: {exc}") from exc


@app.get("/dashboard/summary")
def summary() -> dict:
    return fetch_one(
        """
        SELECT
            COALESCE(SUM(net_revenue), 0) AS total_revenue,
            COUNT(order_id) AS total_orders,
            COUNT(DISTINCT customer) AS total_customers,
            COALESCE(AVG(net_revenue), 0) AS average_order_value
        FROM sales
        """
    )


@app.get("/dashboard/revenue-by-month")
def revenue_by_month() -> list[dict]:
    return fetch_all(
        """
        SELECT
            strftime('%Y-%m', order_date) AS month,
            ROUND(SUM(net_revenue), 2) AS revenue,
            COUNT(order_id) AS orders
        FROM sales
        GROUP BY month
        ORDER BY month
        """
    )


@app.get("/dashboard/revenue-by-region")
def revenue_by_region() -> list[dict]:
    return fetch_all(
        """
        SELECT
            region,
            ROUND(SUM(net_revenue), 2) AS revenue,
            COUNT(order_id) AS orders
        FROM sales
        GROUP BY region
        ORDER BY revenue DESC
        """
    )


@app.get("/dashboard/top-products")
def top_products() -> list[dict]:
    return fetch_all(
        """
        SELECT
            product,
            category,
            ROUND(SUM(net_revenue), 2) AS revenue,
            SUM(quantity) AS units_sold
        FROM sales
        GROUP BY product, category
        ORDER BY revenue DESC
        LIMIT 10
        """
    )


@app.get("/dashboard/category-share")
def category_share() -> list[dict]:
    return fetch_all(
        """
        SELECT
            category,
            ROUND(SUM(net_revenue), 2) AS revenue
        FROM sales
        GROUP BY category
        ORDER BY revenue DESC
        """
    )


@app.get("/sales")
def sales(limit: int = 100) -> list[dict]:
    return fetch_all(
        """
        SELECT *
        FROM sales
        ORDER BY order_date DESC
        LIMIT ?
        """,
        (limit,),
    )
