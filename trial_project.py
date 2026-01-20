import streamlit as st
import pandas as pd
import numpy as np

# ==================================================
# PAGE CONFIG (Mobile + Executive)
# ==================================================
st.set_page_config(
    page_title="Daily FBI Bancassurance",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================================================
# STYLE
# ==================================================
st.markdown("""
<style>
body { background-color: #F4F6F9; }
.block-container { padding-top: 1rem; }

.card {
    background: white;
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 14px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}

.kpi {
    font-size: 26px;
    font-weight: 800;
}

.sub { color: #6b7280; font-size: 13px; }

.green { color: #16a34a; font-weight: 600; }
.red { color: #dc2626; font-weight: 600; }
.orange { color: #f59e0b; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div style="text-align:center;">
    <h3>📊 Daily Monitoring FBI Bancassurance</h3>
    <div class="sub">As of 15 January 2026</div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# FILTER
# ==================================================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    product = st.selectbox("Produk", ["AMFS", "Rabat Jiwa", "Rabat Kebakaran"])
    period = st.selectbox("Periode", ["Daily", "MTD"])
    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# LEADING INDICATOR
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 🔵 Leading Indicator (Activity)")

col1, col2, col3 = st.columns(3)
col1.metric("NAM Leads", "12.874", "-46%")
col2.metric("CC NB (Polis)", "2.246", "-71%")
col3.metric("Conversion Rate", "17%", "-15%")

st.markdown(
    "<span class='red'>⚠️ Leads dan conversion turun signifikan → risiko penurunan FBI.</span>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# LAGGING INDICATOR
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 🟢 Lagging Indicator (Output & FBI)")

col1, col2 = st.columns(2)
col1.metric("APE NB", "Rp 31,79 M")
col2.metric("Premi NB", "Rp 59,28 M")

col3, col4 = st.columns(2)
col3.metric("FBI Daily", "Rp 5,06 M")
col4.metric("FBI Accrue", "Rp 11,19 M")

st.markdown(
    "<span class='orange'>📌 FBI masih terbantu backlog Desember.</span>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# FBI BY PRODUCT (SIMPLE)
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 📦 Potensi FBI by Product")

fbi_product = pd.DataFrame({
    "Product": ["AMFS", "Rabat Jiwa", "Rabat Kebakaran"],
    "Potensi FBI (Rp M)": [8.23, 0.99, 0.99]
}).set_index("Product")

st.bar_chart(fbi_product)

st.markdown(
    "<span class='green'>✔ Kontributor utama: AMFS (>80%).</span>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# DAILY TREND
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 📈 Daily FBI Trend")

trend = pd.DataFrame({
    "HK": list(range(1, 24)),
    "Avg Jan–Dec 25": np.random.uniform(0.8, 1.6, 23),
    "Jan 26": np.random.uniform(0.6, 2.2, 23),
}).set_index("HK")

st.line_chart(trend)

st.markdown(
    "<span class='orange'>📉 FBI harian masih di bawah rata-rata historis.</span>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# EXECUTIVE SUMMARY
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 🧠 Executive Insight")

st.markdown("""
- 🔴 **Leading indicator melemah** (leads & conversion).
- 🟡 **Lagging masih aman** karena backlog.
- 🔵 **AMFS menjadi tumpuan utama FBI.**
- ⚠️ Risiko penurunan FBI **1–2 minggu ke depan** bila tidak ada intervensi.
""")

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# FOOTER
# ==================================================
st.markdown("""
<div style="text-align:center; font-size:12px; color:#9ca3af;">
© 2026 Bancassurance Performance Monitoring
</div>
""", unsafe_allow_html=True)
