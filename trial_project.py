# ==================================================
# MOBILE MODERN FBI BANCASSURANCE
# REAL-TIME EXCEL (UPLOAD SAFE VERSION)
# ==================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="FBI Bancassurance",
    page_icon="📊",
    layout="centered"
)

# ==================================================
# STYLE (HIGH CONTRAST - SAFE)
# ==================================================
st.markdown("""
<style>
html, body {
    background-color: #F2F4F8;
    color: #020617;
}
.block-container {
    padding: 1.2rem 1rem 2rem 1rem;
}
.header-title {
    font-size: 1.9rem;
    font-weight: 800;
}
.header-subtitle {
    font-size: 0.85rem;
    color: #475569;
    margin-bottom: 1.4rem;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin: 1.4rem 0 0.6rem 0;
}
.card {
    background: #FFFFFF;
    padding: 16px;
    border-radius: 16px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    margin-bottom: 12px;
}
.metric-title {
    font-size: 0.8rem;
    color: #475569;
    font-weight: 600;
}
.metric-value {
    font-size: 1.45rem;
    font-weight: 800;
}
.small {
    font-size: 0.75rem;
    color: #64748B;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.markdown('<div class="header-title">Daily FBI Bancassurance</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="header-subtitle">as {datetime.now().strftime("%d %B %Y")}</div>',
    unsafe_allow_html=True
)

# ==================================================
# FILE UPLOADER (KEY FIX)
# ==================================================
uploaded_file = st.file_uploader(
    "📂 Upload data_fbi.xlsx",
    type=["xlsx"]
)

if uploaded_file is None:
    st.warning("Silakan upload file Excel terlebih dahulu.")
    st.stop()

# ==================================================
# LOAD DATA SAFELY
# ==================================================
@st.cache_data(ttl=60)
def load_data(file):
    return {
        "kpi": pd.read_excel(file, sheet_name="kpi"),
        "amfs": pd.read_excel(file, sheet_name="amfs"),
        "jiwa": pd.read_excel(file, sheet_name="jiwa"),
        "kebakaran": pd.read_excel(file, sheet_name="kebakaran"),
        "trend": pd.read_excel(file, sheet_name="daily_trend")
    }

data = load_data(uploaded_file)

# ==================================================
# KPI CARDS
# ==================================================
st.markdown('<div class="section-title">Key Highlights</div>', unsafe_allow_html=True)
cols = st.columns(len(data["kpi"]))

for col, row in zip(cols, data["kpi"].itertuples()):
    col.markdown(f"""
    <div class="card">
        <div class="metric-title">{row.metric}</div>
        <div class="metric-value">{row.value} {row.unit}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# AMFS
# ==================================================
st.markdown('<div class="section-title">AMFS Snapshot</div>', unsafe_allow_html=True)
for _, r in data["amfs"].iterrows():
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">{r['metric']}</div>
        <div class="metric-value">{r['value']} {r['unit']}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# JIWA
# ==================================================
st.markdown('<div class="section-title">Rabat Jiwa</div>', unsafe_allow_html=True)
for _, r in data["jiwa"].iterrows():
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">{r['metric']}</div>
        <div class="metric-value">Rp {r['value']} M</div>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# KEBAKARAN
# ==================================================
st.markdown('<div class="section-title">Rabat Kebakaran</div>', unsafe_allow_html=True)
for _, r in data["kebakaran"].iterrows():
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">{r['metric']}</div>
        <div class="metric-value">Rp {r['value']} M</div>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# DAILY TREND
# ==================================================
st.markdown('<div class="section-title">Daily Trend FBI</div>', unsafe_allow_html=True)

fig, ax = plt.subplots()
ax.plot(data["trend"]["hk"], data["trend"]["dec25"], label="Dec '25")
ax.plot(data["trend"]["hk"], data["trend"]["jan26"], label="Jan '26")
ax.set_xlabel("HK")
ax.set_ylabel("Rp M")
ax.legend()
ax.grid(True)

st.pyplot(fig, use_container_width=True)

# ==================================================
# FOOTNOTE
# ==================================================
st.markdown("""
<div class="small">
* Data akan auto-refresh setiap 60 detik setelah Excel diperbarui.
</div>
""", unsafe_allow_html=True)
