import streamlit as st
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIG (MOBILE FIRST)
# =========================
st.set_page_config(
    page_title="Bancassurance Performance App",
    page_icon="📊",
    layout="centered"
)

# =========================
# SESSION STATE
# =========================
if "role" not in st.session_state:
    st.session_state.role = None

if "data" not in st.session_state:
    st.session_state.data = None

# =========================
# SIMPLE LOGIN
# =========================
st.sidebar.title("🔐 Login")

role = st.sidebar.selectbox(
    "Pilih Role",
    ["User", "Admin"]
)

if role == "Admin":
    password = st.sidebar.text_input("Password Admin", type="password")
    if password == "admin123":   # 👉 ganti password sesuai kebijakan
        st.session_state.role = "Admin"
        st.sidebar.success("Login sebagai Admin")
    else:
        st.sidebar.warning("Password Admin salah")
        st.stop()
else:
    st.session_state.role = "User"

# =========================
# HEADER
# =========================
st.title("📊 Bancassurance Performance Report")
st.caption("Digital Monitoring Nilai Pertanggungan & Fee Based Income")

# =========================
# ADMIN UPLOAD
# =========================
if st.session_state.role == "Admin":
    uploaded_file = st.file_uploader(
        "📤 Upload Data Bancassurance (CSV)",
        type=["csv"]
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state.data = df
        st.success("✅ Data berhasil di-upload")

# =========================
# DATA AVAILABILITY CHECK
# =========================
if st.session_state.data is None:
    st.info("📌 Data belum tersedia. Menunggu Admin upload data.")
    st.stop()

df = st.session_state.data.copy()

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
# FILTER (MOBILE FRIENDLY)
# =========================
with st.expander("🔎 Filter Data"):
    tipe = st.multiselect(
        "Tipe Kerjasama",
        df["Tipe_Kerjasama"].unique(),
        default=df["Tipe_Kerjasama"].unique()
    )

df = df[df["Tipe_Kerjasama"].isin(tipe)]

# =========================
# MOBILE MENU (TABS)
# =========================
tab1, tab2, tab3 = st.tabs([
    "📊 Summary",
    "📋 Detail",
    "📈 Chart"
])

# =========================
# SUMMARY TAB
# =========================
with tab1:
    st.subheader("📌 Executive Summary")

    st.metric("Total NP Nov-25", f"Rp {df['NP_Nov25'].sum():,.0f}")
    st.metric("Growth NP YoY", f"{df['NP_Growth_YoY_%'].mean():.1f}%")

    st.metric("Total FBI Nov-25", f"Rp {df['FBI_Nov25'].sum():,.2f}")
    st.metric("Growth FBI YoY", f"{df['FBI_Growth_YoY_%'].mean():.1f}%")

# =========================
# DETAIL TAB
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
# CHART TAB
# =========================
with tab3:
    st.subheader("📈 Growth YoY Comparison")

    chart = (
        df.groupby("Jenis_Asuransi")[["NP_Growth_YoY","FBI_Growth_YoY"]]
        .sum()
    )

    st.bar_chart(chart)
