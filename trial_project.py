# ==================================================
# DAILY MONITORING FBI BANCASSURANCE
# ==================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Daily Monitoring FBI Bancassurance",
    layout="wide"
)

# ==================================================
# STYLE
# ==================================================
st.markdown("""
<style>
.title {
    font-size:32px;
    font-weight:800;
}
.subtitle {
    font-size:14px;
    color:gray;
    margin-bottom:20px;
}
.section {
    font-size:20px;
    font-weight:700;
    margin-top:30px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.markdown(
    '<div class="title">Daily Monitoring Leading & Lagging FBI Bancassurance</div>',
    unsafe_allow_html=True
)
st.markdown(
    f'<div class="subtitle">as {datetime.now().strftime("%d %B %Y")}</div>',
    unsafe_allow_html=True
)

# ==================================================
# DATA - POL FEE BANCASSURANCE (AMFS)
# ==================================================
amfs = pd.DataFrame({
    "Komponen": [
        "NAM Leads","Cabang","Outlet",
        "CC NB","Cabang","Outlet",
        "Conv. Rate","Cabang","Outlet",
        "APE NB","Cabang","Outlet",
        "Premi NB","Retail","HVC",
        "FBI Daily","FBI Accrue"
    ],
    "Satuan": [
        "Leads","Leads","Leads",
        "Polis","Polis","Polis",
        "%","%","%",
        "Rp M","Rp M","Rp M",
        "Rp M","Rp M","Rp M",
        "Rp M","Rp M"
    ],
    "1–29 Dec '25": [
        20724,19530,1194,
        5909,5320,589,
        29,27,49,
        146.06,72.25,73.81,
        419.19,136.77,282.42,
        23.70,25.03
    ],
    "1–9 Dec '25": [
        7779,7376,403,
        1375,1246,129,
        18,17,32,
        30.31,13.80,16.51,
        121.34,35.42,85.91,
        5.85,None
    ],
    "1–31 Dec '25": [
        23819,22272,1547,
        7658,6818,840,
        32,31,54,
        204.12,102.46,101.65,
        544.98,167.73,377.25,
        29.84,None
    ],
    "1–12 Jan '26": [
        7874,7518,356,
        1168,1116,52,
        15,15,15,
        16.61,12.55,4.06,
        101.41,23.14,78.28,
        3.01,None
    ]
})

st.markdown('<div class="section">Pol Fee Bancassurance (AMFS)</div>', unsafe_allow_html=True)
st.dataframe(amfs, use_container_width=True)

# ==================================================
# LAYOUT 2 COLUMNS
# ==================================================
col1, col2 = st.columns(2)

# ==================================================
# POL FEE RABAT JIWA
# ==================================================
with col1:
    jiwa = pd.DataFrame({
        "Komponen": [
            "Booking Asuransi","KPR","KSM","KUM",
            "Premi*","KPR","KSM","KUM",
            "Potensi FBI*","KPR","KSM","KUM",
            "Progres Pembukuan"
        ],
        "Satuan": ["Rp M"] * 13,
        "Nilai": [
            5.648,1.367,2.084,2.197,
            66.92,15.35,33.14,18.43,
            8.23,1.45,3.87,2.92,
            0.03
        ]
    })

    st.markdown('<div class="section">Pol Fee Rabat Jiwa</div>', unsafe_allow_html=True)
    st.dataframe(jiwa, use_container_width=True)

# ==================================================
# POL FEE RABAT KEBAKARAN
# ==================================================
with col2:
    kebakaran = pd.DataFrame({
        "Komponen": [
            "Booking Asuransi","KPR","KUM",
            "Premi*","KPR","KUM",
            "Potensi FBI*","KPR","KUM",
            "Progres Pembukuan"
        ],
        "Satuan": ["Rp M"] * 10,
        "Nilai": [
            2.750,1.367,1.382,
            5.14,3.28,1.86,
            1.03,0.28,0.24,
            0.05
        ]
    })

    st.markdown('<div class="section">Pol Fee Rabat Kebakaran</div>', unsafe_allow_html=True)
    st.dataframe(kebakaran, use_container_width=True)

# ==================================================
# DAILY TREND FBI AMFS
# ==================================================
st.markdown('<div class="section">Daily Trend FBI AMFS (based on Issued Date)</div>', unsafe_allow_html=True)

hk = list(range(1, 24))
dec25 = [0.4,0.5,0.7,0.6,1.0,1.8,1.4,1.3,1.5,1.2,1.0,0.8,1.1,1.9,1.6,1.8,2.0,1.7,3.5,6.2,0,0,0]
jan26 = [0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,0.9,1.1,1.0,0.9,1.2,1.3,1.4,1.6,1.7,1.8,2.1,0,0,0,0]
avg = [1.0] * 23

fig, ax = plt.subplots()
ax.plot(hk, dec25, label="Dec '25")
ax.plot(hk, jan26, label="Jan '26")
ax.plot(hk, avg, linestyle="--", label="Avg Jan–Dec '25")

ax.set_xlabel("HK")
ax.set_ylabel("Rp M")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# ==================================================
# FOOTNOTE
# ==================================================
st.markdown("""
**Catatan:**  
* Proses rekonsiliasi atas booking bulan Dec '25 seluruh asuradur diestimasi selesai pada 20 Jan '26.
""")
