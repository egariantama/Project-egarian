import streamlit as st
import pandas as pd
import random

# ==================================================
# PAGE CONFIG (MOBILE FRIENDLY)
# ==================================================
st.set_page_config(
    page_title="Proliga Putri 2026",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================================================
# SESSION STATE (AMAN & WAJIB)
# ==================================================
DEFAULT_STATE = {
    "simulated": False,
    "points": {},
    "win": 0,
    "lose": 0,
    "jlm_results": []
}

for k, v in DEFAULT_STATE.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==================================================
# GLOBAL CSS (VISIBILITY FIX + MOBILE)
# ==================================================
st.markdown("""
<style>
html, body, .stApp {
    background:#ffffff;
    color:#111111;
    font-family:-apple-system, BlinkMacSystemFont, sans-serif;
}

/* TAB */
button[data-baseweb="tab"] {
    color:#7209b7 !important;
    font-weight:700;
}
button[aria-selected="true"] {
    border-bottom:3px solid #f72585 !important;
    color:#f72585 !important;
}

/* INPUT TEXT VISIBILITY */
label, span, div[data-baseweb="select"] * {
    color:#111111 !important;
    font-weight:600 !important;
}

/* CARD */
.card {
    background:white;
    border-radius:18px;
    padding:18px;
    margin-bottom:18px;
    box-shadow:0 6px 18px rgba(0,0,0,.08);
}

/* STAT */
.stat-box {
    background:linear-gradient(135deg,#f72585,#7209b7);
    color:white;
    border-radius:16px;
    padding:16px;
    text-align:center;
}
.stat-value {
    font-size:1.8rem;
    font-weight:800;
}

/* BUTTON */
.stButton>button {
    background:linear-gradient(90deg,#f72585,#7209b7);
    color:white;
    border-radius:18px;
    padding:14px;
    font-weight:700;
    width:100%;
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

score_options = ["— Pilih Skor —","3-0","3-1","3-2","2-3","1-3","0-3"]
score_points = {
    "3-0":(3,0),"3-1":(3,0),"3-2":(2,1),
    "2-3":(1,2),"1-3":(0,3),"0-3":(0,3)
}

# ==================================================
# AUTO SIMULATE
# ==================================================
def auto_simulate(a,b):
    diff = teams_strength[a] - teams_strength[b]
    if diff >= 2:
        pool = ["3-0","3-1","3-2"]
    elif diff == 1:
        pool = ["3-1","3-2","2-3"]
    elif diff == 0:
        pool = ["3-2","2-3","3-1","1-3"]
    else:
        pool = ["0-3","1-3","2-3"]
    return random.choice(pool)

# ==================================================
# TABS
# ==================================================
tab_home, tab_input, tab_klasemen = st.tabs(
    ["🏠 Home","✍️ Input","🏆 Klasemen"]
)

# ==================================================
# HOME (REALTIME)
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

    if st.session_state.jlm_results:
        df_jlm = pd.DataFrame(
            st.session_state.jlm_results,
            columns=["No","Lawan","Skor","Poin","Hasil"]
        )
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📋 Detail Pertandingan JLM")
        st.dataframe(df_jlm.set_index("No"), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# INPUT (REALTIME)
# ==================================================
with tab_input:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✍️ Input Hasil Jakarta Livin Mandiri")

    points = {t:0 for t in teams}
    win = lose = 0
    jlm_results = []
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
            key=f"match_{i}"
        )

        if score == "— Pilih Skor —":
            valid = False
            continue

        pj, po = score_points[score]
        points["Jakarta Livin Mandiri"] += pj
        points[opp] += po

        hasil = "Menang" if pj > po else "Kalah"
        poin_jlm = pj

        win += hasil == "Menang"
        lose += hasil == "Kalah"

        jlm_results.append([i+1, opp, score, poin_jlm, hasil])

    # REALTIME UPDATE
    st.session_state.points = points
    st.session_state.win = win
    st.session_state.lose = lose
    st.session_state.jlm_results = jlm_results

    if st.button("🚀 Simulasikan Musim"):
        if not valid:
            st.warning("Lengkapi semua skor")
        else:
            for i in range(len(teams)):
                for j in range(i+1, len(teams)):
                    a, b = teams[i], teams[j]
                    if "Jakarta Livin Mandiri" in (a,b):
                        continue
                    for _ in range(2):
                        s = auto_simulate(a,b)
                        pa, pb = score_points[s]
                        points[a] += pa
                        points[b] += pb

            st.session_state.points = points
            st.session_state.simulated = True
            st.success("Simulasi selesai 🎉")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# KLASMEN (RAPI + HIGHLIGHT)
# ==================================================
with tab_klasemen:
    if not st.session_state.points:
        st.info("Silakan input skor terlebih dahulu")
    else:
        df = pd.DataFrame(
            st.session_state.points.items(),
            columns=["Tim","Poin"]
        ).sort_values("Poin", ascending=False).reset_index(drop=True)

        df.insert(0, "Peringkat", df.index + 1)

        def highlight_jlm(row):
            return [
                "background-color:#c7f9cc;font-weight:800" if row["Tim"]=="Jakarta Livin Mandiri" else ""
                for _ in row
            ]

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🏆 Klasemen Akhir")
        st.dataframe(
            df[["Peringkat","Tim","Poin"]]
            .style.apply(highlight_jlm, axis=1),
            use_container_width=True
        )

        rank = df[df["Tim"]=="Jakarta Livin Mandiri"]["Peringkat"].values[0]
        if rank <= 4:
            st.success(f"✅ Jakarta Livin Mandiri LOLOS FINAL FOUR (Peringkat {rank})")
        else:
            st.error(f"❌ Jakarta Livin Mandiri TIDAK LOLOS FINAL FOUR (Peringkat {rank})")

        st.markdown("</div>", unsafe_allow_html=True)
