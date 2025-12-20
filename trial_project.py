import streamlit as st
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIG (MOBILE READY)
# =========================
st.set_page_config(
    page_title="Bancassurance Digital Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# GLOBAL STYLE (DIGITAL LOOK)
# =========================
st.markdown("""
<style>
.metric-card {
    background: #0f172a;
    padding: 16px;
    border-radius: 14px;
    color: white;
}
.small-text {
    font-size: 12px;
    opacity: 0.7;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("📊 Bancassurance Digital Dashboard")
st.caption("Nilai Pertanggungan & Fee Based Income")

# =========================
# SIDEBAR MENU
# =========================
st.sidebar.title("🧭 Menu")
menu = st.sidebar.radio(
    "Navigasi",
    ["Dashboard", "Detail Performance", "Subtotal", "Chart"]
)

st.sidebar.divider()

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.sidebar.file_uploader(
    "📤 Upload CSV dari Excel",
    type=["csv"]
)

if uploaded_file is None:
    st.info("📌 Upload file **CSV** terlebih dahulu")
    st.stop()

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(uploaded_file)

required_cols = [
    "Tipe_Kerjasama", "Jenis_Asuransi", "Asuradur",
    "NP_Nov24", "NP_Dec24", "NP_Nov25",
    "FBI_Nov24", "FBI_Dec24", "FBI_Nov25"
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"❌ Kolom tidak ditemukan: {missing}")
    st.stop()

num_cols = [
    "NP_Nov24", "NP_Dec24", "NP_Nov25",
    "FBI_Nov24", "FBI_Dec24", "FBI_Nov25"
]

df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

# =========================
# CALCULATION
# =========================
df["NP_Growth_YTD"] = df["NP_Nov25"] - df["NP_Dec24"]
df["NP_Growth_YTD_%"] = np.where(df["NP_Dec24"] > 0, df["NP_Growth_YTD"] / df["NP_Dec24"] * 100, 0)

df["NP_Growth_YoY"] = df["NP_Nov25"] - df["NP_Nov24"]
df["NP_Growth_YoY_%"] = np.where(df["NP_Nov24"] > 0, df["NP_Growth_YoY"] / df["NP_Nov24"] * 100, 0)

df["FBI_Growth_YoY"] = df["FBI_Nov25"] - df["FBI_Nov24"]
df["FBI_Growth_YoY_%"] = np.where(df["FBI_Nov24"] > 0, df["FBI_Growth_YoY"] / df["FBI_Nov24"] * 100, 0)

# =========================
# FILTER
# =========================
st.sidebar.subheader("🔎 Filter")
tipe = st.sidebar.multiselect(
    "Tipe Kerjasama",
    df["Tipe_Kerjasama"].unique(),
    default=df["Tipe_Kerjasama"].unique()
)

df_f = df[df["Tipe_Kerjasama"].isin(tipe)]

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":
    st.subheader("📌 Executive Summary")

    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    c1.metric("Total NP Nov-25", f"{df_f['NP_Nov25'].sum():,.0f}")
    c2.metric(
        "Growth NP YoY (%)",
        f"{(df_f['NP_Growth_YoY'].sum()/df_f['NP_Nov24'].sum()*100 if df_f['NP_Nov24'].sum()>0 else 0):.1f}%"
    )
    c3.metric("Total FBI Nov-25", f"{df_f['FBI_Nov25'].sum():,.2f}")
    c4.metric(
        "Growth FBI YoY (%)",
        f"{(df_f['FBI_Growth_YoY'].sum()/df_f['FBI_Nov24'].sum()*100 if df_f['FBI_Nov24'].sum()>0 else 0):.1f}%"
    )

# =========================
# DETAIL PERFORMANCE
# =========================
elif menu == "Detail Performance":
    st.subheader("📋 Detail Performance")

    display_cols = [
        "Tipe_Kerjasama", "Jenis_Asuransi", "Asuradur",
        "NP_Nov24", "NP_Dec24", "NP_Nov25",
        "NP_Growth_YTD", "NP_Growth_YTD_%",
        "NP_Growth_YoY", "NP_Growth_YoY_%",
        "FBI_Nov24", "FBI_Dec24", "FBI_Nov25",
        "FBI_Growth_YoY", "FBI_Growth_YoY_%"
    ]

    st.dataframe(
        df_f[display_cols],
        use_container_width=True,
        height=520
    )

# =========================
# SUBTOTAL
# =========================
elif menu == "Subtotal":
    st.subheader("📌 Subtotal per Tipe Kerjasama")

    subtotal = df_f.groupby("Tipe_Kerjasama", as_index=False).sum(numeric_only=True)
    st.dataframe(subtotal, use_container_width=True)

# =========================
# CHART
# =========================
elif menu == "Chart":
    st.subheader("📈 Growth YoY Comparison")

    chart = (
        df_f.groupby("Jenis_Asuransi")[["NP_Growth_YoY", "FBI_Growth_YoY"]]
        .sum()
    )

    st.bar_chart(chart)
