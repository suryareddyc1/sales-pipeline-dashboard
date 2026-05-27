from pathlib import Path
from typing import BinaryIO
import pandas as pd

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "customer",
    "region",
    "product",
    "category",
    "quantity",
    "unit_price",
    "discount",
}


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        col.strip().lower().replace(" ", "_").replace("-", "_")
        for col in df.columns
    ]
    return df


def clean_sales_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = _normalize_columns(df)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    df = df[list(REQUIRED_COLUMNS)].copy()

    text_columns = ["order_id", "customer", "region", "product", "category"]
    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["discount"] = pd.to_numeric(df["discount"], errors="coerce").fillna(0)

    df = df.dropna(subset=["order_id", "order_date", "quantity", "unit_price"])
    df = df[(df["quantity"] > 0) & (df["unit_price"] >= 0)]
    df["discount"] = df["discount"].clip(lower=0, upper=1)

    df["quantity"] = df["quantity"].astype(int)
    df["gross_revenue"] = df["quantity"] * df["unit_price"]
    df["discount_amount"] = df["gross_revenue"] * df["discount"]
    df["net_revenue"] = df["gross_revenue"] - df["discount_amount"]

    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
    df = df.drop_duplicates(subset=["order_id"], keep="last")

    output_columns = [
        "order_id",
        "order_date",
        "customer",
        "region",
        "product",
        "category",
        "quantity",
        "unit_price",
        "discount",
        "gross_revenue",
        "discount_amount",
        "net_revenue",
    ]
    return df[output_columns]


def load_csv_file(file: BinaryIO) -> pd.DataFrame:
    return pd.read_csv(file)


def load_csv_path(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def to_records(df: pd.DataFrame) -> list[dict]:
    return df.to_dict(orient="records")
