import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Financial Health",
    page_icon="💰",
    layout="centered"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

[data-testid="stAppViewContainer"]{
    background:#F4F7FC;
}

.block-container{
    max-width:430px;
    padding-top:1rem;
    padding-bottom:2rem;
}

.title-app{
    font-size:28px;
    font-weight:700;
    color:#111827;
    margin-bottom:5px;
}

.subtitle-app{
    color:#6B7280;
    font-size:14px;
    margin-bottom:20px;
}

.metric-card{
    background:white;
    padding:18px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 6px 20px rgba(0,0,0,0.06);
}

.metric-label{
    color:#6B7280;
    font-size:13px;
    font-weight:500;
}

.metric-value{
    color:#111827;
    font-size:24px;
    font-weight:700;
}

.insight-card{
    background:white;
    padding:20px;
    border-radius:22px;
    margin-top:15px;
    box-shadow:0 6px 20px rgba(0,0,0,0.06);
}

.card-title{
    color:#111827;
    font-size:18px;
    font-weight:700;
    margin-bottom:12px;
}

.card-text{
    color:#4B5563;
    line-height:1.8;
}

.goal-card{
    background:white;
    padding:20px;
    border-radius:22px;
    margin-top:15px;
    box-shadow:0 6px 20px rgba(0,0,0,0.06);
}

.goal-item{
    color:#111827;
    font-size:15px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# INPUT
# =====================================

st.markdown(
    '<div class="title-app">💰 Financial Health</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle-app">Personal Financial Dashboard</div>',
    unsafe_allow_html=True
)

with st.expander("✏️ Input Financial Data", expanded=True):

    income = st.number_input(
        "Pendapatan Bulanan (Rp)",
        value=10000000
    )

    expense = st.number_input(
        "Pengeluaran Bulanan (Rp)",
        value=6000000
    )

    debt = st.number_input(
        "Cicilan Bulanan (Rp)",
        value=1500000
    )

    investment = st.number_input(
        "Investasi Bulanan (Rp)",
        value=1000000
    )

    emergency_fund = st.number_input(
        "Dana Darurat Saat Ini (Rp)",
        value=15000000
    )

# =====================================
# CALCULATION
# =====================================

saving = income - expense

saving_ratio = (saving / income * 100) if income else 0
debt_ratio = (debt / income * 100) if income else 0
invest_ratio = (investment / income * 100) if income else 0

target_emergency = expense * 6

emergency_ratio = (
    emergency_fund / target_emergency * 100
    if target_emergency > 0 else 0
)

saving_score = min((saving_ratio/20)*25,25)
debt_score = max(25-(debt_ratio/30)*25,0)
invest_score = min((invest_ratio/10)*25,25)
emergency_score = min((emergency_ratio/100)*25,25)

score = round(
    saving_score+
    debt_score+
    invest_score+
    emergency_score
)

score = min(score,100)

# =====================================
# CATEGORY
# =====================================

if score >= 80:
    category = "Sangat Sehat"
    color = "#10B981"
elif score >= 60:
    category = "Cukup Sehat"
    color = "#F59E0B"
elif score >= 40:
    category = "Perlu Perbaikan"
    color = "#EF4444"
else:
    category = "Risiko Tinggi"
    color = "#DC2626"

# =====================================
# GAUGE CHART
# =====================================

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=score,
    number={
        'font':{
            'size':48,
            'color':'#111827'
        }
    },
    gauge={
        'axis':{'range':[0,100]},
        'bar':{'color':color},
        'bgcolor':'white',
        'borderwidth':0,
        'steps':[
            {'range':[0,40],'color':'#FEE2E2'},
            {'range':[40,60],'color':'#FEF3C7'},
            {'range':[60,80],'color':'#DBEAFE'},
            {'range':[80,100],'color':'#D1FAE5'}
        ]
    }
))

fig.update_layout(
    height=280,
    margin=dict(l=20,r=20,t=20,b=20),
    paper_bgcolor="#F4F7FC",
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown(
    f"""
    <div style='text-align:center;
                font-size:22px;
                font-weight:700;
                color:{color};'>
        {category}
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# KPI CARDS
# =====================================

col1,col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">
            Saving Ratio
        </div>
        <div class="metric-value">
            {saving_ratio:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">
            Debt Ratio
        </div>
        <div class="metric-value">
            {debt_ratio:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

col3,col4 = st.columns(2)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">
            Investment Ratio
        </div>
        <div class="metric-value">
            {invest_ratio:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">
            Emergency Fund
        </div>
        <div class="metric-value">
            {emergency_ratio:.0f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================
# AI INSIGHT
# =====================================

insight = f"""
Keuangan Anda berada pada kategori {category.lower()}.

Sisa dana bulanan sebesar
Rp {saving:,.0f}.

Prioritas berikutnya adalah meningkatkan
investasi rutin dan menjaga dana darurat
minimal 6 bulan pengeluaran.
"""

st.markdown(f"""
<div class="insight-card">
<div class="card-title">
💡 AI Insight
</div>

<div class="card-text">
{insight}
</div>
</div>
""", unsafe_allow_html=True)

# =====================================
# GOALS
# =====================================

st.markdown("""
<div class="goal-card">

<div class="card-title">
🎯 Financial Goals
</div>

<div class="goal-item">
✅ Dana Darurat
</div>

<div class="goal-item">
✅ Investasi Rutin
</div>

<div class="goal-item">
🟡 Dana Pensiun
</div>

<div class="goal-item">
🟡 Passive Income
</div>

</div>
""", unsafe_allow_html=True)

# =====================================
# SUMMARY
# =====================================

st.write("")

st.metric(
    "Sisa Dana Bulanan",
    f"Rp {saving:,.0f}"
)
