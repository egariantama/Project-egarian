import streamlit as st

# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="BancaPocket",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# DATA CONTOH
# Nanti bisa diganti dengan Excel / database
# ============================================================

ASURADUR = [
    {
        "nama": "ASKRIDA",
        "jenis": "Asuransi Umum",
        "status": "Active",
        "warna": "#2563EB",
        "inisial": "A",
        "produk": [
            "KSM",
            "KUM",
            "KUR",
            "Asuransi Kebakaran",
            "Credit Life"
        ],
        "deskripsi": "Mitra Bancassurance untuk perlindungan kredit dan aset.",
        "contact": "Bancassurance ASKRIDA",
        "phone": "021-xxxxxxx"
    },
    {
        "nama": "ASPAN",
        "jenis": "Asuransi Umum",
        "status": "Active",
        "warna": "#10B981",
        "inisial": "A",
        "produk": [
            "KSM",
            "KUM",
            "KUR",
            "Asuransi Kebakaran"
        ],
        "deskripsi": "Mitra Bancassurance untuk kebutuhan perlindungan kredit.",
        "contact": "Bancassurance ASPAN",
        "phone": "021-xxxxxxx"
    },
    {
        "nama": "BOSOWA",
        "jenis": "Asuransi Umum",
        "status": "Active",
        "warna": "#F59E0B",
        "inisial": "B",
        "produk": [
            "KSM",
            "KUM",
            "Asuransi Kebakaran"
        ],
        "deskripsi": "Mitra Bancassurance untuk perlindungan kredit dan properti.",
        "contact": "Bancassurance BOSOWA",
        "phone": "021-xxxxxxx"
    },
    {
        "nama": "JASINDO",
        "jenis": "Asuransi Umum",
        "status": "Active",
        "warna": "#7C3AED",
        "inisial": "J",
        "produk": [
            "KSM",
            "KUM",
            "KUR",
            "Asuransi Kebakaran",
            "Machinery Breakdown"
        ],
        "deskripsi": "Mitra Bancassurance untuk berbagai kebutuhan proteksi.",
        "contact": "Bancassurance JASINDO",
        "phone": "021-xxxxxxx"
    },
    {
        "nama": "SINARMAS",
        "jenis": "Asuransi Umum",
        "status": "Active",
        "warna": "#EF4444",
        "inisial": "S",
        "produk": [
            "KSM",
            "KUM",
            "KUR",
            "Asuransi Kebakaran"
        ],
        "deskripsi": "Mitra Bancassurance untuk perlindungan kredit dan aset.",
        "contact": "Bancassurance SINARMAS",
        "phone": "021-xxxxxxx"
    }
]


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        linear-gradient(
            180deg,
            #F8FAFC 0%,
            #EEF4FF 100%
        );
}

/* Hilangkan menu Streamlit */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Container */

.block-container {
    max-width: 760px;
    padding-top: 25px;
    padding-bottom: 80px;
}

/* Header */

.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
}

.logo-box {
    width: 52px;
    height: 52px;
    border-radius: 17px;

    background:
        linear-gradient(
            135deg,
            #2563EB,
            #60A5FA
        );

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 25px;

    box-shadow:
        0px 10px 25px
        rgba(37,99,235,0.25);
}

.title {
    font-size: 25px;
    font-weight: 800;
    color: #0F172A;
}

.subtitle {
    color: #64748B;
    font-size: 13px;
    margin-top: 3px;
}

/* Welcome */

.welcome {
    padding: 24px;

    border-radius: 26px;

    background:
        linear-gradient(
            135deg,
            #1D4ED8,
            #3B82F6
        );

    color: white;

    box-shadow:
        0px 15px 35px
        rgba(37,99,235,0.22);

    margin-bottom: 20px;
}

.welcome-title {
    font-size: 22px;
    font-weight: 800;
}

.welcome-text {
    font-size: 13px;
    opacity: 0.85;
    margin-top: 6px;
}

/* Search */

.search-title {
    font-size: 14px;
    font-weight: 700;
    color: #334155;
    margin-bottom: 7px;
}

/* Section */

.section-title {
    font-size: 18px;
    font-weight: 800;
    color: #0F172A;
    margin-top: 25px;
    margin-bottom: 12px;
}

/* Insurance Card */

.insurance-card {
    background: rgba(255,255,255,0.88);

    border: 1px solid
        rgba(226,232,240,0.9);

    border-radius: 22px;

    padding: 17px;

    margin-bottom: 12px;

    box-shadow:
        0px 7px 22px
        rgba(15,23,42,0.05);
}

.insurance-row {
    display: flex;
    align-items: center;
}

.insurance-icon {
    width: 48px;
    height: 48px;

    border-radius: 15px;

    display: flex;
    align-items: center;
    justify-content: center;

    color: white;

    font-size: 19px;
    font-weight: 800;

    margin-right: 13px;
}

.insurance-name {
    font-weight: 800;
    font-size: 16px;
    color: #0F172A;
}

.insurance-type {
    font-size: 12px;
    color: #64748B;
    margin-top: 3px;
}

.active {
    margin-left: auto;

    background: #DCFCE7;
    color: #15803D;

    font-size: 10px;
    font-weight: 700;

    padding: 5px 9px;

    border-radius: 20px;
}

/* Detail */

.detail-card {
    background: white;

    border-radius: 26px;

    padding: 24px;

    box-shadow:
        0px 12px 35px
        rgba(15,23,42,0.08);
}

.detail-header {
    display: flex;
    align-items: center;
}

.detail-icon {
    width: 64px;
    height: 64px;

    border-radius: 20px;

    display: flex;
    align-items: center;
    justify-content: center;

    color: white;

    font-size: 25px;
    font-weight: 800;

    margin-right: 15px;
}

.detail-name {
    font-size: 23px;
    font-weight: 800;
}

.detail-type {
    color: #64748B;
    font-size: 13px;
}

.description {
    color: #475569;
    font-size: 13px;
    line-height: 1.6;

    margin-top: 18px;
}

/* Product */

.product {
    display: inline-block;

    background: #EFF6FF;

    color: #1D4ED8;

    padding: 8px 12px;

    border-radius: 12px;

    margin: 4px;

    font-size: 12px;
    font-weight: 600;
}

/* Info */

.info-card {
    background: #F8FAFC;

    border-radius: 17px;

    padding: 15px;

    margin-top: 10px;
}

.info-label {
    font-size: 11px;
    color: #94A3B8;
}

.info-value {
    font-size: 13px;
    font-weight: 700;
    color: #334155;

    margin-top: 4px;
}

/* Bottom navigation */

.bottom-nav {
    position: fixed;

    bottom: 15px;

    left: 50%;

    transform: translateX(-50%);

    width: min(92%, 700px);

    background:
        rgba(255,255,255,0.94);

    backdrop-filter: blur(15px);

    border:
        1px solid
        rgba(226,232,240,0.9);

    border-radius: 22px;

    padding: 12px 20px;

    display: flex;

    justify-content:
        space-around;

    box-shadow:
        0px 12px 35px
        rgba(15,23,42,0.13);

    z-index: 999;
}

.nav-item {
    text-align: center;

    color: #94A3B8;

    font-size: 10px;
}

.nav-active {
    color: #2563EB;
    font-weight: 700;
}

.nav-icon {
    font-size: 19px;
    margin-bottom: 2px;
}

/* Mobile */

@media (max-width: 600px) {

    .block-container {
        padding-left: 16px;
        padding-right: 16px;
    }

    .title {
        font-size: 22px;
    }

    .welcome {
        padding: 20px;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "selected" not in st.session_state:
    st.session_state.selected = None


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="app-header">

    <div>
        <div class="title">
            BancaPocket
        </div>

        <div class="subtitle">
            Bancassurance Partner Information
        </div>
    </div>

    <div class="logo-box">
        🛡️
    </div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# WELCOME CARD
# ============================================================

st.markdown(
    """
<div class="welcome">

    <div class="welcome-title">
        Hello, Pegawai 👋
    </div>

    <div class="welcome-text">
        Temukan informasi Asuradur Partner
        Bancassurance dengan cepat.
    </div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# DETAIL PAGE
# ============================================================

if st.session_state.selected:

    selected = next(
        x for x in ASURADUR
        if x["nama"] == st.session_state.selected
    )

    if st.button("← Kembali ke Daftar"):

        st.session_state.selected = None
        st.rerun()

    st.markdown(
        f"""
<div class="detail-card">

    <div class="detail-header">

        <div
            class="detail-icon"
            style="background:{selected['warna']};"
        >
            {selected['inisial']}
        </div>

        <div>

            <div class="detail-name">
                {selected['nama']}
            </div>

            <div class="detail-type">
                {selected['jenis']}
            </div>

        </div>

    </div>

    <div class="description">
        {selected['deskripsi']}
    </div>

    <div class="section-title">
        Produk yang tersedia
    </div>

    <div>
        {
            ''.join(
                f'<span class="product">{p}</span>'
                for p in selected["produk"]
            )
        }
    </div>

    <div class="section-title">
        Informasi Kontak
    </div>

    <div class="info-card">

        <div class="info-label">
            PIC / Contact
        </div>

        <div class="info-value">
            {selected['contact']}
        </div>

    </div>

    <div class="info-card">

        <div class="info-label">
            Telepon
        </div>

        <div class="info-value">
            {selected['phone']}
        </div>

    </div>

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# MAIN PAGE
# ============================================================

else:

    st.markdown(
        """
<div class="search-title">
    Cari Asuradur
</div>
""",
        unsafe_allow_html=True
    )

    search = st.text_input(
        "Cari",
        placeholder="Contoh: ASKRIDA...",
        label_visibility="collapsed"
    )

    # Filter

    hasil = [
        x for x in ASURADUR
        if search.lower() in x["nama"].lower()
    ]

    st.markdown(
        """
<div class="section-title">
    Asuradur Partner
</div>
""",
        unsafe_allow_html=True
    )

    if not hasil:

        st.info(
            "Asuradur tidak ditemukan."
        )

    for insurer in hasil:

        st.markdown(
            f"""
<div class="insurance-card">

    <div class="insurance-row">

        <div
            class="insurance-icon"
            style="
                background:
                linear-gradient(
                    135deg,
                    {insurer['warna']},
                    #93C5FD
                );
            "
        >
            {insurer['inisial']}
        </div>

        <div>

            <div class="insurance-name">
                {insurer['nama']}
            </div>

            <div class="insurance-type">
                {insurer['jenis']}
            </div>

        </div>

        <div class="active">
            ● Active
        </div>

    </div>

</div>
""",
            unsafe_allow_html=True
        )

        if st.button(
            f"Lihat {insurer['nama']}",
            key=f"btn_{insurer['nama']}",
            use_container_width=True
        ):

            st.session_state.selected = insurer["nama"]
            st.rerun()


# ============================================================
# BOTTOM NAVIGATION
# ============================================================

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
    unsafe_allow_html=True
)
