import streamlit as st

# ============================================================
# BancaPocket - Simple Mobile Dashboard
# ============================================================

st.set_page_config(
    page_title="BancaPocket",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
# Demo data
# Ganti bagian ini nanti dengan data Excel
# ------------------------------------------------------------
ASURADUR = [
    {
        "nama": "ASKRIDA",
        "jenis": "Asuransi Umum",
        "status": "Active",
        "warna": "#2563EB",
        "produk": ["KSM", "KUM", "KUR", "Asuransi Kebakaran", "Credit Life"],
        "deskripsi": "Mitra Bancassurance untuk perlindungan kredit dan aset.",
        "pic": "Bancassurance ASKRIDA",
        "phone": "021-XXXXXXX",
    },
    {
        "nama": "ASPAN",
        "jenis": "Asuransi Umum",
        "status": "Active",
        "warna": "#10B981",
        "produk": ["KSM", "KUM", "KUR", "Asuransi Kebakaran"],
        "deskripsi": "Mitra Bancassurance untuk kebutuhan perlindungan kredit.",
        "pic": "Bancassurance ASPAN",
        "phone": "021-XXXXXXX",
    },
    {
        "nama": "BOSOWA",
        "jenis": "Asuransi Umum",
        "status": "Active",
        "warna": "#F59E0B",
        "produk": ["KSM", "KUM", "Asuransi Kebakaran"],
        "deskripsi": "Mitra Bancassurance untuk perlindungan kredit dan aset.",
        "pic": "Bancassurance BOSOWA",
        "phone": "021-XXXXXXX",
    },
    {
        "nama": "JASINDO",
        "jenis": "Asuransi Umum",
        "status": "Active",
        "warna": "#7C3AED",
        "produk": ["KSM", "KUM", "KUR", "Asuransi Kebakaran", "Machinery Breakdown"],
        "deskripsi": "Mitra Bancassurance untuk berbagai kebutuhan proteksi.",
        "pic": "Bancassurance JASINDO",
        "phone": "021-XXXXXXX",
    },
]

# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #EEF4FF 100%);
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        max-width: 760px;
        padding: 24px 18px 100px 18px;
    }

    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }

    .brand-title {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
    }

    .brand-subtitle {
        color: #64748B;
        font-size: 12px;
        margin-top: 5px;
    }

    .logo {
        width: 50px;
        height: 50px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #2563EB, #60A5FA);
        box-shadow: 0 10px 25px rgba(37, 99, 235, .22);
        font-size: 25px;
    }

    .welcome {
        background: linear-gradient(135deg, #1D4ED8, #3B82F6);
        border-radius: 24px;
        padding: 22px;
        color: white;
        box-shadow: 0 15px 35px rgba(37, 99, 235, .20);
        margin-bottom: 20px;
    }

    .welcome-title {
        font-size: 20px;
        font-weight: 800;
    }

    .welcome-text {
        font-size: 12px;
        opacity: .86;
        margin-top: 6px;
    }

    .section-title {
        font-size: 17px;
        font-weight: 800;
        color: #0F172A;
        margin: 20px 0 10px 0;
    }

    .insurer-card {
        background: rgba(255,255,255,.92);
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 16px;
        margin-bottom: 10px;
        box-shadow: 0 7px 22px rgba(15,23,42,.05);
    }

    .insurer-row {
        display: flex;
        align-items: center;
    }

    .insurer-icon {
        width: 48px;
        height: 48px;
        min-width: 48px;
        border-radius: 15px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: 800;
        margin-right: 13px;
    }

    .insurer-name {
        color: #0F172A;
        font-size: 15px;
        font-weight: 800;
    }

    .insurer-type {
        color: #64748B;
        font-size: 11px;
        margin-top: 3px;
    }

    .active-pill {
        margin-left: auto;
        background: #DCFCE7;
        color: #15803D;
        padding: 5px 9px;
        border-radius: 20px;
        font-size: 9px;
        font-weight: 700;
    }

    .detail-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 12px 35px rgba(15,23,42,.07);
    }

    .detail-top {
        display: flex;
        align-items: center;
    }

    .detail-icon {
        width: 62px;
        height: 62px;
        min-width: 62px;
        border-radius: 19px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 23px;
        font-weight: 800;
        margin-right: 14px;
    }

    .detail-name {
        font-size: 22px;
        font-weight: 800;
        color: #0F172A;
    }

    .detail-type {
        font-size: 12px;
        color: #64748B;
        margin-top: 3px;
    }

    .description {
        color: #475569;
        font-size: 12px;
        line-height: 1.65;
        margin: 18px 0;
    }

    .product {
        display: inline-block;
        background: #EFF6FF;
        color: #1D4ED8;
        padding: 7px 10px;
        border-radius: 10px;
        margin: 3px;
        font-size: 10px;
        font-weight: 700;
    }

    .info {
        background: #F8FAFC;
        border-radius: 15px;
        padding: 13px;
        margin-top: 9px;
    }

    .info-label {
        color: #94A3B8;
        font-size: 10px;
    }

    .info-value {
        color: #334155;
        font-size: 12px;
        font-weight: 700;
        margin-top: 3px;
    }

    .bottom-nav {
        position: fixed;
        left: 50%;
        bottom: 12px;
        transform: translateX(-50%);
        width: min(92%, 680px);
        background: rgba(255,255,255,.94);
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 10px 14px;
        display: flex;
        justify-content: space-around;
        box-shadow: 0 12px 35px rgba(15,23,42,.13);
        z-index: 999;
    }

    .nav-item {
        text-align: center;
        color: #94A3B8;
        font-size: 9px;
        font-weight: 600;
    }

    .nav-active {
        color: #2563EB;
    }

    .nav-icon {
        font-size: 17px;
        margin-bottom: 2px;
    }

    /* Perkecil tombol Streamlit agar terasa seperti mobile app */
    div.stButton > button {
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        background: white;
        color: #2563EB;
        font-weight: 700;
        min-height: 38px;
    }

    div.stButton > button:hover {
        border-color: #93C5FD;
        color: #1D4ED8;
        background: #F8FAFC;
    }

    @media (max-width: 600px) {
        .block-container {
            padding-left: 14px;
            padding-right: 14px;
        }

        .brand-title {
            font-size: 23px;
        }

        .welcome {
            border-radius: 21px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Session state
# ------------------------------------------------------------
if "selected_insurer" not in st.session_state:
    st.session_state.selected_insurer = None

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <div>
            <div class="brand-title">BancaPocket</div>
            <div class="brand-subtitle">Bancassurance Partner Information</div>
        </div>
        <div class="logo">🛡️</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Detail page
# ------------------------------------------------------------
if st.session_state.selected_insurer:

    insurer = next(
        item for item in ASURADUR
        if item["nama"] == st.session_state.selected_insurer
    )

    if st.button("←  Kembali ke daftar", use_container_width=True):
        st.session_state.selected_insurer = None
        st.rerun()

    products_html = "".join(
        f'<span class="product">{product}</span>'
        for product in insurer["produk"]
    )

    st.markdown(
        f"""
        <div class="detail-card">
            <div class="detail-top">
                <div class="detail-icon"
                     style="background:linear-gradient(135deg,{insurer['warna']},#93C5FD);">
                    {insurer['nama'][0]}
                </div>

                <div>
                    <div class="detail-name">{insurer['nama']}</div>
                    <div class="detail-type">{insurer['jenis']} · {insurer['status']}</div>
                </div>
            </div>

            <div class="description">
                {insurer['deskripsi']}
            </div>

            <div class="section-title">Produk Bancassurance</div>

            <div>{products_html}</div>

            <div class="section-title">Informasi Kontak</div>

            <div class="info">
                <div class="info-label">PIC</div>
                <div class="info-value">{insurer['pic']}</div>
            </div>

            <div class="info">
                <div class="info-label">Telepon</div>
                <div class="info-value">{insurer['phone']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# Home page
# ------------------------------------------------------------
else:

    st.markdown(
        """
        <div class="welcome">
            <div class="welcome-title">Hello, Pegawai 👋</div>
            <div class="welcome-text">
                Temukan informasi Asuradur Partner Bancassurance
                dengan cepat dan mudah.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    search = st.text_input(
        "Cari Asuradur",
        placeholder="🔍  Cari nama Asuradur...",
        label_visibility="collapsed",
    )

    results = [
        insurer for insurer in ASURADUR
        if search.strip().lower() in insurer["nama"].lower()
    ]

    st.markdown(
        '<div class="section-title">Asuradur Partner</div>',
        unsafe_allow_html=True,
    )

    if not results:
        st.info("Asuradur tidak ditemukan.")
    else:
        for insurer in results:

            st.markdown(
                f"""
                <div class="insurer-card">
                    <div class="insurer-row">

                        <div class="insurer-icon"
                             style="background:linear-gradient(135deg,{insurer['warna']},#93C5FD);">
                            {insurer['nama'][0]}
                        </div>

                        <div>
                            <div class="insurer-name">{insurer['nama']}</div>
                            <div class="insurer-type">{insurer['jenis']}</div>
                        </div>

                        <div class="active-pill">● ACTIVE</div>

                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                f"Lihat {insurer['nama']} →",
                key=f"open_{insurer['nama']}",
                use_container_width=True,
            ):
                st.session_state.selected_insurer = insurer["nama"]
                st.rerun()

# ------------------------------------------------------------
# Bottom navigation
# ------------------------------------------------------------
st.markdown(
    """
    <div class="bottom-nav">
        <div class="nav-item nav-active">
            <div class="nav-icon">⌂</div>
            Home
        </div>

        <div class="nav-item">
            <div class="nav-icon">🛡️</div>
            Partner
        </div>

        <div class="nav-item">
            <div class="nav-icon">📚</div>
            Guide
        </div>

        <div class="nav-item">
            <div class="nav-icon">ℹ️</div>
            Info
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
