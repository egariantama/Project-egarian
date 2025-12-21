import streamlit as st
import pandas as pd
import random
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Proliga Putri 2026 - JLM Simulator",
    layout="centered"
)

# =========================
# DATA
# =========================
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

score_points = {
    "3-0": (3, 0),
    "3-1": (3, 0),
    "3-2": (2, 1),
    "2-3": (1, 2),
    "1-3": (0, 3),
    "0-3": (0, 3),
}

score_options = ["Pilih Skor", "3-0", "3-1", "3-2", "2-3", "1-3", "0-3"]

jlm_matches = [
    "Sumut Falcons","Sumut Falcons",
    "Bandung BJB Tandamata","Bandung BJB Tandamata",
    "Jakarta Electric PLN","Jakarta Electric PLN",
    "Gresik Phonska Plus","Gresik Phonska Plus",
    "Jakarta Pertamina Enduro","Jakarta Pertamina Enduro",
    "Jakarta Popsivo Polwan","Jakarta Popsivo Polwan"
]

# =========================
# SESSION STATE INIT
# =========================
if "simulated" not in st.session_state:
    st.session_state.simulated = False
    st.session_state.points = {t: 0 for t in teams}
    st.session_state.jlm_results = []

# =========================
# AUTO SIMULATOR (NON JLM)
# =========================
def auto_simulate(a, b):
    diff = teams_strength[a] - teams_strength[b]
    if diff >= 2:
        pool = ["3-0", "3-1", "3-2"]
    elif diff == 1:
        pool = ["3-1", "3-2", "2-3"]
    elif diff == 0:
        pool = ["3-2", "2-3", "3-1", "1-3"]
    else:
        pool = ["0-3", "1-3", "2-3"]
    return random.choice(pool)

# =========================
# UI
# =========================
st.title("🏐 Proliga Putri 2026")
st.caption("Simulasi Musim — Jakarta Livin Mandiri")

tab_home, tab_input, tab_table = st.tabs(
    ["🏠 Home", "✍️ Input JLM", "🏆 Klasemen"]
)

# =========================
# INPUT TAB
# =========================
with tab_input:
    st.subheader("Input 12 Pertandingan Jakarta Livin Mandiri")

    user_scores = []
    valid = True

    for i, opp in enumerate(jlm_matches):
        score = st.selectbox(
            f"Match {i+1} vs {opp}",
            score_options,
            key=f"match_{i}"
        )
        if score == "Pilih Skor":
            valid = False
        user_scores.append((opp, score))

    if st.button("🚀 Simulasikan Musim"):
        if not valid:
            st.warning("Lengkapi semua skor terlebih dahulu")
        else:
            points = {t: 0 for t in teams}
            jlm_results = []

            # JLM Matches
            for opp, score in user_scores:
                pj, po = score_points[score]
                points["Jakarta Livin Mandiri"] += pj
                points[opp] += po
                result = "Menang" if pj > po else "Kalah"
                jlm_results.append((opp, score, result))

            # Non-JLM Matches
            for i in range(len(teams)):
                for j in range(i+1, len(teams)):
                    a, b = teams[i], teams[j]
                    if "Jakarta Livin Mandiri" in (a, b):
                        continue
                    for _ in range(2):
                        s = auto_simulate(a, b)
                        pa, pb = score_points[s]
                        points[a] += pa
                        points[b] += pb

            st.session_state.points = points
            st.session_state.jlm_results = jlm_results
            st.session_state.simulated = True

            st.success("Simulasi berhasil ✅")

# =========================
# HOME TAB
# =========================
with tab_home:
    if not st.session_state.simulated:
        st.info("Silakan input hasil pertandingan JLM terlebih dahulu")
    else:
        wins = [r for r in st.session_state.jlm_results if r[2] == "Menang"]
        losses = [r for r in st.session_state.jlm_results if r[2] == "Kalah"]

        st.subheader("Ringkasan Jakarta Livin Mandiri")
        st.metric("Menang", len(wins))
        st.metric("Kalah", len(losses))

        st.markdown("### 🟢 Menang")
        for opp, score, _ in wins:
            st.write(f"✔ vs **{opp}** — {score}")

        st.markdown("### 🔴 Kalah")
        for opp, score, _ in losses:
            st.write(f"✖ vs **{opp}** — {score}")

# =========================
# KLASMEN TAB
# =========================
with tab_table:
    if not st.session_state.simulated:
        st.info("Belum ada simulasi")
    else:
        df = (
            pd.DataFrame(
                st.session_state.points.items(),
                columns=["Tim", "Poin"]
            )
            .sort_values("Poin", ascending=False)
            .reset_index(drop=True)
        )

        df["Peringkat"] = df.index + 1
        st.dataframe(df[["Peringkat", "Tim", "Poin"]], use_container_width=True)

        rank = df[df["Tim"] == "Jakarta Livin Mandiri"]["Peringkat"].values[0]

        if rank <= 4:
            st.success(f"✅ JLM LOLOS FINAL FOUR (Peringkat {rank})")
        else:
            st.error(f"❌ JLM TIDAK LOLOS FINAL FOUR (Peringkat {rank})")
