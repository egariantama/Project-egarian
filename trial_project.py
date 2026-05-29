import streamlit as st

st.set_page_config(
    page_title="Financial Health Dashboard",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Financial Health Dashboard")

st.sidebar.header("Input Data")

income = st.sidebar.number_input(
    "Pendapatan Bulanan",
    min_value=0,
    value=10000000,
    step=500000
)

expense = st.sidebar.number_input(
    "Pengeluaran Bulanan",
    min_value=0,
    value=6000000,
    step=500000
)

debt = st.sidebar.number_input(
    "Total Cicilan Bulanan",
    min_value=0,
    value=1000000,
    step=500000
)

investment = st.sidebar.number_input(
    "Investasi Bulanan",
    min_value=0,
    value=1000000,
    step=500000
)

emergency_fund = st.sidebar.number_input(
    "Total Dana Darurat Saat Ini",
    min_value=0,
    value=10000000,
    step=1000000
)

# =====================
# Perhitungan
# =====================

saving = income - expense

saving_ratio = (saving / income) * 100 if income else 0
debt_ratio = (debt / income) * 100 if income else 0
invest_ratio = (investment / income) * 100 if income else 0

target_emergency = expense * 6

emergency_ratio = (
    emergency_fund / target_emergency * 100
    if target_emergency > 0 else 0
)

# =====================
# Scoring
# =====================

saving_score = min((saving_ratio / 20) * 25, 25)

debt_score = max(25 - ((debt_ratio / 30) * 25), 0)

emergency_score = min((emergency_ratio / 100) * 25, 25)

invest_score = min((invest_ratio / 10) * 25, 25)

health_score = round(
    saving_score +
    debt_score +
    emergency_score +
    invest_score
)

health_score = min(health_score, 100)

# =====================
# Dashboard
# =====================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Saving Ratio",
    f"{saving_ratio:.1f}%"
)

col2.metric(
    "Debt Ratio",
    f"{debt_ratio:.1f}%"
)

col3.metric(
    "Investment Ratio",
    f"{invest_ratio:.1f}%"
)

col4.metric(
    "Emergency Fund",
    f"{emergency_ratio:.0f}%"
)

st.divider()

st.subheader("🏆 Financial Health Score")

st.progress(health_score)

st.markdown(
    f"""
    <h1 style='text-align:center'>
    {health_score}/100
    </h1>
    """,
    unsafe_allow_html=True
)

# =====================
# Kategori
# =====================

if health_score >= 80:
    category = "🟢 Sangat Sehat"
elif health_score >= 60:
    category = "🟡 Cukup Sehat"
elif health_score >= 40:
    category = "🟠 Perlu Perbaikan"
else:
    category = "🔴 Risiko Tinggi"

st.success(f"Kategori: {category}")

# =====================
# Detail
# =====================

st.subheader("📊 Ringkasan Keuangan")

st.write(
    f"Pendapatan Bulanan : Rp {income:,.0f}"
)

st.write(
    f"Pengeluaran Bulanan : Rp {expense:,.0f}"
)

st.write(
    f"Sisa Dana : Rp {saving:,.0f}"
)

st.write(
    f"Target Dana Darurat : Rp {target_emergency:,.0f}"
)

# =====================
# Rekomendasi
# =====================

st.subheader("💡 Rekomendasi")

if saving_ratio < 20:
    st.warning(
        "Tingkatkan tabungan minimal 20% dari pendapatan."
    )

if debt_ratio > 30:
    st.warning(
        "Rasio cicilan terlalu tinggi. Idealnya di bawah 30%."
    )

if emergency_ratio < 100:
    st.warning(
        "Dana darurat belum mencapai target 6 bulan pengeluaran."
    )

if invest_ratio < 10:
    st.warning(
        "Alokasi investasi masih rendah."
    )

if health_score >= 80:
    st.balloons()
    st.success(
        "Kondisi keuangan sangat sehat. Fokus pada pengembangan aset dan wealth accumulation."
    )
