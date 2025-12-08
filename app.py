import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Daftar Merchant Google Maps",
    layout="wide"
)

st.title("📍 Daftar Merchant – Klik untuk buka Google Maps")

# =======================
# 1. Load Excel
# =======================

FILE_PATH = "Potensi Ekstensifikasi 2.xlsx"

try:
    df = pd.read_excel(FILE_PATH)
except Exception as e:
    st.error(f"Gagal membuka file Excel: {e}")
    st.stop()

# =======================
# 2. Validasi Kolom
# =======================

required_cols = ["NAMA_MERCHANT", "LAT", "LONG"]
missing = [c for c in required_cols if c not in df.columns]

if len(missing) > 0:
    st.error(f"Kolom berikut tidak ditemukan di Excel: {missing}")
    st.stop()

# =======================
# 3. Tampilkan Daftar Merchant
# =======================

st.subheader("🔗 Klik nama merchant untuk membuka lokasi di Google Maps")

for idx, row in df.iterrows():

    nama = str(row["NAMA_MERCHANT"])
    lat = row["LAT"]
    lon = row["LONG"]

    # Link Google Maps
    url = f"https://www.google.com/maps?q={lat},{lon}"

    st.markdown(
        f"""
        ### [{nama}]({url})
        🧭 Koordinat: `{lat}, {lon}`
        ---
        """,
        unsafe_allow_html=True
    )
