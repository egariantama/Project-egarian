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
# LOAD LOGO
# ==================================================
def load_logo(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = load_logo("logo_jlm.png")

# ==================================================
# GLOBAL CSS (SATU BLOK — AMAN)
# ==================================================
st.markdown("""
<style>
html, body, .stApp {
    background:#ffffff;
    color:#111;
    font-family:-apple-system, BlinkMacSystemFont, sans-serif;
}

/* ===== HEADER ===== */
.app-header {
    display:flex;
    align-items:center;
    gap:14px;
    margin-bottom:6px;
}
.app-header img { height:72px; }
.title { font-size:2rem; font-weight:800; line-height:1.1; }
.subtitle { font-size:0.95rem; color:#666; }

/* ===== REMOVE DEFAULT GAP ===== */
.block-container { padding-top:0.6rem !important; }

/* ===== TAB ===== */
div[data-baseweb="tab-list"] {
    position:sticky;
    top:0;
    z-index:999;
    background:#f5f5f7;
    padding:10px;
    border-radius:22px;
    margin-top:4px;
}

button[data-baseweb="tab"] {
    border-radius:18px;
    padding:8px 16px;
    font-weight:700;
    color:#7209b7;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background:linear-gradient(135deg,#f72585,#7209b7);
    color:white;
    box-shadow:0 6px 16px rgba(114,9,183,.35);
}

/* ===== CARD ===== */
.card {
    background:white;
    border-radius:18px;
    padding:18px;
    margin-bottom:18px;
    box-shadow:0 6px 18px rgba(0,0,0,.08);
}

/* ===== STAT ===== */
.stat-box {
    background:linear-gradient(135deg,#f72585,#7209b7);
    color:white;
    border-radius:16px;
    padding:16px;
    text-align:center;
}
.stat-value { font-size:1.8rem; font-weight:800; }

/* ===== SELECTBOX FIX ===== */
div[data-baseweb="select"] * {
    color:white !important;
    font-weight:800 !important;
}
div[data-baseweb="menu"] * {
    color:#111 !important;
}

/* ===== MOBILE ===== */
@media(max-width:768px){
    .title{font-size:1.5rem;}
    .app-header img{height:60px;}
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER (SATU-SATUNYA)
# ==================================================
st.markdown(f"""
<div class="app-header">
    <img src="data:image/png;base64,{logo_base64}">
    <div>
        <div class="title">Proliga Putri 2026</div>
        <div class="subtitle">Simulasi Musim | Jakarta Livin Mandiri</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATE
# ==================================================
if "points" not in st.session_state:
    st.session_state.points = {}
    st.session_state.win = 0
    st.session_state.lose = 0
    st.session_state.jlm_results = []

# ==================================================
# DATA
# ==================================================
teams_strength = {
    "Jakarta Pertamina Enduro":5,
    "Jakarta Popsivo Polwan":5,
    "Jakarta Electric PLN":4,
    "Gresik Phonska Plus":4,
    "Jakarta Livin Mandiri":3,
    "Bandung BJB Tandamata":2,
    "Sumut Falcons":1
}
teams = list(teams_strength.keys())

score_points = {
    "3-0":(3,0),"3-1":(3,0),"3-2":(2,1),
    "2-3":(1,2),"1-3":(0,3),"0-3":(0,3)
}
score_options = ["— Pilih Skor —"] + list(score_points.keys())

# ==================================================
# AUTO SIMULATE
# ==================================================
def auto_simulate(a,b):
    diff = teams_strength[a] - teams_strength[b]
    pool = ["3-0","3-1","3-2"] if diff>=2 else \
           ["3-1","3-2","2-3"] if diff==1 else \
           ["3-2","2-3","3-1","1-3"] if diff==0 else \
           ["0-3","1-3","2-3"]
    return random.choice(pool)

# ==================================================
# TABS
# ==================================================
tab_home, tab_input, tab_klasemen = st.tabs(["🏠 Home","✍️ Input","🏆 Klasemen"])

# ==================================================
# HOME
# ==================================================
with tab_home:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    c1.markdown(f"<div class='stat-box'>Menang<div class='stat-value'>{st.session_state.win}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='stat-box'>Kalah<div class='stat-value'>{st.session_state.lose}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# INPUT
# ==================================================
with tab_input:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    points = {t:0 for t in teams}
    win = lose = 0
    results = []

    for i, opp in enumerate(teams):
        if opp=="Jakarta Livin Mandiri": continue
        score = st.selectbox(f"Match {i+1} vs {opp}", score_options, key=f"m{i}")
        if score=="— Pilih Skor —": continue
        pj,po = score_points[score]
        points["Jakarta Livin Mandiri"]+=pj
        points[opp]+=po
        win += pj>po
        lose += pj<po
        results.append([opp,score,pj,"Menang" if pj>po else "Kalah"])

    st.session_state.points = points
    st.session_state.win = win
    st.session_state.lose = lose
    st.session_state.jlm_results = results
    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# KLASMEN
# ==================================================
with tab_klasemen:
    if not st.session_state.points:
        st.info("Silakan input skor")
    else:
        df = pd.DataFrame(st.session_state.points.items(),columns=["Tim","Poin"]).sort_values("Poin",ascending=False)
        df.insert(0,"Peringkat",range(1,len(df)+1))
        st.dataframe(df,use_container_width=True)
