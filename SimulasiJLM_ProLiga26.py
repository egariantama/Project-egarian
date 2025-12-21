import streamlit as st
import pandas as pd
import random

# ==================================================
# PAGE CONFIG (MOBILE FIRST)
# ==================================================
st.set_page_config(
    page_title="Proliga Putri 2026",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================================================
# FORCE LIGHT THEME (ANTI DARK MODE)
# ==================================================
st.markdown("""
<style>

/* ROOT */
.stApp,
[data-testid="stAppViewContainer"],
html, body {
    background-color: #ffffff !important;
    color: #2b2b2b !important;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

/* HEADER */
[data-testid="stHeader"] {
    background-color: #ffffff !important;
}

/* TITLES */
h1 { color: #7209b7 !important; font-size: 1.9rem; }
h2, h3 { color: #b5179e !important; }

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
    color: white !important;
    border-radius: 16px;
    padding: 14px;
    font-weight: 600;
    width: 100%;
}

/* SELECTBOX */
.stSelectbox label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #7209b7 !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    background-color: #ffffff !important;
    border-radius: 14px;
}
[data-testid="stDataFrame"] * {
    color: #2b2b2b !important;
}

/* METRIC */
[data-testid="metric-container"] {
    background-color: #f8f8f8 !important;
    border-radius: 14px;
    padding: 14px;
    text-align: center;
}

/* TAB */
button[data-baseweb="tab"] {
    font-size: 0.9rem;
    padding: 10px;
    color: #7209b7 !important;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.title("🏐 Proliga Putri 2026")
st.caption("Simulasi Musim | Jakarta Livin Mandiri")

# ==================================================
# DATA TIM
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
    "3-0": (3, 0),
    "3-1": (3, 0),
    "3-2": (2, 1),
    "2-3": (1, 2),
    "1-3": (0, 3),
    "0-3": (0, 3)
}

# ==================================================
# SESSION STATE INIT
# ==================================================
if "points" not in st.session_state:
    st.session_state.points = {team: 0 for team in teams}
    st.session_state.win = 0
    st.session_state.lose = 0
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
    st.subheader("📊 Ringkasan JLM")

    col1, col2 = st.columns(2)
    col1.metric("Menang", st.session_state.win)
    col2.metric("Kalah", st.session_state.lose)

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# INPUT
# ==================================================
with tab_input:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✍️ Input Hasil Jakarta Livin Mandiri")

    points = {team: 0 for team in teams}
    win, lose = 0, 0

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
        else:
            lose += 1

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

        rank = standings[standings["Tim"]=="Jakarta Livin Mandiri"].index[0] + 1

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🎯 Status Final Four")
        if rank <= 4:
            st.success(f"✅ JLM LOLOS FINAL FOUR (Peringkat {rank})")
        else:
            st.error(f"❌ JLM TIDAK LOLOS (Peringkat {rank})")
        st.markdown("</div>", unsafe_allow_html=True)
