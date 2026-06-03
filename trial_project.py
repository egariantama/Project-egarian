import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="Dashboard Tunggakan Klaim",
    page_icon="📊",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}

.metric-card {
    background: white;
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}

.kpi-title {
    color: #6b7280;
    font-size: 14px;
}

.kpi-value {
    font-size: 32px;
    font-weight: bold;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("📋 Dashboard Tunggakan Klaim Asuransi")
st.caption("Monitoring Outstanding Klaim Bermasalah")

# =========================
# FILTER
# =========================
with st.sidebar:
    st.header("Filter")
    area = st.multiselect(
        "Area",
        ["Jakarta", "Medan", "Surabaya", "Makassar"],
        default=["Jakarta", "Medan", "Surabaya", "Makassar"]
    )

# =========================
# KPI
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Outstanding Tunggakan Klaim",
        "Rp 12,50 M",
        "+8%"
    )

with col2:
    st.metric(
        "Total Pembayaran Klaim",
        "Rp 3,20 M",
        "+15%"
    )

with col3:
    st.metric(
        "Jumlah Kasus Tertunggak",
        "1.256",
        "+45"
    )

with col4:
    st.metric(
        "Rata-rata Aging",
        "47 Hari",
        "-3 Hari"
    )

st.divider()

# =========================
# AGING CLAIM
# =========================
st.subheader("📈 Aging Klaim")

aging_df = pd.DataFrame({
    "Kategori": [
        "0-30 Hari",
        "31-60 Hari",
        "61-90 Hari",
        ">90 Hari"
    ],
    "Jumlah": [
        450,
        320,
        280,
        206
    ]
})

col1, col2 = st.columns([1,1])

with col1:
    fig = px.pie(
        aging_df,
        names="Kategori",
        values="Jumlah",
        hole=0.55
    )

    fig.update_layout(
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:
    st.dataframe(
        aging_df,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# =========================
# OUTSTANDING PER ASURANSI
# =========================
st.subheader("🏢 Outstanding per Asuransi")

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

fig = px.bar(
    asuransi_df,
    x="Outstanding",
    y="Asuransi",
    orientation="h",
    text_auto=True
)

fig.update_layout(
    height=400
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# OUTSTANDING PER AREA
# =========================
st.subheader("📍 Outstanding per Area")

area_df = pd.DataFrame({
    "Area":[
        "Jakarta",
        "Medan",
        "Surabaya",
        "Makassar"
    ],
    "Outstanding":[
        4500000000,
        2800000000,
        2100000000,
        1600000000
    ]
})

fig = px.bar(
    area_df,
    x="Area",
    y="Outstanding",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =========================
# PRIORITAS PENAGIHAN
# =========================
st.subheader("🚨 Prioritas Penagihan (>90 Hari)")

priority_df = pd.DataFrame({
    "Nomor Polis":[
        "POL00123456",
        "POL00987654",
        "POL00543210",
        "POL00112233",
        "POL00445566"
    ],
    "Asuransi":[
        "ABC",
        "XYZ",
        "DEF",
        "GHI",
        "JKL"
    ],
    "Outstanding":[
        150000000,
        120000000,
        95000000,
        80000000,
        70000000
    ],
    "Aging":[
        125,
        115,
        101,
        97,
        93
    ]
})

st.dataframe(
    priority_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# =========================
# DETAIL KLAIM
# =========================
st.subheader("📄 Detail Klaim")

detail_df = pd.DataFrame({
    "Nomor Polis":[
        "POL00123456",
        "POL00987654",
        "POL00543210",
        "POL00112233",
        "POL00445566"
    ],
    "Nama Nasabah":[
        "Andi",
        "Budi",
        "Citra",
        "Dewi",
        "Eko"
    ],
    "Area":[
        "Jakarta",
        "Medan",
        "Surabaya",
        "Makassar",
        "Jakarta"
    ],
    "Outstanding":[
        150000000,
        120000000,
        95000000,
        80000000,
        70000000
    ],
    "Aging":[
        125,
        115,
        101,
        97,
        93
    ]
})

st.dataframe(
    detail_df,
    use_container_width=True,
    hide_index=True
)

# =========================
# EXPORT
# =========================
csv = detail_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Data Klaim",
    data=csv,
    file_name="data_klaim.csv",
    mime="text/csv"
)
