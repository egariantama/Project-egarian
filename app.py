import streamlit as st
import pandas as pd

st.set_page_config(page_title="Daftar Merchant Google Maps", layout="wide")

st.title("📍 Daftar Merchant – Klik untuk buka Google Maps")

# ====== 1. Load Excel =======

# Ubah nama file sesuai folder kamu
FILE_PATH = "Potensi Ekstensifikasi 2.xlsx"

try:
    df = pd.read_excel(FILE_PATH)
except Exception as e:
    st.error(f"Gagal membuka file Excel: {e}")
    st.stop()

# ===== Check required columns =====
required_cols = ["NAMA_MERCHANT", "LAT", "LONG"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"Kolom '{col}' tidak ditemukan di Excel!")
        st.stop()

# ====== 2. Tampilkan daftar link =======

for idx, row in df.iterrows():

    # Buat URL Google Maps berdasar GPS
    url = f"https://www.google.com/maps?q={row['LAT']},{row['LONG']}"

    st.markdown(
        f"""
        🔗 **[{row['NAMA_MERCHANT']}]({url})**  
        📌 Koordinat: {row['LAT']}, {row['LONG']}  
        ---
        """,
        unsafe_allow_html=True
    )

