import streamlit as st
import pandas as pd
import random
import time

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Proliga Putri 2026",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================================================
# SESSION STATE SAFE INIT (ANTI ERROR)
# ==================================================
st.session_state.setdefault("simulated", False)
st.session_state.setdefault("points", {})
st.session_state.setdefault("win", 0)
st.session_state.setdefault("lose", 0)
st.session_state.setdefault("match_results", [])

# ==================================================
# GLOBAL CSS
# ==================================================
st.markdown("""
<style>
html, body, .stApp {
    background-color: #ffffff;
    color: #111111;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}
.card {
    background: white;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}
.stat-box {
    background: linear-gradient(135deg, #f72585, #7209b7);
    color: white;
    border-radius: 16px;
    padding: 16px;
    text-align: center;
}
.stat-value {
    font-size: 1.9rem;
    font-weight: 800;
}
.stButton > button {
    background: linear-gradient(90deg, #f72585, #7209b7);
    color: white;
    border-radius: 18px;
    padding: 14px;
    font-weight: 700;
    width: 100%;
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

score_options = ["— Pilih Skor —", "3-0", "3-1", "3-2", "2-3", "1-3", "0-3"]

score_points = {
    "3-0": (3, 0),
    "3-1": (3, 0),
    "3-2": (2, 1),
    "2-3": (1, 2),
    "1-3": (0, 3),
    "0-3": (0, 3),
}

# ==================================================
# AUTO SIMULATION
# ==================================================
def auto_simulate(a, b):
    diff = teams_strength[a] - teams_strength[b]
    if diff >= 2:
        pool = ["3-0", "3-1", "3-2"]
    elif diff == 1:
        pool = ["3-1", "3-2", "2-3"]
    elif diff == 0:
        pool = ["3-2", "2-3"]
    else:
        pool = ["0-3", "1-3"]
    return random.choice(pool)

# ==================================================
# TABS
# ==================================================
tab_home, tab_input, tab_klasemen = st.tabs(
    ["🏠 Home", "✍️ Input", "🏆 Klasemen"]
)

# ==================================================
# HOME
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

    if st.session_state.simulated:
        df = pd.DataFrame(
            st.session_state.match_results,
            columns=["Lawan", "Skor", "Hasil"]
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("✅ Menang vs")
            for _, r in df[df["Hasil"] == "Menang"].iterrows():
                st.write(f"• {r['Lawan']} ({r['Skor']})")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("❌ Kalah vs")
            for _, r in df[df["Hasil"] == "Kalah"].iterrows():
                st.write(f"• {r['Lawan']} ({r['Skor']})")
            st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# INPUT
# ==================================================
with tab_input:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✍️ Input Hasil Jakarta Livin Mandiri")

    points = {t: 0 for t in teams}
    match_results = []
    win = lose = 0
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
        score = st.selectbox(f"Match {i+1} vs {opp}", score_options, key=f"m{i}")
        if score == "— Pilih Skor —":
            valid = False
            continue

        pj, po = score_points[score]
        points["Jakarta Livin Mandiri"] += pj
        points[opp] += po

        if pj > po:
            win += 1
            match_results.append([opp, score, "Menang"])
        else:
            lose += 1
            match_results.append([opp, score, "Kalah"])

    if st.button("🚀 Simulasikan Musim"):
        if not valid:
            st.warning("Lengkapi semua skor")
        else:
            for a in teams:
                for b in teams:
                    if a != b and "Jakarta Livin Mandiri" not in (a, b):
                        s = auto_simulate(a, b)
                        pa, pb = score_points[s]
                        points[a] += pa
                        points[b] += pb

            st.session_state.points = points
            st.session_state.win = win
            st.session_state.lose = lose
            st.session_state.match_results = match_results
            st.session_state.simulated = True
            st.success("Simulasi selesai 🎉")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# KLASMEN
# ==================================================
with tab_klasemen:
    if not st.session_state.simulated:
        st.info("Silakan simulasi terlebih dahulu")
    else:
        df = pd.DataFrame(
            st.session_state.points.items(),
            columns=["Tim", "Poin"]
        ).sort_values("Poin", ascending=False).reset_index(drop=True)

        st.dataframe(
            df.assign(Peringkat=df.index + 1),
            use_container_width=True
        )
