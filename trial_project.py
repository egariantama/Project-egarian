import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Bancassurance Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# HEADER
# ======================================================
st.title("📊 Bancassurance Performance Dashboard")
st.caption("Executive Snapshot • YTD & YoY Performance")

# ======================================================
# UPLOAD DATA
# ======================================================
uploaded_file = st.file_uploader(
    "📤 Upload Data (Excel / CSV)",
    type=["csv", "xlsx"]
)

if not uploaded_file:
    st.info("Silakan upload file data")
    st.stop()

df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)

# ======================================================
# NORMALISASI KOLOM
# ======================================================
df.columns = (
    df.columns
    .str.strip()
    .str.upper()
    .str.replace(" ", "_")
)

# ======================================================
# VALIDASI
# ======================================================
required_cols = [
    "DATE",
    "TIPE_KERJASAMA",
    "JENIS_ASURANSI",
    "ASURADUR",
    "NILAI_PERTANGGUNGAN",
    "FBI"
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Kolom wajib tidak ditemukan: {missing}")
    st.stop()

# ======================================================
# DATA CLEANING
# ======================================================
df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
df = df.dropna(subset=["DATE"])

df["NILAI_PERTANGGUNGAN"] = pd.to_numeric(df["NILAI_PERTANGGUNGAN"], errors="coerce").fillna(0)
df["FBI"] = pd.to_numeric(df["FBI"], errors="coerce").fillna(0)

df["YEAR"] = df["DATE"].dt.year
df["MONTH"] = df["DATE"].dt.month

# ======================================================
# FILTER (WAJIB SEBELUM HITUNG)
# ======================================================
with st.sidebar:
    st.header("🔎 Filter")

    tipe = st.multiselect(
        "Tipe Kerjasama",
        sorted(df["TIPE_KERJASAMA"].unique()),
        default=sorted(df["TIPE_KERJASAMA"].unique())
    )

    jenis = st.multiselect(
        "Jenis Asuransi",
        sorted(df[df["TIPE_KERJASAMA"].isin(tipe)]["JENIS_ASURANSI"].unique()),
        default=sorted(df[df["TIPE_KERJASAMA"].isin(tipe)]["JENIS_ASURANSI"].unique())
    )

    metric = st.radio("Metric", ["NILAI_PERTANGGUNGAN", "FBI"])

df_f = df[
    (df["TIPE_KERJASAMA"].isin(tipe)) &
    (df["JENIS_ASURANSI"].isin(jenis))
]

# ======================================================
# DEFINISI PERIODE (DARI DATA TERFILTER)
# ======================================================
def period(data, y, m):
    return data[(data["YEAR"] == y) & (data["MONTH"] == m)]

nov_24 = period(df_f, 2024, 11)
dec_24 = period(df_f, 2024, 12)
nov_25 = period(df_f, 2025, 11)

# ======================================================
# KPI
# ======================================================
def growth(cur, prev):
    return ((cur - prev) / prev * 100) if prev > 0 else 0

cur_val = nov_25[metric].sum()
yoy_val = nov_24[metric].sum()
ytd_val = dec_24[metric].sum()

st.subheader("📌 Executive Summary")

c1, c2, c3 = st.columns(3)
c1.metric("Nov-25", f"Rp {cur_val:,.0f}")
c2.metric("Growth YoY", f"{growth(cur_val, yoy_val):.1f}%")
c3.metric("Growth YTD", f"{growth(cur_val, ytd_val):.1f}%")

# ======================================================
# INSIGHT OTOMATIS
# ======================================================
def insight(metric, cur, yoy, ytd):
    if cur > yoy and cur > ytd:
        return f"📈 {metric} menunjukkan pertumbuhan kuat secara YoY dan YTD."
    if cur > yoy:
        return f"⚠️ {metric} tumbuh YoY namun melemah dibanding YTD."
    if cur > ytd:
        return f"⚠️ {metric} membaik secara YTD namun turun YoY."
    return f"🔻 {metric} mengalami kontraksi baik YoY maupun YTD."

st.info(insight(metric.replace("_", " "), cur_val, yoy_val, ytd_val))

st.divider()

# ======================================================
# YOY VARIANCE CHART
# ======================================================
st.subheader("📊 YoY Variance by Jenis Asuransi")

yoy_var = (
    nov_25.groupby("JENIS_ASURANSI")[metric].sum()
    - nov_24.groupby("JENIS_ASURANSI")[metric].sum()
).reset_index(name="YOY_DELTA")

fig = px.bar(
    yoy_var,
    x="JENIS_ASURANSI",
    y="YOY_DELTA",
    color="YOY_DELTA",
    color_continuous_scale="RdYlGn"
)

st.plotly_chart(fig, use_container_width=True)

# ======================================================
# TABEL EXECUTIVE (PIVOT)
# ======================================================
def build_table(metric):
    base = (
        df_f.groupby(
            ["TIPE_KERJASAMA", "JENIS_ASURANSI", "ASURADUR", "YEAR", "MONTH"],
            as_index=False
        )[metric].sum()
    )

    p = base.pivot_table(
        index=["TIPE_KERJASAMA", "JENIS_ASURANSI", "ASURADUR"],
        columns=["YEAR", "MONTH"],
        values=metric,
        aggfunc="sum",
        fill_value=0
    )

    p.columns = [
        "NOV_24" if c == (2024,11) else
        "DEC_24" if c == (2024,12) else
        "NOV_25"
        for c in p.columns
    ]

    p = p.reset_index()

    p["GROWTH_YTD"] = p["NOV_25"] - p["DEC_24"]
    p["GROWTH_YTD_%"] = np.where(p["DEC_24"] > 0, p["GROWTH_YTD"] / p["DEC_24"] * 100, 0)

    p["GROWTH_YOY"] = p["NOV_25"] - p["NOV_24"]
    p["GROWTH_YOY_%"] = np.where(p["NOV_24"] > 0, p["GROWTH_YOY"] / p["NOV_24"] * 100, 0)

    return p

st.subheader("📋 Tabel Kinerja (Executive View)")

table = build_table(metric)

# SUBTOTAL
subtotal = table.groupby(
    ["TIPE_KERJASAMA", "JENIS_ASURANSI"],
    as_index=False
).sum(numeric_only=True)
subtotal["ASURADUR"] = "SUBTOTAL"

# GRAND TOTAL
grand = pd.DataFrame([{
    "TIPE_KERJASAMA": "GRAND TOTAL",
    "JENIS_ASURANSI": "",
    "ASURADUR": "",
    "NOV_24": table["NOV_24"].sum(),
    "DEC_24": table["DEC_24"].sum(),
    "NOV_25": table["NOV_25"].sum(),
    "GROWTH_YTD": table["GROWTH_YTD"].sum(),
    "GROWTH_YOY": table["GROWTH_YOY"].sum(),
    "GROWTH_YTD_%": np.nan,
    "GROWTH_YOY_%": np.nan
}])

final = pd.concat([table, subtotal, grand], ignore_index=True)

st.dataframe(
    final.style
    .format({
        "NOV_24": "{:,.0f}",
        "DEC_24": "{:,.0f}",
        "NOV_25": "{:,.0f}",
        "GROWTH_YTD_%": "{:.1f}%",
        "GROWTH_YOY_%": "{:.1f}%"
    })
    .background_gradient(
        cmap="RdYlGn",
        subset=["GROWTH_YTD_%", "GROWTH_YOY_%"]
    ),
    use_container_width=True
)

# ======================================================
# EXPORT EXCEL
# ======================================================
buffer = BytesIO()
with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
    final.to_excel(writer, index=False, sheet_name="Performance")

st.download_button(
    "📤 Export Excel",
    data=buffer.getvalue(),
    file_name="Bancassurance_YTD_YoY.xlsx"
)
