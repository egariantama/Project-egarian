import streamlit as st
import pandas as pd
import random
import base64

# ==================================================
# PAGE CONFIG (MOBILE FRIENDLY)
# ==================================================
def load_logo(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = load_logo("logo_jlm.png")

st.markdown(f"""
<div style="display:flex; align-items:center; gap:14px; margin-bottom:5px;">
    <img src="data:image/png;base64,{logo_base64}" style="height:80px;">
    <div>
        <div style="font-size:2rem; font-weight:800;">
            Proliga Putri 2026
        </div>
        <div style="font-size:0.95rem; color:#666;">
            Simulasi Musim | Jakarta Livin Mandiri
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

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
st.markdown("""
<style>
/* ===== FIX WARNA FONT SCORE SELECTBOX ===== */

/* teks score yang dipilih */
div[data-baseweb="select"] span {
    color: #111111 !important;
    font-weight: 700 !important;
}

/* dropdown item */
div[data-baseweb="menu"] span {
    color: #111111 !important;
    font-weight: 600 !important;
}

/* placeholder */
div[data-baseweb="select"] input {
    color: #111111 !important;
    font-weight: 600 !important;
}

/* hover item */
div[data-baseweb="menu"] div:hover {
    background-color: #f72585 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* ===== FIX FINAL TEKS SCORE YANG SUDAH DIPILIH ===== */

/* container nilai terpilih */
div[data-baseweb="select"] > div {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* angka skor (3-2, 3-1, dll) */
div[data-baseweb="select"] span {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* icon panah */
div[data-baseweb="select"] svg {
    fill: #ffffff !important;
}

/* dropdown list item */
div[data-baseweb="menu"] span {
    color: #111111 !important;
    font-weight: 600 !important;
}

/* hover dropdown */
div[data-baseweb="menu"] div:hover {
    background-color: #f72585 !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* ===== FORCE TEXT COLOR SELECTBOX (FINAL FIX) ===== */

div[data-baseweb="select"] * {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* arrow dropdown */
div[data-baseweb="select"] svg {
    fill: #ffffff !important;
}

/* dropdown menu item */
div[data-baseweb="menu"] * {
    color: #111111 !important;
    font-weight: 600 !important;
}

/* hover item */
div[data-baseweb="menu"] div:hover * {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* =======================
   MOBILE OPTIMIZATION
   ======================= */
@media (max-width: 768px) {

    /* HEADER */
    h1 {
        font-size: 1.6rem !important;
        line-height: 1.2 !important;
    }
    h2, h3 {
        font-size: 1.15rem !important;
    }

    /* CARD */
    .card {
        padding: 14px !important;
        border-radius: 16px !important;
        margin-bottom: 14px !important;
    }

    /* STAT BOX */
    .stat-box {
        padding: 14px !important;
        border-radius: 18px !important;
        min-height: unset !important;
    }

    .stat-box div:first-child {
        font-size: 0.9rem !important;
        opacity: 0.9;
    }

    .stat-value {
        font-size: 1.6rem !important;
        margin-top: 4px;
    }

    /* REMOVE EXCESS SPACE */
    .element-container:has(.stat-box) {
        margin-bottom: 8px !important;
    }

    /* TABLE */
    .stDataFrame {
        font-size: 0.85rem !important;
    }

    /* BUTTON */
    .stButton>button {
        padding: 12px !important;
        font-size: 0.95rem !important;
        border-radius: 16px !important;
    }
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* =======================
   STICKY TAB HEADER
   ======================= */

/* Container tab */
div[data-baseweb="tab-list"] {
    position: sticky;
    top: 0;
    z-index: 999;
    background: #ffffff;
    padding-top: 6px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(0,0,0,0.06);
}

/* Space agar konten tidak ketutup */
div[data-baseweb="tab-panel"] {
    padding-top: 12px;
}

/* Mobile refinement */
@media (max-width: 768px) {
    div[data-baseweb="tab-list"] {
        top: 0;
        padding-top: 8px;
        padding-bottom: 8px;
    }
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* ======================
   ROUNDED PILL TABS
   ====================== */
div[data-baseweb="tab-list"] {
    display: flex;
    gap: 8px;
    padding: 10px;
    border-radius: 22px;
    background: #f5f5f7;
}

button[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 18px !important;
    padding: 8px 16px !important;
    font-weight: 700 !important;
    transition: all 0.25s ease;
}

/* Active tab */
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg,#f72585,#7209b7) !important;
    color: white !important;
    box-shadow: 0 6px 16px rgba(114,9,183,.35);
}

/* Non-active */
button[data-baseweb="tab"]:not([aria-selected="true"]) {
    color: #7209b7 !important;
}

/* Mobile spacing */
@media (max-width: 768px) {
    button[data-baseweb="tab"] {
        padding: 8px 12px !important;
        font-size: 0.85rem;
    }
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<script>
let startX = null;

document.addEventListener("touchstart", function(e) {
    startX = e.touches[0].clientX;
}, false);

document.addEventListener("touchend", function(e) {
    if (startX === null) return;

    let endX = e.changedTouches[0].clientX;
    let diffX = startX - endX;
    let tabs = document.querySelectorAll('button[data-baseweb="tab"]');
    let activeIndex = [...tabs].findIndex(t => t.getAttribute("aria-selected") === "true");

    if (Math.abs(diffX) > 60) {
        if (diffX > 0 && activeIndex < tabs.length - 1) {
            tabs[activeIndex + 1].click();
        }
        if (diffX < 0 && activeIndex > 0) {
            tabs[activeIndex - 1].click();
        }
    }

    startX = null;
}, false);
</script>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* RATA TENGAH KOLOM PERINGKAT */
[data-testid="stDataFrame"] th:nth-child(1),
[data-testid="stDataFrame"] td:nth-child(1) {
    text-align: center !important;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* =========================
   FIX WARNA TEKS TABEL KLASMEN
   ========================= */
table td, table th {
    color: #111111 !important;
}

/* Tetap putih untuk baris highlight JLM */
table tr td[style*="background-color:#c7f9cc"] {
    color: #111111 !important;
    font-weight: 800 !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* =========================
   FIX BORDER TABEL KLASMEN
   ========================= */
.stDataFrame table {
    border-collapse: collapse !important;
}

.stDataFrame th, 
.stDataFrame td {
    border-bottom: 1px solid rgba(0,0,0,0.12) !important;
    padding: 10px 12px !important;
}

.stDataFrame th {
    font-weight: 700 !important;
    background-color: #f5f5f7 !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* =========================
   SELECTBOX TEXT → HITAM
   (ANDROID + IOS + DESKTOP)
   ========================= */

/* Nilai skor yang TERPILIH */
div[role="combobox"] span {
    color: #111111 !important;
    font-weight: 700 !important;
}

/* Placeholder */
div[role="combobox"] input {
    color: #111111 !important;
}

/* Icon panah */
div[role="combobox"] svg {
    fill: #111111 !important;
}

/* Dropdown list */
div[role="listbox"] span {
    color: #111111 !important;
    font-weight: 600 !important;
}

/* Hover / selected item */
div[role="option"][aria-selected="true"] span {
    background-color: #f72585 !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================

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
            st.markdown("""
<div style="
    background:#fff8cc;
    border:1px solid #ffd666;
    border-radius:16px;
    padding:14px;
    font-weight:700;
    color:#5c4b00;
">
⚠️ Lengkapi semua skor
</div>
""", unsafe_allow_html=True)
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
            columns=["Tim", "Poin"]
        ).sort_values("Poin", ascending=False).reset_index(drop=True)

        df.insert(0, "Peringkat", df.index + 1)

        # ✅ FIX INDENTASI + HIGHLIGHT KONTRAS
        def highlight_jlm(row):
            if row["Tim"] == "Jakarta Livin Mandiri":
                return [
                    "background-color:#bbf7d0; color:#064e3b; font-weight:800"
                    for _ in row
                ]
            else:
                return ["" for _ in row]

        styled_df = (
            df[["Peringkat", "Tim", "Poin"]]
            .style
            .apply(highlight_jlm, axis=1)
            .set_properties(
                subset=["Peringkat", "Poin"],
                **{"text-align": "center"}
            )
            .set_properties(
                subset=["Tim"],
                **{"text-align": "left"}
            )
        )

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🏆 Klasemen Akhir")

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )

        # ✅ POSISI BENAR (SEJAJAR dataframe)
        rank = df[df["Tim"] == "Jakarta Livin Mandiri"]["Peringkat"].values[0]

        if rank <= 4:
            st.success(f"✅ Jakarta Livin Mandiri LOLOS FINAL FOUR (Peringkat {rank})")
        else:
            st.error(f"❌ Jakarta Livin Mandiri TIDAK LOLOS FINAL FOUR (Peringkat {rank})")

        st.markdown("</div>", unsafe_allow_html=True)
