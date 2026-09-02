import streamlit as st
import pandas as pd

# Konfigurasi Halaman (Tampilan Mobile-Friendly)
st.set_page_config(
    page_title="Daftar Rekanan Asuransi",
    page_icon="🏥",
    layout="centered"
)

# --- DATA DUMMY REKANAN ---
@st.cache_data
def load_data():
    return pd.DataFrame([
        {
            "Nama Rumah Sakit": "RS Medika Utama",
            "Kategori": "Rumah Sakit",
            "Kota": "Jakarta Selatan",
            "Asuransi": ["Prudential", "Manulife", "AXA Mandiri"],
            "Layanan": "VIP, Rawat Inap, UGD 24 Jam",
            "Telepon": "(021) 555-0192"
        },
        {
            "Nama Rumah Sakit": "Klinik Sehat Bersama",
            "Kategori": "Klinik",
            "Kota": "Jakarta Pusat",
            "Asuransi": ["BPJS", "Prudential", "Allianz"],
            "Layanan": "Rawat Jalan, Gigi",
            "Telepon": "(021) 555-0143"
        },
        {
            "Nama Rumah Sakit": "RS Hermina Sukabumi",
            "Kategori": "Rumah Sakit",
            "Kota": "Bandung",
            "Asuransi": ["Allianz", "Manulife", "Generali"],
            "Layanan": "Rawat Inap, Ibu & Anak",
            "Telepon": "(022) 555-0188"
        },
        {
            "Nama Rumah Sakit": "Klinik Optik Jaya",
            "Kategori": "Optik",
            "Kota": "Surabaya",
            "Asuransi": ["AXA Mandiri", "BPJS"],
            "Layanan": "Pemeriksaan Mata, Kacamata",
            "Telepon": "(031) 555-0177"
        }
    ])

df = load_data()

# --- HEADER APLIKASI ---
st.title("🏥 Rekanan Asuransi")
st.caption("Cari Rumah Sakit, Klinik, dan Optik rekanan asuransi Anda.")

# --- FILTER SEARCH ---
st.subheader("🔍 Cari Provider")

# Ambil daftar unik untuk dropdown
daftar_asuransi = sorted(list(set([asuransi for sublist in df["Asuransi"] for asuransi in sublist])))
daftar_kota = sorted(df["Kota"].unique().tolist())

pilihan_asuransi = st.selectbox("Pilih Asuransi Anda:", ["Semua"] + daftar_asuransi)
pilihan_kota = st.selectbox("Pilih Kota:", ["Semua"] + daftar_kota)
kata_kunci = st.text_input("Nama RS / Klinik (Opsional):")

# --- LOGIKA FILTER ---
filtered_df = df.copy()

if pilihan_asuransi != "Semua":
    filtered_df = filtered_df[filtered_df["Asuransi"].apply(lambda x: pilihan_asuransi in x)]

if pilihan_kota != "Semua":
    filtered_df = filtered_df[filtered_df["Kota"] == pilihan_kota]

if kata_kunci:
    filtered_df = filtered_df[filtered_df["Nama Rumah Sakit"].str.contains(kata_kunci, case=False)]

st.divider()

# --- TAMPILAN HASIL (CARD STYLE UNTUK MOBILE) ---
st.subheader(f"Hasil Pencarian ({len(filtered_df)})")

if filtered_df.empty:
    st.warning("Tidak ditemukan rekanan yang sesuai dengan kriteria.")
else:
    for idx, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"### {row['Nama Rumah Sakit']}")
            st.caption(f"📍 {row['Kota']} | 🏷️ {row['Kategori']}")
            
            st.write(f"**Layanan:** {row['Layanan']}")
            st.write(f"**Telepon:** {row['Telepon']}")
            
            # Menampilkan badge asuransi
            asuransi_tags = " ".join([f"`{a}`" for a in row['Asuransi']])
            st.write(f"**Asuransi Diterima:** {asuransi_tags}")
            
            st.divider()
