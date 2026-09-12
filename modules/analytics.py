"""
analytics.py
------------
Aggregation and summary statistics for supermarket sales.
"""

import pandas as pd
import numpy as np


# ── helper ────────────────────────────────────────────────────────────────────

def _pct(series: pd.Series) -> pd.Series:
    total = series.sum()
    return (series / total * 100).round(2) if total else series * 0


# ── KPI Summary ───────────────────────────────────────────────────────────────

def kpi_summary(df: pd.DataFrame) -> dict:
    """Return top-level KPIs as a flat dict."""
    return {
        "Total Revenue (₹)": round(df["Sales"].sum(), 2),
        "Total Transactions": len(df),
        "Total Units Sold": int(df["Quantity"].sum()),
        "Avg Transaction Value (₹)": round(df["Sales"].mean(), 2),
        "Avg Rating": round(df["Rating"].mean(), 2),
        "Avg Unit Price (₹)": round(df["Unit Price"].mean(), 2),
    }


# ── Branch / City ─────────────────────────────────────────────────────────────

def sales_by_branch(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby(["Branch", "City"])
        .agg(
            Total_Revenue=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Transaction=("Sales", "mean"),
            Avg_Rating=("Rating", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("Total_Revenue", ascending=False)
    )
    grp["Revenue_Share_%"] = _pct(grp["Total_Revenue"])
    return grp


# ── Category ──────────────────────────────────────────────────────────────────

def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby("Category")
        .agg(
            Total_Revenue=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Total_Units=("Quantity", "sum"),
            Avg_Unit_Price=("Unit Price", "mean"),
            Avg_Rating=("Rating", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("Total_Revenue", ascending=False)
    )
    grp["Revenue_Share_%"] = _pct(grp["Total_Revenue"])
    return grp


# ── Product ───────────────────────────────────────────────────────────────────

def sales_by_product(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby(["Product", "Category"])
        .agg(
            Total_Revenue=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Total_Units=("Quantity", "sum"),
            Avg_Unit_Price=("Unit Price", "mean"),
            Avg_Rating=("Rating", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("Total_Revenue", ascending=False)
    )
    return grp


# ── Customer Type ─────────────────────────────────────────────────────────────

def sales_by_customer_type(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby("Customer Type")
        .agg(
            Total_Revenue=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Transaction=("Sales", "mean"),
            Avg_Rating=("Rating", "mean"),
        )
        .round(2)
        .reset_index()
    )
    grp["Revenue_Share_%"] = _pct(grp["Total_Revenue"])
    return grp


# ── Gender ────────────────────────────────────────────────────────────────────

def sales_by_gender(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby("Gender")
        .agg(
            Total_Revenue=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Transaction=("Sales", "mean"),
        )
        .round(2)
        .reset_index()
    )
    grp["Revenue_Share_%"] = _pct(grp["Total_Revenue"])
    return grp


# ── Payment Method ────────────────────────────────────────────────────────────

def sales_by_payment(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby("Payment")
        .agg(
            Total_Revenue=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Transaction=("Sales", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("Total_Revenue", ascending=False)
    )
    grp["Revenue_Share_%"] = _pct(grp["Total_Revenue"])
    return grp


# ── Time Series ───────────────────────────────────────────────────────────────

def daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    ts = (
        df.groupby("Date")
        .agg(Total_Revenue=("Sales", "sum"), Transactions=("Invoice ID", "count"))
        .round(2)
        .reset_index()
        .sort_values("Date")
    )
    ts["7d_MA"] = ts["Total_Revenue"].rolling(7, min_periods=1).mean().round(2)
    return ts


def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    tmp = df.copy()
    tmp["Month"] = tmp["Date"].dt.to_period("M")
    ms = (
        tmp.groupby("Month")
        .agg(Total_Revenue=("Sales", "sum"), Transactions=("Invoice ID", "count"))
        .round(2)
        .reset_index()
    )
    ms["Month"] = ms["Month"].astype(str)
    return ms


# ── Rating Distribution ───────────────────────────────────────────────────────

def rating_distribution(df: pd.DataFrame) -> pd.DataFrame:
    bins = [0, 2, 3, 4, 4.5, 5]
    labels = ["< 2", "2–3", "3–4", "4–4.5", "4.5–5"]
    tmp = df.copy()
    tmp["Rating_Band"] = pd.cut(tmp["Rating"], bins=bins, labels=labels)
    rd = (
        tmp.groupby("Rating_Band", observed=True)
        .agg(Count=("Rating", "count"), Avg_Sales=("Sales", "mean"))
        .round(2)
        .reset_index()
    )
    rd["Rating_Band"] = rd["Rating_Band"].astype(str)
    return rd


# ── Cross-tab: Category × Branch ─────────────────────────────────────────────

def category_branch_pivot(df: pd.DataFrame) -> pd.DataFrame:
    pivot = df.pivot_table(
        index="Category",
        columns="Branch",
        values="Sales",
        aggfunc="sum",
    ).round(2).fillna(0)
    pivot["Total"] = pivot.sum(axis=1)
    return pivot.sort_values("Total", ascending=False).reset_index()
