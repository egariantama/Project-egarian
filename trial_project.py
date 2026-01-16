# ==================================================
# MOBILE MODERN – FBI BANCASSURANCE DASHBOARD
# ==================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ==================================================
# PAGE CONFIG (MOBILE FIRST)
# ==================================================
st.set_page_config(
    page_title="FBI Bancassurance",
    page_icon="📊",
    layout="centered"
)

# ==================================================
# GLOBAL STYLE (MOBILE MODERN)
# ==================================================
st.markdown("""
<style>
body {
    background-color: #F5F7FA;
}
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}
.header-title {
    font-size: 1.8rem;
    font-weight: 800;
}
.header-subtitle {
    font-size: 0.9rem;
    color: #6B7280;
    margin-bottom: 1.2rem;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin: 1.2rem 0 0.6rem 0;
}
.card {
    background: white;
    padding: 14px;
    border-radius: 14px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.05);
    margin-bottom: 12px;
}
.metric-title {
    font-size: 0.85rem;
    color: #6B7280;
}
.metric-value {
    font-size: 1.4rem;
    font-weight: 800;
}
.small {
    font-size: 0.75rem;
    color: #9CA3AF;
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
# KPI SUMMARY (TOP CARDS)
# ==================================================
st.markdown('<div class="section-title">Key Highlights</div>', unsafe_allow_html=True)

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.markdown("""
    <div class="card">
        <div class="metric-title">FBI Daily</div>
        <div class="metric-value">Rp 3,01 M</div>
        <div class="small">Jan 2026</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
    <div class="card">
        <div class="metric-title">MTD FBI</div>
        <div class="metric-value">Rp 9,14 M</div>
        <div class="small">Accumulated</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
    <div class="card">
        <div class="metric-title">Conv. Rate</div>
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

jiwa_metrics = [
    ("Booking", "Rp 5,65 M"),
    ("Premi", "Rp 66,92 M"),
    ("Potensi FBI", "Rp 8,23 M"),
    ("Progress", "Rp 0,03 M")
]

for title, value in jiwa_metrics:
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

kebakaran_metrics = [
    ("Booking", "Rp 2,75 M"),
    ("Premi", "Rp 5,14 M"),
    ("Potensi FBI", "Rp 1,03 M"),
    ("Progress", "Rp 0,05 M")
]

for title, value in kebakaran_metrics:
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

ax.set_ylabel("Rp M")
ax.set_xlabel("HK")
ax.grid(True)
ax.legend()

st.pyplot(fig, use_container_width=True)

# ==================================================
# FOOTNOTE
# ==================================================
st.markdown("""
<div class="small">
* Rekonsiliasi booking Dec '25 seluruh asuradur diestimasi selesai 20 Jan '26.
</div>
""", unsafe_allow_html=True)
