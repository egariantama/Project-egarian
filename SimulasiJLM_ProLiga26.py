import streamlit as st
import pandas as pd
import random

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Proliga Putri 2026",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================================================
# GLOBAL CSS (FIX VISIBILITY)
# ==================================================
st.markdown("""
<style>
html, body, .stApp {
    background-color: #ffffff !important;
    color: #111111 !important;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ===== TAB FIX ===== */
button[data-baseweb="tab"] {
    color: #7209b7 !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}
button[data-baseweb="tab"]:hover {
    background-color: #f3e8ff !important;
}
button[aria-selected="true"] {
    border-bottom: 3px solid #f72585 !important;
}

/* ===== LABEL FIX ===== */
label {
    color: #111111 !important;
    font-weight: 600 !important;
}

/* ===== HEADINGS ===== */
h1 { color: #7209b7 !important; }
h2, h3 { color: #b5179e !important; }

/* ===== CARD ===== */
.card {
    background-color: #ffffff;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}

/* ===== STAT BOX ===== */
.stat-box {
    background-color: #f5f5f5;
    border-radius: 16px;
    padding: 16px;
    text-align: center;
}
.stat-title {
    font-size: 0.9rem;
    color: #555;
    font-weight: 600;
}
.stat-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #000;
}

/* ===== BUTTON ===== */
.stButton > button {
    background: linear-gradient(90deg, #f72585, #7209b7) !important;
    color: white !important;
    border-radius: 16px;
    padding: 14px;
    font-weight: 600;
    width: 100%;
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] * {
    color: #111111 !important;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.title("🏐 Proliga Putri 2026")
st.caption("Simulasi Musim | Jakarta Livin Mandiri")

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

score_options = [
    "-- Pilih Skor --",
    "3-0", "3-1", "3-2",
    "2-3", "1-3", "0-3"
]

score_points = {
    "3-0": (3, 0), "3-1": (3, 0), "3-2": (2, 1),
    "2-3": (1, 2), "1-3": (0, 3), "0-3": (0, 3)
}

# ==================================================
# SESSION STATE
# ==================================================
if "simulated" not in st.session_state:
    st.session_state.simulated = False
    st.session_state.points = {t: 0 for t in teams}
    st.session_state.win = 0
    st.session_state.lose = 0
    st.session_state.results = []

# ==================================================
# SIMULATOR
# ==================================================
def auto_simulate(a, b):
    diff = teams_strength[a] - teams_strength[b]
    if diff >= 2:
        choices = ["3-0", "3-1", "3-2"]
    elif diff == 1:
        choices = ["3-1", "3-2", "2-3"]
    elif diff == 0:
        choices = list(score_points.keys())
    else:
        choices = ["0-3", "1-3", "2-3"]
    return random.choice(choices)

# ==================================================
# TABS
# ==================================================
tab_home, tab_input, tab_klasemen = st.tabs(["🏠 Home", "✍️ Input", "🏆 Klasemen"])

# ==================================================
# HOME
# ==================================================
with tab_home:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Ringkasan Jakarta Livin Mandiri")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-title">Menang</div>
            <div class="stat-value">{st.session_state.win}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-title">Kalah</div>
            <div class="stat-value">{st.session_state.lose}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# INPUT
# ==================================================
with tab_input:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✍️ Input Hasil Jakarta Livin Mandiri")

    points = {t: 0 for t in teams}
    win, lose = 0, 0
    results = []
    valid = True

    jlm_matches = [
        "Sumut Falcons","Sumut Falcons",
        "Bandung BJB Tandamata","Bandung BJB Tandamata",
        "Jakarta Electric PLN","Jakarta Electric PLN",
        "Gresik Phonska Plus","Gresik Phonska Plus",
        "Jakarta Pertamina Enduro","Jakarta Pertamina Enduro",
        "Jakarta Popsivo Polwan","Jakarta Popsivo Polwan"
    ]

    for i, opp in enumerate(jlm_matches):
        score = st.selectbox(
            f"Match {i+1} vs {opp}",
            score_options,
            key=f"jlm_{i}"
        )

        if score == "-- Pilih Skor --":
            valid = False
            continue

        pj, po = score_points[score]
        points["Jakarta Livin Mandiri"] += pj
        points[opp] += po

        if pj > po:
            win += 1
            results.append([opp, score, "Menang"])
        else:
            lose += 1
            results.append([opp, score, "Kalah"])

    if st.button("🔄 Simulasikan Musim"):
        if not valid:
            st.warning("⚠️ Silakan pilih skor untuk semua pertandingan")
        else:
            for i in range(len(teams)):
                for j in range(i+1, len(teams)):
                    a, b = teams[i], teams[j]
                    if "Jakarta Livin Mandiri" in [a, b]:
                        continue
                    for _ in range(2):
                        s = auto_simulate(a, b)
                        pa, pb = score_points[s]
                        points[a] += pa
                        points[b] += pb

            st.session_state.points = points
            st.session_state.win = win
            st.session_state.lose = lose
            st.session_state.results = results
            st.session_state.simulated = True
            st.success("Simulasi selesai, cek tab Klasemen 🏆")

# ==================================================
# KLASMEN
# ==================================================
with tab_klasemen:
    if not st.session_state.simulated:
        st.info("Silakan input hasil dan jalankan simulasi terlebih dahulu")
    else:
        standings = (
            pd.DataFrame(st.session_state.points.items(), columns=["Tim", "Poin"])
            .sort_values("Poin", ascending=False)
            .reset_index(drop=True)
        )
        standings.index += 1

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🏆 Klasemen Akhir")
        st.dataframe(standings, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        rank = standings[standings["Tim"] == "Jakarta Livin Mandiri"].index[0] + 1

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if rank <= 4:
            st.success(f"✅ JLM LOLOS FINAL FOUR (Peringkat {rank})")
        else:
            st.error(f"❌ JLM TIDAK LOLOS FINAL FOUR (Peringkat {rank})")
        st.markdown("</div>", unsafe_allow_html=True)
