import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Fee Income by Asuradur | Bank Mandiri",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================================================
# CUSTOM CSS (MANDIRI STYLE)
# ==================================================
st.markdown("""
<style>
body { background-color: #F4F6F9; }
.block-container { padding-top: 1rem; padding-bottom: 1rem; }

.header {
    background: linear-gradient(135deg, #003A8F, #0052CC);
    padding: 18px;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 16px;
}

.card {
    background: white;
    padding: 16px;
    border-radius: 16px;
    margin-bottom: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}

.kpi { font-size: 28px; font-weight: 800; color: #003A8F; }
.sub { font-size: 13px; color: #6b7280; }

.green { color: #16a34a; font-weight: 600; }
.red { color: #dc2626; font-weight: 600; }
.orange { color: #f59e0b; font-weight: 600; }

.rank {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid #e5e7eb;
}
.rank:last-child { border-bottom: none; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div class="header">
    <h3>Fee Income by Asuradur</h3>
    <div style="font-size:13px;">Bank Mandiri • January 2024</div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# EXCEL UPLOADER (ANTI CRASH)
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "📤 Upload Excel FBI Asuradur",
    type=["xlsx"]
)
st.markdown("</div>", unsafe_allow_html=True)

@st.cache_data
def load_data(file):
    df = pd.read_excel(file, sheet_name="data")
    df["FBI"] = df["FBI"].fillna(0)
    df["Growth"] = df["Growth"].fillna(0)
    return df

# ==================================================
# FALLBACK DATA (IF EXCEL NOT UPLOADED)
# ==================================================
if uploaded_file:
    data = load_data(uploaded_file)
else:
    st.warning("⚠️ Excel belum diupload. Menampilkan data contoh.")
    data = pd.DataFrame({
        "Asuradur": ["Sinarmas MSIG", "Manulife", "AXA Mandiri", "Allianz", "BNI Life"],
        "FBI": [99, 95, 85.2, 63.2, 32.8],
        "Growth": [18.2, 16.9, 12.4, 9.8, -7.5]
    })

# ==================================================
# KPI OVERVIEW
# ==================================================
total_fbi = data["FBI"].sum()
target = 420
achievement = total_fbi / target

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Performance Overview</div>", unsafe_allow_html=True)
st.markdown(f"<div class='kpi'>IDR {total_fbi:,.1f} M</div>", unsafe_allow_html=True)
st.markdown("<span class='green'>▲ 14.7% vs Last Month</span>", unsafe_allow_html=True)
st.progress(min(achievement, 1.0))
st.markdown(f"<div class='sub'>Achievement: {achievement*100:.1f}% of IDR {target}M</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# DONUT CHART
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### Fee Income Breakdown")

fig, ax = plt.subplots(figsize=(4,4))
colors = ["#003A8F", "#F4C430", "#00A651", "#4DA3FF", "#9CA3AF"]

ax.pie(
    data["FBI"],
    startangle=90,
    colors=colors[:len(data)],
    wedgeprops=dict(width=0.35)
)

top = data.sort_values("FBI", ascending=False).iloc[0]
share = top["FBI"] / total_fbi * 100

ax.text(0, 0, f"{share:.1f}%\n{top['Asuradur']}", ha="center", va="center", fontweight="bold")
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# RANKING
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### Asuradur Ranking")

ranked = data.sort_values("FBI", ascending=False).reset_index(drop=True)

for i, r in ranked.iterrows():
    arrow = "▲" if r["Growth"] >= 0 else "▼"
    color = "green" if r["Growth"] >= 0 else "red"

    st.markdown(f"""
    <div class="rank">
        <div><b>{i+1}. {r['Asuradur']}</b></div>
        <div style="text-align:right;">
            <div><b>{r['FBI']} M</b></div>
            <div class="{color}">{arrow} {r['Growth']}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# INSIGHT
# ==================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)

for _, r in ranked[ranked["Growth"] < 0].iterrows():
    st.markdown(
        f"⚠️ <span class='orange'><b>{r['Asuradur']} perlu perhatian khusus ({r['Growth']}% MoM)</b></span>",
        unsafe_allow_html=True
    )

st.markdown(
    f"✅ <span class='green'><b>{top['Asuradur']} memimpin dengan kontribusi {share:.1f}%</b></span>",
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# FOOTER
# ==================================================
st.markdown("""
<div style="text-align:center; font-size:12px; color:#9ca3af;">
© 2026 Bancassurance Performance Report – Bank Mandiri
</div>
""", unsafe_allow_html=True)
