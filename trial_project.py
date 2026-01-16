# ==================================================
# MOBILE MODERN – FBI BANCASSURANCE (FIXED VISIBILITY)
# ==================================================

import streamlit as st
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
# STRONG HIGH-CONTRAST STYLE (SAFE FOR MOBILE)
# ==================================================
st.markdown("""
<style>
/* Force light mode look */
html, body, [class*="css"] {
    background-color: #F2F4F8 !important;
    color: #111827 !important;
}

/* Main container */
.block-container {
    padding: 1.2rem 1rem 2rem 1rem;
}

/* Header */
.header-title {
    font-size: 1.9rem;
    font-weight: 800;
    color: #0F172A;
}
.header-subtitle {
    font-size: 0.9rem;
    color: #475569;
    margin-bottom: 1.4rem;
}

/* Section title */
.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #020617;
    margin: 1.3rem 0 0.6rem 0;
}

/* Card */
.card {
    background-color: #FFFFFF;
    padding: 16px;
    border-radius: 16px;
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
    margin-bottom: 14px;
}

/* Metric */
.metric-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: #475569;
}
.metric-value {
    font-size: 1.45rem;
    font-weight: 800;
    color: #020617;
    margin-top: 2px;
}

/* Small note */
.small {
    font-size: 0.75rem;
    color: #64748B;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.markdown(
    '<div class="header-title">Daily FBI Bancassurance</div>',
    unsafe_allow_html=True
)
st.markdown(
    f'<div class="header-subtitle">as {datetime.now().strftime("%d %B %Y")}</div>',
    unsafe_allow_html=True
)

# ==================================================
# KPI SUMMARY
# ==================================================
st.markdown('<div class="section-title">Key Highlights</div>', unsafe_allow_html=True)

k1, k2, k3 = st.columns(3)

with k1:
    st.markdown("""
    <div class="card">
        <div class="metric-title">FBI Daily</div>
        <div class="metric-value">Rp 3,01 M</div>
        <div class="small">Jan 2026</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="card">
        <div class="metric-title">MTD FBI</div>
        <div class="metric-value">Rp 9,14 M</div>
        <div class="small">Accumulated</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="card">
        <div class="metric-title">Conversion Rate</div>
        <div class="metric-value">27%</div>
        <div class="small">All Channel</div>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# AMFS SNAPSHOT
# ==================================================
st.markdown('<div class="section-title">AMFS Snapshot</div>', unsafe_allow_html=True)

amfs_cards = [
    ("NAM Leads", "10.969", "Leads"),
    ("CC NB", "2.917", "Polis"),
    ("APE NB", "Rp 74,67 M", ""),
    ("Premi NB", "Rp 227,2 M", "")
]

for title, value, unit in amfs_cards:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="small">{unit}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# RABAT JIWA
# ==================================================
st.markdown('<div class="section-title">Rabat Jiwa</div>', unsafe_allow_html=True)

for title, value in [
    ("Booking", "Rp 5,65 M"),
    ("Premi", "Rp 66,92 M"),
    ("Potensi FBI", "Rp 8,23 M"),
    ("Progress", "Rp 0,03 M")
]:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# RABAT KEBAKARAN
# ==================================================
st.markdown('<div class="section-title">Rabat Kebakaran</div>', unsafe_allow_html=True)

for title, value in [
    ("Booking", "Rp 2,75 M"),
    ("Premi", "Rp 5,14 M"),
    ("Potensi FBI", "Rp 1,03 M"),
    ("Progress", "Rp 0,05 M")
]:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# DAILY TREND CHART
# ==================================================
st.markdown('<div class="section-title">Daily Trend FBI</div>', unsafe_allow_html=True)

hk = list(range(1, 24))
dec25 = [0.4,0.5,0.7,0.6,1.0,1.8,1.4,1.3,1.5,1.2,1.0,0.8,1.1,1.9,1.6,1.8,2.0,1.7,3.5,6.2,0,0,0]
jan26 = [0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,0.9,1.1,1.0,0.9,1.2,1.3,1.4,1.6,1.7,1.8,2.1,0,0,0,0]

fig, ax = plt.subplots()
ax.plot(hk, dec25, label="Dec '25")
ax.plot(hk, jan26, label="Jan '26")

ax.set_xlabel("HK")
ax.set_ylabel("Rp M")
ax.grid(True)
ax.legend()

st.pyplot(fig, use_container_width=True)

# ==================================================
# FOOTNOTE
# ==================================================
st.markdown("""
<div class="small">
* Rekonsiliasi booking Dec '25 seluruh asuradur diestimasi selesai pada 20 Jan 2026.
</div>
""", unsafe_allow_html=True)
