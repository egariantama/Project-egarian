import streamlit as st
import urllib.parse

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Layanan Pernikahan & Keluarga",
    layout="wide"
)

# =========================
# NOMOR WHATSAPP (GANTI)
# =========================
WA_NUMBER = "6281234567890"  # tanpa +

# =========================
# STYLE MOBILE-FIRST
# =========================
st.markdown("""
<style>
body {
    background-color: #F7F9FC;
    color: #1A1A1A;
}

/* ===== HEADER ===== */
.header {
    background: linear-gradient(135deg, #0B1E3D, #1E4DB7);
    padding: 28px;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
.header h1 {
    font-size: 24px;
}
.header p {
    font-size: 14px;
    opacity: 0.95;
}

/* ===== CARD ===== */
.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 18px;
}
.card h3 {
    color: #1E4DB7;
    font-size: 18px;
}
.card li {
    font-size: 14px;
    margin-bottom: 6px;
}

/* ===== BUTTON ===== */
.cta {
    display: block;
    width: 100%;
    text-align: center;
    margin-top: 14px;
    padding: 12px;
    background-color: #FFD200;
    color: #0B1E3D;
    font-weight: 700;
    border-radius: 10px;
    text-decoration: none;
}

/* ===== WHATSAPP FLOAT ===== */
.whatsapp-float {
    position: fixed;
    bottom: 20px;
    right: 18px;
    background-color: #25D366;
    color: white;
    padding: 14px 16px;
    border-radius: 50px;
    font-weight: bold;
    text-decoration: none;
    z-index: 9999;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
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

# =========================
# MENU MOBILE (SELECTBOX)
# =========================
menu = st.selectbox(
    "Pilih Layanan",
    [
        "💍 Paket Wedding & Pembiayaan",
        "💑 Konseling Pernikahan",
        "👨‍👩‍👧 Konseling Parenting",
        "📩 Form Konsultasi"
    ]
)

# =========================
# WEDDING
# =========================
if menu == "💍 Paket Wedding & Pembiayaan":
    st.markdown("""
    <div class="card">
        <h3>Paket Wedding Silver</h3>
        <ul>
            <li>Dekorasi & venue standar</li>
            <li>Katering 300 pax</li>
            <li>Dokumentasi</li>
            <li>Cicilan pembiayaan</li>
        </ul>
        <a class="cta" href="#">Konsultasi Sekarang</a>
    </div>

    <div class="card">
        <h3>Paket Wedding Gold</h3>
        <ul>
            <li>WO profesional</li>
            <li>Dekorasi premium</li>
            <li>Katering 500 pax</li>
            <li>Pembiayaan & modal keluarga</li>
        </ul>
        <a class="cta" href="#">Ajukan Pembiayaan</a>
    </div>
    """, unsafe_allow_html=True)

# =========================
# KONSELING PERNIKAHAN
# =========================
elif menu == "💑 Konseling Pernikahan":
    st.markdown("""
    <div class="card">
        <h3>Konseling Pra Nikah</h3>
        <ul>
            <li>Kesiapan mental & finansial</li>
            <li>Komunikasi pasangan</li>
            <li>Visi rumah tangga</li>
        </ul>
        <a class="cta" href="#">Jadwalkan Sesi</a>
    </div>

    <div class="card">
        <h3>Konseling Pasca Nikah</h3>
        <ul>
            <li>Manajemen konflik</li>
            <li>Penguatan hubungan</li>
            <li>Pendampingan keluarga</li>
        </ul>
        <a class="cta" href="#">Mulai Konseling</a>
    </div>
    """, unsafe_allow_html=True)

# =========================
# PARENTING
# =========================
elif menu == "👨‍👩‍👧 Konseling Parenting":
    st.markdown("""
    <div class="card">
        <h3>Parenting Anak Usia Dini</h3>
        <ul>
            <li>Pola asuh positif</li>
            <li>Perkembangan emosi</li>
            <li>Komunikasi efektif</li>
        </ul>
        <a class="cta" href="#">Konsultasi Parenting</a>
    </div>

    <div class="card">
        <h3>Parenting Remaja</h3>
        <ul>
            <li>Masalah emosi & sosial</li>
            <li>Pendampingan akademik</li>
            <li>Tantangan digital</li>
        </ul>
        <a class="cta" href="#">Mulai Sesi</a>
    </div>
    """, unsafe_allow_html=True)

# =========================
# FORM KONSULTASI
# =========================
elif menu == "📩 Form Konsultasi":
    st.subheader("📩 Form Konsultasi Cepat")

    nama = st.text_input("Nama Lengkap")
    layanan = st.selectbox(
        "Pilih Layanan",
        ["Wedding", "Konseling Pernikahan", "Konseling Parenting"]
    )
    pesan = st.text_area("Ceritakan kebutuhan Anda")

    if st.button("Kirim via WhatsApp"):
        text = f"""
Halo, saya *{nama}*
Saya tertarik dengan layanan *{layanan}*
Pesan:
{pesan}
"""
        encoded = urllib.parse.quote(text)
        wa_url = f"https://wa.me/{WA_NUMBER}?text={encoded}"
        st.markdown(f"[Klik untuk kirim WhatsApp]({wa_url})")

# =========================
# FLOATING WHATSAPP
# =========================
st.markdown(
    f"""
    <a class="whatsapp-float"
       href="https://wa.me/{WA_NUMBER}"
       target="_blank">
       💬 WhatsApp
    </a>
    """,
    unsafe_allow_html=True
)

# =========================
# FOOTER
# =========================
st.markdown("""
<hr>
<p style="text-align:center; font-size:13px; color:#666;">
© 2025 Layanan Pernikahan & Keluarga • Mobile Friendly
</p>
""", unsafe_allow_html=True)
