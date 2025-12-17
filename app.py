import streamlit as st

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Layanan Pernikahan & Keluarga",
    layout="wide"
)

# =========================
# STYLE GLOBAL
# =========================
st.markdown(
    """
    <style>
    body {
        background-color: #F7F9FC;
    }
    .header {
        background: linear-gradient(135deg, #0B1E3D, #1E4DB7);
        padding: 40px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .section-title {
        color: #0B1E3D;
        margin-bottom: 20px;
    }
    .card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        height: 100%;
    }
    .cta {
        display: inline-block;
        margin-top: 15px;
        padding: 10px 16px;
        background-color: #FFD200;
        color: #0B1E3D;
        font-weight: bold;
        border-radius: 8px;
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HEADER
# =========================
st.markdown(
    """
    <div class="header">
        <h1>Layanan Pernikahan & Keluarga</h1>
        <p>Mendampingi perjalanan sakral pernikahan hingga membangun keluarga harmonis</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# MENU NAVIGASI
# =========================
menu = st.tabs([
    "💍 Paket Wedding & Pembiayaan",
    "💑 Konseling Pernikahan",
    "👨‍👩‍👧 Konseling Parenting"
])

# =========================
# TAB 1 – WEDDING
# =========================
with menu[0]:
    st.markdown("<h2 class='section-title'>Penawaran Paket Wedding & Pembiayaan</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h3>Paket Wedding Silver</h3>
                <ul>
                    <li>Venue & dekorasi standar</li>
                    <li>MC & dokumentasi</li>
                    <li>Katering 300 pax</li>
                    <li>Opsi cicilan pembiayaan</li>
                </ul>
                <a class="cta" href="#">Konsultasi Sekarang</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h3>Paket Wedding Gold</h3>
                <ul>
                    <li>Venue premium & dekorasi eksklusif</li>
                    <li>Wedding Organizer profesional</li>
                    <li>Katering 500 pax</li>
                    <li>Pembiayaan & modal usaha keluarga</li>
                </ul>
                <a class="cta" href="#">Ajukan Pembiayaan</a>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# TAB 2 – KONSELING PERNIKAHAN
# =========================
with menu[1]:
    st.markdown("<h2 class='section-title'>Konsultasi & Konseling Pernikahan</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h3>Konseling Pra Nikah</h3>
                <ul>
                    <li>Kesiapan mental & finansial</li>
                    <li>Komunikasi pasangan</li>
                    <li>Perencanaan kehidupan rumah tangga</li>
                </ul>
                <a class="cta" href="#">Jadwalkan Sesi</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h3>Konseling Pasca Nikah</h3>
                <ul>
                    <li>Manajemen konflik rumah tangga</li>
                    <li>Penguatan hubungan suami-istri</li>
                    <li>Pendampingan masalah keluarga</li>
                </ul>
                <a class="cta" href="#">Konseling Sekarang</a>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# TAB 3 – KONSELING PARENTING
# =========================
with menu[2]:
    st.markdown("<h2 class='section-title'>Konsultasi & Konseling Parenting</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h3>Parenting Anak Usia Dini</h3>
                <ul>
                    <li>Pola asuh positif</li>
                    <li>Perkembangan emosi anak</li>
                    <li>Komunikasi efektif orang tua & anak</li>
                </ul>
                <a class="cta" href="#">Konsultasi Parenting</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h3>Parenting Remaja</h3>
                <ul>
                    <li>Pendampingan akademik</li>
                    <li>Masalah emosi & sosial</li>
                    <li>Tantangan digital & pergaulan</li>
                </ul>
                <a class="cta" href="#">Mulai Sesi</a>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# FOOTER
# =========================
st.markdown(
    """
    <hr>
    <p style="text-align:center; color:gray;">
    © 2025 Layanan Pernikahan & Keluarga • Konseling Profesional & Terpercaya
    </p>
    """,
    unsafe_allow_html=True
)
