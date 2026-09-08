import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# BANCA POCKET - Directory Perusahaan Asuransi
# Mobile-first Streamlit application
# ============================================================

st.set_page_config(
    page_title="BancaPocket",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
# 1. DATABASE
# ------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "data" / "Data_Asuransi.xlsx"


@st.cache_data
def load_data():
    if not DATA_FILE.exists():
        return None, (
            f"File database tidak ditemukan.\n\n"
            f"Pastikan file berada di:\n`data/Data_Asuransi.xlsx`"
        )

    try:
        # Membaca sheet pertama secara otomatis
        book = pd.ExcelFile(DATA_FILE)
        sheet = book.sheet_names[0]
        df = pd.read_excel(DATA_FILE, sheet_name=sheet)
        df.columns = [str(c).strip() for c in df.columns]
        return df, None
    except Exception as e:
        return None, f"Gagal membaca Excel: {e}"


# ------------------------------------------------------------
# 2. NORMALISASI KOLOM
# ------------------------------------------------------------
def normalize_name(value):
    return (
        str(value)
        .strip()
        .lower()
        .replace("\n", " ")
        .replace("_", " ")
        .replace("-", " ")
        .replace("/", " ")
    )


def find_column(df, candidates):
    normalized = {normalize_name(c): c for c in df.columns}

    # exact match
    for candidate in candidates:
        key = normalize_name(candidate)
        if key in normalized:
            return normalized[key]

    # partial match
    for col in df.columns:
        ncol = normalize_name(col)
        for candidate in candidates:
            nc = normalize_name(candidate)
            if nc in ncol or ncol in nc:
                return col

    return None


df, load_error = load_data()

if load_error:
    st.markdown(
        f"""
        <div class="error-box">
            <div class="error-title">Database belum tersedia</div>
            <div>{load_error.replace(chr(10), '<br>')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# Kolom utama yang dicari. Aplikasi tetap berjalan walaupun beberapa
# kolom belum tersedia.
COL = {
    "nama": find_column(df, [
        "Nama Asuransi", "Nama Asuradur", "Asuradur", "Perusahaan Asuransi",
        "Nama Perusahaan"
    ]),
    "jenis": find_column(df, [
        "Jenis Asuransi", "Jenis", "Kategori", "Tipe Asuransi"
    ]),
    "investasi": find_column(df, [
        "Investasi", "Investasi (Rp Miliar)", "Investasi Rp Miliar"
    ]),
    "aset": find_column(df, [
        "Aset", "Aset (Rp Miliar)", "Aset Rp Miliar"
    ]),
    "ekuitas": find_column(df, [
        "Ekuitas", "Ekuitas (Rp Miliar)", "Ekuitas Rp Miliar"
    ]),
    "pendapatan": find_column(df, [
        "Pendapatan Jasa Asuransi",
        "Pendapatan Jasa Asuransi (Rp Miliar)",
        "Pendapatan"
    ]),
    "laba": find_column(df, [
        "Laba (Rugi)", "Laba Rugi", "Laba", "Rugi"
    ]),
    "pks_kredit": find_column(df, [
        "PKS Rekanan Perkreditan", "PKS Kredit", "PKS Perkreditan",
        "Rekanan Perkreditan"
    ]),
    "pks_banca": find_column(df, [
        "PKS Bancassurance", "PKS Banca", "Bancassurance"
    ]),
}

# Kalau kolom nama belum ditemukan, gunakan kolom pertama sebagai fallback.
if COL["nama"] is None and len(df.columns) > 0:
    COL["nama"] = df.columns[0]


# ------------------------------------------------------------
# 3. CSS - MOBILE / SMOOTH UI
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 50% -10%, rgba(37,99,235,.16), transparent 32%),
            linear-gradient(180deg, #f7faff 0%, #eef4fb 100%);
    }

    .block-container {
        max-width: 620px;
        padding: 0.7rem 0.75rem 5.5rem 0.75rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Hide Streamlit chrome */
    #MainMenu, footer {
        visibility: hidden;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 24px 22px 25px 22px;
        border-radius: 28px;
        color: white;
        background:
            radial-gradient(circle at 85% 20%, rgba(147,197,253,.55), transparent 28%),
            linear-gradient(135deg, #1746b7 0%, #1769e8 55%, #3185f4 100%);
        box-shadow: 0 14px 35px rgba(30, 91, 210, .20);
        margin-bottom: 14px;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 180px;
        height: 180px;
        right: -70px;
        bottom: -110px;
        border-radius: 50%;
        background: rgba(255,255,255,.13);
    }

    .hero-title {
        font-size: 29px;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        margin-top: 8px;
        font-size: 15px;
        font-weight: 600;
        opacity: .97;
    }

    .hero-caption {
        margin-top: 6px;
        font-size: 12px;
        opacity: .82;
    }

    .shield {
        position: absolute;
        right: 19px;
        top: 18px;
        width: 54px;
        height: 54px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 18px;
        background: rgba(255,255,255,.17);
        border: 1px solid rgba(255,255,255,.30);
        font-size: 29px;
        backdrop-filter: blur(8px);
    }

    .section-title {
        margin: 16px 4px 9px;
        font-size: 20px;
        font-weight: 800;
        color: #12213d;
    }

    .count-text {
        color: #60718f;
        font-size: 13px;
        margin: 2px 4px 10px;
    }

    .company-card {
        background: rgba(255,255,255,.92);
        border: 1px solid #e4ebf4;
        border-radius: 21px;
        padding: 15px;
        margin: 9px 0;
        box-shadow: 0 6px 18px rgba(24, 55, 100, .07);
    }

    .company-top {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .company-icon {
        min-width: 54px;
        width: 54px;
        height: 54px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 20px;
        font-weight: 800;
        background: linear-gradient(135deg,#2563eb,#7cb7ff);
        box-shadow: 0 8px 16px rgba(37,99,235,.18);
    }

    .company-name {
        color: #142443;
        font-size: 14px;
        line-height: 1.25;
        font-weight: 800;
    }

    .company-type {
        color: #74839d;
        font-size: 11px;
        margin-top: 3px;
    }

    .metric-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 7px;
        margin-top: 13px;
    }

    .metric {
        background: #f7f9fc;
        border-radius: 12px;
        padding: 8px 7px;
    }

    .metric-label {
        color: #7a8aa4;
        font-size: 9px;
        font-weight: 600;
    }

    .metric-value {
        color: #203453;
        font-size: 12px;
        font-weight: 800;
        margin-top: 2px;
    }

    .status-row {
        display: flex;
        gap: 7px;
        margin-top: 9px;
    }

    .status {
        flex: 1;
        text-align: center;
        border-radius: 10px;
        padding: 7px 4px;
        font-size: 10px;
        font-weight: 800;
    }

    .yes {
        color: #087a4b;
        background: #e5f8ef;
    }

    .no {
        color: #c93434;
        background: #ffebeb;
    }

    .detail-card {
        background: white;
        border: 1px solid #e3eaf3;
        border-radius: 22px;
        padding: 17px;
        margin: 10px 0;
        box-shadow: 0 8px 22px rgba(24,55,100,.07);
    }

    .detail-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 9px;
    }

    .detail-item {
        border: 1px solid #e7edf5;
        border-radius: 14px;
        padding: 12px;
        background: #fbfcfe;
    }

    .detail-label {
        color: #74839d;
        font-size: 10px;
    }

    .detail-value {
        color: #172844;
        font-size: 15px;
        font-weight: 800;
        margin-top: 4px;
    }

    .error-box {
        padding: 20px;
        margin-top: 12px;
        border-radius: 20px;
        background: #fff0f1;
        color: #b4232b;
        border: 1px solid #ffd2d5;
    }

    .error-title {
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .info-box {
        padding: 14px 16px;
        border-radius: 16px;
        background: #edf5ff;
        border: 1px solid #d6e8ff;
        color: #244b80;
        font-size: 12px;
    }

    /* Streamlit buttons */
    div.stButton > button {
        border-radius: 13px;
        min-height: 42px;
        border: 1px solid #dce5f1;
        background: white;
        color: #52637e;
        font-weight: 700;
    }

    div.stButton > button:hover {
        border-color: #3d7ff0;
        color: #1d62d8;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg,#1754c7,#287cf0);
        border: none;
        color: white;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 16px;
        border: 1px solid #dce5f0;
        background: rgba(255,255,255,.95);
        min-height: 45px;
    }

    .footer-nav {
        position: fixed;
        z-index: 999;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        width: min(590px, calc(100% - 24px));
        background: rgba(255,255,255,.92);
        backdrop-filter: blur(18px);
        border: 1px solid #e3eaf4;
        border-radius: 22px;
        box-shadow: 0 12px 32px rgba(31, 55, 90, .16);
        padding: 9px 12px;
        display: flex;
        justify-content: space-around;
        color: #64748b;
        font-size: 10px;
        font-weight: 700;
    }

    .footer-item {
        text-align: center;
        min-width: 70px;
    }

    .footer-icon {
        font-size: 20px;
        line-height: 22px;
    }

    .footer-active {
        color: #1769e8;
    }

    @media (max-width: 420px) {
        .block-container {
            padding-left: .65rem;
            padding-right: .65rem;
        }

        .hero-title {
            font-size: 26px;
        }

        .metric-value {
            font-size: 11px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# 4. HELPERS
# ------------------------------------------------------------
def safe_number(series):
    return pd.to_numeric(series, errors="coerce").fillna(0)


def format_number(value):
    try:
        if pd.isna(value):
            return "-"
        value = float(value)
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return str(value)


def format_status(value):
    text = str(value).strip().lower()
    if text in {"yes", "ya", "y", "1", "true", "aktif", "active"}:
        return "Yes"
    if text in {"no", "tidak", "n", "0", "false", "nonaktif", "inactive"}:
        return "No"
    return str(value) if str(value).strip() else "-"


def initials(name):
    words = [x for x in str(name).split() if x]
    if not words:
        return "A"
    if len(words) == 1:
        return words[0][:2].upper()
    return (words[0][0] + words[1][0]).upper()


def get_value(row, key):
    col = COL.get(key)
    if col is None or col not in row.index:
        return None
    return row[col]


def classify_type(value):
    text = normalize_name(value)
    if "jiwa" in text or "life" in text:
        return "Asuransi Jiwa"
    if "umum" in text or "general" in text:
        return "Asuransi Umum"
    return str(value) if str(value).strip() else "Belum Dikategorikan"


# ------------------------------------------------------------
# 5. SESSION STATE
# ------------------------------------------------------------
if "category" not in st.session_state:
    st.session_state.category = "Asuransi Umum"

if "selected_company" not in st.session_state:
    st.session_state.selected_company = None


# ------------------------------------------------------------
# 6. HEADER
# ------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="shield">🛡️</div>
        <div class="hero-title">BancaPocket</div>
        <div class="hero-subtitle">Daftar Perusahaan Asuransi</div>
        <div class="hero-caption">Informasi Mitra Asuransi dalam Genggaman Anda</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# 7. CATEGORY BUTTONS
# ------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    if st.button(
        "🏢  Asuransi Umum",
        use_container_width=True,
        type="primary" if st.session_state.category == "Asuransi Umum" else "secondary",
    ):
        st.session_state.category = "Asuransi Umum"
        st.session_state.selected_company = None
        st.rerun()

with c2:
    if st.button(
        "❤  Asuransi Jiwa",
        use_container_width=True,
        type="primary" if st.session_state.category == "Asuransi Jiwa" else "secondary",
    ):
        st.session_state.category = "Asuransi Jiwa"
        st.session_state.selected_company = None
        st.rerun()


# ------------------------------------------------------------
# 8. FILTER DATA
# ------------------------------------------------------------
if COL["jenis"]:
    type_series = df[COL["jenis"]].apply(classify_type)
    filtered = df[type_series == st.session_state.category].copy()

    # Jika tidak ada hasil karena penamaan kategori berbeda,
    # coba pencarian berdasarkan teks.
    if filtered.empty:
        raw = df[COL["jenis"]].astype(str).str.lower()
        keyword = "jiwa" if st.session_state.category == "Asuransi Jiwa" else "umum"
        filtered = df[raw.str.contains(keyword, na=False)].copy()
else:
    filtered = df.copy()

search = st.text_input(
    "🔎",
    placeholder="Cari nama asuransi...",
    label_visibility="collapsed",
)

if search and COL["nama"]:
    filtered = filtered[
        filtered[COL["nama"]]
        .astype(str)
        .str.contains(search, case=False, na=False)
    ]

sort_option = st.selectbox(
    "Urutkan",
    ["Nama A-Z", "Nama Z-A", "Aset Terbesar", "Ekuitas Terbesar", "Investasi Terbesar"],
    label_visibility="collapsed",
)

if COL["nama"]:
    if sort_option == "Nama A-Z":
        filtered = filtered.sort_values(COL["nama"], key=lambda x: x.astype(str).str.lower())
    elif sort_option == "Nama Z-A":
        filtered = filtered.sort_values(COL["nama"], key=lambda x: x.astype(str).str.lower(), ascending=False)
    elif sort_option == "Aset Terbesar" and COL["aset"]:
        filtered = filtered.assign(_sort=safe_number(filtered[COL["aset"]])).sort_values("_sort", ascending=False)
    elif sort_option == "Ekuitas Terbesar" and COL["ekuitas"]:
        filtered = filtered.assign(_sort=safe_number(filtered[COL["ekuitas"]])).sort_values("_sort", ascending=False)
    elif sort_option == "Investasi Terbesar" and COL["investasi"]:
        filtered = filtered.assign(_sort=safe_number(filtered[COL["investasi"]])).sort_values("_sort", ascending=False)


# ------------------------------------------------------------
# 9. DETAIL VIEW
# ------------------------------------------------------------
if st.session_state.selected_company is not None:

    selected_name = st.session_state.selected_company
    selected_rows = df[
        df[COL["nama"]].astype(str) == str(selected_name)
    ] if COL["nama"] else pd.DataFrame()

    if selected_rows.empty:
        st.session_state.selected_company = None
        st.rerun()

    row = selected_rows.iloc[0]

    if st.button("← Kembali ke daftar", use_container_width=True):
        st.session_state.selected_company = None
        st.rerun()

    st.markdown(
        f"""
        <div class="detail-card">
            <div class="company-top">
                <div class="company-icon">{initials(selected_name)}</div>
                <div>
                    <div class="company-name">{selected_name}</div>
                    <div class="company-type">{classify_type(get_value(row, "jenis"))}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_keys = [
        ("Investasi", "investasi"),
        ("Aset", "aset"),
        ("Ekuitas", "ekuitas"),
        ("Pendapatan Jasa Asuransi", "pendapatan"),
        ("Laba (Rugi)", "laba"),
    ]

    cards = []
    for label, key in metric_keys:
        value = get_value(row, key)
        if value is not None:
            try:
                display = format_number(float(value))
            except Exception:
                display = str(value)
            cards.append((label, display))

    for i in range(0, len(cards), 2):
        cols = st.columns(2)
        for j, (label, value) in enumerate(cards[i:i+2]):
            with cols[j]:
                st.markdown(
                    f"""
                    <div class="detail-item">
                        <div class="detail-label">{label}</div>
                        <div class="detail-value">{value}</div>
                        <div class="detail-label">Rp Miliar</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="section-title">Status Kerja Sama</div>', unsafe_allow_html=True)

    pks_kredit = format_status(get_value(row, "pks_kredit"))
    pks_banca = format_status(get_value(row, "pks_banca"))

    k1, k2 = st.columns(2)
    with k1:
        cls = "yes" if pks_kredit == "Yes" else "no"
        st.markdown(
            f"""
            <div class="detail-item">
                <div class="detail-label">PKS Rekanan Perkreditan</div>
                <div class="status {cls}" style="margin-top:8px;">{pks_kredit}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k2:
        cls = "yes" if pks_banca == "Yes" else "no"
        st.markdown(
            f"""
            <div class="detail-item">
                <div class="detail-label">PKS Bancassurance</div>
                <div class="status {cls}" style="margin-top:8px;">{pks_banca}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Grafik profil keuangan
    chart_data = []
    for label, key in [
        ("Investasi", "investasi"),
        ("Aset", "aset"),
        ("Ekuitas", "ekuitas"),
        ("Pendapatan", "pendapatan"),
        ("Laba/Rugi", "laba"),
    ]:
        value = get_value(row, key)
        if value is not None:
            try:
                chart_data.append({"Komponen": label, "Nilai": float(value)})
            except Exception:
                pass

    if chart_data:
        st.markdown('<div class="section-title">Profil Keuangan</div>', unsafe_allow_html=True)
        chart_df = pd.DataFrame(chart_data)
        fig = px.bar(
            chart_df,
            x="Komponen",
            y="Nilai",
            text="Nilai",
        )
        fig.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            marker_color="#287cf0",
        )
        fig.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=15, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#334155"),
            yaxis_title="Rp Miliar",
            xaxis_title=None,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        """
        <div class="info-box">
            Data ditampilkan berdasarkan database BancaPocket yang tersimpan pada file Excel.
        </div>
        """,
        unsafe_allow_html=True,
    )

else:

    st.markdown(
        f'<div class="section-title">Asuradur Partner</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="count-text">Total {len(filtered)} {st.session_state.category}</div>',
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.info("Data asuransi tidak ditemukan.")
    else:
        for idx, (_, row) in enumerate(filtered.iterrows()):

            name = str(get_value(row, "nama") or "Tanpa Nama")
            jenis = classify_type(get_value(row, "jenis"))

            investasi = get_value(row, "investasi")
            aset = get_value(row, "aset")
            ekuitas = get_value(row, "ekuitas")

            pks_kredit = format_status(get_value(row, "pks_kredit"))
            pks_banca = format_status(get_value(row, "pks_banca"))

            # Card
            st.markdown(
                f"""
                <div class="company-card">
                    <div class="company-top">
                        <div class="company-icon">{initials(name)}</div>
                        <div>
                            <div class="company-name">{name}</div>
                            <div class="company-type">{jenis}</div>
                        </div>
                    </div>

                    <div class="metric-row">
                        <div class="metric">
                            <div class="metric-label">Investasi</div>
                            <div class="metric-value">{format_number(investasi)}</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Aset</div>
                            <div class="metric-value">{format_number(aset)}</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Ekuitas</div>
                            <div class="metric-value">{format_number(ekuitas)}</div>
                        </div>
                    </div>

                    <div class="status-row">
                        <div class="status {'yes' if pks_kredit == 'Yes' else 'no'}">
                            PKS Kredit<br>{pks_kredit}
                        </div>
                        <div class="status {'yes' if pks_banca == 'Yes' else 'no'}">
                            PKS Banca<br>{pks_banca}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Button berada setelah card, dibuat sangat sederhana.
            if st.button(
                f"  Lihat detail {name}  ›",
                key=f"detail_{idx}_{name}",
                use_container_width=True,
            ):
                st.session_state.selected_company = name
                st.rerun()


# ------------------------------------------------------------
# 10. FOOTER NAVIGATION
# ------------------------------------------------------------
st.markdown(
    """
    <div class="footer-nav">
        <div class="footer-item footer-active">
            <div class="footer-icon">⌂</div>
            Beranda
        </div>
        <div class="footer-item">
            <div class="footer-icon">🏢</div>
            Asuransi
        </div>
        <div class="footer-item">
            <div class="footer-icon">▥</div>
            Report
        </div>
        <div class="footer-item">
            <div class="footer-icon">ⓘ</div>
            Info
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
