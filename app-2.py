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
WA_NUMBER = "6282147035769"  # ganti nomor asli

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

# =========================
# WA LINK
# =========================
def wa_link(text):
    return f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(text)}"

# =========================
# SIMULASI KREDIT
# =========================
if menu == "💳 Simulasi Kredit Wedding":
    st.subheader("💳 Simulasi Kredit / Cicilan Wedding")

    harga = st.number_input("Harga Paket (Rp)", min_value=50000000, step=10000000)
    dp = st.slider("DP (%)", 10, 50, 20)
    tenor = st.selectbox("Tenor (bulan)", [12, 24, 36, 48, 60])
    bunga = st.slider("Bunga per tahun (%)", 6.0, 15.0, 10.0)

    dp_nominal = harga * dp / 100
    pokok = harga - dp_nominal
    bunga_bulanan = bunga / 12 / 100
    cicilan = (pokok * bunga_bulanan) / (1 - (1 + bunga_bulanan) ** -tenor)

    st.markdown(f"""
    <div class="card">
        <h3>Hasil Simulasi</h3>
        <p>Harga Paket: <b>Rp {harga:,.0f}</b></p>
        <p>DP ({dp}%): <b>Rp {dp_nominal:,.0f}</b></p>
        <p>Tenor: <b>{tenor} bulan</b></p>
        <p><b>Cicilan / bulan:</b></p>
        <div class="price">Rp {cicilan:,.0f}</div>
        <a class="cta" href="{wa_link('Halo, saya ingin ajukan pembiayaan wedding')}">
            Ajukan Sekarang
        </a>
    </div>
    """, unsafe_allow_html=True)

# =========================
# METODE PEMBAYARAN
# =========================
elif menu == "💰 Metode Pembayaran":
    st.subheader("💰 Metode Pembayaran")

    st.markdown("""
    <div class="card">
        <h3>📱 Pembayaran QRIS</h3>
        <ul>
            <li>Mendukung semua e-wallet & mobile banking</li>
            <li>OVO, GoPay, Dana, ShopeePay, Livin’, dll</li>
        </ul>
        <p><b>QRIS akan dikirim via WhatsApp</b></p>
        <a class="cta" href="https://wa.me/6282147035769">
            Minta QRIS
        </a>
    </div>

    <div class="card">
        <h3>🏦 Transfer Bank</h3>
        <ul>
            <li><b>Bank Mandiri</b> : 123000111222 a.n Wedding Service</li>
            <li><b>Bank BNI</b> : 8888888888 a.n Wedding Service</li>
            <li><b>Bank BCA</b> : 7777777777 a.n Wedding Service</li>
            <li><b>Bank BRI</b> : 6666666666 a.n Wedding Service</li>
        </ul>
        <p><i>*Mohon konfirmasi pembayaran via WhatsApp</i></p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# (MENU LAIN TETAP)
# =========================
elif menu == "📩 Form Konsultasi":
    st.subheader("📩 Form Konsultasi Cepat")
    nama = st.text_input("Nama Lengkap")
    layanan = st.selectbox("Pilih Layanan", ["Wedding", "Kredit Wedding", "Konseling"])
    pesan = st.text_area("Pesan")

    if st.button("Kirim via WhatsApp"):
        if nama and pesan:
            st.markdown(f"[📲 Kirim WhatsApp]({wa_link(f'Halo, saya {nama}. {pesan}')})")
        else:
            st.warning("Lengkapi data")

# =========================
# FLOAT WA
# =========================
st.markdown(f"""
<a class="whatsapp-float" href="https://wa.me/{WA_NUMBER}" target="_blank">
💬 WhatsApp
</a>
""", unsafe_allow_html=True)

st.markdown("""
<hr>
<p style="text-align:center; font-size:13px;">
© 2025 Layanan Pernikahan & Keluarga
</p>
""", unsafe_allow_html=True)
