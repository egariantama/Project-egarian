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
# GLOBAL CSS FIX (ANTI TEXT INVISIBLE)
# ==================================================
st.markdown("""
<style>
/* BASE */
html, body, .stApp {
    background-color: #ffffff !important;
    color: #1a1a1a !important;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

/* TITLES */
h1 { color: #7209b7 !important; }
h2, h3, h4 { color: #b5179e !important; }

/* GENERAL TEXT */
.stMarkdown, .stText, label, span, p {
    color: #1a1a1a !important;
}

/* CARD */
.card {
    background-color: #ffffff;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(90deg, #f72585, #7209b7) !important;
    color: #ffffff !important;
    border-radius: 16px;
    padding: 14px;
    font-weight: 600;
    width: 100%;
}

/* METRIC FIX (INI KUNCI) */
[data-testid="metric-container"] {
    background-color: #f5f5f5 !important;
    border-radius: 14px;
    padding: 14px;
}
.stMetricLabel {
    color: #333333 !important;
    font-weight: 600 !important;
}
.stMetricValue {
    color: #000000 !important;
    font-weight: 700 !important;
}

/* SELECTBOX LABEL */
.stSelectbox label {
    color: #333333 !important;
    font-weight: 600;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    background-color: #ffffff !important;
}
[data-testid="stDataFrame"] * {
    color: #1a1a1a !important;
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

score_options = ["3-0", "3-1", "3-2", "2-3", "1-3", "0-3"]
score_points = {
    "3-0": (3, 0), "3-1": (3, 0), "3-2": (2, 1),
    "2-3": (1, 2), "1-3": (0, 3), "0-3": (0, 3)
}

# ==================================================
# SESSION STATE
# ==================================================
if "points" not in st.session_state:
    st.session_state.points = {team: 0 for team in teams}
    st.session_state.win = 0
    st.session_state.lose = 0
    st.session_state.results = []
    st.session_state.simulated = False

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
        choices = score_options
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

    col1, col2 = st.columns(2)
    col1.metric("Menang", st.session_state.win)
    col2.metric("Kalah", st.session_state.lose)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.simulated:
        df = pd.DataFrame(
            st.session_state.results,
            columns=["Lawan", "Skor", "Hasil"]
        )
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📋 Detail Pertandingan JLM")
        st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Belum ada data hasil pertandingan")

# ==================================================
# INPUT
# ==================================================
with tab_input:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✍️ Input Hasil Jakarta Livin Mandiri")

    points = {team: 0 for team in teams}
    win, lose = 0, 0
    results = []

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
            index=3,
            key=f"jlm_{i}"
        )

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

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# KLASMEN
# ==================================================
with tab_klasemen:
    if not st.session_state.simulated:
        st.info("Silakan input hasil JLM dan klik **Simulasikan Musim**")
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
        st.subheader("🎯 Status Final Four")
        st.success(f"✅ LOLOS FINAL FOUR (Peringkat {rank})") if rank <= 4 else \
        st.error(f"❌ TIDAK LOLOS (Peringkat {rank})")
        st.markdown("</div>", unsafe_allow_html=True)
