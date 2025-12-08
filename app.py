import streamlit as st
import pandas as pd
import io

# --- 1. Persiapan Data ---
data_string = """
NAMA_MERCHANT,LAT,LONG
PD MATERIAL CIBALOK,6.6132027,106.8066751
MEDIA ELEKTRONIK 3,6.6063072,106.8021991
Kent X Gusli HomeS,6.6073314,106.8002995
JIPANG CEL,6.6043556,106.8039727
Indo Prima Computer,6.6066264,106.8008805
devaiz coorporate,6.6095033,106.801439
CygnusWorks Indonesia,6.6076137,106.8053613
CITY ELECTRONIC,6.6060265,106.8006652
Bogor Neon,6.6085674,106.8041497
BKTech Komputindo,6.611017,106.8053853
TOKO LENGKAP TERMURAH TERLENGKAP,6.4845179,106.8423677
Levoait Air Purifier Cibinong City Mall,6.4843587,106.8418851
JBL Official Store Cibinong City Mall,6.4843587,106.8418851
IT GALERI Cibinong City Mall,6.4842002,106.8412312
BOSCH Electornic city,6.4844693,106.8421802
AGRES ID CIBINONG CITY MALL 1 LAPTOP SPESIALIS,6.4842002,106.8423123
TOKO KOMPUTER DAN AKSESORIES,6.5690996,106.8077601
Toko digital cahaya,6.577761,106.8075371
RamaStore,6.5778193,106.8075136
LG,6.569193,106.807814
Lenovo Handphone,6.569193,106.807814
Jual beli handphone oppo vivo iphone dan lain lain,6.577761,106.8075372
InKQ,6.56947,106.8079
Handajaya Computer,6.5693051,106.8077829
Condel Service,6.5758667,106.8082511
Popyvora,6.6116114,106.8103135
PanggungDigital,6.6056214,106.8129063
Matrial Epul,6.6153052,106.8183351
KEDAI DATA,6.6112593,106.8097489
Jual Kepingan CD Bp Tanto,6.6182139,106.8123361
Hjamaludin cell,6.6162339,106.8128572
Bengkel Motor 3M,6.6163773,106.8175873
Aceng Production Bogor Kota,6.6050875,106.8140603
Abicom Servis Komputer,6.6178859,106.8157697
SENTUL SHOP,6.5675072,106.8582132
PUSAT ELEKTRONIK SENTUL BOGOR,6.5671158,106.8587295
Laptop Sentul,6.5685382,106.8569716
KLIkNKLIK Aeon Sentul City,6.56834,106.8588641
JBL AEON SENTUL,6.5667823,106.8587381
Electronic Aeon Store Sentul City,6.5675052,106.8582185
Courts ON Mall Sentul City,6.5667229,106.8572357
Service Komputer dan Laptop Lengkap,6.6150861,106.8002864
Pojoks Komputer,6.6150706,106.8003277
Kingkong Elektronik,6.614369,106.8028821
Denpoo Official store bogor,6.6127687,106.802485
Vidiotron runningtext bogor,6.6026773,106.8137921
Sound Story Botani Square,6.6014221,106.8017254
"""
df = pd.read_csv(io.StringIO(data_string))

# --- 2. Fungsi untuk Membuat Tautan Google Maps (FORMAT PALING STABIL) ---
def create_map_link(lat, lon):
    """
    Membuat URL Google Maps yang menggunakan skema 'dir' dengan koordinat tujuan.
    Ini adalah format yang sangat stabil dan cenderung mengarahkan dengan benar.
    """
    return f"maps.google.com{lat},{lon}"

# Menambahkan kolom tautan ke DataFrame
df['Link Google Maps'] = df.apply(
    lambda row: create_map_link(row['LAT'], row['LONG']),
    axis=1
)

# --- 3. Konfigurasi dan Tampilan Streamlit ---
st.set_page_config(
    page_title="Daftar Merchant & Google Maps",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📍 Daftar Merchant dengan Tautan Google Maps")
st.markdown("---")

st.subheader("Data Merchant")

# Tampilan DataFrame
# Menggunakan Try-Except untuk memastikan aplikasi tidak crash jika LinkColumn masih error
try:
    st.dataframe(
        df[['NAMA_MERCHANT', 'LAT', 'LONG', 'Link Google Maps']],
        hide_index=True,
        column_config={
            "Link Google Maps": st.column_config.LinkColumn(
                "Lokasi di Google Maps",
                help="Klik untuk membuka lokasi di Google Maps",
                # display_funcs dihapus untuk keandalan maksimal
            )
        }
    )
except Exception:
    # Fallback ke tampilan link sebagai teks biasa jika konfigurasi kolom gagal
    st.warning("Gagal memuat tabel interaktif. Menampilkan tautan sebagai teks. Mohon salin link untuk membuka Maps.")
    st.dataframe(
        df[['NAMA_MERCHANT', 'LAT', 'LONG', 'Link Google Maps']],
        hide_index=True,
    )

st.markdown("---")
st.info("""
**Cara menggunakan:**
Pastikan Anda menjalankan aplikasi Streamlit di browser modern. Tautan di kolom **Lokasi di Google Maps** seharusnya kini mengarahkan ke koordinat yang tepat.
""")

# --- Pilihan Interaktif untuk Pengujian (Menggunakan Link Button yang Stabil) ---
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
    
    # link_button adalah cara paling stabil untuk memastikan URL terbuka
    st.sidebar.link_button("Buka di Google Maps 🗺️", map_link)
