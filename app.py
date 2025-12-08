import streamlit as st
import pandas as pd

st.title("📍 Daftar Merchant Google Maps")

# Data merchant bisa kamu ganti
data = [
    {"nama": "Kedai Kopi ABC", "alamat": "Kedai Kopi ABC Denpasar"},
    {"nama": "Toko Roti Mawar", "alamat": "Toko Roti Mawar Denpasar"},
    {"nama": "Ayam Bakar Madu", "alamat": "Ayam Bakar Madu Renon"},
]

df = pd.DataFrame(data)

for i, row in df.iterrows():
    url = f"https://www.google.com/maps?q={row['alamat'].replace(' ', '+')}"
    st.markdown(
        f"🔗 **[{row['nama']}]({url})** – _{row['alamat']}_",
        unsafe_allow_html=True
    )
