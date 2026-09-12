# 🛒 Supermarket Sales Analytics Dashboard

A full-featured data analytics dashboard for supermarket sales, built with **Python**, **Streamlit**, and **Plotly**.

---

## 📊 Features

| Tab | What it shows |
|---|---|
| **Overview** | KPI cards, category pie, daily revenue trend, sales box plot |
| **Data Quality** | Missing values, dtype check, Sales = Qty × Price verification |
| **Branch & City** | Revenue by branch, ratings, category × branch heatmap |
| **Category & Product** | Revenue rankings, top products, scatter plot |
| **Customer Analysis** | Member vs Normal, gender split, rating distribution |
| **Payment** | Revenue and transaction count by payment method |
| **Time Trends** | Daily line chart with 7-day MA, monthly bar chart |
| **Business Insights** | 10 auto-generated recommendations |
| **Raw Data** | Searchable table with CSV download |

---

## 🗂️ Project Structure

```
supermarket_analytics/
├── app.py                  ← Streamlit entry point
├── requirements.txt
├── data/
│   └── supermarket_sales.csv
└── modules/
    ├── data_loader.py      ← Load, validate, clean data
    ├── analytics.py        ← KPIs, aggregations, pivot tables
    ├── charts.py           ← All Plotly chart builders
    └── insights.py         ← Auto business insights
```

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## ☁️ Deploy on Streamlit Community Cloud (Free)

1. Fork or push this repo to your GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** → select this repo → set main file to `app.py`
4. Click **Deploy** — you get a free public URL!

---

## 📦 Dataset

- **File:** `data/supermarket_sales.csv`
- **Rows:** 500 transactions
- **Columns:** Invoice ID, Date, Branch, City, Customer Type, Gender, Product, Category, Quantity, Unit Price, Payment, Rating, Sales

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io) — Frontend dashboard
- [Plotly](https://plotly.com/python/) — Interactive charts
- [Pandas](https://pandas.pydata.org) — Data manipulation
- [NumPy](https://numpy.org) — Numerical operations

---

*Made with IBM Bob*
