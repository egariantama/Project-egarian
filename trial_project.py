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
# HEADER
# =========================
st.title("📊 Bancassurance Performance Report")
st.caption("Nilai Pertanggungan & Fee Based Income (Rp Miliar)")

# =========================
# UPLOAD EXCEL
# =========================
st.sidebar.header("📤 Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload Excel Bancassurance",
    type=["xlsx"]
)

if uploaded_file is None:
    st.warning("⚠️ Silakan upload file Excel terlebih dahulu")
    st.stop()

# =========================
# LOAD DATA
# =========================
df = pd.read_excel(uploaded_file)

required_cols = [
    "Tipe_Kerjasama", "Jenis_Asuransi", "Asuradur",
    "NP_Nov24", "NP_Dec24", "NP_Nov25",
    "FBI_Nov24", "FBI_Dec24", "FBI_Nov25"
]

missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"❌ Kolom berikut tidak ditemukan di Excel: {missing_cols}")
    st.stop()

# =========================
# DATA PREP
# =========================
num_cols = required_cols[3:]
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

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
st.sidebar.header("🔎 Filter")
tipe_filter = st.sidebar.multiselect(
    "Tipe Kerjasama",
    df["Tipe_Kerjasama"].unique(),
    default=df["Tipe_Kerjasama"].unique()
)

filtered = df[df["Tipe_Kerjasama"].isin(tipe_filter)]

# =========================
# KPI SUMMARY
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
    st.metric(
        "Growth NP YoY (%)",
        f"{(filtered['NP_Growth_YoY'].sum() / filtered['NP_Nov24'].sum() * 100):.1f}%"
        if filtered["NP_Nov24"].sum() > 0 else "0%"
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
        f"{(filtered['FBI_Growth_YoY'].sum() / filtered['FBI_Nov24'].sum() * 100):.1f}%"
        if filtered["FBI_Nov24"].sum() > 0 else "0%"
    )

# =========================
# DETAIL TABLE
# =========================
st.subheader("📋 Detail Performance")

display_cols = [
    "Tipe_Kerjasama", "Jenis_Asuransi", "Asuradur",
    "NP_Nov24", "NP_Dec24", "NP_Nov25",
    "NP_Growth_YTD", "NP_Growth_YTD_%",
    "NP_Growth_YoY", "NP_Growth_YoY_%",
    "FBI_Nov24", "FBI_Dec24", "FBI_Nov25",
    "FBI_Growth_YoY",
