import streamlit as st
import pandas as pd
import io

# --- 1. Data Merchant ---
data_string = """
NAMA_MERCHANT,LAT,LONG
PD MATERIAL CIBALOK,-6.6132027,106.8066751
MEDIA ELEKTRONIK 3,-6.6063072,106.8021991
KENT X GUSLI HOMES,-6.6073314,106.8002995
JIPANG CEL,-6.6043556,106.8039727
INDO PRIMA COMPUTER,-6.6066264,106.8008805
DEVAIZ COORPORATE,-6.6095033,106.8014339
CYGNUSWORKS INDONESIA,-6.6076137,106.8053613
CITY ELECTRONIC,-6.6060265,106.8006652
BOGOR NEON,-6.6085674,106.8041497
BK TECH COMPUTINDO,-6.611017,106.8053853
TOKO LAPTOP TERMURAH TERLENGKAP,-6.4845179,106.8423677
LEVOIT AIR PURIFIER CIBINONG CITY MALL,-6.4843587,106.8418851
JBL OFFICIAL STORE CIBINONG CITY MALL,-6.4843587,106.8418851
IT GALERI CIBINONG CITY MALL,-6.4842002,106.8423123
BOSCH ELECTORNIC CITY,-6.4844693,106.8421802
AGRES ID CIBINONG CITY MALL 1 LAPTOP SPESIALIS,-6.4842002,106.8423123
TOKO KOMPUTER DAN ACESSORIES,-6.5690996,106.8077601
TOKO DIGITAL CAHAYA,-6.577761,106.8075371
RAMASTORE,-6.5778193,106.8075136
LG,-6.569193,106.807814
LENOVO HANDPHONE,-6.569193,106.807814
JUAL BELI HANDPHONE OPPO VIVO IPHONE DAN LAIN LAIN,-6.577761,106.8075372
INKQ,-6.56947,106.8079
HANDJAYA COMPUTER,-6.5693051,106.8077829
CONDEL SERVICE,-6.5758667,106.8082511
POPYVORA,-6.6116114,106.8103135
PANGGUNGDIGITAL,-6.6056214,106.8129063
MATRIAL EPUL,-6.6153052,106.8183351
KEDAI DATA,-6.6112593,106.8097489
JUAL KEPINGAN CD BP TANTO,-6.6182139,106.8123361
HJAMALUDIN CELL,-6.6162339,106.8128572
BENGKEL MOTOR 3M,-6.6163773,106.8175873
ACENG PRODUCTION BOGOR KOTA,-6.6050875,106.8140603
ABICOM SERVIS KOMPUTER,-6.6178859,106.8157697
SENTUL SHOP,-6.5675072,106.8582132
PUSAT ELEKTRONIK SENTUL BOGOR,-6.5671158,106.8587295
LAPTOP SENTUL,-6.5685382,106.8569716
KLIKNKLIK AEON SENTUL CITY,-6.56834,106.8558641
JBL AEON SENTUL,-6.5667823,106.8587381
ELECTRONIC AEON STORE SENTUL CITY,-6.5675052,106.8582185
COURTS ON MALL SENTUL CITY,-6.5667229,106.8572357
SERVICE KOMPUTER DAN LAPTOP LENGKAP,-6.6150861,106.8002864
POJOKS KOMPUTER,-6.6150706,106.8003277
KINGKONG ELEKTRONIK,-6.614369,106.8028821
DENPOO OFFICIAL STORE BOGOR,-6.6127687,106.802485
VIDIOTRON RUNNINGTEXT BOGOR,-6.6026773,106.8137921
SOUND STORY BOTANI SQUARE,-6.6014221,106.8071254
"""
df = pd.read_csv(io.StringIO(data_string))

# --- 2. Fungsi untuk Membuat Tautan Google Maps (URL DIRECTIONS STANDAR) ---
def create_map_link(lat, lon):
    """
    Menggunakan URL Directions API standar: 
    https://www.google.com/maps/dir/?api=1&destination=<LAT>,<LONG>
    Ini adalah format yang paling stabil dan tidak menyebabkan 404.
    """
    # Mengubah prefix yang bermasalah menjadi prefix yang stabil dan menggunakan parameter standar
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}&travelmode=driving"

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

st.title("🗺️ Daftar Merchant (Solusi URL Directions API)")
st.markdown("---")
st.success("Kami beralih ke URL Directions Google Maps yang paling stabil. Ini dijamin akan memunculkan mode Arah/Rute.")

st.subheader("Pilih Merchant Tujuan Anda:")

# Menampilkan setiap merchant menggunakan st.link_button
for index, row in df.iterrows():
    name = row['NAMA_MERCHANT']
    map_link = row['Link Google Maps']
    location_text = f"Lat: {row['LAT']}, Long: {row['LONG']}"
    
    # Menggunakan st.link_button yang stabil
    st.link_button(
        label=f"🚦 Mulai Arah/Rute ke: {name}", 
        url=map_link,
        help=f"Langsung membuka mode Directions ke: {location_text}"
    )
    # Menambahkan detail lokasi
    st.caption(location_text)

st.markdown("---")
st.info("""
**Langkah Penting Setelah Mengklik Tombol:**
1.  Tab baru akan terbuka di Google Maps.
2.  Google Maps akan secara otomatis mendeteksi lokasi Anda saat ini sebagai titik awal.
3.  Anda akan melihat tombol besar untuk **"Mulai Navigasi"** atau **"Arah"**.
""")
