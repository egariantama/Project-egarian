import streamlit as st
import pandas as pd
import io

# --- 1. Persiapan Data Merchant di Kawasan Bogor Suryakencana ---
# Data merchant yang lebih banyak di sekitar Bank Mandiri Bogor Suryakencana
data_string = """
NAMA_MERCHANT,LAT,LONG,KATEGORI
Bank Mandiri KCP Bogor Suryakencana,-6.606708,106.801642,Bank
Toko Selamat Bogor,-6.6044085,106.7995618,Roti & Kue
Toko Abc,-6.6062598,106.8011268,Toko Ritel
Toko Glory Bogor,-6.6053384,106.8000661,Toko Ritel
Naga Kencana Bogor - Toko Buku dan Alat Tulis Kantor,-6.6068994,106.8015534,Toko Alat Tulis
Jaya Makmur Toko,-6.6050043,106.8000041,Toko Ritel
Asemka Suryakencana,-6.6039535,106.7995191,Toko Eceran
Toko Sari Sari,-6.6039589,106.7995244,Toko Pakaian
Toko Manisan Asinan,-6.6064998,106.8013893,Toko Camilan
Toko Kue Lapis Bogor Sangkuriang,-6.6044431,106.7995246,Roti & Kue
Toko Roti Bogor Permai (Boper),-6.6064998,106.8013893,Roti & Kue
"""
df = pd.read_csv(io.StringIO(data_string))

# --- 2. Fungsi untuk Membuat Tautan Google Maps yang Akurat ---
def create_map_link(lat, lon):
    """
    Membuat URL Google Maps yang menggunakan format universal:
    https://www.google.com/maps/search/?api=1&query=<LAT>,<LONG>
    """
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

# Menambahkan kolom tautan ke DataFrame
df['Link Google Maps'] = df.apply(
    lambda row: create_map_link(row['LAT'], row['LONG']),
    axis=1
)

# --- 3. Konfigurasi dan Tampilan Streamlit ---
st.set_page_config(
    page_title="Daftar Merchant Bogor Suryakencana",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📍 Daftar Merchant di Kawasan Bank Mandiri Bogor Suryakencana")
st.markdown("---")

st.subheader("Data Merchant")

# Tampilan DataFrame menggunakan LinkColumn yang stabil
try:
    st.dataframe(
        df[['NAMA_MERCHANT', 'KATEGORI', 'ALAMAT SINGKAT', 'Link Google Maps']],
        hide_index=True,
        column_order=('NAMA_MERCHANT', 'KATEGORI', 'ALAMAT SINGKAT', 'Link Google Maps'),
        column_config={
            "NAMA_MERCHANT": st.column_config.TextColumn("Nama Merchant"),
            "KATEGORI": st.column_config.TextColumn("Kategori"),
            "ALAMAT SINGKAT": st.column_config.TextColumn("Alamat Singkat"),
            "Link Google Maps": st.column_config.LinkColumn(
                "Lokasi di Google Maps",
                help="Klik untuk membuka lokasi yang tepat di Google Maps",
                display_funcs=lambda x: "Lihat Peta" # Menampilkan teks "Lihat Peta"
            )
        }
    )
except Exception as e:
    # Fallback jika st.column_config.LinkColumn masih error
    st.warning(f"Gagal memuat tabel interaktif ({type(e).__name__}). Menampilkan tautan sebagai teks.")
    st.dataframe(
        df[['NAMA_MERCHANT', 'KATEGORI', 'ALAMAT SINGKAT', 'Link Google Maps']],
        hide_index=True,
    )

st.markdown("---")
st.info("""
**Instruksi:** Klik tautan **Lihat Peta** di kolom paling kanan untuk langsung diarahkan ke lokasi merchant di Google Maps.
""")
