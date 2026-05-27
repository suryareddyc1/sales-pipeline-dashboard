from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sales.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                order_id TEXT PRIMARY KEY,
                order_date TEXT NOT NULL,
                customer TEXT NOT NULL,
                region TEXT NOT NULL,
                product TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                discount REAL NOT NULL,
                gross_revenue REAL NOT NULL,
                discount_amount REAL NOT NULL,
                net_revenue REAL NOT NULL
            )
            """
        )
        conn.commit()


def replace_sales_records(records: list[dict]) -> int:
    with get_connection() as conn:
        conn.execute("DELETE FROM sales")
        conn.executemany(
            """
            INSERT INTO sales (
                order_id, order_date, customer, region, product, category,
                quantity, unit_price, discount, gross_revenue,
                discount_amount, net_revenue
            ) VALUES (
                :order_id, :order_date, :customer, :region, :product, :category,
                :quantity, :unit_price, :discount, :gross_revenue,
                :discount_amount, :net_revenue
            )
            """,
            records,
        )
        conn.commit()
    return len(records)


def fetch_all(query: str, params: tuple = ()) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def fetch_one(query: str, params: tuple = ()) -> dict:
    with get_connection() as conn:
        row = conn.execute(query, params).fetchone()
    return dict(row) if row else {}
