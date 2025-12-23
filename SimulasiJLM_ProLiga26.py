import streamlit as st
import pandas as pd
import random
import base64

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Proliga Putri 2026",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================================================
# LOGO + HEADER
# ==================================================
def load_logo(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = load_logo("logo_jlm.png")

st.markdown(f"""
<div style="display:flex; align-items:center; gap:14px; margin-bottom:8px;">
    <img src="data:image/png;base64,{logo_base64}" style="height:72px;">
    <div>
        <div style="font-size:2rem; font-weight:800; line-height:1.1;">
            Proliga Putri 2026
        </div>
        <div style="font-size:0.95rem; color:#666;">
            Simulasi Musim | Jakarta Livin Mandiri
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATE
# ==================================================
DEFAULT_STATE = {
    "simulated": False,
    "points": {},
    "win": 0,
    "lose": 0,
    "jlm_results": []
}

for k, v in DEFAULT_STATE.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==================================================
# GLOBAL CSS (CLEAN & STABLE)
# ==================================================
st.markdown("""
<style>
html, body, .stApp {
    background:#ffffff;
    color:#111111;
    font-family:-apple-system, BlinkMacSystemFont, sans-serif;
}

/* CARD */
.card {
    background:white;
    border-radius:18px;
    padding:18px;
    margin-bottom:18px;
    box-shadow:0 6px 18px rgba(0,0,0,.08);
}

/* STAT */
.stat-box {
    background:linear-gradient(135deg,#f72585,#7209b7);
    color:white;
    border-radius:16px;
    padding:16px;
    text-align:center;
}
.stat-value {
    font-size:1.8rem;
    font-weight:800;
}

/* BUTTON */
.stButton>button {
    background:linear-gradient(90deg,#f72585,#7209b7);
    color:white;
    border-radius:18px;
    padding:14px;
    font-weight:700;
    width:100%;
}

/* TAB STYLE */
button[data-baseweb="tab"] {
    font-weight:700;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background:linear-gradient(135deg,#f72585,#7209b7);
    color:white !important;
    border-radius:16px;
}

/* TABLE */
.stDataFrame th {
    background:#f5f5f7;
    font-weight:700;
}
.stDataFrame td, .stDataFrame th {
    border-bottom:1px solid rgba(0,0,0,.12);
}

/* CENTER PERINGKAT */
[data-testid="stDataFrame"] th:nth-child(1),
[data-testid="stDataFrame"] td:nth-child(1) {
    text-align:center;
    font-weight:700;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* =========================
   FINAL TAB PILL FIX (LOCKED)
   ========================= */

/* TAB CONTAINER */
div[data-baseweb="tab-list"] {
    background: #f5f5f7 !important;
    border-radius: 26px !important;
    padding: 8px !important;
    gap: 6px !important;
}

/* TAB UMUM */
button[data-baseweb="tab"] {
    background: transparent !important;
    color: #7209b7 !important;
    font-weight: 700 !important;

    border-radius: 20px !important;
    padding: 10px 18px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;

    opacity: 1 !important;
    min-height: 42px !important;
}

/* TAB AKTIF */
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg,#f72585,#7209b7) !important;
    color: #ffffff !important;
    box-shadow: 0 6px 16px rgba(114,9,183,.35);
}

/* PAKSA TEKS & EMOJI TERLIHAT */
button[data-baseweb="tab"] span,
button[data-baseweb="tab"] svg {
    color: inherit !important;
    opacity: 1 !important;
}

/* MOBILE ANDROID */
@media (max-width: 768px) {
    button[data-baseweb="tab"] {
        font-size: 0.9rem !important;
        padding: 10px 14px !important;
    }
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* =========================
   FIX LABEL MATCH TIDAK TERLIHAT
   ========================= */

/* LABEL st.selectbox */
div[data-testid="stSelectbox"] label {
    color: #111111 !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    opacity: 1 !important;
    margin-bottom: 6px !important;
    display: block !important;
}

/* MOBILE ANDROID */
@media (max-width: 768px) {
    div[data-testid="stSelectbox"] label {
        font-size: 0.9rem !important;
    }
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* =========================
   FIX RINGKASAN HOME MOBILE
   ========================= */

/* Container kolom Home */
div[data-testid="column"] {
    display: flex;
    flex-direction: column;
}

/* MOBILE → FORCE 2 STAT DALAM 1 BARIS */
@media (max-width: 768px) {

    /* Bungkus stat-box agar sejajar */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        gap: 10px !important;
    }

    /* Stat box lebih ramping */
    .stat-box {
        flex: 1 !important;
        padding: 12px !important;
        border-radius: 14px !important;
    }

    .stat-box div:first-child {
        font-size: 0.85rem !important;
    }

    .stat-value {
        font-size: 1.4rem !important;
    }
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* =========================
   SPASI MENANG & KALAH
   ========================= */

/* Tambah jarak antar stat-box */
.stat-box {
    margin-bottom: 12px !important;
}

/* Mobile: spasi lebih halus */
@media (max-width: 768px) {
    .stat-box {
        margin-bottom: 14px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# ✅ FINAL SELECTBOX FIX (ANDROID / IOS / DESKTOP)
# ==================================================
st.markdown("""
<style>
/* SELECTBOX FINAL FIX — JANGAN DITIMPA */

div[data-baseweb="select"] {
    background:#ffffff !important;
    border-radius:14px !important;
    border:1px solid #ccc !important;
}

div[data-baseweb="select"] span {
    color:#111111 !important;
    -webkit-text-fill-color:#111111 !important;
    font-weight:700 !important;
}

div[data-baseweb="select"] input {
    color:#111111 !important;
    -webkit-text-fill-color:#111111 !important;
}

div[data-baseweb="select"] svg {
    fill:#111111 !important;
}

div[data-baseweb="menu"] span {
    color:#111111 !important;
    font-weight:600 !important;
}

div[data-baseweb="menu"] div:hover {
    background:#f72585 !important;
}
div[data-baseweb="menu"] div:hover span {
    color:#ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# DATA
# ==================================================
teams_strength = {
    "Jakarta Pertamina Enduro": 5,
    "Jakarta Popsivo Polwan": 5,
    "Jakarta Electric PLN": 4,
    "Gresik Phonska Plus": 4,
    "Jakarta Livin Mandiri": 3,
    "Bandung BJB Tandamata": 2,
    "Sumut Falcons": 1
}
teams = list(teams_strength.keys())

score_options = ["— Pilih Skor —","3-0","3-1","3-2","2-3","1-3","0-3"]
score_points = {
    "3-0":(3,0),"3-1":(3,0),"3-2":(2,1),
    "2-3":(1,2),"1-3":(0,3),"0-3":(0,3)
}

# ==================================================
# AUTO SIMULATE
# ==================================================
def auto_simulate(a,b):
    diff = teams_strength[a] - teams_strength[b]
    if diff >= 2:
        pool = ["3-0","3-1","3-2"]
    elif diff == 1:
        pool = ["3-1","3-2","2-3"]
    elif diff == 0:
        pool = ["3-2","2-3","3-1","1-3"]
    else:
        pool = ["0-3","1-3","2-3"]
    return random.choice(pool)

# ==================================================
# TABS
# ==================================================
tab_home, tab_input, tab_klasemen = st.tabs(
    ["🏠 Home","✍️ Input","🏆 Klasemen"]
)

# ==================================================
# HOME (REALTIME + DETAIL JLM DIKEMBALIKAN)
# ==================================================
with tab_home:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Ringkasan Jakarta Livin Mandiri")

    c1, c2 = st.columns(2)
    c1.markdown(
        f"<div class='stat-box'><div>Menang</div><div class='stat-value'>{st.session_state.win}</div></div>",
        unsafe_allow_html=True
    )
    c2.markdown(
        f"<div class='stat-box'><div>Kalah</div><div class='stat-value'>{st.session_state.lose}</div></div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ===============================
    # DETAIL MATCH JLM (AMAN)
    # ===============================
    if st.session_state.jlm_results and len(st.session_state.jlm_results) > 0:
        df_jlm = pd.DataFrame(
            st.session_state.jlm_results,
            columns=["No", "Lawan", "Skor", "Poin", "Hasil"]
        )

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📋 Detail Pertandingan JLM")
        st.dataframe(
            df_jlm.set_index("No"),
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Belum ada hasil pertandingan. Silakan input skor di menu Input ✍️")

# ==================================================
# INPUT (REALTIME + BUTTON SIMULASI DIKEMBALIKAN)
# ==================================================
with tab_input:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✍️ Input Hasil Jakarta Livin Mandiri")

    # --- selectbox match (punyamu tetap) ---
    for i, opp in enumerate(jlm_matches):
        score = st.selectbox(
            f"Match {i+1} vs {opp}",
            score_options,
            key=f"match_{i}"
        )

    # ===============================
    # 🚀 BUTTON SIMULASI MUSIM (HANYA DI INPUT)
    # ===============================
    if st.button("🚀 Simulasikan Musim"):
        if not valid:
            st.markdown("""
            <div style="
                background:linear-gradient(135deg,#fde7f3,#e9d5ff);
                border:1px solid #d8b4fe;
                border-radius:16px;
                padding:14px;
                font-weight:700;
                color:#5b21b6;
                text-align:center;
                margin-top:12px;
            ">
            ⚠️ Lengkapi semua skor terlebih dahulu
            </div>
            """, unsafe_allow_html=True)
        else:
            for i in range(len(teams)):
                for j in range(i + 1, len(teams)):
                    a, b = teams[i], teams[j]
                    if "Jakarta Livin Mandiri" in (a, b):
                        continue
                    for _ in range(2):
                        s = auto_simulate(a, b)
                        pa, pb = score_points[s]
                        points[a] += pa
                        points[b] += pb

            st.session_state.points = points
            st.session_state.simulated = True
            st.success("Simulasi musim selesai 🎉")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# KLASMEN
# ==================================================
with tab_klasemen:
    if st.session_state.points:
        df = pd.DataFrame(
            st.session_state.points.items(),
            columns=["Tim","Poin"]
        ).sort_values("Poin", ascending=False).reset_index(drop=True)

        df.insert(0, "Peringkat", df.index + 1)

        def highlight_jlm(row):
            return [
                "background-color:#bbf7d0; color:#064e3b; font-weight:800"
                if row["Tim"]=="Jakarta Livin Mandiri" else ""
                for _ in row
            ]

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🏆 Klasemen Akhir")
        st.dataframe(
            df.style.apply(highlight_jlm, axis=1),
            use_container_width=True,
            hide_index=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
