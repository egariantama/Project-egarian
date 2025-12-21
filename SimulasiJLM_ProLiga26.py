import streamlit as st
import pandas as pd
import random

# ======================
# KONFIGURASI HALAMAN
# ======================
st.set_page_config(
    page_title="Simulasi Proliga 2026 - JLM",
    layout="centered"
)

# ======================
# STYLE MOBILE APP (PUTIH – PINK – UNGU)
# ======================
st.markdown("""
<style>
/* Background */
body {
    background-color: #ffffff;
}

/* Title */
h1, h2, h3 {
    color: #6a00f4;
}

/* Card style */
.card {
    background-color: #ffffff;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}

/* Selectbox */
.stSelectbox label {
    font-weight: 600;
    color: #6a00f4;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #f72585, #7209b7);
    color: white;
    border-radius: 14px;
    padding: 12px;
    font-weight: 600;
    width: 100%;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background-color: #e5e5e5;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.title("🏐 Proliga Putri 2026")
st.caption("Simulasi Musim | Jakarta Livin Mandiri")

# ======================
# DATA TIM & KEKUATAN
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
# FUNGSI SIMULASI OTOMATIS
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
# INPUT HASIL JLM (CARD)
# ======================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🎯 Hasil Pertandingan JLM")

points = {team: 0 for team in teams}
jlm_results = []

jlm_matches = [
    "Sumut Falcons", "Sumut Falcons",
    "Bandung BJB Tandamata", "Bandung BJB Tandamata",
    "Jakarta Electric PLN", "Jakarta Electric PLN",
    "Gresik Phonska Plus", "Gresik Phonska Plus",
    "Jakarta Pertamina Enduro", "Jakarta Pertamina Enduro",
    "Jakarta Popsivo Polwan", "Jakarta Popsivo Polwan"
]

for idx, opponent in enumerate(jlm_matches):
    score = st.selectbox(
        f"Match {idx+1} vs {opponent}",
        score_options,
        index=3
    )

    p_jlm, p_opp = score_points[score]
    points["Jakarta Livin Mandiri"] += p_jlm
    points[opponent] += p_opp

    jlm_results.append({
        "Lawan": opponent,
        "Skor": score,
        "Poin JLM": p_jlm
    })

st.markdown("</div>", unsafe_allow_html=True)

# ======================
# AUTO SIMULASI MATCH LAIN
# ======================
for i in range(len(teams)):
    for j in range(i + 1, len(teams)):
        team_a = teams[i]
        team_b = teams[j]

        if "Jakarta Livin Mandiri" in [team_a, team_b]:
            continue

        for _ in range(2):
            score = auto_simulate(team_a, team_b)
            pa, pb = score_points[score]
            points[team_a] += pa
            points[team_b] += pb

# ======================
# KLASMEN
# ======================
standings = (
    pd.DataFrame(points.items(), columns=["Tim", "Poin"])
    .sort_values("Poin", ascending=False)
    .reset_index(drop=True)
)
standings.index += 1

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🏆 Klasemen Akhir")
st.dataframe(standings, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ======================
# STATUS TARGET
# ======================
jlm_rank = standings[standings["Tim"] == "Jakarta Livin Mandiri"].index[0] + 1

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🎯 Target Final Four")

if jlm_rank <= 4:
    st.success(f"✅ JLM LOLOS FINAL FOUR — Peringkat {jlm_rank}")
else:
    st.error(f"❌ JLM TIDAK LOLOS — Peringkat {jlm_rank}")

st.markdown("</div>", unsafe_allow_html=True)
