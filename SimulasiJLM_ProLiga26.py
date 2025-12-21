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
# GLOBAL CSS (FORCED LIGHT + ANIMATION)
# ==================================================
st.markdown("""
<style>
html, body, .stApp {
    background-color: #ffffff !important;
    color: #111111 !important;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ---------- TAB FIX ---------- */
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

/* ---------- HEADINGS ---------- */
h1 { color: #7209b7 !important; }
h2, h3 { color: #b5179e !important; }

/* ---------- LABEL FIX ---------- */
label {
    color: #111111 !important;
    font-weight: 600 !important;
}

/* ---------- CARD ---------- */
.card {
    background-color: #ffffff;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    animation: fadeUp 0.6s ease-in-out;
}

/* ---------- ANIMATION ---------- */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ---------- STAT BOX ---------- */
.stat-box {
    background: linear-gradient(135deg, #f72585, #7209b7);
    color: white;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
}
.stat-title {
    font-size: 0.85rem;
    opacity: 0.9;
}
.stat-value {
    font-size: 1.9rem;
    font-weight: 800;
}

/* ---------- BUTTON ---------- */
.stButton > button {
    background: linear-gradient(90deg, #f72585, #7209b7) !important;
    color: white !important;
    border-radius: 18px;
    padding: 14px;
    font-weight: 700;
    width: 100%;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 10px 25px rgba(114,9,183,0.35);
}

/* ---------- DATAFRAME ---------- */
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

score_options = ["— Pilih Skor —", "3-0", "3-1", "3-2", "2-3", "1-3", "0-3"]

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
    st.session_state.results = []
    st.session_state.win = 0
    st.session_state.lose = 0

# ==================================================
# SIMULATOR
# ==================================================
def auto_simulate(a, b):
    diff = teams_strength[a] - teams_strength[b]
    if diff >= 2:
        pool = ["3-0", "3-1", "3-2"]
    elif diff == 1:
        pool = ["3-1", "3-2", "2-3"]
    elif diff == 0:
        pool = score_points.keys()
    else:
        pool = ["0-3", "1-3", "2-3"]
    return random.choice(list(pool))

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
    st.subheader("✍️ Input Hasil JLM")

    points = {t: 0 for t in teams}
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

    valid = True

    for i, opp in enumerate(jlm_matches):
        score = st.selectbox(
            f"Match {i+1} vs {opp}",
            score_options,
            key=f"m{i}"
        )

        if score == "— Pilih Skor —":
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

    if st.button("🚀 Simulasikan Musim"):
        if not valid:
            st.warning("⚠️ Lengkapi semua skor terlebih dahulu")
        else:
            with st.spinner("Mensimulasikan liga..."):
                time.sleep(1.2)

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
            st.session_state.results = results
            st.session_state.win = win
            st.session_state.lose = lose
            st.session_state.simulated = True
            st.success("Simulasi selesai 🎉")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# KLASMEN
# ==================================================
with tab_klasemen:
    if not st.session_state.simulated:
        st.info("Silakan lakukan simulasi terlebih dahulu")
    else:
        df = (
            pd.DataFrame(st.session_state.points.items(), columns=["Tim", "Poin"])
            .sort_values("Poin", ascending=False)
            .reset_index(drop=True)
        )
        df.index += 1

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🏆 Klasemen Akhir")
        st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        rank = df[df["Tim"] == "Jakarta Livin Mandiri"].index[0] + 1

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if rank <= 4:
            st.success(f"✅ JLM LOLOS FINAL FOUR (Peringkat {rank})")
        else:
            st.error(f"❌ JLM TIDAK LOLOS FINAL FOUR (Peringkat {rank})")
        st.markdown("</div>", unsafe_allow_html=True)
