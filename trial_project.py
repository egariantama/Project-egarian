import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

# ============================================================
# BANCAPOCKET - MOBILE INSURANCE PARTNER DIRECTORY
# ============================================================

st.set_page_config(
    page_title="BancaPocket",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DATA_FILE = Path("data/Data Asuransi.xlsx")

# -----------------------------
# CSS - mobile / smooth UI
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { font-family: Inter, sans-serif; }
html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp {
    background:
      radial-gradient(circle at 50% -10%, #DCEAFF 0%, rgba(220,234,255,0) 34%),
      linear-gradient(180deg,#F5F8FD 0%,#F8FAFD 100%);
}
#MainMenu, header, footer { visibility:hidden; }
.block-container {
    max-width: 620px !important;
    padding: 10px 12px 95px !important;
}

/* Hero */
.hero {
    position:relative;
    overflow:hidden;
    padding:24px 21px 22px;
    border-radius:28px;
    color:#fff;
    background:linear-gradient(135deg,#0D47A1 0%,#1465DF 55%,#3B8DFF 100%);
    box-shadow:0 18px 38px rgba(37,99,235,.24);
    margin-bottom:14px;
}
.hero:before {
    content:"";
    position:absolute;
    width:210px;height:210px;
    right:-70px;top:-90px;
    border-radius:50%;
    background:rgba(255,255,255,.10);
}
.hero-title {font-size:28px;font-weight:800;letter-spacing:-.7px;}
.hero-sub {font-size:16px;font-weight:700;margin-top:4px;}
.hero-desc {font-size:11px;opacity:.88;margin-top:7px;}
.hero-shield {
    position:absolute;right:22px;bottom:18px;
    font-size:49px;
    filter:drop-shadow(0 7px 10px rgba(0,0,0,.12));
}

/* Segmented selector */
div[data-testid="stRadio"] > div {
    background:#E9EFF7;
    border-radius:16px;
    padding:4px;
    gap:4px;
}
div[data-testid="stRadio"] label {
    border-radius:12px;
    padding:9px 5px !important;
    font-size:12px !important;
    font-weight:700 !important;
}
div[data-testid="stRadio"] label[data-checked="true"] {
    background:#125BDD !important;
    color:white !important;
    box-shadow:0 5px 12px rgba(18,91,221,.22);
}

/* Search */
div[data-testid="stTextInput"] label {display:none;}
div[data-testid="stTextInput"] input {
    height:46px;
    border-radius:15px;
    border:1px solid #D8E2EF;
    background:#fff;
    font-size:13px;
    box-shadow:0 5px 18px rgba(15,23,42,.04);
}

/* Cards */
.ins-card {
    background:rgba(255,255,255,.96);
    border:1px solid #E2EAF3;
    border-radius:20px;
    padding:14px;
    margin:9px 0;
    box-shadow:0 8px 24px rgba(15,23,42,.055);
}
.ins-top {display:flex;gap:11px;align-items:flex-start;}
.ins-logo {
    width:50px;height:50px;min-width:50px;
    border-radius:15px;
    background:#F7FAFE;
    border:1px solid #E3EBF5;
    display:flex;align-items:center;justify-content:center;
    font-size:23px;
}
.ins-name {
    color:#102A52;
    font-size:14px;
    line-height:1.25;
    font-weight:800;
}
.ins-type {font-size:10px;color:#71819A;margin-top:4px;}
.arrow {font-size:25px;color:#5C7495;margin-left:auto;}
.data-row {
    display:grid;
    grid-template-columns:1fr 1fr 1fr 1.05fr 1.05fr;
    gap:5px;
    margin-top:12px;
}
.lbl {font-size:8px;color:#7A8AA2;}
.val {font-size:12px;color:#183A68;font-weight:800;margin-top:2px;}
.badge {
    padding:7px 4px;
    border-radius:10px;
    text-align:center;
    font-size:8px;
    font-weight:800;
}
.yes {background:#E2F8EE;color:#10945C;}
.no {background:#FFE6E6;color:#D92D20;}

.section-title {
    color:#10213E;
    font-size:18px;
    font-weight:800;
    margin:17px 2px 9px;
}
.counter {font-size:12px;color:#5D708D;font-weight:600;margin:9px 2px;}

.metric {
    background:#fff;
    border:1px solid #E1EAF3;
    border-radius:17px;
    padding:13px;
    box-shadow:0 7px 20px rgba(15,23,42,.045);
}
.metric-label {font-size:9px;color:#71819A;}
.metric-value {font-size:18px;color:#153761;font-weight:800;margin-top:3px;}
.metric-sub {font-size:8px;color:#8A99AC;margin-top:3px;}

.detail-head {
    background:#fff;
    border:1px solid #E1EAF3;
    border-radius:21px;
    padding:16px;
    box-shadow:0 8px 25px rgba(15,23,42,.05);
}
.detail-logo {
    width:62px;height:62px;border-radius:18px;
    display:flex;align-items:center;justify-content:center;
    background:#F7FAFE;border:1px solid #E2EAF3;
    font-size:29px;
}
.detail-name {font-size:19px;font-weight:800;color:#102A52;line-height:1.2;}
.detail-type {font-size:11px;color:#72839B;margin-top:4px;}

div.stButton > button {
    width:100%;
    min-height:39px;
    border-radius:12px;
    border:1px solid #D9E3EF;
    background:#fff;
    color:#173A68;
    font-weight:700;
}
.primary-btn div.stButton > button {
    background:linear-gradient(135deg,#1767E8,#2B82FF);
    color:#fff;border:0;
    box-shadow:0 8px 18px rgba(37,99,235,.18);
}

/* hide button text used only as card action */
.card-action div.stButton > button {
    margin-top:9px;
    font-size:11px;
}

/* bottom nav */
.bottom-space {height:4px;}
.nav-caption {
    text-align:center;color:#5D708D;font-size:9px;font-weight:700;margin-top:2px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Helpers
# -----------------------------
def money(v):
    try:
        return f"{float(v):,.0f}".replace(",", ".")
    except Exception:
        return "0"

def status_badge(label, value):
    ok = str(value).strip().lower() in {"yes", "ya", "y", "true", "1"}
    return f"""
    <div>
        <div class="lbl">{label}</div>
        <div class="badge {'yes' if ok else 'no'}">{'Yes' if ok else 'No'}</div>
    </div>
    """

def load_data():
    if not DATA_FILE.exists():
        st.error("File data/Data Asuransi.xlsx belum ditemukan.")
        st.stop()

    data = pd.read_excel(DATA_FILE)
    data.columns = [str(c).strip() for c in data.columns]

    aliases = {
        "Asuradur":"Nama Asuransi",
        "Nama Asuradur":"Nama Asuransi",
        "Jenis":"Jenis Asuransi",
        "Investasi (Rp Miliar)":"Investasi",
        "Aset (Rp Miliar)":"Aset",
        "Ekuitas (Rp Miliar)":"Ekuitas",
        "Pendapatan Jasa Asuransi (Rp Miliar)":"Pendapatan Jasa Asuransi",
        "Laba (Rugi) (Rp Miliar)":"Laba (Rugi)",
        "PKS Kredit":"PKS Rekanan Perkreditan",
    }
    data = data.rename(columns={k:v for k,v in aliases.items() if k in data.columns})

    required = [
        "Nama Asuransi","Jenis Asuransi","Investasi","Aset","Ekuitas",
        "Pendapatan Jasa Asuransi","Laba (Rugi)",
        "PKS Rekanan Perkreditan","PKS Bancassurance"
    ]
    missing = [c for c in required if c not in data.columns]
    if missing:
        st.error("Kolom berikut belum ada di Excel: " + ", ".join(missing))
        st.stop()

    for c in ["Investasi","Aset","Ekuitas","Pendapatan Jasa Asuransi","Laba (Rugi)"]:
        data[c] = pd.to_numeric(data[c], errors="coerce").fillna(0)

    for c in ["PKS Rekanan Perkreditan","PKS Bancassurance"]:
        data[c] = data[c].fillna("No").astype(str).str.strip()

    if "Logo" not in data.columns:
        data["Logo"] = "🏢"
    data["Logo"] = data["Logo"].fillna("🏢").astype(str)

    return data


df = load_data()

if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected" not in st.session_state:
    st.session_state.selected = None
if "category" not in st.session_state:
    st.session_state.category = "Asuransi Umum"


# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">BancaPocket</div>
    <div class="hero-sub">Daftar Perusahaan Asuransi</div>
    <div class="hero-desc">Informasi Mitra Asuransi dalam Genggaman Anda</div>
    <div class="hero-shield">🛡️</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# DETAIL PAGE
# ============================================================
if st.session_state.page == "detail":
    selected = st.session_state.selected
    row = df[df["Nama Asuransi"].astype(str) == str(selected)]

    if row.empty:
        st.session_state.page = "home"
        st.session_state.selected = None
        st.rerun()

    r = row.iloc[0]

    if st.button("←  Kembali ke Daftar", use_container_width=True):
        st.session_state.page = "home"
        st.session_state.selected = None
        st.rerun()

    st.markdown('<div class="section-title">Profil Perusahaan</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="detail-head">
        <div style="display:flex;gap:13px;align-items:center;">
            <div class="detail-logo">{r["Logo"]}</div>
            <div>
                <div class="detail-name">{r["Nama Asuransi"]}</div>
                <div class="detail-type">{r["Jenis Asuransi"]}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Informasi Keuangan</div>', unsafe_allow_html=True)

    metrics = [
        ("Investasi", r["Investasi"]),
        ("Aset", r["Aset"]),
        ("Ekuitas", r["Ekuitas"]),
        ("Pendapatan Jasa Asuransi", r["Pendapatan Jasa Asuransi"]),
        ("Laba (Rugi)", r["Laba (Rugi)"]),
    ]

    for start in range(0, len(metrics), 2):
        cols = st.columns(2)
        for idx, (label, value) in enumerate(metrics[start:start+2]):
            with cols[idx]:
                st.markdown(
                    f"""<div class="metric">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{money(value)}</div>
                    <div class="metric-sub">Rp Miliar</div>
                    </div>""",
                    unsafe_allow_html=True
                )

    st.markdown('<div class="section-title">Status Kerja Sama</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="metric">{status_badge("PKS Rekanan Perkreditan", r["PKS Rekanan Perkreditan"])}</div>',
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f'<div class="metric">{status_badge("PKS Bancassurance", r["PKS Bancassurance"])}</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-title">Grafik Keuangan</div>', unsafe_allow_html=True)

    labels = ["Investasi","Aset","Ekuitas","Pendapatan","Laba/Rugi"]
    values = [
        r["Investasi"], r["Aset"], r["Ekuitas"],
        r["Pendapatan Jasa Asuransi"], r["Laba (Rugi)"]
    ]

    fig = go.Figure(
        go.Bar(
            x=labels,
            y=values,
            text=[money(x) for x in values],
            textposition="outside",
            marker=dict(
                color=["#2563EB","#4F8DF7","#7BAAF7","#57A8FF","#18A96B"],
                line=dict(width=0)
            )
        )
    )
    fig.update_layout(
        height=310,
        margin=dict(l=0,r=0,t=25,b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter",color="#526A88",size=10),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True,gridcolor="#EDF2F7",title="Rp Miliar"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})


# ============================================================
# HOME PAGE
# ============================================================
else:
    selected_category = st.radio(
        "Kategori",
        ["🏢 Asuransi Umum", "❤️ Asuransi Jiwa"],
        index=0 if st.session_state.category == "Asuransi Umum" else 1,
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state.category = "Asuransi Umum" if "Umum" in selected_category else "Asuransi Jiwa"

    search = st.text_input(
        "Search",
        placeholder="🔎  Cari nama asuransi...",
        label_visibility="collapsed",
    )

    result = df[
        df["Jenis Asuransi"].astype(str).str.strip().str.lower()
        == st.session_state.category.lower()
    ].copy()

    if search.strip():
        result = result[
            result["Nama Asuransi"].astype(str)
            .str.contains(search.strip(), case=False, na=False)
        ]

    result = result.sort_values("Nama Asuransi")

    st.markdown(
        f'<div class="counter">Total {len(result)} {st.session_state.category} <span style="float:right;">Urutkan A–Z</span></div>',
        unsafe_allow_html=True
    )

    if result.empty:
        st.info("Perusahaan tidak ditemukan. Coba kata kunci lain.")
    else:
        for idx, (_, r) in enumerate(result.iterrows()):
            safe_key = f"detail_{idx}_{abs(hash(str(r['Nama Asuransi'])))}"

            st.markdown(f"""
            <div class="ins-card">
                <div class="ins-top">
                    <div class="ins-logo">{r["Logo"]}</div>
                    <div style="flex:1;">
                        <div class="ins-name">{r["Nama Asuransi"]}</div>
                        <div class="ins-type">{r["Jenis Asuransi"]}</div>
                    </div>
                    <div class="arrow">›</div>
                </div>

                <div class="data-row">
                    <div>
                        <div class="lbl">Investasi</div>
                        <div class="val">{money(r["Investasi"])}</div>
                    </div>
                    <div>
                        <div class="lbl">Aset</div>
                        <div class="val">{money(r["Aset"])}</div>
                    </div>
                    <div>
                        <div class="lbl">Ekuitas</div>
                        <div class="val">{money(r["Ekuitas"])}</div>
                    </div>
                    {status_badge("PKS Kredit",r["PKS Rekanan Perkreditan"])}
                    {status_badge("PKS Banca",r["PKS Bancassurance"])}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Tombol transparan secara visual tetapi tetap native Streamlit
            if st.button(
                f"Lihat Detail • {r['Nama Asuransi']}",
                key=safe_key,
                use_container_width=True
            ):
                st.session_state.selected = r["Nama Asuransi"]
                st.session_state.page = "detail"
                st.rerun()


# -----------------------------
# Bottom navigation
# -----------------------------
st.markdown('<div class="bottom-space"></div>', unsafe_allow_html=True)
n1, n2, n3, n4 = st.columns(4)

with n1:
    if st.button("⌂", key="nav_home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('<div class="nav-caption">Beranda</div>', unsafe_allow_html=True)

with n2:
    if st.button("🏢", key="nav_asuransi", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('<div class="nav-caption">Asuransi</div>', unsafe_allow_html=True)

with n3:
    if st.button("▥", key="nav_report", use_container_width=True):
        total = len(df)
        umum = int((df["Jenis Asuransi"] == "Asuransi Umum").sum())
        jiwa = int((df["Jenis Asuransi"] == "Asuransi Jiwa").sum())
        banca = int((df["PKS Bancassurance"].str.lower() == "yes").sum())
        st.info(f"Report: {total} perusahaan • Umum {umum} • Jiwa {jiwa} • PKS Bancassurance Yes {banca}")
    st.markdown('<div class="nav-caption">Report</div>', unsafe_allow_html=True)

with n4:
    if st.button("ⓘ", key="nav_info", use_container_width=True):
        st.info("BancaPocket — Direktori informasi perusahaan asuransi rekanan Bancassurance.")
    st.markdown('<div class="nav-caption">Info</div>', unsafe_allow_html=True)
