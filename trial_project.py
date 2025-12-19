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
# CUSTOM CSS (MOCKUP DESIGN)
# =========================
st.markdown("""
<style>
body {
    background-color: #F5F7FA;
}
.main-title {
    font-size: 32px;
    font-weight: bold;
    color: #003366;
}
.sub-title {
    font-size: 16px;
    color: #6c757d;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
}
.metric-value {
    font-size: 26px;
    font-weight: bold;
    color: #0d6efd;
}
.metric-label {
    color: #6c757d;
}
.sidebar-title {
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("<div class='sidebar-title'>BancaSmart Menu</div>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "",
    ["Dashboard", "Cross-Sell Recommendation", "Simulation Impact"]
)

st.sidebar.markdown("---")
st.sidebar.write("📊 Unit Bancassurance")
st.sidebar.write("🏦 Bank Mandiri (Mockup)")

# =========================
# MOCK DATA
# =========================
data = pd.DataFrame({
    "Nasabah": [f"Nasabah {i}" for i in range(1, 21)],
    "Dana (Juta)": np.random.randint(50, 2000, 20),
    "Usia": np.random.randint(23, 60, 20),
    "Produk Dimiliki": np.random.choice(
        ["None", "Health", "Life"], 20
    )
})

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.markdown("<div class='main-title'>BancaSmart Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Monitoring Kinerja Bancassurance Cabang</div>", unsafe_allow_html=True)
    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("<div class='card'><div class='metric-label'>Total GWP (YTD)</div><div class='metric-value'>Rp 12,5 M</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><div class='metric-label'>Total Polis</div><div class='metric-value'>186</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'><div class='metric-label'>Conversion Rate</div><div class='metric-value'>28%</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='card'><div class='metric-label'>Nasabah High Potential</div><div class='metric-value'>42</div></div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("### 📈 Distribusi Dana Nasabah")
    st.bar_chart(data["Dana (Juta)"])

    st.markdown("### 📋 Daftar Nasabah")
    st.dataframe(data, use_container_width=True)

# =========================
# RECOMMENDATION ENGINE
# =========================
elif menu == "Cross-Sell Recommendation":

    st.markdown("<div class='main-title'>Cross-Sell Recommendation</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Rekomendasi Produk Asuransi Otomatis</div>", unsafe_allow_html=True)
    st.write("")

    def recommend(row):
        if row["Dana (Juta)"] > 1000:
            return "Whole Life / Legacy"
        elif row["Usia"] < 35:
            return "Health Insurance"
        else:
            return "Life Protection"

    data["Rekomendasi Produk"] = data.apply(recommend, axis=1)
    data["Priority"] = np.where(data["Dana (Juta)"] > 1000, "HIGH", "MEDIUM")

    st.markdown("### 🎯 Nasabah Prioritas")
    st.dataframe(
        data[["Nasabah", "Dana (Juta)", "Usia", "Rekomendasi Produk", "Priority"]],
        use_container_width=True
    )

    st.success("✅ Rekomendasi dapat digunakan langsung oleh RM sebagai sales guidance")

# =========================
# SIMULATION
# =========================
elif menu == "Simulation Impact":

    st.markdown("<div class='main-title'>Simulation & Financial Impact</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Simulasi Kontribusi Bancassurance</div>", unsafe_allow_html=True)
    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        nasabah = st.number_input("Jumlah Nasabah Prospek", 10, 500, 100)
    with col2:
        success_rate = st.slider("Success Rate (%)", 5, 80, 25)
    with col3:
        premi = st.number_input("Rata-rata Premi (Juta)", 5, 200, 30)

    gwp = nasabah * (success_rate / 100) * premi

    st.markdown("### 💰 Hasil Simulasi")
    st.metric("Proyeksi GWP", f"Rp {gwp:,.1f} Juta")
    st.metric("Estimasi Fee Based Income", f"Rp {gwp * 0.25:,.1f} Juta")

    st.info("📌 Gunakan simulasi ini untuk pengajuan program & target cabang")

