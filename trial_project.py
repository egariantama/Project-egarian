import streamlit as st
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="BancaSmart | Bancassurance Dashboard",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
body { background-color: #F5F7FA; }
.main-title { font-size: 32px; font-weight: bold; color: #003366; }
.sub-title { font-size: 16px; color: #6c757d; }
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
}
.metric-value { font-size: 26px; font-weight: bold; color: #0d6efd; }
.metric-label { color: #6c757d; }
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD EXCEL DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_excel(
        "data/data_nasabah_bancassurance.xlsx",
        sheet_name="DATA"
    )

df = load_data()

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.title("Filter Data")
min_dana, max_dana = st.sidebar.slider(
    "Dana Nasabah (Juta)",
    int(df["Dana_Juta"].min()),
    int(df["Dana_Juta"].max()),
    (
        int(df["Dana_Juta"].min()),
        int(df["Dana_Juta"].max())
    )
)

filtered_df = df[
    (df["Dana_Juta"] >= min_dana) &
    (df["Dana_Juta"] <= max_dana)
]

menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Cross-Sell Recommendation", "Simulation Impact"]
)

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.markdown("<div class='main-title'>BancaSmart Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Monitoring Kinerja Bancassurance</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class='card'>
            <div class='metric-label'>Total Nasabah</div>
            <div class='metric-value'>{len(filtered_df)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='card'>
            <div class='metric-label'>Total Dana</div>
            <div class='metric-value'>Rp {filtered_df['Dana_Juta'].sum():,.0f} Jt</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        high_potential = filtered_df[filtered_df["Dana_Juta"] > 1000]
        st.markdown(f"""
        <div class='card'>
            <div class='metric-label'>High Potential</div>
            <div class='metric-value'>{len(high_potential)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        penetration = round(
            (filtered_df["Produk_Dimiliki"] != "None").mean() * 100, 1
        )
        st.markdown(f"""
        <div class='card'>
            <div class='metric-label'>Insurance Penetration</div>
            <div class='metric-value'>{penetration}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📋 Data Nasabah")
    st.dataframe(filtered_df, use_container_width=True)

# =========================
# RECOMMENDATION ENGINE
# =========================
elif menu == "Cross-Sell Recommendation":

    st.markdown("<div class='main-title'>Cross-Sell Recommendation</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Rekomendasi Otomatis Produk Asuransi</div>", unsafe_allow_html=True)

    def recommend(row):
        if row["Dana_Juta"] > 1000:
            return "Whole Life / Legacy"
        elif row["Usia"] < 35:
            return "Health Insurance"
        else:
            return "Life Protection"

    filtered_df["Rekomendasi Produk"] = filtered_df.apply(recommend, axis=1)
    filtered_df["Priority"] = np.where(
        filtered_df["Dana_Juta"] > 1000, "HIGH", "MEDIUM"
    )

    st.dataframe(
        filtered_df[
            ["Nasabah", "Dana_Juta", "Usia", "Produk_Dimiliki", "Rekomendasi Produk", "Priority"]
        ],
        use_container_width=True
    )

# =========================
# SIMULATION
# =========================
elif menu == "Simulation Impact":

    st.markdown("<div class='main-title'>Simulation & Financial Impact</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Simulasi Kontribusi Bancassurance</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        nasabah = st.number_input("Jumlah Prospek", 10, 1000, 100)
    with col2:
        success_rate = st.slider("Success Rate (%)", 5, 80, 25)
    with col3:
        premi = st.number_input("Rata-rata Premi (Juta)", 5, 500, 30)

    gwp = nasabah * (success_rate / 100) * premi

    st.metric("Proyeksi GWP", f"Rp {gwp:,.1f} Juta")
    st.metric("Estimasi Fee Based Income", f"Rp {gwp * 0.25:,.1f} Juta")
