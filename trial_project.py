import streamlit as st
import pandas as pd
from pathlib import Path
import html
import re

# ============================================================
# BANCAPOCKET - MOBILE INSURANCE PARTNER DIRECTORY
# ============================================================

st.set_page_config(
    page_title="BancaPocket",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DATA_FILE = Path("data/Data_Asuransi.xlsx")

# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 50% -10%, rgba(37,99,235,.15), transparent 32%),
        linear-gradient(180deg, #f7faff 0%, #eef4fc 100%);
}

.block-container {
    max-width: 760px !important;
    padding: 1rem .75rem 5.5rem !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Header */
.bp-header {
    position: relative;
    overflow: hidden;
    border-radius: 0 0 30px 30px;
    padding: 25px 22px 28px;
    color: white;
    background: linear-gradient(135deg, #1245a0 0%, #2563eb 55%, #3b82f6 100%);
    box-shadow: 0 12px 30px rgba(37,99,235,.20);
    margin: -16px -12px 18px;
}

.bp-header:after {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    right: -80px;
    top: -100px;
    border-radius: 50%;
    background: rgba(255,255,255,.10);
}

.bp-brand {
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -.8px;
    position: relative;
    z-index: 2;
}

.bp-subtitle {
    font-size: 15px;
    font-weight: 600;
    margin-top: 2px;
    position: relative;
    z-index: 2;
}

.bp-caption {
    font-size: 12px;
    opacity: .85;
    margin-top: 7px;
    position: relative;
    z-index: 2;
}

.bp-shield {
    position: absolute;
    right: 20px;
    top: 26px;
    width: 62px;
    height: 62px;
    border-radius: 20px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size: 32px;
    background: rgba(255,255,255,.16);
    border: 1px solid rgba(255,255,255,.35);
    z-index: 2;
}

/* Search */
.search-label {
    font-size: 13px;
    font-weight: 700;
    color: #17233d;
    margin: 0 0 7px 3px;
}

div[data-testid="stTextInput"] input {
    border-radius: 15px !important;
    min-height: 48px !important;
    border: 1px solid #d9e2ef !important;
    background: white !important;
    font-size: 14px !important;
    box-shadow: 0 5px 18px rgba(25,55,100,.06);
}

/* Category buttons */
div.stButton > button {
    border-radius: 14px !important;
    min-height: 44px !important;
    font-weight: 700 !important;
    border: 1px solid #dce5f1 !important;
    background: white !important;
    color: #4b5f7d !important;
    box-shadow: 0 4px 12px rgba(30,60,100,.04);
}

div.stButton > button:hover {
    border-color: #2563eb !important;
    color: #2563eb !important;
}

.category-active div.stButton > button {
    background: linear-gradient(135deg,#1555c8,#2563eb) !important;
    color: white !important;
    border-color: #1555c8 !important;
}

.section-title {
    font-size: 22px;
    font-weight: 800;
    color: #14213d;
    margin: 20px 0 3px;
}

.section-count {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 12px;
}

/* Company card */
.company-card {
    background: rgba(255,255,255,.96);
    border: 1px solid #e1e9f3;
    border-radius: 21px;
    padding: 16px;
    margin: 10px 0;
    box-shadow: 0 8px 24px rgba(36,65,105,.07);
}

.company-head {
    display:flex;
    align-items:center;
    gap:13px;
    margin-bottom:14px;
}

.company-logo {
    width:58px;
    height:58px;
    flex:0 0 58px;
    border-radius:17px;
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size:21px;
    font-weight:800;
    background:linear-gradient(135deg,#2563eb,#60a5fa);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.4);
}

.company-name {
    color:#17233d;
    font-size:16px;
    line-height:1.25;
    font-weight:800;
}

.company-type {
    color:#71829d;
    font-size:12px;
    margin-top:4px;
}

.arrow {
    margin-left:auto;
    font-size:24px;
    color:#526783;
}

.metrics {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:7px;
}

.metric {
    background:#f7faff;
    border:1px solid #e6edf6;
    border-radius:12px;
    padding:9px 8px;
}

.metric-label {
    color:#71829d;
    font-size:10px;
    margin-bottom:4px;
}

.metric-value {
    color:#17233d;
    font-size:13px;
    font-weight:800;
}

.status-row {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:8px;
    margin-top:9px;
}

.status {
    border-radius:11px;
    padding:8px 6px;
    text-align:center;
    font-size:10px;
    font-weight:700;
}

.status.yes {
    background:#e4f8ef;
    color:#079455;
}

.status.no {
    background:#ffebeb;
    color:#e23838;
}

/* Detail */
.detail-card {
    background:white;
    border:1px solid #dfe8f3;
    border-radius:22px;
    padding:18px;
    margin-top:14px;
    box-shadow:0 10px 28px rgba(36,65,105,.08);
}

.detail-title {
    font-size:18px;
    font-weight:800;
    color:#17233d;
}

.detail-sub {
    font-size:12px;
    color:#71829d;
    margin-top:3px;
    margin-bottom:14px;
}

.detail-grid {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:9px;
}

.detail-metric {
    border:1px solid #e2eaf4;
    border-radius:14px;
    padding:11px;
}

.detail-metric .label {
    color:#71829d;
    font-size:10px;
}

.detail-metric .value {
    color:#17233d;
    font-size:15px;
    font-weight:800;
    margin-top:3px;
}

.empty {
    text-align:center;
    padding:35px 15px;
    background:white;
    border:1px dashed #cbd7e7;
    border-radius:20px;
    color:#71829d;
}

/* Bottom navigation */
.bottom-nav {
    position:fixed;
    z-index:999;
    left:50%;
    transform:translateX(-50%);
    bottom:10px;
    width:min(720px, calc(100% - 22px));
    background:rgba(255,255,255,.94);
    backdrop-filter:blur(16px);
    border:1px solid #dce6f1;
    border-radius:22px;
    box-shadow:0 10px 35px rgba(20,45,85,.14);
    display:grid;
    grid-template-columns:repeat(4,1fr);
    padding:8px 5px;
}

.nav-item {
    text-align:center;
    color:#71829d;
    font-size:10px;
    font-weight:600;
    padding:6px 2px;
}

.nav-icon {
    font-size:20px;
    line-height:1.1;
    margin-bottom:3px;
}

.nav-active {
    color:#2563eb;
}

/* Desktop still looks like phone/tablet */
@media (min-width: 900px) {
    .block-container { max-width: 780px !important; }
}

/* Mobile */
@media (max-width: 480px) {
    .bp-brand { font-size:25px; }
    .section-title { font-size:20px; }
    .metrics { gap:5px; }
    .metric-value { font-size:12px; }
    .company-card { padding:13px; }
    .company-logo { width:52px; height:52px; flex-basis:52px; }
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def normalize_column(name):
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def find_column(df, aliases):
    normalized = {normalize_column(c): c for c in df.columns}

    # exact normalized match
    for alias in aliases:
        key = normalize_column(alias)
        if key in normalized:
            return normalized[key]

    # partial match
    for alias in aliases:
        key = normalize_column(alias)
        for norm, original in normalized.items():
            if key in norm or norm in key:
                return original

    return None


def format_number(value):
    if pd.isna(value):
        return "-"
    try:
        value = float(value)
        if value.is_integer():
            return f"{value:,.0f}".replace(",", ".")
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return str(value)


def clean_yes_no(value):
    if pd.isna(value):
        return "No"
    text = str(value).strip().lower()
    if text in ["yes", "y", "ya", "1", "true", "ada", "aktif"]:
        return "Yes"
    return "No"


def company_initial(name):
    words = re.findall(r"[A-Za-z0-9]+", str(name))
    if not words:
        return "A"
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return words[0][:2].upper()


@st.cache_data
def load_data():
    if not DATA_FILE.exists():
        return None, f"File {DATA_FILE.as_posix()} belum ditemukan."

    try:
        # Default: first sheet
        df = pd.read_excel(DATA_FILE)
        df = df.dropna(how="all").copy()
        return df, None
    except Exception as e:
        return None, f"Gagal membaca Excel: {e}"


def prepare_data(df):
    mapping = {
        "name": find_column(df, [
            "Nama Asuransi", "Nama Asuradur", "Asuransi",
            "Asuradur", "Nama Perusahaan"
        ]),
        "type": find_column(df, [
            "Jenis Asuransi", "Jenis", "Kategori",
            "Tipe Asuransi", "Type"
        ]),
        "investment": find_column(df, [
            "Investasi", "Investasi (Rp Miliar)", "Investments"
        ]),
        "assets": find_column(df, [
            "Aset", "Aset (Rp Miliar)", "Assets"
        ]),
        "equity": find_column(df, [
            "Ekuitas", "Ekuitas (Rp Miliar)", "Equity"
        ]),
        "premium": find_column(df, [
            "Pendapatan Jasa Asuransi",
            "Pendapatan Jasa Asuransi (Rp Miliar)",
            "Pendapatan Asuransi"
        ]),
        "profit": find_column(df, [
            "Laba (Rugi)", "Laba Rugi",
            "Laba (Rugi) (Rp Miliar)", "Profit"
        ]),
        "credit": find_column(df, [
            "PKS Rekanan Perkreditan",
            "PKS Kredit", "PKS Rekanan Kredit"
        ]),
        "banca": find_column(df, [
            "PKS Bancassurance", "PKS Banca", "Bancassurance"
        ]),
    }

    out = pd.DataFrame()

    if mapping["name"]:
        out["Nama Asuransi"] = df[mapping["name"]].astype(str).str.strip()
    else:
        # fallback: first column
        out["Nama Asuransi"] = df.iloc[:, 0].astype(str).str.strip()

    if mapping["type"]:
        out["Jenis Asuransi"] = df[mapping["type"]].fillna("").astype(str).str.strip()
    else:
        out["Jenis Asuransi"] = "Asuransi Umum"

    for key, label in [
        ("investment", "Investasi"),
        ("assets", "Aset"),
        ("equity", "Ekuitas"),
        ("premium", "Pendapatan Jasa Asuransi"),
        ("profit", "Laba (Rugi)"),
    ]:
        if mapping[key]:
            out[label] = pd.to_numeric(
                df[mapping[key]].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
                errors="coerce"
            )
        else:
            out[label] = pd.NA

    for key, label in [
        ("credit", "PKS Rekanan Perkreditan"),
        ("banca", "PKS Bancassurance"),
    ]:
        if mapping[key]:
            out[label] = df[mapping[key]].apply(clean_yes_no)
        else:
            out[label] = "No"

    out = out[out["Nama Asuransi"].str.lower().ne("nan")]
    out = out[out["Nama Asuransi"].str.strip().ne("")]
    out = out.drop_duplicates(subset=["Nama Asuransi"], keep="first").reset_index(drop=True)

    return out, mapping


def infer_type(value):
    text = str(value).lower()
    if "jiwa" in text or "life" in text:
        return "Asuransi Jiwa"
    return "Asuransi Umum"


# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------
df_raw, error = load_data()

if error:
    st.markdown(
        f'<div style="padding:18px;border-radius:16px;background:#ffe8ec;color:#d92d45;font-weight:700;">'
        f'⚠️ {html.escape(error)}<br><span style="font-size:12px;font-weight:500;">'
        f'Upload file Excel ke folder <b>data</b> dengan nama <b>Data_Asuransi.xlsx</b>.</span></div>',
        unsafe_allow_html=True
    )
    st.stop()

df, column_mapping = prepare_data(df_raw)

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown("""
<div class="bp-header">
    <div class="bp-brand">BancaPocket</div>
    <div class="bp-subtitle">Daftar Perusahaan Asuransi</div>
    <div class="bp-caption">Informasi Mitra Asuransi dalam Genggaman Anda</div>
    <div class="bp-shield">🛡️</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Category state
# ------------------------------------------------------------
if "category" not in st.session_state:
    st.session_state.category = "Asuransi Umum"

c1, c2 = st.columns(2)

with c1:
    if st.session_state.category == "Asuransi Umum":
        st.markdown('<div class="category-active">', unsafe_allow_html=True)
    if st.button("🏢  Asuransi Umum", use_container_width=True):
        st.session_state.category = "Asuransi Umum"
        st.session_state.selected_company = None
        st.rerun()
    if st.session_state.category == "Asuransi Umum":
        st.markdown('</div>', unsafe_allow_html=True)

with c2:
    if st.session_state.category == "Asuransi Jiwa":
        st.markdown('<div class="category-active">', unsafe_allow_html=True)
    if st.button("♥  Asuransi Jiwa", use_container_width=True):
        st.session_state.category = "Asuransi Jiwa"
        st.session_state.selected_company = None
        st.rerun()
    if st.session_state.category == "Asuransi Jiwa":
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# Search
# ------------------------------------------------------------
st.markdown('<div class="search-label">Cari Asuradur</div>', unsafe_allow_html=True)
search = st.text_input(
    "search",
    placeholder="🔎  Cari nama asuransi...",
    label_visibility="collapsed"
)

category = st.session_state.category

# Infer category when the Excel has no explicit category column
if column_mapping["type"]:
    filtered = df[df["Jenis Asuransi"].apply(infer_type).eq(category)].copy()
else:
    # If no type column exists, show all data under the selected category.
    filtered = df.copy()

if search.strip():
    filtered = filtered[
        filtered["Nama Asuransi"].str.contains(
            search.strip(), case=False, na=False
        )
    ].copy()

# ------------------------------------------------------------
# Sort
# ------------------------------------------------------------
sort_options = [
    "Nama Asuransi",
    "Investasi",
    "Aset",
    "Ekuitas",
    "Laba (Rugi)",
]

sort_by = st.selectbox(
    "Urutkan",
    sort_options,
    index=0,
    label_visibility="collapsed"
)

if sort_by == "Nama Asuransi":
    filtered = filtered.sort_values("Nama Asuransi", key=lambda s: s.str.lower())
else:
    filtered = filtered.sort_values(sort_by, ascending=False, na_position="last")

# ------------------------------------------------------------
# Section
# ------------------------------------------------------------
st.markdown(
    f'<div class="section-title">Asuradur Partner</div>'
    f'<div class="section-count">Total {len(filtered)} {category}</div>',
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# Cards
# ------------------------------------------------------------
if "selected_company" not in st.session_state:
    st.session_state.selected_company = None

if filtered.empty:
    st.markdown(
        '<div class="empty">🔎<br><br><b>Asuradur tidak ditemukan</b><br>'
        'Coba gunakan kata kunci lain.</div>',
        unsafe_allow_html=True
    )
else:
    for idx, row in filtered.iterrows():
        name = str(row["Nama Asuransi"])
        initials = company_initial(name)
        selected = st.session_state.selected_company == name

        credit = clean_yes_no(row["PKS Rekanan Perkreditan"])
        banca = clean_yes_no(row["PKS Bancassurance"])

        # IMPORTANT:
        # This HTML is intentionally built as one continuous string.
        # It avoids Streamlit Markdown interpreting indented HTML
        # as a code block.
        card_html = (
            '<div class="company-card">'
            '<div class="company-head">'
            f'<div class="company-logo">{html.escape(initials)}</div>'
            '<div style="min-width:0;">'
            f'<div class="company-name">{html.escape(name)}</div>'
            f'<div class="company-type">{html.escape(category)}</div>'
            '</div>'
            '<div class="arrow">›</div>'
            '</div>'
            '<div class="metrics">'
            '<div class="metric">'
            '<div class="metric-label">Investasi</div>'
            f'<div class="metric-value">{format_number(row["Investasi"])}</div>'
            '</div>'
            '<div class="metric">'
            '<div class="metric-label">Aset</div>'
            f'<div class="metric-value">{format_number(row["Aset"])}</div>'
            '</div>'
            '<div class="metric">'
            '<div class="metric-label">Ekuitas</div>'
            f'<div class="metric-value">{format_number(row["Ekuitas"])}</div>'
            '</div>'
            '</div>'
            '<div class="status-row">'
            f'<div class="status {"yes" if credit == "Yes" else "no"}">'
            f'PKS Kredit<br>{credit}'
            '</div>'
            f'<div class="status {"yes" if banca == "Yes" else "no"}">'
            f'PKS Banca<br>{banca}'
            '</div>'
            '</div>'
            '</div>'
        )

        st.markdown(card_html, unsafe_allow_html=True)

        if st.button(
            "Lihat Detail" if not selected else "Tutup Detail",
            key=f"detail_{idx}_{re.sub(r'[^a-zA-Z0-9]', '_', name)}",
            use_container_width=True
        ):
            st.session_state.selected_company = None if selected else name
            st.rerun()

        if selected:
            st.markdown(
                '<div class="detail-card">'
                f'<div class="detail-title">{html.escape(name)}</div>'
                f'<div class="detail-sub">{html.escape(category)}</div>'
                '<div class="detail-grid">'
                '<div class="detail-metric">'
                '<div class="label">Investasi</div>'
                f'<div class="value">{format_number(row["Investasi"])} <small>Rp Miliar</small></div>'
                '</div>'
                '<div class="detail-metric">'
                '<div class="label">Aset</div>'
                f'<div class="value">{format_number(row["Aset"])} <small>Rp Miliar</small></div>'
                '</div>'
                '<div class="detail-metric">'
                '<div class="label">Ekuitas</div>'
                f'<div class="value">{format_number(row["Ekuitas"])} <small>Rp Miliar</small></div>'
                '</div>'
                '<div class="detail-metric">'
                '<div class="label">Pendapatan Jasa Asuransi</div>'
                f'<div class="value">{format_number(row["Pendapatan Jasa Asuransi"])} <small>Rp Miliar</small></div>'
                '</div>'
                '<div class="detail-metric">'
                '<div class="label">Laba (Rugi)</div>'
                f'<div class="value">{format_number(row["Laba (Rugi)"])} <small>Rp Miliar</small></div>'
                '</div>'
                '<div class="detail-metric">'
                '<div class="label">PKS Rekanan Perkreditan</div>'
                f'<div class="value">{credit}</div>'
                '</div>'
                '<div class="detail-metric">'
                '<div class="label">PKS Bancassurance</div>'
                f'<div class="value">{banca}</div>'
                '</div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )

# ------------------------------------------------------------
# Bottom navigation
# ------------------------------------------------------------
st.markdown("""
<div class="bottom-nav">
    <div class="nav-item nav-active">
        <div class="nav-icon">⌂</div>
        Beranda
    </div>
    <div class="nav-item">
        <div class="nav-icon">🏢</div>
        Asuransi
    </div>
    <div class="nav-item">
        <div class="nav-icon">▥</div>
        Report
    </div>
    <div class="nav-item">
        <div class="nav-icon">ⓘ</div>
        Info
    </div>
</div>
""", unsafe_allow_html=True)
