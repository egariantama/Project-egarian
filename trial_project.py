import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Financial Health",
    page_icon="💰",
    layout="centered"
)

# =========================
# CSS PREMIUM FINTECH
# =========================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

[data-testid="stAppViewContainer"]{
    background:linear-gradient(
        180deg,
        #0F172A 0%,
        #1E293B 100%
    );
}

.block-container{
    max-width:430px;
    padding-top:1rem;
    padding-bottom:2rem;
}

.title{
    color:white;
    font-size:30px;
    font-weight:700;
}

.subtitle{
    color:#94A3B8;
    margin-bottom:20px;
}

.hero{
    background:linear-gradient(
        135deg,
        #00C6FF,
        #0072FF
    );
    border-radius:30px;
    padding:25px;
    text-align:center;
    color:white;
    margin-bottom:15px;
    box-shadow:
    0px 15px 40px rgba(0,114,255,.4);
}

.hero-score{
    font-size:72px;
    font-weight:800;
}

.hero-category{
    font-size:22px;
    font-weight:600;
}

.card{
    border-radius:22px;
    padding:20px;
    color:white;
    text-align:center;
    margin-bottom:10px;
}

.metric-label{
    font-size:14px;
}

.metric-value{
    font-size:28px;
    font-weight:700;
}

.insight{
    background:white;
    color:#111827;
    border-radius:25px;
    padding:20px;
    margin-top:15px;
    box-shadow:0 8px 20px rgba(0,0,0,.15);
}

.goal{
    background:white;
    color:#111827;
    border-radius:25px;
    padding:20px;
    margin-top:15px;
    box-shadow:0 8px 20px rgba(0,0,0,.15);
}

.goal-item{
    font-size:17px;
    margin-bottom:10px;
}

.stButton > button{
    background:linear-gradient(
        135deg,
        #00C6FF,
        #0072FF
    );
    color:white;
    border:none;
    border-radius:15px;
    height:55px;
    font-weight:bold;
    width:100%;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown(
    '<div class="title">💰 Financial Health</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Personal Finance Dashboard</div>',
    unsafe_allow_html=True
)

# =========================
# INPUT
# =========================

with st.expander("📋 Input Data Keuangan", expanded=True):

    income = st.number_input(
        "Pendapatan Bulanan",
        min_value=0,
        value=None,
        placeholder="Contoh: 10,000,000"
    )

    expense = st.number_input(
        "Pengeluaran Bulanan",
        min_value=0,
        value=None,
        placeholder="Contoh: 6,000,000"
    )

    debt = st.number_input(
        "Cicilan Bulanan",
        min_value=0,
        value=None,
        placeholder="Contoh: 1,500,000"
    )

    investment = st.number_input(
        "Investasi Bulanan",
        min_value=0,
        value=None,
        placeholder="Contoh: 1,000,000"
    )

    emergency_fund = st.number_input(
        "Dana Darurat Saat Ini",
        min_value=0,
        value=None,
        placeholder="Contoh: 15,000,000"
    )

    proses = st.button(
        "🚀 Analisis Financial Health",
        use_container_width=True
    )

# =========================
# BELUM ANALISIS
# =========================

if not proses:
    st.info(
        "👆 Silakan isi seluruh data keuangan terlebih dahulu, lalu klik tombol Analisis Financial Health."
    )
    st.stop()

# =========================
# VALIDASI
# =========================

if (
    income is None or
    expense is None or
    debt is None or
    investment is None or
    emergency_fund is None
):
    st.error("Semua field wajib diisi.")
    st.stop()

# =========================
# CALCULATION
# =========================

saving = income - expense

saving_ratio = (
    saving / income * 100
    if income > 0 else 0
)

debt_ratio = (
    debt / income * 100
    if income > 0 else 0
)

invest_ratio = (
    investment / income * 100
    if income > 0 else 0
)

target_emergency = expense * 6

emergency_ratio = (
    emergency_fund / target_emergency * 100
    if target_emergency > 0 else 0
)

saving_score = min((saving_ratio / 20) * 25, 25)
debt_score = max(25 - (debt_ratio / 30) * 25, 0)
invest_score = min((invest_ratio / 10) * 25, 25)
emergency_score = min((emergency_ratio / 100) * 25, 25)

score = round(
    saving_score +
    debt_score +
    invest_score +
    emergency_score
)

score = min(score, 100)

# =========================
# CATEGORY
# =========================

if score >= 80:
    category = "🟢 Sangat Sehat"
elif score >= 60:
    category = "🟡 Sehat"
elif score >= 40:
    category = "🟠 Perlu Perbaikan"
else:
    category = "🔴 Risiko Tinggi"

# =========================
# HERO CARD
# =========================

st.markdown(f"""
<div class="hero">

<div style="font-size:22px;">
Financial Health Score
</div>

<div class="hero-score">
{score}
</div>

<div class="hero-category">
{category}
</div>

</div>
""", unsafe_allow_html=True)

# =========================
# GAUGE
# =========================

fig = go.Figure(go.Indicator(
    mode="gauge",
    value=score,
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': '#38BDF8'},
        'steps': [
            {'range': [0, 40], 'color': '#7F1D1D'},
            {'range': [40, 60], 'color': '#92400E'},
            {'range': [60, 80], 'color': '#1E3A8A'},
            {'range': [80, 100], 'color': '#14532D'}
        ]
    }
))

fig.update_layout(
    height=250,
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# KPI CARDS
# =========================

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card" style="background:linear-gradient(135deg,#8B5CF6,#6D28D9)">
        <div class="metric-label">Saving Ratio</div>
        <div class="metric-value">{saving_ratio:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card" style="background:linear-gradient(135deg,#EC4899,#BE185D)">
        <div class="metric-label">Debt Ratio</div>
        <div class="metric-value">{debt_ratio:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown(f"""
    <div class="card" style="background:linear-gradient(135deg,#06B6D4,#2563EB)">
        <div class="metric-label">Investment</div>
        <div class="metric-value">{invest_ratio:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="card" style="background:linear-gradient(135deg,#10B981,#059669)">
        <div class="metric-label">Emergency Fund</div>
        <div class="metric-value">{emergency_ratio:.0f}%</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# AI INSIGHT
# =========================

st.markdown(f"""
<div class="insight">

<h3>💡 AI Insight</h3>

<p>
Anda memiliki sisa dana bulanan sebesar
<b>Rp {saving:,.0f}</b>.
</p>

<p>
Kondisi keuangan Anda saat ini berada pada kategori
<b>{category}</b>.
</p>

<p>
Prioritas berikutnya:
</p>

<ul>
<li>Meningkatkan investasi rutin</li>
<li>Mengurangi utang konsumtif</li>
<li>Menjaga dana darurat minimal 6 bulan pengeluaran</li>
</ul>

</div>
""", unsafe_allow_html=True)

# =========================
# GOALS
# =========================

st.markdown("""
<div class="goal">

<h3>🎯 Financial Goals</h3>

<div class="goal-item">✅ Dana Darurat</div>
<div class="goal-item">✅ Investasi Rutin</div>
<div class="goal-item">🟡 Dana Pensiun</div>
<div class="goal-item">🟡 Passive Income</div>
<div class="goal-item">🔵 Financial Freedom</div>

</div>
""", unsafe_allow_html=True)

# =========================
# SUMMARY
# =========================

st.metric(
    "Sisa Dana Bulanan",
    f"Rp {saving:,.0f}"
)

st.metric(
    "Target Dana Darurat",
    f"Rp {target_emergency:,.0f}"
)
