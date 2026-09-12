"""
data_loader.py
--------------
Handles loading, validation, and cleaning of the supermarket sales CSV.
"""

import pandas as pd
import numpy as np
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "supermarket_sales.csv"

EXPECTED_COLUMNS = [
    "Invoice ID", "Date", "Branch", "City", "Customer Type",
    "Gender", "Product", "Category", "Quantity", "Unit Price",
    "Payment", "Rating", "Sales"
]


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load CSV and return a cleaned DataFrame."""
    df = pd.read_csv(path)
    df = _normalize_columns(df)
    df = _parse_types(df)
    df = _fix_sales(df)
    return df


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from column names."""
    df.columns = df.columns.str.strip()
    return df


def _parse_types(df: pd.DataFrame) -> pd.DataFrame:
    """Cast columns to proper dtypes."""
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Unit Price"] = pd.to_numeric(df["Unit Price"], errors="coerce")
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    return df


def _fix_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Recompute Sales = Quantity × Unit Price, overwriting any incorrect values."""
    df["Sales"] = (df["Quantity"] * df["Unit Price"]).round(2)
    return df


def get_quality_report(df_raw: pd.DataFrame) -> dict:
    """
    Produce a data-quality report comparing the raw file to computed values.
    Returns a dict with keys:
        total_rows, missing_per_column, duplicate_rows,
        sales_mismatch_count, sales_mismatch_pct, dtype_summary
    """
    raw = pd.read_csv(DATA_PATH)
    raw.columns = raw.columns.str.strip()

    # Missing values
    missing = raw.isnull().sum()
    missing_dict = missing[missing > 0].to_dict()

    # Duplicates (by Invoice ID)
    dup_count = int(raw.duplicated(subset=["Invoice ID"]).sum())

    # Sales mismatch
    raw["Quantity"] = pd.to_numeric(raw["Quantity"], errors="coerce")
    raw["Unit Price"] = pd.to_numeric(raw["Unit Price"], errors="coerce")
    raw["Sales"] = pd.to_numeric(raw["Sales"], errors="coerce")
    raw["_computed_sales"] = (raw["Quantity"] * raw["Unit Price"]).round(2)
    mismatch = (raw["Sales"].round(2) != raw["_computed_sales"]).sum()

    # dtype summary for display
    dtype_summary = {col: str(dtype) for col, dtype in raw.drop(columns=["_computed_sales"]).dtypes.items()}

    return {
        "total_rows": len(raw),
        "total_columns": len(raw.columns) - 1,  # exclude helper col
        "missing_per_column": missing_dict,
        "duplicate_rows": dup_count,
        "sales_mismatch_count": int(mismatch),
        "sales_mismatch_pct": round(mismatch / len(raw) * 100, 2),
        "dtype_summary": dtype_summary,
    }
