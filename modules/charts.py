"""
charts.py
---------
All Plotly chart builders. Each function returns a plotly Figure.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Shared colour palette ──────────────────────────────────────────────────────
PALETTE = px.colors.qualitative.Set2
ACCENT  = "#3b82d4"


def _base_layout(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#1f2328")),
        paper_bgcolor="white",
        plot_bgcolor="#f7f8fa",
        font=dict(family="Segoe UI, system-ui, sans-serif", size=13, color="#1f2328"),
        margin=dict(t=60, b=40, l=40, r=20),
        legend=dict(bgcolor="white", bordercolor="#e5e7eb", borderwidth=1),
    )
    fig.update_xaxes(gridcolor="#e5e7eb", linecolor="#e5e7eb")
    fig.update_yaxes(gridcolor="#e5e7eb", linecolor="#e5e7eb")
    return fig


# ── Revenue by Branch ─────────────────────────────────────────────────────────

def branch_revenue_bar(df_branch: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_branch,
        x="Branch",
        y="Total_Revenue",
        color="City",
        text="Total_Revenue",
        color_discrete_sequence=PALETTE,
        labels={"Total_Revenue": "Revenue (₹)", "Branch": "Branch"},
    )
    fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
    return _base_layout(fig, "Total Revenue by Branch")


def branch_avg_rating_bar(df_branch: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_branch,
        x="Branch",
        y="Avg_Rating",
        color="City",
        text="Avg_Rating",
        color_discrete_sequence=PALETTE,
        labels={"Avg_Rating": "Avg Rating", "Branch": "Branch"},
    )
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig.update_yaxes(range=[0, 5.5])
    return _base_layout(fig, "Average Customer Rating by Branch")


# ── Revenue by Category ───────────────────────────────────────────────────────

def category_revenue_bar(df_cat: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_cat.sort_values("Total_Revenue"),
        x="Total_Revenue",
        y="Category",
        orientation="h",
        color="Category",
        text="Total_Revenue",
        color_discrete_sequence=PALETTE,
        labels={"Total_Revenue": "Revenue (₹)"},
    )
    fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
    fig.update_layout(showlegend=False)
    return _base_layout(fig, "Total Revenue by Category")


def category_pie(df_cat: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        df_cat,
        names="Category",
        values="Total_Revenue",
        color_discrete_sequence=PALETTE,
        hole=0.4,
    )
    fig.update_traces(textinfo="label+percent", pull=[0.03] * len(df_cat))
    return _base_layout(fig, "Category Revenue Share")


# ── Top Products ──────────────────────────────────────────────────────────────

def top_products_bar(df_prod: pd.DataFrame, n: int = 10) -> go.Figure:
    top = df_prod.head(n)
    fig = px.bar(
        top.sort_values("Total_Revenue"),
        x="Total_Revenue",
        y="Product",
        orientation="h",
        color="Category",
        text="Total_Revenue",
        color_discrete_sequence=PALETTE,
        labels={"Total_Revenue": "Revenue (₹)", "Product": "Product"},
    )
    fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
    return _base_layout(fig, f"Top {n} Products by Revenue")


# ── Customer Type & Gender ────────────────────────────────────────────────────

def customer_type_donut(df_ct: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        df_ct,
        names="Customer Type",
        values="Total_Revenue",
        color_discrete_sequence=[ACCENT, "#7c5cd8"],
        hole=0.45,
    )
    fig.update_traces(textinfo="label+percent")
    return _base_layout(fig, "Revenue: Member vs Normal")


def gender_bar(df_gender: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_gender,
        x="Gender",
        y="Total_Revenue",
        color="Gender",
        text="Total_Revenue",
        color_discrete_sequence=[ACCENT, "#e0538c"],
        labels={"Total_Revenue": "Revenue (₹)"},
    )
    fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
    fig.update_layout(showlegend=False)
    return _base_layout(fig, "Revenue by Gender")


# ── Payment Method ────────────────────────────────────────────────────────────

def payment_pie(df_pay: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        df_pay,
        names="Payment",
        values="Total_Revenue",
        color_discrete_sequence=PALETTE,
        hole=0.4,
    )
    fig.update_traces(textinfo="label+percent")
    return _base_layout(fig, "Revenue by Payment Method")


def payment_bar(df_pay: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_pay,
        x="Payment",
        y="Transactions",
        color="Payment",
        text="Transactions",
        color_discrete_sequence=PALETTE,
        labels={"Transactions": "No. of Transactions"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False)
    return _base_layout(fig, "Transaction Count by Payment Method")


# ── Time Series ───────────────────────────────────────────────────────────────

def daily_sales_line(df_ts: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_ts["Date"], y=df_ts["Total_Revenue"],
        mode="lines", name="Daily Revenue",
        line=dict(color="#aac4e8", width=1.5),
    ))
    fig.add_trace(go.Scatter(
        x=df_ts["Date"], y=df_ts["7d_MA"],
        mode="lines", name="7-Day Moving Avg",
        line=dict(color=ACCENT, width=2.5),
    ))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Revenue (₹)",
        legend=dict(bgcolor="white", bordercolor="#e5e7eb", borderwidth=1),
    )
    return _base_layout(fig, "Daily Revenue Trend with 7-Day Moving Average")


def monthly_sales_bar(df_ms: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_ms,
        x="Month",
        y="Total_Revenue",
        text="Total_Revenue",
        color="Total_Revenue",
        color_continuous_scale="Blues",
        labels={"Total_Revenue": "Revenue (₹)", "Month": "Month"},
    )
    fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
    fig.update_coloraxes(showscale=False)
    return _base_layout(fig, "Monthly Revenue")


# ── Rating Distribution ───────────────────────────────────────────────────────

def rating_bar(df_rating: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_rating,
        x="Rating_Band",
        y="Count",
        color="Count",
        text="Count",
        color_continuous_scale="Teal",
        labels={"Rating_Band": "Rating Band", "Count": "No. of Transactions"},
    )
    fig.update_traces(textposition="outside")
    fig.update_coloraxes(showscale=False)
    return _base_layout(fig, "Rating Distribution")


# ── Scatter: Unit Price vs Sales ──────────────────────────────────────────────

def price_vs_sales_scatter(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df,
        x="Unit Price",
        y="Sales",
        color="Category",
        size="Quantity",
        hover_data=["Product", "Branch", "City"],
        color_discrete_sequence=PALETTE,
        labels={"Unit Price": "Unit Price (₹)", "Sales": "Sales (₹)"},
        opacity=0.75,
    )
    return _base_layout(fig, "Unit Price vs Sales (bubble size = Quantity)")


# ── Category × Branch Heatmap ─────────────────────────────────────────────────

def category_branch_heatmap(pivot: pd.DataFrame) -> go.Figure:
    branch_cols = [c for c in pivot.columns if c not in ("Category", "Total")]
    z = pivot[branch_cols].values
    fig = go.Figure(go.Heatmap(
        z=z,
        x=branch_cols,
        y=pivot["Category"].tolist(),
        colorscale="Blues",
        text=z,
        texttemplate="₹%{text:,.0f}",
        showscale=True,
        colorbar=dict(title="Revenue (₹)"),
    ))
    fig.update_layout(xaxis_title="Branch", yaxis_title="Category")
    return _base_layout(fig, "Revenue Heatmap: Category × Branch")


# ── Box Plot: Sales Distribution by Category ─────────────────────────────────

def sales_boxplot(df: pd.DataFrame) -> go.Figure:
    fig = px.box(
        df,
        x="Category",
        y="Sales",
        color="Category",
        color_discrete_sequence=PALETTE,
        points="outliers",
        labels={"Sales": "Sales per Transaction (₹)"},
    )
    fig.update_layout(showlegend=False)
    return _base_layout(fig, "Sales Distribution by Category")
