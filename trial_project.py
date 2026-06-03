import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Insurance Collection",
    page_icon="📊",
    layout="centered"
)

# =====================================================
# CSS PREMIUM MOBILE
# =====================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

.stApp {
    background: #0F172A;
}

.main .block-container{
    max-width:430px;
    padding-top:1rem;
    padding-bottom:100px;
}

div[data-testid="stToolbar"]{
    display:none;
}

section[data-testid="stSidebar"]{
    display:none;
}

.hero-card{
    background: linear-gradient(
        135deg,
        #2563EB,
        #7C3AED
    );

    padding:24px;
    border-radius:28px;
    color:white;
    margin-bottom:18px;
    box-shadow:0 10px 30px rgba(0,0,0,.25);
}

.hero-title{
    font-size:14px;
    opacity:.8;
}

.hero-value{
    font-size:36px;
    font-weight:800;
    margin-top:10px;
}

.hero-sub{
    margin-top:8px;
    font-size:13px;
    opacity:.8;
}

.metric-card{
    background:#1E293B;
    border-radius:24px;
    padding:18px;
    text-align:center;
    color:white;
}

.metric-label{
    color:#94A3B8;
    font-size:12px;
}

.metric-value{
    font-size:22px;
    font-weight:700;
}

.section-title{
    color:white;
    font-size:18px;
    font-weight:700;
    margin-top:20px;
    margin-bottom:10px;
}

.rank-card{
    background:#1E293B;
    border-radius:22px;
    padding:16px;
    margin-bottom:10px;
    color:white;
}

.alert-card{
    background:#1E293B;
    border-left:5px solid #EF4444;
    border-radius:20px;
    padding:16px;
    margin-bottom:10px;
    color:white;
}

.progress-wrap{
    background:#1E293B;
    padding:18px;
    border-radius:24px;
}

.bottom-nav{
    position:fixed;
    bottom:12px;
    left:50%;
    transform:translateX(-50%);
    width:390px;
    background:rgba(30,41,59,.85);
    backdrop-filter:blur(20px);
    border-radius:24px;
    padding:14px;
    text-align:center;
    color:white;
    z-index:999;
}

.bottom-nav span{
    margin:0 18px;
    font-size:22px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div style="color:white;">
<h4>👋 Selamat Datang</h4>
<p>Dashboard Tunggakan Asuransi</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# HERO CARD
# =====================================================

st.markdown("""
<div class="hero-card">
    <div class="hero-title">
        Outstanding Klaim
    </div>

    <div class="hero-value">
        Rp 12,5 M
    </div>

    <div class="hero-sub">
        ▼ 8% dibanding bulan lalu
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# KPI
# =====================================================

c1,c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">
            Pembayaran
        </div>

        <div class="metric-value">
            Rp 3,2 M
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">
            Total Kasus
        </div>

        <div class="metric-value">
            1.256
        </div>
    </div>
    """, unsafe_allow_html=True)

c3,c4 = st.columns(2)

with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">
            Avg Aging
        </div>

        <div class="metric-value">
            47 Hari
        </div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">
            Recovery
        </div>

        <div class="metric-value">
            82%
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# AGING
# =====================================================

st.markdown(
    '<div class="section-title">📈 Aging Distribution</div>',
    unsafe_allow_html=True
)

fig = go.Figure()

fig.add_trace(go.Bar(
    y=["0-30","31-60","61-90",">90"],
    x=[45,30,15,10],
    orientation='h'
))

fig.update_layout(
    height=250,
    paper_bgcolor="#0F172A",
    plot_bgcolor="#0F172A",
    font_color="white",
    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP INSURANCE
# =====================================================

st.markdown(
    '<div class="section-title">🏆 Top Outstanding</div>',
    unsafe_allow_html=True
)

ranking = [
    ("🥇","Asuransi ABC","Rp 2,5 M"),
    ("🥈","Asuransi XYZ","Rp 1,8 M"),
    ("🥉","Asuransi DEF","Rp 1,2 M"),
]

for medal,nama,nilai in ranking:

    st.markdown(f"""
    <div class="rank-card">
        <b>{medal} {nama}</b><br>
        Outstanding : {nilai}
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# PRIORITY CASE
# =====================================================

st.markdown(
    '<div class="section-title">🚨 Prioritas Penagihan</div>',
    unsafe_allow_html=True
)

priority = [
    ("POL00123456","Rp150 Jt","125 Hari"),
    ("POL00987654","Rp120 Jt","115 Hari"),
    ("POL00888888","Rp95 Jt","101 Hari")
]

for polis,outstanding,aging in priority:

    st.markdown(f"""
    <div class="alert-card">
        <b>{polis}</b><br><br>
        Outstanding : {outstanding}<br>
        Aging : {aging}
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# DETAIL
# =====================================================

st.markdown(
    '<div class="section-title">📄 Detail Klaim</div>',
    unsafe_allow_html=True
)

df = pd.DataFrame({
    "Polis":[
        "POL00123456",
        "POL00987654",
        "POL00888888",
        "POL00777777"
    ],
    "Area":[
        "Jakarta",
        "Medan",
        "Surabaya",
        "Makassar"
    ],
    "Outstanding":[
        150000000,
        120000000,
        95000000,
        85000000
    ],
    "Aging":[
        125,
        115,
        101,
        95
    ]
})

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# DOWNLOAD
# =====================================================

csv = df.to_csv(index=False).encode()

st.download_button(
    "⬇ Export Data",
    csv,
    "klaim.csv",
    "text/csv"
)

# =====================================================
# NAVIGATION
# =====================================================

st.markdown("""
<div class="bottom-nav">
<span>🏠</span>
<span>📈</span>
<span>📋</span>
<span>👤</span>
</div>
""", unsafe_allow_html=True)
