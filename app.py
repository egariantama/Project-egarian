import streamlit as st
import pandas as pd
import io

# --- 1. Persiapan Data Merchant di Kawasan Bogor Suryakencana ---
# Data sekarang mencakup kolom ALAMAT SINGKAT untuk mencegah KeyError
data_string = """
NAMA_MERCHANT,LAT,LONG,KATEGORI,ALAMAT SINGKAT
Bank Mandiri KCP Bogor Suryakencana,-6.606708,106.801642,Bank,Jl. Suryakencana No.310
Toko Selamat Bogor,-6.6044085,106.7995618,Roti & Kue,Jl. Suryakencana No.15
Toko Abc,-6.6062598,106.8011268,Toko Ritel,Jl. Suryakencana No.111
Toko Glory Bogor,-6.6053384,106.8000661,Toko Ritel,Jl. Suryakencana No.96
Naga Kencana Bogor - Toko Buku dan Alat Tulis Kantor,-6.6068994,106.8015534,Toko Alat Tulis,Jl. Suryakencana No.139
Jaya Makmur Toko,-6.6050043,106.8000041,Toko Ritel,Jl. Suryakencana No.51
Asemka Suryakencana,-6.6039535,106.7995191,Toko Eceran,Jl. Suryakencana
Toko Sari Sari,-6.6039589,106.7995244,Toko Pakaian,Jl. Suryakencana
Toko Manisan Asinan,-6.6064998,106.8013893,Toko Camilan,Jl. Suryakencana No.288
Toko Kue Lapis Bogor Sangkuriang,-6.6044431,106.7995246,Roti & Kue,Jl. Suryakencana No.16
Toko Roti Bogor Permai (Boper),-6.6064998,106.8013893,Roti & Kue,Jl. Jend. Sudirman
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

# Tampilan DataFrame
try:
    st.dataframe(
        # Pastikan semua nama kolom yang dipanggil di sini ada di DataFrame
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
                # Menghapus display_funcs untuk Type Error dan menggunakan default display (URL)
                # atau jika ingin menampilkan teks yang berbeda:
                display_funcs=lambda x: "Lihat Peta" 
            )
        }
    )
except Exception:
    # Fallback ke tampilan link sebagai teks biasa jika konfigurasi kolom gagal
    st.warning("Gagal memuat tabel interaktif. Menampilkan tautan sebagai teks.")
    st.dataframe(
        df[['NAMA_MERCHANT', 'KATEGORI', 'ALAMAT SINGKAT', 'Link Google Maps']],
        hide_index=True,
    )

st.markdown("---")

# --- Pilihan Interaktif untuk Pengujian ---
st.sidebar.header("Coba Langsung")
selected_merchant = st.sidebar.selectbox(
    "Pilih Merchant untuk Coba Buka Maps:",
    df['NAMA_MERCHANT']
)

if selected_merchant:
    selected_row = df[df['NAMA_MERCHANT'] == selected_merchant].iloc[0]
    map_link = selected_row['Link Google Maps']
    
    st.sidebar.markdown(f"**{selected_merchant}**")
    st.sidebar.markdown(f"LAT: **{selected_row['LAT']}** | LONG: **{selected_row['LONG']}**")
    
    st.sidebar.link_button("Buka di Google Maps 🗺️", map_link)
