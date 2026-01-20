import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ==================================================
# PAGE CONFIG (Mobile Friendly)
# ==================================================
st.set_page_config(
    page_title="Bancassurance | Fee Based Income",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>
body {
    background-color: #F5F7FA;
}
.block-container {
    padding-top: 1rem;
}
.card {
    background: white;
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    margin-bottom: 14px;
}
.kpi {
    font-size: 26px;
    font-weight: 800;
}
.sub {
    color: #6b7280;
    font-size: 13px;
}
.success {
    color: #16a34a;
    font-weight: 600;
}
.danger {
    color: #dc2626;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# DUMMY DATA
# ==================================================
data = {
    "Month": ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr"],
    "Life": [210, 220, 215, 230, 245, 268],
    "Health": [90, 92, 95, 98, 100, 103],
    "Investment": [95, 100, 102, 108, 112, 118],
    "General": [70, 68, 66, 65, 64, 63],
}

df = pd.DataFrame(data)

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div style="text-align:center; margin-bottom:10px;">
    <h2>📊 Fee Based Income</h2>
    <div class="sub">Bancassurance Report</div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# FILTERS
# ==================================================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    period = st.selectbox("📅 Period", ["April 2024", "March 2024", "YTD 2024"])
    region = st.selectbox("📍 Region", ["All Regions", "Jakarta", "Bali Nusra", "Jawa Timur"])
    product = st.selectbox("📦 Product", ["All Products", "Life", "Health", "Investment", "General"])
    channel = st.selectbox("🏦 Channel", ["Branch", "Digital", "RM"])
    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# KPI SECTION
# ==================================================
total_fbi = 550.7
growth = 12.5

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Total Fee Based Income</div>", unsafe_allow_html=True)
st.markdown(f"<div class='kpi'>IDR {total_fbi:,.1f} M</div>", unsafe_allow_html=True)

if growth >= 0:
    st.markdown(f"<div class='success'>▲ {growth}% vs Last Month</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='danger'>▼ {growth}% vs Last Month</div>", unsafe_allow_html=True)

st.markdown("<br>⚠️ <b>Insight:</b> General Insurance mengalami penurunan 5% MoM", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# LINE CHART
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<b>Fee Income Trend</b>", unsafe_allow_html=True)

chart_data = df.set_index("Month")
st.line_chart(chart_data)

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# DONUT CHART (Using Pie)
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<b>Contribution by Product</b>", unsafe_allow_html=True)

pie_data = pd.DataFrame({
    "Product": ["Life", "Health", "Investment", "General"],
    "Value": [268, 103, 118, 63]
})

st.pyplot(
    pie_data.set_index("Product").plot.pie(
        y="Value",
        legend=False,
        autopct='%1.1f%%',
        figsize=(4,4)
    ).figure
)

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# PRODUCT CARDS
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.metric("Life Insurance", "IDR 267.7 M", "+15.8% MoM")
    st.metric("Investment Product", "IDR 117.9 M", "+9.2% MoM")

with col2:
    st.metric("Health Insurance", "IDR 103.3 M", "+10.3% MoM")
    st.metric("General Insurance", "IDR 62.8 M", "-5.0% MoM")

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# FOOTER
# ==================================================
st.markdown("""
<div style="text-align:center; font-size:12px; color:#9ca3af; margin-top:12px;">
© 2026 Bancassurance Performance Dashboard
</div>
""", unsafe_allow_html=True)
