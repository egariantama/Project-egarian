import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Tunggakan Klaim",
    page_icon="📊",
    layout="centered"
)

# ==================================================
# CSS MOBILE APP STYLE
# ==================================================
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.main .block-container{
    max-width:420px;
    margin:auto;
    padding-top:1rem;
    padding-bottom:5rem;
}

.stApp{
    background-color:#F4F7FC;
}

.app-header{
    background:linear-gradient(135deg,#0052CC,#007BFF);
    padding:20px;
    border-radius:20px;
    color:white;
    margin-bottom:15px;
}

.kpi-card{
    background:white;
    border-radius:18px;
    padding:15px;
    box-shadow:0px 3px 12px rgba(0,0,0,0.08);
    text-align:center;
}

.kpi-title{
    color:#888;
    font-size:12px;
}

.kpi-value{
    font-size:22px;
    font-weight:700;
    color:#111;
}

.section-title{
    font-size:18px;
    font-weight:700;
    margin-top:15px;
    margin-bottom:10px;
}

.rank-card{
    background:white;
    border-radius:18px;
    padding:15px;
    margin-bottom:10px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.06);
}

.priority-card{
    background:white;
    border-left:5px solid #ff4b4b;
    border-radius:15px;
    padding:15px;
    margin-bottom:10px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.06);
}

.bottom-nav{
    position:fixed;
    bottom:0;
    left:50%;
    transform:translateX(-50%);
    width:420px;
    background:white;
    border-top:1px solid #ddd;
    padding:10px;
    text-align:center;
    z-index:999;
}

.bottom-nav span{
    margin:0 10px;
    font-size:22px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# DATA DUMMY
# ==================================================
aging_df = pd.DataFrame({
    "Kategori":[
        "0-30 Hari",
        "31-60 Hari",
        "61-90 Hari",
        ">90 Hari"
    ],
    "Jumlah":[450,320,280,206]
})

asuransi_df = pd.DataFrame({
    "Asuransi":[
        "Asuransi ABC",
        "Asuransi XYZ",
        "Asuransi DEF",
        "Asuransi GHI",
        "Asuransi JKL"
    ],
    "Outstanding":[
        2500000000,
        1800000000,
        1200000000,
        950000000,
        700000000
    ]
})

priority_df = pd.DataFrame({
    "Polis":[
        "POL00123456",
        "POL00987654",
        "POL00543210"
    ],
    "Outstanding":[
        "Rp150 Jt",
        "Rp120 Jt",
        "Rp95 Jt"
    ],
    "Aging":[
        "125 Hari",
        "115 Hari",
        "101 Hari"
    ]
})

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div class="app-header">
    <h3>📋 Dashboard Klaim</h3>
    <p>Monitoring Tunggakan Klaim Asuransi</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# KPI CARDS
# ==================================================
col1,col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Outstanding Klaim</div>
        <div class="kpi-value">Rp12,5 M</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Pembayaran Klaim</div>
        <div class="kpi-value">Rp3,2 M</div>
    </div>
    """, unsafe_allow_html=True)

col3,col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Kasus</div>
        <div class="kpi-value">1.256</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Avg Aging</div>
        <div class="kpi-value">47 Hari</div>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# AGING
# ==================================================
st.markdown(
    '<div class="section-title">📈 Aging Klaim</div>',
    unsafe_allow_html=True
)

fig = px.pie(
    aging_df,
    names="Kategori",
    values="Jumlah",
    hole=0.65
)

fig.update_layout(
    height=350,
    margin=dict(l=10,r=10,t=10,b=10),
    showlegend=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# RANKING ASURANSI
# ==================================================
st.markdown(
    '<div class="section-title">🏆 Top Outstanding Asuransi</div>',
    unsafe_allow_html=True
)

for i,row in asuransi_df.iterrows():

    medal = "🏅"

    if i == 0:
        medal = "🥇"

    elif i == 1:
        medal = "🥈"

    elif i == 2:
        medal = "🥉"

    nominal = f"Rp {row['Outstanding']/1000000000:.1f} M"

    st.markdown(f"""
    <div class="rank-card">
        <b>{medal} {row['Asuransi']}</b><br>
        Outstanding : {nominal}
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# PRIORITAS PENAGIHAN
# ==================================================
st.markdown(
    '<div class="section-title">🚨 Prioritas Penagihan</div>',
    unsafe_allow_html=True
)

for _,row in priority_df.iterrows():

    st.markdown(f"""
    <div class="priority-card">
        <b>{row['Polis']}</b><br><br>
        Outstanding : {row['Outstanding']}<br>
        Aging : {row['Aging']}
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# DETAIL DATA
# ==================================================
st.markdown(
    '<div class="section-title">📄 Detail Klaim</div>',
    unsafe_allow_html=True
)

detail = pd.DataFrame({
    "Polis":[
        "POL00123456",
        "POL00987654",
        "POL00543210",
        "POL00333333",
        "POL00777777"
    ],
    "Area":[
        "Jakarta",
        "Medan",
        "Surabaya",
        "Makassar",
        "Bandung"
    ],
    "Outstanding":[
        150000000,
        120000000,
        95000000,
        85000000,
        65000000
    ],
    "Aging":[
        125,
        115,
        101,
        88,
        75
    ]
})

st.dataframe(
    detail,
    use_container_width=True,
    hide_index=True
)

# ==================================================
# DOWNLOAD
# ==================================================
csv = detail.to_csv(index=False).encode('utf-8')

st.download_button(
    "⬇ Download Data",
    csv,
    "klaim.csv",
    "text/csv"
)

# ==================================================
# BOTTOM NAVIGATION
# ==================================================
st.markdown("""
<div class="bottom-nav">
<span>🏠</span>
<span>📋</span>
<span>📈</span>
<span>👤</span>
</div>
""", unsafe_allow_html=True)
