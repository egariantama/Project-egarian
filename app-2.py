import streamlit as st
import urllib.parse

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Layanan Pernikahan & Keluarga",
    layout="centered"
)

# =========================
# NOMOR WHATSAPP
# =========================
WA_NUMBER = "6282147035769"

# =========================
# STYLE
# =========================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #F7F9FC !important;
    color: #1A1A1A !important;
}
.header {
    background: linear-gradient(135deg, #0B1E3D, #1E4DB7);
    padding: 26px;
    border-radius: 18px;
    color: white !important;
    text-align: center;
    margin-bottom: 18px;
}
.header h1, .header p { color: white !important; }
.promo {
    background: linear-gradient(90deg, #FFD200, #FFB703);
    padding: 14px;
    border-radius: 14px;
    text-align: center;
    font-weight: 700;
    margin-bottom: 18px;
    animation: pulse 1.8s infinite;
}
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.03); }
    100% { transform: scale(1); }
}
.card {
    background: #FFFFFF !important;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 16px;
}
.card * { color: #1A1A1A !important; }
.card h3 { color: #1E4DB7 !important; }
.price { font-size: 20px; font-weight: 800; margin: 10px 0; }
.cta {
    display: block;
    width: 100%;
    text-align: center;
    margin-top: 14px;
    padding: 14px;
    background-color: #1E4DB7;
    color: white !important;
    font-weight: 700;
    border-radius: 14px;
    text-decoration: none;
}
.whatsapp-float {
    position: fixed;
    bottom: 18px;
    right: 16px;
    background-color: #25D366;
    color: white !important;
    padding: 14px 18px;
    border-radius: 50px;
    font-weight: bold;
    text-decoration: none;
    z-index: 9999;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class="header">
    <h1>💍 Layanan Pernikahan & Keluarga</h1>
    <p>Dari persiapan pernikahan hingga membangun keluarga harmonis</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="promo">
🔥 Booking Sekarang & Dapatkan Potongan Hingga <b>20%</b> 🔥
</div>
""", unsafe_allow_html=True)

# =========================
# MENU
# =========================
menu = st.selectbox(
    "📌 Pilih Layanan",
    [
        "💍 Paket Wedding & Pembiayaan",
        "💳 Simulasi Kredit Wedding",
        "💰 Metode Pembayaran",
        "💑 Konseling Pernikahan",
        "👨‍👩‍👧 Konseling Parenting",
        "📩 Form Konsultasi"
    ]
)

def wa_link(text):
    return f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(text)}"

# =========================
# PAKET WEDDING
# =========================
if menu == "💍 Paket Wedding & Pembiayaan":
    st.markdown(f"""
    <div class="card">
        <h3>Paket Wedding Silver</h3>
        <div class="price">Rp 350.000.000</div>
        <ul>
            <li>Dekorasi & venue standar</li>
            <li>Katering 300 pax</li>
            <li>Dokumentasi</li>
            <li>Opsi cicilan / pembiayaan</li>
        </ul>
        <a class="cta" href="{wa_link('Halo, saya tertarik Paket Wedding Silver')}">
            Booking Sekarang
        </a>
    </div>

    <div class="card">
        <h3>Paket Wedding Gold</h3>
        <div class="price">Rp 550.000.000</div>
        <ul>
            <li>WO profesional full day</li>
            <li>Dekorasi premium</li>
            <li>Katering 500 pax</li>
            <li>Pembiayaan & modal awal keluarga</li>
        </ul>
        <a class="cta" href="{wa_link('Halo, saya tertarik Paket Wedding Gold')}">
            Ajukan Pembiayaan
        </a>
    </div>
    """, unsafe_allow_html=True)

# =========================
# SIMULASI KREDIT
# =========================
elif menu == "💳 Simulasi Kredit Wedding":
    st.subheader("💳 Simulasi Kredit / Cicilan Wedding")

    harga = st.number_input("Harga Paket (Rp)", min_value=50000000, step=10000000)
    dp = st.slider("DP (%)", 10, 50, 20)
    tenor = st.selectbox("Tenor (bulan)", [12, 24, 36, 48, 60])

    bunga = 6.9  # FIX per tahun
    st.info("📌 Bunga FIX 6,9% per tahun")

    dp_nominal = harga * dp / 100
    pokok = harga - dp_nominal
    bunga_bulanan = bunga / 12 / 100

    cicilan = (pokok * bunga_bulanan) / (1 - (1 + bunga_bulanan) ** -tenor)

    st.markdown(f"""
    <div class="card">
        <h3>Hasil Simulasi Kredit</h3>
        <p>Pokok Pembiayaan:</p>
        <b>Rp {pokok:,.0f}</b>
        <p>Bunga:</p>
        <b>6,9% FIX per tahun</b>
        <p>Cicilan per bulan:</p>
        <div class="price">Rp {cicilan:,.0f}</div>
        <a class="cta" href="{wa_link('Halo, saya ingin ajukan kredit wedding bunga fix 6,9%')}">
            Ajukan Sekarang
        </a>
    </div>
    """, unsafe_allow_html=True)

# =========================
# METODE PEMBAYARAN
# =========================
elif menu == "💰 Metode Pembayaran":
    st.markdown("""
    <div class="card">
        <h3>📱 QRIS</h3>
        <p>QRIS akan dikirim via WhatsApp</p>
    </div>

    <div class="card">
        <h3>🏦 Transfer Bank</h3>
        <ul>
            <li>Mandiri : 123000111222</li>
            <li>BNI : 8888888888</li>
            <li>BCA : 7777777777</li>
            <li>BRI : 6666666666</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================
# KONSELING
# =========================
elif menu == "💑 Konseling Pernikahan":
    st.markdown(f"""
    <div class="card">
        <h3>Konseling Pra & Pasca Nikah</h3>
        <ul>
            <li>Kesiapan mental & finansial</li>
            <li>Manajemen konflik</li>
            <li>Penguatan komunikasi</li>
        </ul>
        <a class="cta" href="{wa_link('Halo, saya ingin konseling pernikahan')}">
            Jadwalkan Sesi
        </a>
    </div>
    """, unsafe_allow_html=True)

elif menu == "👨‍👩‍👧 Konseling Parenting":
    st.markdown(f"""
    <div class="card">
        <h3>Konseling Parenting</h3>
        <ul>
            <li>Parenting anak & remaja</li>
            <li>Pola asuh positif</li>
            <li>Pendampingan keluarga</li>
        </ul>
        <a class="cta" href="{wa_link('Halo, saya ingin konseling parenting')}">
            Konsultasi Sekarang
        </a>
    </div>
    """, unsafe_allow_html=True)

# =========================
# FORM
# =========================
elif menu == "📩 Form Konsultasi":
    nama = st.text_input("Nama")
    pesan = st.text_area("Pesan")
    if st.button("Kirim WhatsApp"):
        st.markdown(f"[📲 Kirim]({wa_link(f'Halo saya {nama}. {pesan}')})")

# =========================
# FLOAT WA
# =========================
st.markdown(f"""
<a class="whatsapp-float" href="https://wa.me/{WA_NUMBER}" target="_blank">
💬 WhatsApp
</a>
""", unsafe_allow_html=True)

