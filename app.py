import streamlit as st
import pandas as pd
import io

# --- 1. Data Merchant ---
# Data yang Anda sediakan dalam pesan terakhir
data_string = """
NAMA_MERCHANT,LAT,LONG
Toko Antena Digital Parabola Bogor,-6.6070787,106.8052767
PD MATERIAL CIBALOK,-6.6132027,106.8066751
MEDIA ELEKTRONIK 3,-6.6063072,106.8021991
Kent X Gusli HomeS,-6.6073314,106.8002995
JIPANG CEL,-6.6043556,106.8039727
Indo Prima Computer,-6.6066264,106.8008805
devaiz coorporate,-6.6095033,106.8014339
CygnusWorks Indonesia,-6.6076137,106.8053613
CITY ELECTRONIC,-6.6060265,106.8006652
Bogor Neon,-6.6085674,106.8041497
BK Tech Computindo,-6.611017,106.8053853
TOKO LAPTOP TERMURAH TERLENGKAP,-6.4845179,106.8423677
Levoit Air Purifier Cibinong City Mall,-6.4843587,106.8418851
JBL Official Store Cibinong City Mall,-6.4843587,106.8418851
IT GALERI Cibinong City Mall,-6.4842002,106.8423123
BOSCH Electornic city,-6.4844693,106.8421802
AGRES ID CIBINONG CITY MALL 1 LAPTOP SPESIALIS,-6.4842002,106.8423123
TOKO KOMPUTER DAN ACESSORIES,-6.5690996,106.8077601
Toko digital cahaya,-6.577761,106.8075371
RamaStore,-6.5778193,106.8075136
LG,-6.569193,106.807814
Lenovo Handphone,-6.569193,106.807814
Jual beli handphone oppo vivo iphone dan lain lain,-6.577761,106.8075372
InkQ,-6.56947,106.8079
Handjaya Computer,-6.5693051,106.8077829
Condel Service,-6.5758667,106.8082511
Popyvora,-6.6116114,106.8103135
PanggungDigital,-6.6056214,106.8129063
Matrial Epul,-6.6153052,106.8183351
KEDAI DATA,-6.6112593,106.8097489
Jual Kepingan CD Bp Tanto,-6.6182139,106.8123361
Hjamaludin cell,-6.6162339,106.8128572
Bengkel Motor 3M,-6.6163773,106.8175873
Aceng Production Bogor Kota,-6.6050875,106.8140603
Abicom Servis Komputer,-6.6178859,106.8157697
SENTUL SHOP,-6.5675072,106.8582132
PUSAT ELEKTRONIK SENTUL BOGOR,-6.5671158,106.8587295
Laptop Sentul,-6.5685382,106.8569716
KLIKnKLIK Aeon Sentul City,-6.56834,106.8558641
JBL AEON SENTUL,-6.5667823,106.8587381
Electronic Aeon Store Sentul City,-6.5675052,106.8582185
Courts ON Mall Sentul City,-6.5667229,106.8572357
Service Komputer dan Laptop Lengkap,-6.6150861,106.8002864
Pojoks Komputer,-6.6150706,106.8003277
Kingkong Elektronik,-6.614369,106.8028821
Denpoo Official store bogor,-6.6127687,106.802485
Vidiotron runningtext bogor,-6.6026773,106.8137921
Sound Story Botani Square,-6.6014221,106.8071254
"""
# Tambahkan kolom ALAMAT dan KATEGORI ke DataFrame 
# (Hanya jika Anda ingin menampilkannya di Streamlit, tapi untuk meminimalkan error 
# mari kita fokus pada LAT/LONG dan NAMA_MERCHANT saja)
# Kita akan menggunakan data_string asli yang hanya memiliki NAMA_MERCHANT, LAT, LONG
df = pd.read_csv(io.StringIO(data_string))


# --- 2. Fungsi untuk Membuat Tautan Google Maps (URL STANDAR UNIVERSAL) ---
def create_map_link(lat, lon):
    """
    Menggunakan format URL Directions API Google Maps yang paling umum 
    dan dijamin tidak diblokir oleh Streamlit/browser.
    """
    # Menggunakan https://www.google.com/maps/dir/?api=1&destination=<LAT>,<LONG>
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"

# Menambahkan kolom tautan ke DataFrame
df['Link Google Maps'] = df.apply(
    lambda row: create_map_link(row['LAT'], row['LONG']),
    axis=1
)

# --- 3. Konfigurasi dan Tampilan Streamlit ---

st.set_page_config(
    page_title="Daftar Merchant & Rute Maps",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🗺️ Daftar Merchant (Solusi Final & Universal)")
st.markdown("---")
st.success("Kami beralih ke format URL Google Maps Directions yang **paling standar dan universal** (`maps/dir/?api=1`). Ini seharusnya menyelesaikan masalah 404.")

st.subheader("Klik nama merchant di bawah ini untuk langsung diarahkan:")

# Menampilkan setiap merchant menggunakan st.link_button
for index, row in df.iterrows():
    name = row['NAMA_MERCHANT']
    map_link = row['Link Google Maps']
    location_text = f"Lat: {row['LAT']}, Long: {row['LONG']}"
    
    # Menggunakan st.link_button yang stabil
    st.link_button(
        label=f"➡️ {name}", 
        url=map_link,
        help=f"Langsung membuka Directions ke: {location_text}"
    )
    # Menambahkan detail lokasi
    st.caption(location_text)

st.markdown("---")
st.warning("""
**PENTING:** Jika solusi ini masih gagal (misalnya, hanya muncul peta, bukan mode Arah/Rute), maka lingkungan *hosting* Streamlit Anda **secara fundamental memblokir** semua URL Directions Google Maps.

**Verifikasi:** Coba salin URL dari salah satu tombol yang dihasilkan dan tempelkan langsung di bilah alamat *browser* Anda untuk memastikan bahwa tautan itu sendiri berfungsi dengan benar di luar Streamlit.
""")
