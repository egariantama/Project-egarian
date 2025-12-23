import streamlit as st
import pandas as pd
import random
import base64

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Proliga Putri 2026",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================================================
# LOGO + HEADER
# ==================================================
def load_logo(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = load_logo("logo_jlm.png")

st.markdown(f"""
<div style="display:flex; align-items:center; gap:14px; margin-bottom:8px;">
    <img src="data:image/png;base64,{logo_base64}" style="height:72px;">
    <div>
        <div style="font-size:2rem; font-weight:800; line-height:1.1;">
            Proliga Putri 2026
        </div>
        <div style="font-size:0.95rem; color:#666;">
            Simulasi Musim | Jakarta Livin Mandiri
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATE
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
# JADWAL PERTANDINGAN JLM (WAJIB ADA)
# ==================================================
jlm_matches = [
    "Sumut Falcons","Sumut Falcons",
    "Bandung BJB Tandamata","Bandung BJB Tandamata",
    "Jakarta Electric PLN","Jakarta Electric PLN",
    "Gresik Phonska Plus","Gresik Phonska Plus",
    "Jakarta Pertamina Enduro","Jakarta Pertamina Enduro",
    "Jakarta Popsivo Polwan","Jakarta Popsivo Polwan"
]

# ==================================================
# AUTO SIMULATE
# ==================================================
def auto_simulate(a, b):
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
# INPUT (REALTIME + SIMULASI)
# ==================================================
with tab_input:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✍️ Input Hasil Jakarta Livin Mandiri")

    points = {t: 0 for t in teams}
    win = lose = 0
    jlm_results = []
    valid = True

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
        win += hasil == "Menang"
        lose += hasil == "Kalah"

        jlm_results.append([i+1, opp, score, pj, hasil])

    st.session_state.points = points
    st.session_state.win = win
    st.session_state.lose = lose
    st.session_state.jlm_results = jlm_results

    if st.button("🚀 Simulasikan Musim"):
        if not valid:
            st.warning("Lengkapi semua skor terlebih dahulu")
        else:
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
            st.session_state.simulated = True
            st.success("Simulasi musim selesai 🎉")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# KLASMEN
# ==================================================
with tab_klasemen:
    if st.session_state.points:
        df = pd.DataFrame(
            st.session_state.points.items(),
            columns=["Tim","Poin"]
        ).sort_values("Poin", ascending=False).reset_index(drop=True)

        df.insert(0, "Peringkat", df.index + 1)

        def highlight_jlm(row):
            return [
                "background-color:#bbf7d0; color:#064e3b; font-weight:800"
                if row["Tim"]=="Jakarta Livin Mandiri" else ""
                for _ in row
            ]

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🏆 Klasemen Akhir")
        st.dataframe(
            df.style.apply(highlight_jlm, axis=1),
            use_container_width=True,
            hide_index=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
