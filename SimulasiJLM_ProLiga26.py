import streamlit as st
import pandas as pd
import random

# ======================
# PAGE CONFIG (MOBILE FIRST)
# ======================
st.set_page_config(
    page_title="Proliga Putri 2026",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ======================
# MOBILE FIRST WHITE UI
# ======================
st.markdown("""
<style>

/* ===== GLOBAL ===== */
html, body, [class*="css"]  {
    background-color: #ffffff !important;
    color: #2b2b2b;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ===== HEADER ===== */
h1 {
    color: #7209b7;
    font-size: 1.8rem;
}
h2, h3 {
    color: #b5179e;
}

/* ===== CARD ===== */
.card {
    background: #ffffff;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}

/* ===== SELECTBOX ===== */
.stSelectbox label {
    font-weight: 600;
    font-size: 0.9rem;
    color: #7209b7;
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(90deg, #f72585, #7209b7);
    color: white;
    border-radius: 14px;
    padding: 14px;
    font-weight: 600;
    font-size: 0.95rem;
    width: 100%;
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 14px;
    overflow: hidden;
}
[data-testid="stDataFrame"] * {
    color: #2b2b2b !important;
    font-size: 0.85rem;
}

/* ===== METRIC ===== */
[data-testid="metric-container"] {
    background-color: #f9f9f9;
    border-radius: 14px;
    padding: 14px;
    text-align: center;
}
[data-testid="metric-container"] label {
    font-size: 0.8rem;
}

/* ===== TAB ===== */
button[data-baseweb="tab"] {
    font-size: 0.9rem;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.title("🏐 Proliga Putri 2026")
st.caption("Simulasi Musim • Jakarta Livin Mandiri")

# ======================
# TAB NAVIGATION
# ======================
tab_home, tab_input, tab_klasemen = st.tabs(
    ["🏠 Home", "✍️ Input", "🏆 Klasemen"]
)

# ======================
# DATA TIM
# ======================
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

# ======================
# AUTO SIMULATION
# ======================
def auto_simulate(a, b):
    diff = teams_strength[a] - teams_strength[b]
    if diff >= 2:
        return random.choice(["3-0","3-1","3-2"])
    elif diff == 1:
        return random.choice(["3-1","3-2","2-3"])
    elif diff == 0:
        return random.choice(score_options)
    else:
        return random.choice(["0-3","1-3","2-3"])

# ======================
# SESSION STATE
# ======================
if "points" not in st.session_state:
    st.session_state.points = {t: 0 for t in teams}
    st.session_state.win = 0
    st.session_state.lose = 0

# ======================
# HOME
# ======================
with tab_home:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Ringkasan JLM")
    st.metric("Menang", st.session_state.win)
    st.metric("Kalah", st.session_state.lose)
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# INPUT
# ======================
with tab_input:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✍️ Input Match Jakarta Livin Mandiri")

    points = {t: 0 for t in teams}
    win, lose = 0, 0

    opponents = [
        "Sumut Falcons","Sumut Falcons",
        "Bandung BJB Tandamata","Bandung BJB Tandamata",
        "Jakarta Electric PLN","Jakarta Electric PLN",
        "Gresik Phonska Plus","Gresik Phonska Plus",
        "Jakarta Pertamina Enduro","Jakarta Pertamina Enduro",
        "Jakarta Popsivo Polwan","Jakarta Popsivo Polwan"
    ]

    for i, opp in enumerate(opponents):
        score = st.selectbox(
            f"Match {i+1} vs {opp}",
            score_options,
            index=3,
            key=f"jlm{i}"
        )
        pj, po = score_points[score]
        points["Jakarta Livin Mandiri"] += pj
        points[opp] += po

        if pj > po:
            win += 1
        else:
            lose += 1

    st.session_state.points = points
    st.session_state.win = win
    st.session_state.lose = lose

    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# SIMULATE OTHER MATCHES
# ======================
for i in range(len(teams)):
    for j in range(i+1, len(teams)):
        a, b = teams[i], teams[j]
        if "Jakarta Livin Mandiri" in [a, b]:
            continue
        for _ in range(2):
            s = auto_simulate(a, b)
            pa, pb = score_points[s]
            st.session_state.points[a] += pa
            st.session_state.points[b] += pb

# ======================
# KLASMEN
# ======================
with tab_klasemen:
    table = (
        pd.DataFrame(st.session_state.points.items(), columns=["Tim", "Poin"])
        .sort_values("Poin", ascending=False)
        .reset_index(drop=True)
    )
    table.index += 1

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏆 Klasemen Akhir")
    st.dataframe(table, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    rank = table[table["Tim"]=="Jakarta Livin Mandiri"].index[0] + 1

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if rank <= 4:
        st.success(f"✅ JLM Lolos Final Four (Peringkat {rank})")
    else:
        st.error(f"❌ JLM Gagal Final Four (Peringkat {rank})")
    st.markdown("</div>", unsafe_allow_html=True)
