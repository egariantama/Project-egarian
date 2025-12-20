import streamlit as st
import pandas as pd
import numpy as np
import os
from fpdf import FPDF

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Bancassurance Performance Report",
    page_icon="📊",
    layout="centered"
)

DATA_PATH = "data/bancassurance.csv"
ADMIN_KEY = "MANDIRI2025"   # 🔐 ganti sesuai kebijakan internal

# =========================
# BRANDING BANK MANDIRI
# =========================
st.markdown("""
<style>
/* ===== GLOBAL ===== */
body, .stApp {
    background-color: #ffffff;
    color: #1f2937;
    font-family: 'Segoe UI', sans-serif;
}

/* ===== HEADER ===== */
h1, h2, h3 {
    color: #003d79;
    font-weight: 700;
}

/* ===== METRIC CARD ===== */
.metric-card {
    background: #ffffff;
    border: 2px solid #e5e7eb;
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 14px;
}

.metric-label {
    font-size: 14px;
    color: #6b7280;
}

.metric-value {
    font-size: 24px;
    font-weight: 800;
    color: #003d79;
}

/* ===== GROWTH ===== */
.positive { color: #1b5e20; font-weight: 700; }
.negative { color: #b71c1c; font-weight: 700; }
.neutral  { color: #6b7280; }

/* ===== PRIMARY BUTTON ===== */
.stButton > button {
    width: 100%;
    background-color: #003d79;
    color: #ffffff;
    border-radius: 12px;
    padding: 12px;
    font-weight: 700;
    border: none;
    font-size: 15px;
}

.stButton > button:hover {
    background-color: #002855;
}

/* ===== SECONDARY BUTTON ===== */
.secondary-btn button {
    background-color: #f9b233 !important;
    color: #003d79 !important;
}

/* ===== EXPANDER ===== */
details summary {
    font-weight: 700;
    color: #003d79;
}

/* Hide footer */
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("📊 Bancassurance Performance Report")
st.caption("Monitoring Nilai Pertanggungan & Fee Based Income")

# =========================
# ADMIN ACCESS
# =========================
st.markdown("### 🔐 Admin Access")
admin_input = st.text_input(
    "Masukkan Admin Key (hanya untuk upload data)",
    type="password",
    placeholder="Admin Only"
)

is_admin = admin_input == ADMIN_KEY

# =========================
# ADMIN UPLOAD (PROTECTED)
# =========================
if is_admin:
    with st.expander("📤 Upload / Update Data Bancassurance (CSV)"):
        uploaded_file = st.file_uploader(
            "Upload File CSV dari Excel",
            type=["csv"]
        )
        if uploaded_file:
            df_upload = pd.read_csv(uploaded_file)
            os.makedirs("data", exist_ok=True)
            df_upload.to_csv(DATA_PATH, index=False)
            st.success("✅ Data berhasil diperbarui oleh Admin")
else:
    st.info("ℹ️ Upload data hanya dapat dilakukan oleh Admin")

# =========================
# LOAD DATA
# =========================
if not os.path.exists(DATA_PATH):
    st.warning("📌 Data belum tersedia. Menunggu Admin upload data.")
    st.stop()

df = pd.read_csv(DATA_PATH)

# =========================
# VALIDATION
# =========================
required_cols = [
    "Tipe_Kerjasama","Jenis_Asuransi","Asuradur",
    "NP_Nov24","NP_Dec24","NP_Nov25",
    "FBI_Nov24","FBI_Dec24","FBI_Nov25"
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Kolom tidak lengkap: {missing}")
    st.stop()

num_cols = required_cols[3:]
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

# =========================
# CALCULATION
# =========================
df["NP_Growth_YoY"] = df["NP_Nov25"] - df["NP_Nov24"]
df["NP_Growth_YoY_%"] = np.where(
    df["NP_Nov24"] > 0,
    df["NP_Growth_YoY"] / df["NP_Nov24"] * 100,
    0
)

df["FBI_Growth_YoY"] = df["FBI_Nov25"] - df["FBI_Nov24"]
df["FBI_Growth_YoY_%"] = np.where(
    df["FBI_Nov24"] > 0,
    df["FBI_Growth_YoY"] / df["FBI_Nov24"] * 100,
    0
)

# =========================
# FILTER
# =========================
with st.expander("🔎 Filter Data"):
    tipe = st.multiselect(
        "Tipe Kerjasama",
        df["Tipe_Kerjasama"].unique(),
        default=df["Tipe_Kerjasama"].unique()
    )

df = df[df["Tipe_Kerjasama"].isin(tipe)]

# =========================
# HELPER
# =========================
def growth_class(val):
    if val > 0:
        return "positive"
    elif val < 0:
        return "negative"
    return "neutral"

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["📊 Summary", "📋 Detail", "📈 Chart"])

# =========================
# SUMMARY
# =========================
with tab1:
    st.markdown("### 📌 Executive Summary")

    total_np = df["NP_Nov25"].sum()
    total_fbi = df["FBI_Nov25"].sum()
    np_growth = df["NP_Growth_YoY_%"].mean()
    fbi_growth = df["FBI_Growth_YoY_%"].mean()

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Nilai Pertanggungan (Nov-25)</div>
        <div class="metric-value">Rp {total_np:,.0f}</div>
    </div>

    <div class="metric-card">
        <div class="metric-label">Growth NP YoY</div>
        <div class="metric-value {growth_class(np_growth)}">{np_growth:.1f}%</div>
    </div>

    <div class="metric-card">
        <div class="metric-label">Total Fee Based Income (Nov-25)</div>
        <div class="metric-value">Rp {total_fbi:,.2f}</div>
    </div>

    <div class="metric-card">
        <div class="metric-label">Growth FBI YoY</div>
        <div class="metric-value {growth_class(fbi_growth)}">{fbi_growth:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# DETAIL
# =========================
with tab2:
    st.markdown("### 📋 Detail Bancassurance Performance")

    display_cols = [
        "Tipe_Kerjasama","Jenis_Asuransi","Asuradur",
        "NP_Nov25","NP_Growth_YoY","NP_Growth_YoY_%",
        "FBI_Nov25","FBI_Growth_YoY","FBI_Growth_YoY_%"
    ]

    st.dataframe(
        df[display_cols].style.format({
            "NP_Nov25":"{:,.0f}",
            "NP_Growth_YoY":"{:,.0f}",
            "NP_Growth_YoY_%":"{:.1f}%",
            "FBI_Nov25":"{:,.2f}",
            "FBI_Growth_YoY":"{:,.2f}",
            "FBI_Growth_YoY_%":"{:.1f}%"
        }),
        use_container_width=True
    )

# =========================
# CHART
# =========================
with tab3:
    st.markdown("### 📈 Growth YoY Comparison")

    chart_data = (
        df.groupby("Jenis_Asuransi")[["NP_Growth_YoY","FBI_Growth_YoY"]]
        .sum()
    )
    st.bar_chart(chart_data)

# =========================
# EXPORT PDF
# =========================
def generate_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Bancassurance Performance Report", ln=True)

    pdf.set_font("Arial", size=11)
    pdf.ln(4)
    pdf.cell(0, 8, f"Total NP Nov-25 : Rp {df['NP_Nov25'].sum():,.0f}", ln=True)
    pdf.cell(0, 8, f"Total FBI Nov-25 : Rp {df['FBI_Nov25'].sum():,.2f}", ln=True)

    path = "data/Bancassurance_Report.pdf"
    pdf.output(path)
    return path

st.markdown("---")
if st.button("📥 Export PDF Laporan Pimpinan"):
    pdf_path = generate_pdf(df)
    with open(pdf_path, "rb") as f:
        st.download_button(
            "⬇️ Download PDF",
            f,
            file_name="Bancassurance_Performance_Report.pdf"
        )
