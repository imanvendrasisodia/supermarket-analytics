"""
app.py  –  Supermarket Sales Analytics Dashboard
==================================================
Run with:   streamlit run app.py
"""

import sys
from pathlib import Path

# Make modules importable regardless of working directory
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import pandas as pd

from modules.data_loader import load_data, get_quality_report
from modules import analytics as an
from modules import charts as ch
from modules.insights import generate_insights

# ─────────────────────────────────────────────────────────────────────────────
# Page configuration
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Supermarket Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* KPI cards */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        text-align: center;
    }
    .kpi-value { font-size: 1.65rem; font-weight: 700; color: #1f2328; }
    .kpi-label { font-size: 0.82rem; color: #57606a; margin-top: 4px; }

    /* Insight cards */
    .insight-success {
        background: #f0fdf4; border-left: 4px solid #22c55e;
        border-radius: 6px; padding: 0.85rem 1rem; margin-bottom: 0.6rem;
    }
    .insight-warning {
        background: #fffbeb; border-left: 4px solid #f59e0b;
        border-radius: 6px; padding: 0.85rem 1rem; margin-bottom: 0.6rem;
    }
    .insight-info {
        background: #eff6ff; border-left: 4px solid #3b82f6;
        border-radius: 6px; padding: 0.85rem 1rem; margin-bottom: 0.6rem;
    }
    .insight-title { font-weight: 600; font-size: 0.95rem; color: #1f2328; }
    .insight-detail { font-size: 0.85rem; color: #57606a; margin-top: 3px; }

    /* Section headers */
    .section-header {
        font-size: 1.15rem; font-weight: 600; color: #1f2328;
        border-bottom: 2px solid #3b82d4; padding-bottom: 6px;
        margin-bottom: 1rem; margin-top: 0.5rem;
    }

    /* Quality badge */
    .badge-ok   { color:#16a34a; font-weight:600; }
    .badge-warn { color:#d97706; font-weight:600; }
    .badge-bad  { color:#dc2626; font-weight:600; }

    /* Table styling */
    .dataframe thead th { background:#f7f8fa !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Data load (cached)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading dataset…")
def get_data():
    return load_data()


@st.cache_data(show_spinner="Running quality checks…")
def get_quality(_df):
    return get_quality_report(_df)


df_full = get_data()

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar – Filters
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg", width=80)
    st.markdown("## 🛒 Supermarket Analytics")
    st.markdown("---")

    st.markdown("### 🔎 Filters")

    branches   = sorted(df_full["Branch"].unique())
    cities     = sorted(df_full["City"].unique())
    categories = sorted(df_full["Category"].unique())
    payments   = sorted(df_full["Payment"].unique())
    genders    = sorted(df_full["Gender"].unique())
    cust_types = sorted(df_full["Customer Type"].unique())

    sel_branches   = st.multiselect("Branch",        branches,   default=branches)
    sel_cities     = st.multiselect("City",          cities,     default=cities)
    sel_categories = st.multiselect("Category",      categories, default=categories)
    sel_payments   = st.multiselect("Payment",       payments,   default=payments)
    sel_genders    = st.multiselect("Gender",        genders,    default=genders)
    sel_cust_types = st.multiselect("Customer Type", cust_types, default=cust_types)

    min_date = df_full["Date"].min().date()
    max_date = df_full["Date"].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    st.markdown("---")
    st.caption("Data: supermarket_sales.csv · 500 rows")


# ─────────────────────────────────────────────────────────────────────────────
# Apply filters
# ─────────────────────────────────────────────────────────────────────────────
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_dt, end_dt = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_dt, end_dt = df_full["Date"].min(), df_full["Date"].max()

df = df_full[
    df_full["Branch"].isin(sel_branches)
    & df_full["City"].isin(sel_cities)
    & df_full["Category"].isin(sel_categories)
    & df_full["Payment"].isin(sel_payments)
    & df_full["Gender"].isin(sel_genders)
    & df_full["Customer Type"].isin(sel_cust_types)
    & df_full["Date"].between(start_dt, end_dt)
].copy()

if df.empty:
    st.warning("⚠️ No data matches the current filters. Please adjust the sidebar selections.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# Pre-compute analytics
# ─────────────────────────────────────────────────────────────────────────────
kpis        = an.kpi_summary(df)
df_branch   = an.sales_by_branch(df)
df_cat      = an.sales_by_category(df)
df_prod     = an.sales_by_product(df)
df_ct       = an.sales_by_customer_type(df)
df_gender   = an.sales_by_gender(df)
df_pay      = an.sales_by_payment(df)
df_ts       = an.daily_sales(df)
df_ms       = an.monthly_sales(df)
df_rating   = an.rating_distribution(df)
pivot       = an.category_branch_pivot(df)


# ─────────────────────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("# 🛒 Supermarket Sales Analytics Dashboard")
st.markdown(
    f"Showing **{len(df):,}** of **{len(df_full):,}** records · "
    f"Date range: **{start_dt.date()}** → **{end_dt.date()}**"
)
st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# Navigation tabs
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📊 Overview",
    "🔍 Data Quality",
    "🏪 Branch & City",
    "📦 Category & Product",
    "👥 Customer Analysis",
    "💳 Payment",
    "📅 Time Trends",
    "💡 Business Insights",
    "📋 Raw Data",
])

tab_overview, tab_quality, tab_branch, tab_cat, tab_customer, tab_pay, tab_time, tab_insights, tab_raw = tabs


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 – OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab_overview:
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)

    kpi_items = list(kpis.items())
    cols = st.columns(3)
    for i, (label, value) in enumerate(kpi_items):
        with cols[i % 3]:
            fmt = f"₹{value:,.2f}" if "₹" in label else (
                  f"{value:,.0f}" if isinstance(value, (int, float)) and value == int(value)
                  else f"{value:,.2f}"
            )
            st.markdown(
                f'<div class="kpi-card">'
                f'<div class="kpi-value">{fmt}</div>'
                f'<div class="kpi-label">{label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick charts: category pie + branch bar
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(ch.category_pie(df_cat), use_container_width=True, key="overview_cat_pie")
    with c2:
        st.plotly_chart(ch.branch_revenue_bar(df_branch), use_container_width=True, key="overview_branch_rev")

    # Daily trend full-width
    st.plotly_chart(ch.daily_sales_line(df_ts), use_container_width=True, key="overview_daily_line")

    # Sales distribution box plot
    st.plotly_chart(ch.sales_boxplot(df), use_container_width=True, key="overview_boxplot")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 – DATA QUALITY
# ═══════════════════════════════════════════════════════════════════════════════
with tab_quality:
    st.markdown('<div class="section-header">Data Quality Report</div>', unsafe_allow_html=True)

    quality = get_quality(df_full)

    qc1, qc2, qc3, qc4 = st.columns(4)

    with qc1:
        st.metric("Total Rows", f"{quality['total_rows']:,}")
    with qc2:
        st.metric("Total Columns", quality['total_columns'])
    with qc3:
        dup = quality["duplicate_rows"]
        st.metric("Duplicate Invoice IDs", dup,
                  delta="✅ None" if dup == 0 else f"⚠️ {dup} found",
                  delta_color="normal" if dup == 0 else "inverse")
    with qc4:
        mm = quality["sales_mismatch_count"]
        st.metric("Sales Mismatches", mm,
                  delta="✅ None" if mm == 0 else f"⚠️ {mm} fixed",
                  delta_color="normal" if mm == 0 else "inverse")

    st.markdown("---")

    col_miss, col_dtype = st.columns(2)

    with col_miss:
        st.markdown("#### 🔎 Missing Values per Column")
        if quality["missing_per_column"]:
            miss_df = pd.DataFrame(
                quality["missing_per_column"].items(),
                columns=["Column", "Missing Count"]
            )
            miss_df["Missing %"] = (miss_df["Missing Count"] / quality["total_rows"] * 100).round(2)
            st.dataframe(miss_df, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No missing values found in any column.")

    with col_dtype:
        st.markdown("#### 🗂️ Column Data Types")
        dtype_df = pd.DataFrame(
            quality["dtype_summary"].items(),
            columns=["Column", "Data Type"]
        )
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### ✅ Sales = Quantity × Unit Price")

    mm_count = quality["sales_mismatch_count"]
    if mm_count == 0:
        st.success(
            "All Sales values match Quantity × Unit Price. "
            "The dataset is internally consistent."
        )
    else:
        st.warning(
            f"{mm_count} rows ({quality['sales_mismatch_pct']}%) had Sales values "
            f"that didn't match Quantity × Unit Price. "
            f"These have been automatically **recomputed** in the loaded dataset."
        )

    st.markdown("#### 📊 Sample of Cleaned Data (first 10 rows)")
    st.dataframe(df_full.head(10), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 – BRANCH & CITY
# ═══════════════════════════════════════════════════════════════════════════════
with tab_branch:
    st.markdown('<div class="section-header">Branch & City Performance</div>', unsafe_allow_html=True)

    # Summary table
    st.markdown("#### 📋 Branch Summary Table")
    disp_branch = df_branch.rename(columns={
        "Total_Revenue": "Total Revenue (₹)",
        "Transactions": "Transactions",
        "Avg_Transaction": "Avg Transaction (₹)",
        "Avg_Rating": "Avg Rating",
        "Revenue_Share_%": "Revenue Share (%)",
    })
    st.dataframe(
        disp_branch.style.format({
            "Total Revenue (₹)": "₹{:,.2f}",
            "Avg Transaction (₹)": "₹{:,.2f}",
            "Avg Rating": "{:.2f}",
            "Revenue Share (%)": "{:.2f}%",
        }),
        use_container_width=True, hide_index=True
    )

    b1, b2 = st.columns(2)
    with b1:
        st.plotly_chart(ch.branch_revenue_bar(df_branch), use_container_width=True, key="branch_rev_bar")
    with b2:
        st.plotly_chart(ch.branch_avg_rating_bar(df_branch), use_container_width=True, key="branch_rating_bar")

    st.plotly_chart(ch.category_branch_heatmap(pivot), use_container_width=True, key="branch_heatmap")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 – CATEGORY & PRODUCT
# ═══════════════════════════════════════════════════════════════════════════════
with tab_cat:
    st.markdown('<div class="section-header">Category & Product Analysis</div>', unsafe_allow_html=True)

    st.markdown("#### 📋 Category Summary Table")
    disp_cat = df_cat.rename(columns={
        "Total_Revenue": "Total Revenue (₹)",
        "Transactions": "Transactions",
        "Total_Units": "Units Sold",
        "Avg_Unit_Price": "Avg Unit Price (₹)",
        "Avg_Rating": "Avg Rating",
        "Revenue_Share_%": "Revenue Share (%)",
    })
    st.dataframe(
        disp_cat.style.format({
            "Total Revenue (₹)": "₹{:,.2f}",
            "Avg Unit Price (₹)": "₹{:,.2f}",
            "Avg Rating": "{:.2f}",
            "Revenue Share (%)": "{:.2f}%",
        }),
        use_container_width=True, hide_index=True
    )

    c1c, c2c = st.columns(2)
    with c1c:
        st.plotly_chart(ch.category_revenue_bar(df_cat), use_container_width=True, key="cat_rev_bar")
    with c2c:
        st.plotly_chart(ch.category_pie(df_cat), use_container_width=True, key="cat_pie")

    st.markdown("---")
    st.markdown("#### 🏅 Top Products")

    n_top = st.slider("Number of top products to display", min_value=5, max_value=20, value=10, step=5)
    st.plotly_chart(ch.top_products_bar(df_prod, n=n_top), use_container_width=True, key="top_products_bar")

    st.markdown("#### 📋 Full Product Table")
    disp_prod = df_prod.rename(columns={
        "Total_Revenue": "Total Revenue (₹)",
        "Transactions": "Transactions",
        "Total_Units": "Units Sold",
        "Avg_Unit_Price": "Avg Unit Price (₹)",
        "Avg_Rating": "Avg Rating",
    })
    st.dataframe(
        disp_prod.style.format({
            "Total Revenue (₹)": "₹{:,.2f}",
            "Avg Unit Price (₹)": "₹{:,.2f}",
            "Avg Rating": "{:.2f}",
        }),
        use_container_width=True, hide_index=True
    )

    st.markdown("---")
    st.markdown("#### 🔬 Unit Price vs Sales Scatter")
    st.plotly_chart(ch.price_vs_sales_scatter(df), use_container_width=True, key="cat_scatter")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 – CUSTOMER ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_customer:
    st.markdown('<div class="section-header">Customer Analysis</div>', unsafe_allow_html=True)

    ct1, ct2 = st.columns(2)

    with ct1:
        st.markdown("#### 💳 Customer Type")
        disp_ct = df_ct.rename(columns={
            "Total_Revenue": "Total Revenue (₹)",
            "Transactions": "Transactions",
            "Avg_Transaction": "Avg Transaction (₹)",
            "Avg_Rating": "Avg Rating",
            "Revenue_Share_%": "Revenue Share (%)",
        })
        st.dataframe(
            disp_ct.style.format({
                "Total Revenue (₹)": "₹{:,.2f}",
                "Avg Transaction (₹)": "₹{:,.2f}",
                "Avg Rating": "{:.2f}",
                "Revenue Share (%)": "{:.2f}%",
            }),
            use_container_width=True, hide_index=True
        )
        st.plotly_chart(ch.customer_type_donut(df_ct), use_container_width=True, key="cust_type_donut")

    with ct2:
        st.markdown("#### ⚥ Gender")
        disp_g = df_gender.rename(columns={
            "Total_Revenue": "Total Revenue (₹)",
            "Transactions": "Transactions",
            "Avg_Transaction": "Avg Transaction (₹)",
            "Revenue_Share_%": "Revenue Share (%)",
        })
        st.dataframe(
            disp_g.style.format({
                "Total Revenue (₹)": "₹{:,.2f}",
                "Avg Transaction (₹)": "₹{:,.2f}",
                "Revenue Share (%)": "{:.2f}%",
            }),
            use_container_width=True, hide_index=True
        )
        st.plotly_chart(ch.gender_bar(df_gender), use_container_width=True, key="cust_gender_bar")

    st.markdown("---")
    st.markdown("#### ⭐ Rating Distribution")
    disp_r = df_rating.rename(columns={
        "Rating_Band": "Rating Band",
        "Count": "Transactions",
        "Avg_Sales": "Avg Sales (₹)",
    })
    rc1, rc2 = st.columns([2, 3])
    with rc1:
        st.dataframe(
            disp_r.style.format({"Avg Sales (₹)": "₹{:,.2f}"}),
            use_container_width=True, hide_index=True
        )
    with rc2:
        st.plotly_chart(ch.rating_bar(df_rating), use_container_width=True, key="cust_rating_bar")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 – PAYMENT
# ═══════════════════════════════════════════════════════════════════════════════
with tab_pay:
    st.markdown('<div class="section-header">Payment Method Analysis</div>', unsafe_allow_html=True)

    disp_pay = df_pay.rename(columns={
        "Total_Revenue": "Total Revenue (₹)",
        "Transactions": "Transactions",
        "Avg_Transaction": "Avg Transaction (₹)",
        "Revenue_Share_%": "Revenue Share (%)",
    })
    st.dataframe(
        disp_pay.style.format({
            "Total Revenue (₹)": "₹{:,.2f}",
            "Avg Transaction (₹)": "₹{:,.2f}",
            "Revenue Share (%)": "{:.2f}%",
        }),
        use_container_width=True, hide_index=True
    )

    p1, p2 = st.columns(2)
    with p1:
        st.plotly_chart(ch.payment_pie(df_pay), use_container_width=True, key="pay_pie")
    with p2:
        st.plotly_chart(ch.payment_bar(df_pay), use_container_width=True, key="pay_bar")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 7 – TIME TRENDS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_time:
    st.markdown('<div class="section-header">Sales Trends Over Time</div>', unsafe_allow_html=True)

    st.plotly_chart(ch.daily_sales_line(df_ts), use_container_width=True, key="time_daily_line")
    st.plotly_chart(ch.monthly_sales_bar(df_ms), use_container_width=True, key="time_monthly_bar")

    st.markdown("#### 📋 Monthly Summary Table")
    disp_ms = df_ms.rename(columns={
        "Total_Revenue": "Total Revenue (₹)",
        "Transactions": "Transactions",
    })
    st.dataframe(
        disp_ms.style.format({"Total Revenue (₹)": "₹{:,.2f}"}),
        use_container_width=True, hide_index=True
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 8 – BUSINESS INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_insights:
    st.markdown('<div class="section-header">Business Insights & Recommendations</div>', unsafe_allow_html=True)
    st.markdown(
        "The following insights are automatically derived from the data. "
        "They reflect patterns in the current filtered dataset."
    )
    st.markdown("<br>", unsafe_allow_html=True)

    insights = generate_insights(kpis, df_branch, df_cat, df_prod, df_ct, df_pay, df_ms, df_rating)

    for ins in insights:
        css_class = f"insight-{ins['type']}"
        st.markdown(
            f'<div class="{css_class}">'
            f'<div class="insight-title">{ins["icon"]} {ins["title"]}</div>'
            f'<div class="insight-detail">{ins["detail"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 9 – RAW DATA
# ═══════════════════════════════════════════════════════════════════════════════
with tab_raw:
    st.markdown('<div class="section-header">Raw Data Explorer</div>', unsafe_allow_html=True)
    st.markdown(
        f"Displaying **{len(df):,}** rows matching the current filters. "
        "Adjust sidebar filters to narrow the view."
    )

    search_term = st.text_input("🔍 Search (Invoice ID, Product, Category, City, Branch)", "")
    if search_term:
        mask = df.apply(lambda col: col.astype(str).str.contains(search_term, case=False, na=False)).any(axis=1)
        display_df = df[mask]
    else:
        display_df = df

    st.dataframe(
        display_df.style.format({
            "Unit Price": "₹{:.2f}",
            "Sales": "₹{:.2f}",
        }),
        use_container_width=True,
        height=520,
    )

    # Download button
    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="filtered_supermarket_sales.csv",
        mime="text/csv",
    )

# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#57606a; font-size:0.8rem;'>"
    "Supermarket Sales Analytics · Built with Streamlit & Plotly · Made with IBM Bob"
    "</div>",
    unsafe_allow_html=True,
)
