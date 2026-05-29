import streamlit as st

st.set_page_config(
    page_title="Financial Health",
    page_icon="💰",
    layout="centered"
)

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background:#F4F7FC;
}

.block-container{
    padding-top:1rem;
    max-width:420px;
}

.card{
    background:white;
    padding:20px;
    border-radius:25px;
    box-shadow:0 8px 25px rgba(0,0,0,0.08);
    margin-bottom:15px;
}

.hero{
    background:linear-gradient(135deg,#00C6FF,#0072FF);
    color:white;
    padding:30px;
    border-radius:30px;
    text-align:center;
    box-shadow:0 10px 30px rgba(0,114,255,0.3);
}

.metric-card{
    background:white;
    border-radius:20px;
    padding:15px;
    text-align:center;
    box-shadow:0 5px 15px rgba(0,0,0,0.08);
}

.label{
    color:gray;
    font-size:13px;
}

.value{
    font-size:22px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

score = 82

st.markdown(f"""
<div class="hero">
    <h3>Financial Health Score</h3>
    <h1>{score}</h1>
    <p>Sangat Sehat</p>
</div>
""", unsafe_allow_html=True)

st.write("")

col1,col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="label">Saving Ratio</div>
        <div class="value">28%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="label">Debt Ratio</div>
        <div class="value">15%</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

st.markdown("""
<div class="card">
<h4>💡 AI Insight</h4>

Keuangan Anda berada pada kategori sehat.

Fokus berikutnya adalah meningkatkan investasi dan mempertahankan dana darurat minimal 6 bulan pengeluaran.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<h4>🎯 Financial Goals</h4>

✅ Dana Darurat

✅ Investasi Rutin

🟡 Persiapan Pensiun

🟡 Passive Income
</div>
""", unsafe_allow_html=True)
