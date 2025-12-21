import streamlit as st
import pandas as pd

# ======================
# KONFIGURASI HALAMAN
# ======================
st.set_page_config(
    page_title="Simulasi Proliga 2026 - JLM",
    layout="centered"
)

st.title("🏐 Simulasi Proliga Putri 2026")
st.subheader("Jakarta Livin Mandiri (JLM)")

# ======================
# DATA DASAR
# ======================
teams = [
    "Jakarta Pertamina Enduro",
    "Jakarta Popsivo Polwan",
    "Gresik Phonska Plus",
    "Jakarta Electric PLN",
    "Bandung BJB Tandamata",
    "Sumut Falcons"
]

matches = [
    "Sumut Falcons (1)",
    "Sumut Falcons (2)",
    "Bandung BJB (1)",
    "Bandung BJB (2)",
    "Jakarta Electric PLN (1)",
    "Jakarta Electric PLN (2)",
    "Gresik Phonska (1)",
    "Gresik Phonska (2)",
    "Jakarta Pertamina (1)",
    "Jakarta Pertamina (2)",
    "Popsivo Polwan (1)",
    "Popsivo Polwan (2)"
]

score_options = [
    "3-0", "3-1", "3-2",
    "2-3", "1-3", "0-3"
]

# ======================
# FUNGSI HITUNG POIN
# ======================
def calculate_points(score):
    if score in ["3-0", "3-1"]:
        return 3
    elif score == "3-2":
        return 2
    elif score == "2-3":
        return 1
    else:
        return 0

# ======================
# INPUT HASIL MATCH
# ======================
st.markdown("### 🎯 Input Hasil Pertandingan JLM")

results = []
total_points = 0

for match in matches:
    score = st.selectbox(
        f"Hasil vs {match}",
        score_options,
        index=3
    )
    point = calculate_points(score)
    total_points += point

    results.append({
        "Lawan": match,
        "Skor": score,
        "Poin": point
    })

df_results = pd.DataFrame(results)

# ======================
# OUTPUT HASIL JLM
# ======================
st.markdown("### 📊 Hasil Pertandingan JLM")
st.dataframe(df_results, use_container_width=True)

st.metric("Total Poin JLM", total_points)

# ======================
# SIMULASI KLASMEN (DUMMY REALISTIS)
# ======================
standings = pd.DataFrame({
    "Tim": [
        "Jakarta Pertamina Enduro",
        "Jakarta Popsivo Polwan",
        "Jakarta Electric PLN",
        "Jakarta Livin Mandiri",
        "Gresik Phonska Plus",
        "Bandung BJB Tandamata",
        "Sumut Falcons"
    ],
    "Poin": [
        27, 25, 20, total_points, 14, 9, 4
    ]
}).sort_values("Poin", ascending=False).reset_index(drop=True)

standings.index += 1

st.markdown("### 🏆 Klasemen Simulasi Proliga 2026")
st.dataframe(standings, use_container_width=True)

# ======================
# STATUS LOLOS
# ======================
jlm_rank = standings[standings["Tim"] == "Jakarta Livin Mandiri"].index[0] + 1

if jlm_rank <= 4:
    st.success(f"✅ JLM LOLOS FINAL FOUR (Peringkat {jlm_rank})")
else:
    st.error(f"❌ JLM GAGAL LOLOS (Peringkat {jlm_rank})")

