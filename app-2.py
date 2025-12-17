import streamlit as st
import urllib.parse

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Wedding to Fund",
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
    <h1>💍 Wedding to Fund</h1>
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
        "💰 Metode Pembayaran",
        "💑 Konseling Pernikahan",
        "👨‍👩‍👧 Konseling Parenting",
        "📩 Form Konsultasi"
    ]
)

# =========================
# PAKET WEDDING
# =========================
if menu == "💍 Paket Wedding & Pembiayaan":

    st.subheader("💍 Pilih Paket Wedding & Skema Cicilan")

    paket = st.radio(
        "Pilih Paket Wedding",
        ["Silver – Rp 350.000.000", "Gold – Rp 550.000.000"]
    )

    if "Silver" in paket:
        harga = 350_000_000
        paket_nama = "Paket Wedding Silver"
    else:
        harga = 550_000_000
        paket_nama = "Paket Wedding Gold"

    # ===== CARD =====
    st.markdown(f"""
    <div class="card">
        <h3>{paket_nama}</h3>
        <div class="price">Rp {harga:,.0f}</div>
        <ul>
            <li>Dekorasi & WO profesional</li>
            <li>Katering sesuai paket</li>
            <li>Dokumentasi & support keluarga</li>
            <li><b>Tersedia cicilan bunga FIX 6,9%</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ===== SIMULASI =====
    dp = st.slider("DP (%)", 10, 50, 20)
    tenor = st.selectbox("Tenor (bulan)", [12, 24, 36, 48, 60])

    bunga = 6.9
    bunga_bulanan = bunga / 12 / 100
    dp_nominal = harga * dp / 100
    pokok = harga - dp_nominal
    cicilan = (pokok * bunga_bulanan) / (1 - (1 + bunga_bulanan) ** -tenor)

    st.markdown(f"""
    <div class="card">
        <h3>📊 Hasil Simulasi Cicilan</h3>
        <p>Harga Paket: <b>Rp {harga:,.0f}</b></p>
        <p>DP ({dp}%): <b>Rp {dp_nominal:,.0f}</b></p>
        <p>Pokok Pembiayaan: <b>Rp {pokok:,.0f}</b></p>
        <p>Bunga: <b>6,9% FIX per tahun</b></p>
        <p>Cicilan per bulan:</p>
        <div class="price">Rp {cicilan:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    # ===== CTA DIPISAH (INI PENTING) =====
    st.markdown(
        f"""
        <a class="cta" href="https://wa.me/{WA_NUMBER}?text=Halo, saya ingin ajukan {paket_nama} DP {dp}% tenor {tenor} bulan. Cicilan Rp {cicilan:,.0f}/bulan"
        target="_blank">
        🚀 Ajukan Sekarang
        </a>
        """,
        unsafe_allow_html=True
    )

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
    st.subheader("💑 Konseling Pernikahan")

    psikolog = st.selectbox(
        "Pilih Psikolog",
        [
            "Dr. Maya Putri, M.Psi – Pra Nikah & Komunikasi",
            "Ahmad Fauzi, M.Psi – Pasca Nikah & Emosi",
            "Konselor Online – Fleksibel & Privat"
        ]
    )

    if psikolog.startswith("Dr. Maya"):
        deskripsi = [
            "Spesialis Pra Nikah & Komunikasi Pasangan",
            "Pengelolaan konflik rumah tangga",
            "Penguatan emotional bonding"
        ]
        pesan_wa = "Halo, saya ingin konseling pernikahan dengan Dr. Maya Putri"
    elif psikolog.startswith("Ahmad"):
        deskripsi = [
            "Konseling Pasca Nikah",
            "Masalah kepercayaan & emosi",
            "Manajemen stres keluarga"
        ]
        pesan_wa = "Halo, saya ingin konseling pernikahan dengan Ahmad Fauzi"
    else:
        deskripsi = [
            "Sesi via Zoom / WhatsApp Call",
            "Cocok untuk pasangan LDR",
            "Privasi terjamin"
        ]
        pesan_wa = "Halo, saya ingin konseling pernikahan online"

    st.markdown(f"""
    <div class="card">
        <h3>🧠 {psikolog}</h3>
        <ul>
            <li>{deskripsi[0]}</li>
            <li>{deskripsi[1]}</li>
            <li>{deskripsi[2]}</li>
        </ul>
        <a class="cta" href="https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(pesan_wa)}">
            Konsultasi Sekarang
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











