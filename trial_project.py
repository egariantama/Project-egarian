import streamlit as st
import pandas as pd
import numpy as np

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Bancassurance Performance Report",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_excel(
        "data/bancassurance_report.xlsx",
        sheet_name="DATA"
    )

df = load_data()

# =========================
# CALCULATION
# =========================
df["NP_Growth_YTD"] = df["NP_Nov25"] - df["NP_Dec24"]
df["NP_Growth_YoY"] = df["NP_Nov25"] - df["NP_Nov24"]

df["FBI_Growth_YoY"] = df["FBI_Nov25"] - df["FBI_Nov24"]

df["NP_Growth_YTD_%"] = np.where(
    df["NP_Dec24"] > 0,
    df["NP_Growth_YTD"] / df["NP_Dec24"] * 100,
    0
)

df["NP_Growth_YoY_%"] = np.where(
    df["NP_Nov24"] > 0,
    df["NP_Growth_YoY"] / df["NP_Nov24"] * 100,
    0
)

df["FBI_Growth_YoY_%"] = np.where(
    df["FBI_Nov24"] > 0,
    df["FBI_Growth_YoY"] / df["FBI_Nov24"] * 100,
    0
)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Filter")
tipe = st.sidebar.multiselect(
    "Tipe Kerjasama",
    df["Tipe_Kerjasama"].unique(),
    default=df["Tipe_Kerjasama"].unique()
)

filtered = df[df["Tipe_Kerjasama"].isin(tipe)]

# =========================
# HEADER
# =========================
st.title("📊 Bancassurance Performance Report")
st.caption("Nilai Pertanggungan & Fee Based Income (Rp Miliar)")

# =========================
# KPI SUMMARY
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total NP Nov-25",
        f"{filtered['NP_Nov25'].sum():,.0f}",
        f"{filtered['NP_Growth_YoY'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Growth NP YoY (%)",
        f"{filtered['NP_Growth_YoY_%'].mean():.1f}%"
    )

with col3:
    st.metric(
        "Total FBI Nov-25",
        f"{filtered['FBI_Nov25'].sum():,.2f}",
        f"{filtered['FBI_Growth_YoY'].sum():,.2f}"
    )

with col4:
    st.metric(
        "Growth FBI YoY (%)",
        f"{filtered['FBI_Growth_YoY_%'].mean():.1f}%"
    )

# =========================
# TABLE VIEW (REPORT STYLE)
# =========================
st.subheader("📋 Detail Performance")

report_view = filtered[[
    "Tipe_Kerjasama", "Jenis_Asuransi", "Asuradur",
    "NP_Nov24", "NP_Dec24", "NP_Nov25",
    "NP_Growth_YTD", "NP_Growth_YTD_%",
    "NP_Growth_YoY", "NP_Growth_YoY_%",
    "FBI_Nov24", "FBI_Dec24", "FBI_Nov25",
    "FBI_Growth_YoY", "FBI_Growth_YoY_%"
]]

st.dataframe(
    report_view.style.format({
        "NP_Nov24": "{:,.0f}",
        "NP_Dec24": "{:,.0f}",
        "NP_Nov25": "{:,.0f}",
        "NP_Growth_YTD": "{:,.0f}",
        "NP_Growth_YTD_%": "{:.1f}%",
        "NP_Growth_YoY": "{:,.0f}",
        "NP_Growth_YoY_%": "{:.1f}%",
        "FBI_Nov24": "{:,.2f}",
        "FBI_Dec24": "{:,.2f}",
        "FBI_Nov25": "{:,.2f}",
        "FBI_Growth_YoY": "{:,.2f}",
        "FBI_Growth_YoY_%": "{:.1f}%"
    }),
    use_container_width=True
)

# =========================
# SUBTOTAL
# =========================
st.subheader("📌 Subtotal by Tipe Kerjasama")

subtotal = filtered.groupby("Tipe_Kerjasama").sum(numeric_only=True).reset_index()

st.dataframe(subtotal, use_container_width=True)

# =========================
# CHART
# =========================
st.subheader("📈 NP & FBI Growth YoY")

st.bar_chart(
    filtered.set_index("Jenis_Asuransi")[["NP_Growth_YoY", "FBI_Growth_YoY"]]
)
