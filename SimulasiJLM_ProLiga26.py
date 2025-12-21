import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

# ======================
# KONFIGURASI HALAMAN
# ======================
st.set_page_config(
    page_title="Proliga 2026 Simulator",
    layout="centered"
)

# ======================
# STYLE (PINK – UNGU – PUTIH)
# ======================
st.markdown("""
<style>
body { background-color: #ffffff; }
h1, h2, h3 { color: #7b2cbf; }
.stButton>button {
    background-color: #f72585;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏐 Proliga Putri 2026 Simulator")
st.caption("Monte Carlo Simulation | Jakarta Livin Mandiri")

# ======================
# DATA TIM & KEKUATAN
# ======================
teams = {
    "Jakarta Pertamina Enduro": 5,
    "Jakarta Popsivo Polwan": 5,
    "Jakarta Electric PLN": 4,
    "Gresik Phonska Plus": 4,
    "Jakarta Livin Mandiri": 3,
    "Bandung BJB Tandamata": 2,
    "Sumut Falcons": 1
}

score_map = {
    "3-0": (3, 0),
    "3-1": (3, 0),
    "3-2": (2, 1),
    "2-3": (1, 2),
    "1-3": (0, 3),
    "0-3": (0, 3)
}

score_choices = list(score_map.keys())

# ======================
# FUNGSI SIMULASI MATCH
# ======================
def simulate_match(team_a, team_b):
    diff = teams[team_a] - teams[team_b]

    if diff >= 2:
        probs = ["3-0", "3-1", "3-2", "2-3"]
    elif diff == 1:
        probs = ["3-1", "3-2", "2-3"]
    elif diff == 0:
        probs = score_choices
    else:
        probs = ["0-3", "1-3", "2-3"]

    return random.choice(probs)

# ======================
# SIMULASI 1 MUSIM
# ======================
def simulate_season():
    points = {t: 0 for t in teams}

    team_list = list(teams.keys())

    for i in range(len(team_list)):
        for j in range(i + 1, len(team_list)):
            for _ in range(2):  # double round robin
                a, b = team_list[i], team_list[j]
                score = simulate_match(a, b)
                pa, pb = score_map[score]
                points[a] += pa
                points[b] += pb

    return points

# ======================
# MONTE CARLO
# ======================
st.markdown("### 🎯 Mode Target: **Final Four (Top 4)**")

iterations = st.slider(
    "Jumlah Simulasi Musim",
    min_value=100,
    max_value=3000,
    value=1000,
    step=100
)

if st.button("🚀 Jalankan Simulasi"):
    qualify_count = 0
    jlm_points = []

    for _ in range(iterations):
        season = simulate_season()
        ranking = sorted(season.items(), key=lambda x: x[1], reverse=True)
        top4 = [t[0] for t in ranking[:4]]

        jlm_points.append(season["Jakarta Livin Mandiri"])

        if "Jakarta Livin Mandiri" in top4:
            qualify_count += 1

    probability = round((qualify_count / iterations) * 100, 2)

    # ======================
    # OUTPUT
    # ======================
    st.success(f"📊 Peluang JLM Lolos Final Four: **{probability}%**")

    # ======================
    # GRAFIK DISTRIBUSI POIN
    # ======================
    st.markdown("### 📈 Distribusi Poin JLM")

    fig, ax = plt.subplots()
    ax.hist(jlm_points, bins=15)
    ax.set_xlabel("Total Poin")
    ax.set_ylabel("Frekuensi")

    st.pyplot(fig)

    # ======================
    # INTERPRETASI
    # ======================
    if probability >= 60:
        st.success("🔥 JLM SANGAT AMAN DI 4 BESAR")
    elif probability >= 40:
        st.warning("⚠️ JLM BERSAING KETAT")
    else:
        st.error("❌ JLM RISIKO GAGAL FINAL FOUR")
