import streamlit as st
import pandas as pd
import random

# ======================
# KONFIGURASI HALAMAN
# ======================
st.set_page_config(
    page_title="Proliga Putri 2026",
    layout="centered"
)

# ======================
# GLOBAL STYLE
# ======================
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #0f0f14, #15151f);
    color: white;
}
h1, h2, h3 {
    color: #c77dff;
}
.card {
    background-color: #ffffff;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.25);
}
.stSelectbox label {
    font-weight: 600;
    color: #7209b7;
}
.stButton>button {
    background: linear-gradient(90deg, #f72585, #7209b7);
    color: white;
    border-radius: 14px;
    padding: 12px;
    font-weight: 600;
    width: 100%;
}
[data-testid="stDataFrame"] {
    background-color: white;
    color: black;
}
[data-testid="stDataFrame"] * {
    color: black !important;
}
[data-testid="metric-container"] {
    background-color: #ffffff;
    padding: 12px;
    border-radius: 14px;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.title("🏐 Proliga Putri 2026")
st.caption("Simulasi Musim | Jakarta Livin Mandiri")

# ======================
# TAB NAVIGATION
# ======================
tab_home, tab_input, tab_klasemen = st.tabs(["🏠 Home", "✍️ Input", "🏆 Klasemen"])

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
# SIMULASI OTOMATIS
# ======================
def auto_simulate(team_a, team_b):
    diff = teams_strength[team_a] - teams_strength[team_b]
    if diff >= 2:
        choices = ["3-0", "3-1", "3-2"]
    elif diff == 1:
        choices = ["3-1", "3-2", "2-3"]
    elif diff == 0:
        choices = score_options
    else:
        choices = ["0-3", "1-3", "2-3"]
    return random.choice(choices)

# ======================
# SESSION STATE
# ======================
if "points" not in st.session_state:
    st.session_state.points = {team: 0 for team in teams}
    st.session_state.win = 0
    st.session_state.lose = 0

# ======================
# HOME TAB
# ======================
with tab_home:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Ringkasan Jakarta Livin Mandiri")
    st.metric("Menang", st.session_state.win)
    st.metric("Kalah", st.session_state.lose)
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# INPUT TAB
# ======================
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
            key=f"m{i}"
        )
        pj, po = score_points[score]
        points["Jakarta Livin Mandiri"] += pj
        points[opp] += po

        if pj > po:
            win += 1
        else:
            lose += 1

    # Simpan ke session
    st.session_state.points = points
    st.session_state.win = win
    st.session_state.lose = lose

    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# SIMULASI MATCH LAIN
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
# KLASMEN TAB
# ======================
with tab_klasemen:
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
