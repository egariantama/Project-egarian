import streamlit as st
import pandas as pd
import numpy as np
import os
from fpdf import FPDF

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Bancassurance Performance App",
    page_icon="📊",
    layout="centered"
)

DATA_PATH = "data/bancassurance.csv"

USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "user": {"password": "user123", "role": "User"}
}

# =========================
# BRANDING (MANDIRI STYLE)
# =========================
st.markdown("""
<style>
body { background-color: #f5f7fa; }
h1, h2, h3 { color: #003d79; }

.metric-card {
    background: white;
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 12px;
}

.label { font-size: 14px; color: #6c757d; }
.value { font-size: 22px; font-weight: bold; }

.positive { color: #2e7d32; }
.negative { color: #c62828; }
.neutral { color: #6c757d; }

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN
# =========================
st.sidebar.title("🔐 Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username not in USERS or USERS[username]["password"] != password:
    st.sidebar.warning("Login gagal")
    st.stop()

role = USERS[username]["role"]
st.sidebar.success(f"Login sebagai {role}")

# =========================
# HEADER
# =========================
st.title("📊 Bancassurance Performance Report")
st.caption("Executive Monitoring Nilai Pertanggungan & Fee Based Income")

# =========================
# ADMIN UPLOAD (PERSISTENT)
# =========================
if role == "Admin":
    uploaded_file = st.file_uploader("📤 Upload Data Bancassurance (CSV)", type=["csv"])
    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file)
        os.makedirs("data", exist_ok=True)
        df_upload.to_csv(DATA_PATH, index=False)
        st.success("✅ Data berhasil disimpan")

# =========================
# LOAD DATA
# =========================
if not os.path.exists(DATA_PATH):
    st.info("📌 Data belum tersedia. Menunggu Admin upload.")
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
df["NP_Growth_YoY_%"] = np.where(df["NP_Nov24"] > 0, df["NP_Growth_YoY"] / df["NP_Nov24"] * 100, 0)

df["FBI_Growth_YoY"] = df["FBI_Nov25"] - df["FBI_Nov24"]
df["FBI_Growth_YoY_%"] = np.where(df["FBI_Nov24"] > 0, df["FBI_Growth_YoY"] / df["FBI_Nov24"] * 100, 0)

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
# TABS (MOBILE FRIENDLY)
# =========================
tab1, tab2, tab3 = st.tabs(["📊 Summary", "📋 Detail", "📈 Chart"])

# =========================
# SUMMARY
# =========================
with tab1:
    total_np = df["NP_Nov25"].sum()
    total_fbi = df["FBI_Nov25"].sum()
    np_growth = df["NP_Growth_YoY_%"].mean()
    fbi_growth = df["FBI_Growth_YoY_%"].mean()

    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Total NP Nov-25</div>
        <div class="value">Rp {total_np:,.0f}</div>
    </div>
    <div class="metric-card">
        <div class="label">Growth NP YoY</div>
        <div class="value {growth_class(np_growth)}">{np_growth:.1f}%</div>
    </div>
    <div class="metric-card">
        <div class="label">Total FBI Nov-25</div>
        <div class="value">Rp {total_fbi:,.2f}</div>
    </div>
    <div class="metric-card">
        <div class="label">Growth FBI YoY</div>
        <div class="value {growth_class(fbi_growth)}">{fbi_growth:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# DETAIL
# =========================
with tab2:
    st.subheader("📋 Bancassurance Performance Detail")
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
    st.subheader("📈 Growth YoY Comparison")
    chart_data = df.groupby("Jenis_Asuransi")[["NP_Growth_YoY","FBI_Growth_YoY"]].sum()
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
    pdf.ln(5)
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
