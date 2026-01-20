import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Fee Income by Asuradur | Bank Mandiri",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================================================
# CUSTOM CSS (MANDIRI STYLE)
# ==================================================
st.markdown("""
<style>
body {
    background-color: #F4F6F9;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.header {
    background: linear-gradient(135deg, #003A8F, #0052CC);
    padding: 18px;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 16px;
}

.card {
    background: white;
    padding: 16px;
    border-radius: 16px;
    margin-bottom: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}

.kpi {
    font-size: 28px;
    font-weight: 800;
    color: #003A8F;
}

.sub {
    font-size: 13px;
    color: #6b7280;
}

.green { color: #16a34a; font-weight: 600; }
.red { color: #dc2626; font-weight: 600; }
.orange { color: #f59e0b; font-weight: 600; }

.rank {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid #e5e7eb;
}
.rank:last-child {
    border-bottom: none;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div class="header">
    <h3>Fee Income by Asuradur</h3>
    <div style="font-size:13px;">Bank Mandiri • January 2024</div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# FILTER (SIMPLE)
# ==================================================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("📅 Period", ["January 2024"])
    with col2:
        st.selectbox("📍 Region", ["All Regions"])
    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# KPI OVERVIEW
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Performance Overview</div>", unsafe_allow_html=True)
st.markdown("<div class='kpi'>IDR 375,800,000</div>", unsafe_allow_html=True)
st.markdown("<span class='green'>▲ 14.7% vs Last Month</span>", unsafe_allow_html=True)
st.progress(0.893)
st.markdown("<div class='sub'>Achievement: 89.3% of IDR 420M</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# DATA
# ==================================================
data = pd.DataFrame({
    "Asuradur": ["Sinarmas MSIG", "Manulife", "AXA Mandiri", "Allianz", "BNI Life"],
    "FBI": [99, 95, 85.2, 63.2, 32.8],
    "Growth": [18.2, 16.9, 12.4, 9.8, -7.5]
})

# ==================================================
# DONUT CHART
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### Fee Income Breakdown")

fig, ax = plt.subplots(figsize=(4,4))
colors = ["#003A8F", "#F4C430", "#00A651", "#4DA3FF", "#9CA3AF"]

ax.pie(
    data["FBI"],
    labels=None,
    startangle=90,
    colors=colors,
    wedgeprops=dict(width=0.35)
)
ax.text(0, 0, "26.5%\nSinarmas\nMSIG", ha='center', va='center', fontsize=12, fontweight='bold')

st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# RANKING LIST
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### Asuradur Ranking")

for i, row in data.iterrows():
    growth_class = "green" if row["Growth"] >= 0 else "red"
    arrow = "▲" if row["Growth"] >= 0 else "▼"

    st.markdown(f"""
    <div class="rank">
        <div><b>{i+1}. {row['Asuradur']}</b></div>
        <div style="text-align:right;">
            <div><b>{row['FBI']} M</b></div>
            <div class="{growth_class}">{arrow} {row['Growth']}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# INSIGHT / ALERT
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.markdown("⚠️ <span class='orange'><b>BNI Life perlu perhatian khusus (-7.5% MoM)</b></span>",
            unsafe_allow_html=True)

st.markdown("✅ <span class='green'><b>Sinarmas MSIG memimpin dengan kontribusi 26.5%</b></span>",
            unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# FOOTER
# ==================================================
st.markdown("""
<div style="text-align:center; font-size:12px; color:#9ca3af;">
© 2026 Bancassurance Performance Report – Bank Mandiri
</div>
""", unsafe_allow_html=True)
