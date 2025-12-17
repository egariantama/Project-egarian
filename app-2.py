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
# NOMOR WHATSAPP (GANTI)
# =========================
WA_NUMBER = "6281234567890"  # tanpa +

# =========================
# STYLE MOBILE-FIRST (FIX WARNA)
# =========================
st.markdown("""
<style>
/* RESET */
html, body, [class*="css"] {
    background-color: #F7F9FC !important;
    color: #1A1A1A !important;
}

/* ===== HEADER ===== */
.header {
    background: linear-gradient(135deg, #0B1E3D, #1E4DB7);
    padding: 26px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 22px;
}
.header h1 {
    font-size: 22px;
    margin-bottom: 6px;
}
.header p {
    font-size: 14px;
    opacity: 0.95;
}

/* ===== CARD ===== */
.card {
    background: #FFFFFF;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 16px;
    color: #1A1A1A;
}
.card h3 {
    color: #1E4DB7;
    font-size: 17px;
    margin-bottom: 10px;
}
.card ul {
    padding-left: 18px;
}
.card li {
    font-size: 14px;
    margin-bottom: 6px;
    color: #1A1A1A;
}

/* ===== BUTTON ===== */
.cta {
    display: block;
    width: 100%;
    text-align: center;
    margin-top: 14px;
    padding: 12px;
    background-color: #FFD200;
    color: #0B1E3D !important;
    font-weight: 700;
    border-radius: 12px;
    text-decoration: none;
}

/* ===== WHATSAPP FLOAT ===== */
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
# MENU MOBILE
# =========================
menu = st.selectbox(
    "📌 Pilih Layanan",
    [
        "💍 Paket Wedding & Pembiayaan",
        "💑 Konseling Pernikahan",
        "👨‍👩‍👧 Konseling Parenting",
        "📩 Form Konsultasi"
    ]
)

# =========================
# TEMPLATE LINK WA
# =========================
def wa_link(pesan):
    encoded = urllib.parse.quote(pesan)
    return f"https://wa.me/{WA_NUMBER}?text={encoded}"

# =========================
# WEDDING
# =========================
if menu == "💍 Paket Wedding & Pembiayaan":
    st.markdown(f"""
    <div class="card">
        <h3>Paket Wedding Silver</h3>
        <ul>
            <li>Dekorasi & venue standar</li>
            <li>Katering 300 pax</li>
            <li>Dokumentasi</li>
            <li>Cicilan pembiayaan</li>
        </ul>
        <a class="cta" href="{wa_link('Halo, saya tertarik Paket Wedding Silver')}">Konsultasi Sekarang</a>
    </div>

    <div class="card">
        <h3>Paket Wedding Gold</h3>
        <ul>
            <li>WO profesional</li>
            <li>Dekorasi premium</li>
            <li>Katering 500 pax</li>
            <li>Pembiayaan & modal keluarga</li>
        </ul>
        <a class="cta" href="{wa_link('Halo, saya tertarik Paket Wedding Gold')}">Ajukan Pembiayaan</a>
    </div>
    """, unsafe_allow_html=True)

# =========================
# KONSELING PERNIKAHAN
# =========================
elif menu == "💑 Konseling Pernikahan":
    st.markdown(f"""
    <div class="card">
        <h3>Konseling Pra Nikah</h3>
        <ul>
            <li>Kesiapan mental & finansial</li>
            <li>Komunikasi pasangan</li>
            <li>Visi rumah tangga</li>
        </ul>
        <a class="cta" href="{wa_link('Halo, saya ingin Konseling Pra Nikah')}">Jadwalkan Sesi</a>
    </div>

    <div class="card">
        <h3>Konseling Pasca Nikah</h3>
        <ul>
            <li>Manajemen konflik</li>
            <li>Penguatan hubungan</li>
            <li>Pendampingan keluarga</li>
        </ul>
        <a class="cta" href="{wa_link('Halo, saya ingin Konseling Pasca Nikah')}">Mulai Konseling</a>
    </div>
    """, unsafe_allow_html=True)

# =========================
# PARENTING
# =========================
elif menu == "👨‍👩‍👧 Konseling Parenting":
    st.markdown(f"""
    <div class="card">
        <h3>Parenting Anak Usia Dini</h3>
        <ul>
            <li>Pola asuh positif</li>
            <li>Perkembangan emosi</li>
            <li>Komunikasi efektif</li>
        </ul>
        <a class="cta" href="{wa_link('Halo, saya ingin Konseling Parenting Anak')}">Konsultasi Parenting</a>
    </div>

    <div class="card">
        <h3>Parenting Remaja</h3>
        <ul>
            <li>Masalah emosi & sosial</li>
            <li>Pendampingan akademik</li>
            <li>Tantangan digital</li>
        </ul>
        <a class="cta" href="{wa_link('Halo, saya ingin Konseling Parenting Remaja')}">Mulai Sesi</a>
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
        if nama and pesan:
            text = f"Halo, saya {nama}. Saya tertarik {layanan}. Pesan: {pesan}"
            st.markdown(f"[📲 Klik kirim WhatsApp]({wa_link(text)})")
        else:
            st.warning("Mohon lengkapi nama dan pesan")

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
© 2025 Layanan Pernikahan & Keluarga • Mobile Optimized
</p>
""", unsafe_allow_html=True)
