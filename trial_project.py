import streamlit as st
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Bancassurance Performance Report",
    layout="wide"
)

# =========================
# TITLE
# =========================
st.title("📊 Bancassurance Performance Report")
st.caption("Nilai Pertanggungan & Fee Based Income (Rp Miliar)")

# =========================
# SIDEBAR - UPLOAD FILE
# =========================
st.sidebar.header("📤 Upload Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload file Excel (.xlsx) atau CSV",
    type=["xlsx", "csv"]
)

if uploaded_file is None:
    st.warning("⚠️ Silakan upload file terlebih dahulu")
    st.stop()

# =========================
# LOAD DATA (ROBUST)
# =========================
try:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        # explicit engine to avoid Python 3.13 issue
        df = pd.read_excel(uploaded_file, engine="openpyxl")
except Exception as e:
    st.error("❌ Gagal membaca file")
    st.exception(e)
    st.stop()

# =========================
# REQUIRED COLUMNS
# =========================
required_cols = [
    "Tipe_Kerjasama",
    "Jenis_Asuransi",
    "Asuradur",
    "NP_Nov24",
    "NP_Dec24",
    "NP_Nov25",
    "FBI_Nov24",
    "FBI_Dec24",
    "FBI_Nov25"
]

missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"❌ Kolom berikut tidak ditemukan: {missing_cols}")
    st.stop()

# =========================
# DATA PREPARATION
# =========================
numeric_cols = [
    "NP_Nov24",
    "NP_Dec24",
    "NP_Nov25",
    "FBI_Nov24",
    "FBI_Dec24",
    "FBI_Nov25"
]

df[numeric_cols] = (
    df[numeric_cols]
    .apply(pd.to_numeric, errors="coerce")
    .fillna(0)
)

# =========================
# CALCULATION
# =========================
df["NP_Growth_YTD"] = df["NP_Nov25"] - df["NP_Dec24"]
df["NP_Growth_YTD_%"] = np.where(
    df["NP_Dec24"] > 0,
    df["NP_Growth_YTD"] / df["NP_Dec24"] * 100,
    0
)

df["NP_Growth_YoY"] = df["NP_Nov25"] - df["NP_Nov24"]
df["NP_Growth_YoY_%"] = np.where(
    df["NP_Nov24"] > 0,
    df["NP_Growth_YoY"] / df["NP_Nov24"] * 100,
    0
)

df["FBI_Growth_YoY"] = df["FBI_Nov25"] - df["FBI_Nov24"]
df["FBI_Growth_YoY_%"] = np.where(
    df["FBI_Nov24"] > 0,
    df["FBI_Growth_YoY"] / df["FBI_Nov24"] * 100,
    0
)

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("🔎 Filter Data")

tipe_filter = st.sidebar.multiselect(
    "Tipe Kerjasama",
    options=df["Tipe_Kerjasama"].unique(),
    default=df["Tipe_Kerjasama"].unique()
)

filtered = df[df["Tipe_Kerjasama"].isin(tipe_filter)]

# =========================
# EXECUTIVE SUMMARY
# =========================
st.subheader("📌 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total NP Nov-25",
        f"{filtered['NP_Nov25'].sum():,.0f}",
        f"{filtered['NP_Growth_YoY'].sum():,.0f}"
    )

with col2:
    yoy_np_pct = (
        filtered["NP_Growth_YoY"].sum()
        / filtered["NP_Nov24"].sum() * 100
        if filtered["NP_Nov24"].sum() > 0 else 0
    )
    st.metric("Growth NP YoY (%)", f"{yoy_np_pct:.1f}%")

with col3:
    st.metric(
        "Total FBI Nov-25",
        f"{filtered['FBI_Nov25'].sum():,.2f}",
        f"{filtered['FBI_Growth_YoY'].sum():,.2f}"
    )

with col4:
    yoy_fbi_pct = (
        filtered["FBI_Growth_YoY"].sum()
        / filtered["FBI_Nov24"].sum() * 100
        if filtered["FBI_Nov24"].sum() > 0 else 0
    )
    st.metric("Growth FBI YoY (%)", f"{yoy_fbi_pct:.1f}%")

# =========================
# DETAIL TABLE
# =========================
st.subheader("📋 Detail Performance")

display_cols = [
    "Tipe_Kerjasama",
    "Jenis_Asuransi",
    "Asuradur",
    "NP_Nov24",
    "NP_Dec24",
    "NP_Nov25",
    "NP_Growth_YTD",
    "NP_Growth_YTD_%",
    "NP_Growth_YoY",
    "NP_Growth_YoY_%",
    "FBI_Nov24",
    "FBI_Dec24",
    "FBI_Nov25",
    "FBI_Growth_YoY",
    "FBI_Growth_YoY_%"
]

st.dataframe(
    filtered[display_cols].style.format({
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
st.subheader("📌 Subtotal per Tipe Kerjasama")

subtotal = (
    filtered
    .groupby("Tipe_Kerjasama", as_index=False)
    .sum(numeric_only=True)
)

st.dataframe(subtotal, use_container_width=True)

# =========================
# TOTAL
# =========================
st.subheader("🏁 Total Keseluruhan")

total = (
    filtered[numeric_cols + [
        "NP_Growth_YTD",
        "NP_Growth_YoY",
        "FBI_Growth_YoY"
    ]]
    .sum()
    .to_frame("Total")
    .T
)

st.dataframe(total, use_container_width=True)

# =========================
# CHART
# =========================
st.subheader("📈 Growth YoY Comparison")

chart_data = (
    filtered
    .groupby("Jenis_Asuransi")[["NP_Growth_YoY", "FBI_Growth_YoY"]]
    .sum()
)

st.bar_chart(chart_data)
