"""
insights.py
-----------
Rule-based business insight generator derived from analytics DataFrames.
"""

import pandas as pd


def generate_insights(
    kpis: dict,
    df_branch: pd.DataFrame,
    df_cat: pd.DataFrame,
    df_prod: pd.DataFrame,
    df_ct: pd.DataFrame,
    df_pay: pd.DataFrame,
    df_ms: pd.DataFrame,
    df_rating: pd.DataFrame,
) -> list[dict]:
    """
    Return a list of insight dicts:
        { "icon": str, "title": str, "detail": str, "type": "success"|"warning"|"info" }
    """
    insights = []

    # ── Best Branch ───────────────────────────────────────────────────────────
    best_branch = df_branch.iloc[0]
    insights.append({
        "icon": "🏆",
        "title": f"Top Branch: {best_branch['Branch']} ({best_branch['City']})",
        "detail": (
            f"Branch {best_branch['Branch']} in {best_branch['City']} generated "
            f"₹{best_branch['Total_Revenue']:,.2f} in revenue "
            f"({best_branch['Revenue_Share_%']}% of total) "
            f"with an average rating of {best_branch['Avg_Rating']:.2f}."
        ),
        "type": "success",
    })

    # ── Worst Branch ──────────────────────────────────────────────────────────
    worst_branch = df_branch.iloc[-1]
    insights.append({
        "icon": "⚠️",
        "title": f"Underperforming Branch: {worst_branch['Branch']} ({worst_branch['City']})",
        "detail": (
            f"Branch {worst_branch['Branch']} in {worst_branch['City']} has the lowest revenue "
            f"at ₹{worst_branch['Total_Revenue']:,.2f}. "
            f"Consider targeted promotions or inventory expansion."
        ),
        "type": "warning",
    })

    # ── Best Category ─────────────────────────────────────────────────────────
    best_cat = df_cat.iloc[0]
    insights.append({
        "icon": "📦",
        "title": f"Best-Selling Category: {best_cat['Category']}",
        "detail": (
            f"{best_cat['Category']} leads with ₹{best_cat['Total_Revenue']:,.2f} revenue "
            f"across {best_cat['Transactions']} transactions "
            f"({best_cat['Revenue_Share_%']}% share). "
            f"Prioritise shelf space and stock levels."
        ),
        "type": "success",
    })

    # ── Weakest Category ──────────────────────────────────────────────────────
    weak_cat = df_cat.iloc[-1]
    insights.append({
        "icon": "📉",
        "title": f"Low-Revenue Category: {weak_cat['Category']}",
        "detail": (
            f"{weak_cat['Category']} contributes only {weak_cat['Revenue_Share_%']}% of revenue. "
            f"Evaluate pricing, placement, or bundling strategies."
        ),
        "type": "warning",
    })

    # ── Top Product ───────────────────────────────────────────────────────────
    top_prod = df_prod.iloc[0]
    insights.append({
        "icon": "⭐",
        "title": f"Top Product: {top_prod['Product']}",
        "detail": (
            f"'{top_prod['Product']}' ({top_prod['Category']}) is the highest-grossing product "
            f"with ₹{top_prod['Total_Revenue']:,.2f} from {top_prod['Transactions']} transactions. "
            f"Ensure consistent availability."
        ),
        "type": "success",
    })

    # ── Customer Type ─────────────────────────────────────────────────────────
    if len(df_ct) >= 2:
        ct_sorted = df_ct.sort_values("Total_Revenue", ascending=False)
        top_ct = ct_sorted.iloc[0]
        low_ct = ct_sorted.iloc[1]
        if top_ct["Customer Type"] == "Member":
            insights.append({
                "icon": "💳",
                "title": "Members Drive More Revenue",
                "detail": (
                    f"Members account for {top_ct['Revenue_Share_%']}% of total revenue. "
                    f"Investing in a loyalty programme rewards and membership drives is recommended."
                ),
                "type": "info",
            })
        else:
            insights.append({
                "icon": "💡",
                "title": "Normal Customers Lead Revenue",
                "detail": (
                    f"Non-member customers generate {top_ct['Revenue_Share_%']}% of revenue. "
                    f"A conversion campaign to convert them into members could boost retention."
                ),
                "type": "info",
            })

    # ── Payment Method ────────────────────────────────────────────────────────
    top_pay = df_pay.sort_values("Transactions", ascending=False).iloc[0]
    insights.append({
        "icon": "💰",
        "title": f"Most-Used Payment Method: {top_pay['Payment']}",
        "detail": (
            f"{top_pay['Payment']} is used in {top_pay['Transactions']} transactions. "
            f"Ensure payment terminals for this method are always operational."
        ),
        "type": "info",
    })

    # ── Monthly Trend ─────────────────────────────────────────────────────────
    if len(df_ms) >= 2:
        peak_month = df_ms.sort_values("Total_Revenue", ascending=False).iloc[0]
        low_month = df_ms.sort_values("Total_Revenue").iloc[0]
        insights.append({
            "icon": "📅",
            "title": f"Peak Month: {peak_month['Month']}",
            "detail": (
                f"{peak_month['Month']} recorded the highest monthly revenue of "
                f"₹{peak_month['Total_Revenue']:,.2f}. "
                f"Replicate successful campaigns from this period."
            ),
            "type": "success",
        })
        insights.append({
            "icon": "📆",
            "title": f"Slowest Month: {low_month['Month']}",
            "detail": (
                f"{low_month['Month']} had the lowest revenue at ₹{low_month['Total_Revenue']:,.2f}. "
                f"Consider seasonal offers or flash sales to boost off-peak performance."
            ),
            "type": "warning",
        })

    # ── Rating ────────────────────────────────────────────────────────────────
    avg_rating = kpis["Avg Rating"]
    if avg_rating >= 4.0:
        insights.append({
            "icon": "😊",
            "title": f"Strong Customer Satisfaction (Avg Rating: {avg_rating})",
            "detail": "Average rating is above 4.0 — customers are satisfied. Maintain service quality.",
            "type": "success",
        })
    elif avg_rating >= 3.5:
        insights.append({
            "icon": "😐",
            "title": f"Moderate Customer Satisfaction (Avg Rating: {avg_rating})",
            "detail": "Average rating is between 3.5 and 4.0. There is room to improve staff service and product quality.",
            "type": "warning",
        })
    else:
        insights.append({
            "icon": "😟",
            "title": f"Low Customer Satisfaction (Avg Rating: {avg_rating})",
            "detail": "Average rating is below 3.5. Immediate action is needed to improve the shopping experience.",
            "type": "warning",
        })

    return insights
