import streamlit as st
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Bancassurance Digital Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# STYLE CSS
# =========================
st.markdown("""
<style>
h1, h2, h3 {
    font-family: "Segoe UI", sans-serif;
}
.metric-title {
    font-size: 14px;
    color: #6c757d;
}
.metric-value {
    font-size: 24px;
    font-weight: bold;
}
.card {
    background-color: #ffffff;
    padding: 16px;
    border-radius: 10px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}
.sidebar .sidebar-content {
    background-color: #0d47a1;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("📊 Bancassurance Digital Dashboard")
st.write("Laporan Nilai Pertanggungan & Fee Based Income")

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.selectbox(
    "📌 Menu",
    ["Dashboard", "Detail Performance", "Subtotal", "Growth Chart"]
)

uploaded_file = st.sidebar.file_uploader(
    "📤 Upload Data (CSV)",
    type=["csv"]
)

if uploaded_file is None:
    st.sidebar.warning("Upload file CSV dari Excel terlebih dahulu")
    st.stop()

# =========================
# READ DATA
# =========================
try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error("❌ Tidak bisa membaca file CSV")
    st.stop()

required_cols = [
    "Tipe_Kerjasama","Jenis_Asuransi","Asuradur",
    "NP_Nov24","NP_Dec24","NP_Nov25",
    "FBI_Nov24","FBI_Dec24","FBI_Nov25"
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Kolom tidak lengkap: {missing}")
    st.stop()

df[required_cols[3:]] = df[required_cols[3:]].apply(pd.to_numeric, errors="coerce").fillna(0)

# =========================
# CALCULATIONS
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
st.sidebar.markdown("---")
tipe_filter = st.sidebar.multiselect(
    "Filter Tipe Kerjasama",
    df["Tipe_Kerjasama"].unique(),
    default=df["Tipe_Kerjasama"].unique()
)
df = df[df["Tipe_Kerjasama"].isin(tipe_filter)]

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":
    st.subheader("📌 Summary Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("<div class='card'><div class='metric-title'>Total NP Nov-25</div><div class='metric-value'>Rp {:,.0f}</div></div>".format(df["NP_Nov25"].sum()), unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><div class='metric-title'>Growth NP YoY (%)</div><div class='metric-value'>{:.1f}%</div></div>".format(df["NP_Growth_YoY_%"].mean()), unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'><div class='metric-title'>Total FBI Nov-25</div><div class='metric-value'>Rp {:,.2f}</div></div>".format(df["FBI_Nov25"].sum()), unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='card'><div class='metric-title'>Growth FBI YoY (%)</div><div class='metric-value'>{:.1f}%</div></div>".format(df["FBI_Growth_YoY_%"].mean()), unsafe_allow_html=True)

# =========================
# DETAIL PERFORMANCE
elif menu == "Detail Performance":
    st.subheader("📋 Detail Performance")
    disp_cols = [
        "Tipe_Kerjasama","Jenis_Asuransi","Asuradur",
        "NP_Nov24","NP_Dec24","NP_Nov25",
        "NP_Growth_YTD","NP_Growth_YTD_%","NP_Growth_YoY","NP_Growth_YoY_%",
        "FBI_Nov24","FBI_Dec24","FBI_Nov25","FBI_Growth_YoY","FBI_Growth_YoY_%"
    ]
    st.dataframe(df[disp_cols].style.format({
        "NP_Nov24":"{:,.0f}","NP_Nov25":"{:,.0f}","NP_Growth_YTD":"{:,.0f}",
        "NP_Growth_YTD_%":"{:.1f}%","NP_Growth_YoY_%":"{:.1f}%"
    }), use_container_width=True)

# =========================
# SUBTOTAL
elif menu == "Subtotal":
    st.subheader("📌 Subtotal per Tipe Kerjasama")
    st.dataframe(df.groupby("Tipe_Kerjasama", as_index=False).sum(numeric_only=True), use_container_width=True)

# =========================
# CHART
elif menu == "Growth Chart":
    st.subheader("📈 Growth YoY Chart")

    chart_data = df.groupby("Jenis_Asuransi")[["NP_Growth_YoY","FBI_Growth_YoY"]].sum()
    st.bar_chart(chart_data)
