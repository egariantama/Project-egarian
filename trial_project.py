
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# BancaPocket Premium v2
# Mobile-first Bancassurance Partner Information
# ============================================================

st.set_page_config(
    page_title="BancaPocket",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Global CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F4F7FB;
}

#MainMenu, header, footer {
    visibility: hidden;
}

.block-container {
    max-width: 760px;
    padding: 20px 16px 90px 16px;
}

/* Native Streamlit controls */
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stTextInput"] > div > div {
    border-radius: 14px;
}

div.stButton > button {
    border-radius: 13px;
    min-height: 42px;
    font-weight: 700;
    border: 1px solid #DCE5F2;
    background: #FFFFFF;
}

div.stButton > button:hover {
    border-color: #2563EB;
    color: #2563EB;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #123A88 0%, #2563EB 55%, #60A5FA 100%);
    border-radius: 26px;
    padding: 24px;
    color: white;
    box-shadow: 0 16px 34px rgba(37, 99, 235, .20);
    margin-bottom: 18px;
}

.hero-title {
    font-size: 27px;
    font-weight: 800;
    margin: 0;
}

.hero-subtitle {
    font-size: 12px;
    opacity: .86;
    margin-top: 4px;
}

.hero-text {
    font-size: 13px;
    line-height: 1.6;
    margin-top: 18px;
    max-width: 620px;
}

.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,.16);
    border: 1px solid rgba(255,255,255,.22);
    border-radius: 999px;
    padding: 7px 11px;
    font-size: 10px;
    font-weight: 700;
    margin-top: 13px;
}

/* Section */
.section {
    font-size: 18px;
    font-weight: 800;
    color: #0F172A;
    margin: 20px 0 10px 0;
}

/* Cards */
.card {
    background: white;
    border: 1px solid #E3EAF4;
    border-radius: 20px;
    padding: 17px;
    box-shadow: 0 7px 24px rgba(15, 23, 42, .05);
}

.mini-label {
    font-size: 10px;
    color: #64748B;
    font-weight: 600;
}

.mini-value {
    font-size: 21px;
    color: #0F172A;
    font-weight: 800;
    margin-top: 5px;
}

.status {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 999px;
    background: #DCFCE7;
    color: #15803D;
    font-size: 9px;
    font-weight: 800;
}

/* Partner tile */
.partner {
    background: white;
    border: 1px solid #E3EAF4;
    border-radius: 20px;
    padding: 16px;
    margin-bottom: 10px;
    box-shadow: 0 7px 24px rgba(15, 23, 42, .05);
}

.partner-name {
    font-size: 15px;
    font-weight: 800;
    color: #0F172A;
}

.partner-type {
    font-size: 10px;
    color: #64748B;
    margin-top: 3px;
}

/* Detail */
.detail {
    background: white;
    border: 1px solid #E3EAF4;
    border-radius: 24px;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, .06);
}

.detail-title {
    font-size: 23px;
    font-weight: 800;
    color: #0F172A;
}

.detail-sub {
    color: #64748B;
    font-size: 11px;
}

.pill {
    display: inline-block;
    background: #EEF4FF;
    color: #1D4ED8;
    padding: 7px 10px;
    border-radius: 10px;
    margin: 3px;
    font-size: 10px;
    font-weight: 700;
}

/* Timeline */
.timeline-item {
    background: white;
    border: 1px solid #E3EAF4;
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 8px;
}

.timeline-date {
    color: #2563EB;
    font-size: 12px;
    font-weight: 800;
}

.timeline-label {
    color: #475569;
    font-size: 11px;
    margin-top: 3px;
}

/* Bottom nav */
.bottom-space {
    height: 55px;
}

/* Mobile */
@media (max-width: 600px) {
    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }

    .hero {
        padding: 20px;
        border-radius: 22px;
    }

    .hero-title {
        font-size: 24px;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Demo data
# -----------------------------
DEFAULT_PARTNERS = pd.DataFrame([
    ["ASKRIDA", "Asuransi Umum", "Active", "KSM, KUM, KUR, Kebakaran, Credit Life", "Bancassurance ASKRIDA"],
    ["ASPAN", "Asuransi Umum", "Active", "KSM, KUM, KUR, Kebakaran", "Bancassurance ASPAN"],
    ["BOSOWA", "Asuransi Umum", "Active", "KSM, KUM, Kebakaran", "Bancassurance BOSOWA"],
    ["JASINDO", "Asuransi Umum", "Active", "KSM, KUM, KUR, Kebakaran, MBI", "Bancassurance JASINDO"],
], columns=["Asuradur", "Jenis", "Status", "Produk", "PIC"])

DEFAULT_METRICS = pd.DataFrame([
    ["ASKRIDA", 1107.67, 31.34, 13.56, 43.29],
    ["ASPAN", 923.22, 12.40, 8.20, 82.91],
    ["BOSOWA", 90.21, 0.49, 0.49, 100.00],
    ["JASINDO", 928.28, 21.10, 36.52, 173.06],
], columns=["Asuradur", "Outstanding", "Pengajuan", "Pembayaran", "Rasio"])

DEFAULT_HISTORY = pd.DataFrame({
    "Bulan": pd.date_range("2024-01-01", periods=24, freq="MS"),
    "Komitmen": [56.7,56.7,56.7,56.7,56.7,56.7,56.7,56.7,56.7,56.7,56.7,56.7,
                 56.7,56.7,56.7,56.7,56.7,56.7,56.7,56.7,56.7,56.7,56.7,56.7],
    "Realisasi": [35,42,50,58,61,57,56,54,52,50,47,45,43,40,37,34,30,28,26,24,22,20,19,18]
})

# -----------------------------
# Optional Excel loader
# -----------------------------
def load_excel():
    candidates = [
        Path("data/Master Data.xlsx"),
        Path("Master Data.xlsx"),
    ]
    for path in candidates:
        if path.exists():
            try:
                raw = pd.read_excel(path)
                cols = {str(c).strip().upper(): c for c in raw.columns}
                if "ASURADUR" in cols:
                    partner_names = raw[cols["ASURADUR"]].dropna().astype(str).str.strip().drop_duplicates()
                    if len(partner_names):
                        partners = DEFAULT_PARTNERS.copy()
                        partners = partners[partners["Asuradur"].isin(partner_names)].copy()
                        for name in partner_names:
                            if name not in set(partners["Asuradur"]):
                                partners.loc[len(partners)] = [name, "Asuransi", "Active", "Belum dipetakan", "-"]
                        return partners, DEFAULT_METRICS
            except Exception:
                pass
    return DEFAULT_PARTNERS, DEFAULT_METRICS

partners, metrics = load_excel()

# -----------------------------
# Session
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_partner" not in st.session_state:
    st.session_state.selected_partner = None

# -----------------------------
# Header
# -----------------------------
h1, h2 = st.columns([5, 1])
with h1:
    st.markdown("### 🛡️ BancaPocket")
    st.caption("Bancassurance Partner Information")
with h2:
    st.markdown("## 🔵")

# -----------------------------
# Detail page
# -----------------------------
if st.session_state.page == "detail" and st.session_state.selected_partner:
    name = st.session_state.selected_partner
    p = partners[partners["Asuradur"] == name].iloc[0]
    m = metrics[metrics["Asuradur"] == name]
    m = m.iloc[0] if not m.empty else None

    if st.button("← Kembali", use_container_width=True):
        st.session_state.page = "home"
        st.session_state.selected_partner = None
        st.rerun()

    st.markdown('<div class="section">Profil Asuradur</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="detail">
            <div class="detail-title">🏢 {p['Asuradur']}</div>
            <div class="detail-sub">{p['Jenis']} · {p['Status']}</div>
            <br>
            <div class="mini-label">Produk Bancassurance</div>
            <div style="margin-top:8px;">
                {''.join(f'<span class="pill">{x.strip()}</span>' for x in str(p['Produk']).split(','))}
            </div>
            <br>
            <div class="mini-label">PIC</div>
            <div class="mini-value" style="font-size:15px;">{p['PIC']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if m is not None:
        st.markdown('<div class="section">Monitoring Klaim</div>', unsafe_allow_html=True)
        a,b = st.columns(2)
        with a:
            st.markdown(f"<div class='card'><div class='mini-label'>Outstanding</div><div class='mini-value'>Rp {m['Outstanding']:,.2f} M</div></div>", unsafe_allow_html=True)
        with b:
            st.markdown(f"<div class='card'><div class='mini-label'>Rasio Pembayaran</div><div class='mini-value'>{m['Rasio']:.2f}%</div></div>", unsafe_allow_html=True)

        st.markdown('<div class="section">History Pembayaran</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=DEFAULT_HISTORY["Bulan"],
            y=DEFAULT_HISTORY["Komitmen"],
            name="Komitmen",
            mode="lines",
            line=dict(color="#CBD5E1", width=3, dash="dash")
        ))
        fig.add_trace(go.Scatter(
            x=DEFAULT_HISTORY["Bulan"],
            y=DEFAULT_HISTORY["Realisasi"],
            name="Realisasi",
            mode="lines+markers",
            line=dict(color="#2563EB", width=4)
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor="white",
            plot_bgcolor="white",
            legend=dict(orientation="h", y=-0.18),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#EEF2F7")
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section">Perjanjian</div>', unsafe_allow_html=True)
    t1,t2,t3 = st.columns(3)
    with t1:
        st.markdown("<div class='card'><div class='mini-label'>Perjanjian</div><div class='mini-value' style='font-size:15px;'>10 Agu 2022</div></div>", unsafe_allow_html=True)
    with t2:
        st.markdown("<div class='card'><div class='mini-label'>Komitmen</div><div class='mini-value' style='font-size:15px;'>Des 2022</div></div>", unsafe_allow_html=True)
    with t3:
        st.markdown("<div class='card'><div class='mini-label'>Status</div><br><span class='status'>ACTIVE</span></div>", unsafe_allow_html=True)

# -----------------------------
# Home page
# -----------------------------
else:
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Hello, Pegawai 👋</div>
        <div class="hero-subtitle">Bancassurance Partner Information</div>
        <div class="hero-text">
            Temukan Asuradur yang telah bekerja sama dengan Bancassurance
            dan akses informasi partner dengan cepat.
        </div>
        <span class="hero-badge">● PARTNER DIRECTORY</span>
    </div>
    """, unsafe_allow_html=True)

    search = st.text_input(
        "Cari Asuradur",
        placeholder="🔎  Cari nama Asuradur...",
        label_visibility="collapsed"
    )

    result = partners[
        partners["Asuradur"].str.contains(search, case=False, na=False)
    ].copy()

    st.markdown('<div class="section">Asuradur Partner</div>', unsafe_allow_html=True)

    if result.empty:
        st.info("Asuradur tidak ditemukan.")
    else:
        for _, p in result.iterrows():
            c1,c2,c3 = st.columns([0.8, 4.0, 1.4])

            with c1:
                st.markdown("### 🏢")

            with c2:
                st.markdown(
                    f"<div class='partner-name'>{p['Asuradur']}</div>"
                    f"<div class='partner-type'>{p['Jenis']} · {p['Status']}</div>",
                    unsafe_allow_html=True
                )

            with c3:
                st.markdown("<span class='status'>ACTIVE</span>", unsafe_allow_html=True)

            if st.button(
                f"Lihat {p['Asuradur']} →",
                key=f"open_{p['Asuradur']}",
                use_container_width=True
            ):
                st.session_state.selected_partner = p["Asuradur"]
                st.session_state.page = "detail"
                st.rerun()

    st.markdown('<div class="section">Ringkasan Partner</div>', unsafe_allow_html=True)
    x1,x2 = st.columns(2)
    with x1:
        st.markdown(f"<div class='card'><div class='mini-label'>Total Asuradur</div><div class='mini-value'>{len(partners)}</div></div>", unsafe_allow_html=True)
    with x2:
        active = int((partners["Status"].str.upper() == "ACTIVE").sum())
        st.markdown(f"<div class='card'><div class='mini-label'>Partner Active</div><div class='mini-value'>{active}</div></div>", unsafe_allow_html=True)

    st.markdown('<div class="section">Quick Access</div>', unsafe_allow_html=True)
    q1,q2,q3 = st.columns(3)
    with q1:
        st.button("🛡️\nPartner", use_container_width=True)
    with q2:
        st.button("📚\nGuide", use_container_width=True)
    with q3:
        st.button("📊\nMonitoring", use_container_width=True)

# -----------------------------
# Bottom navigation
# -----------------------------
st.markdown("<div class='bottom-space'></div>", unsafe_allow_html=True)
n1,n2,n3,n4 = st.columns(4)

with n1:
    if st.button("⌂\nHome", use_container_width=True):
        st.session_state.page = "home"
        st.session_state.selected_partner = None
        st.rerun()

with n2:
    if st.button("🛡️\nPartner", use_container_width=True):
        st.session_state.page = "home"
        st.session_state.selected_partner = None
        st.rerun()

with n3:
    st.button("📚\nGuide", use_container_width=True)

with n4:
    st.button("ℹ️\nInfo", use_container_width=True)

st.caption("BancaPocket • Internal Bancassurance Information")
